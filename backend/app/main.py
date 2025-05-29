from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os
from dotenv import load_dotenv
from sqlmodel import Session

from .models import RequestLog, FeedbackLog, create_db_and_tables, get_session
from .auth import create_access_token, verify_token
from .accounts import verify_account, get_account_id
from .labeling import get_label, get_processing_status, LABELS

load_dotenv()

app = FastAPI(
    title="AI Labeling API",
    description="API for AI-powered text classification using OpenAI models",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:5173",  # React dev servers
        "https://ai-labeling-demo-v0-1.vercel.app",   # Vercel deployment
        "https://*.netlify.app",  # Netlify deployment (backup)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    account_id: str

class LabelRequest(BaseModel):
    text: str
    model_name: str = "gpt-4"

class LabelResponse(BaseModel):
    id: int
    input_text: str
    model_name: str
    predicted_label: Optional[str]
    processing_time: float
    error_message: Optional[str] = None

class FeedbackRequest(BaseModel):
    request_id: int
    is_supported: bool
    corrected_label: Optional[str] = None

class StatusResponse(BaseModel):
    is_busy: bool
    current_user: Optional[str]
    processing_time: float

# Security
security = HTTPBearer()

def get_current_user(authorization: str = Header(None)) -> str:
    """Get current user from JWT token"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    try:
        # Extract token from "Bearer <token>"
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
        payload = verify_token(token)
        return payload.get("sub")
    except (IndexError, AttributeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format"
        )

@app.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT token"""
    if not verify_account(request.username, request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    account_id = get_account_id(request.username)
    access_token = create_access_token(data={"sub": request.username, "account_id": account_id})
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        account_id=account_id
    )

@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get current processing status"""
    status_info = get_processing_status()
    return StatusResponse(**status_info)

@app.post("/label", response_model=LabelResponse)
async def label_text(
    request: LabelRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Label text using AI model"""
    
    # Validate model name
    if request.model_name not in ["gpt-4", "gpt-3.5-turbo"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Model must be either 'gpt-4' or 'gpt-3.5-turbo'"
        )
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key not configured"
        )
    
    account_id = get_account_id(current_user)
    
    # Create request log entry
    request_log = RequestLog(
        account_id=account_id,
        model_name=request.model_name,
        input_text=request.text
    )
    session.add(request_log)
    session.commit()
    session.refresh(request_log)
    
    try:
        # Get label prediction
        predicted_label, error_message, processing_time = await get_label(
            request.text, 
            request.model_name, 
            account_id
        )
        
        # Update request log
        request_log.predicted_label = predicted_label
        request_log.error_message = error_message
        request_log.processing_time = processing_time
        session.add(request_log)
        session.commit()
        
        # If system is busy, return 423 status
        if error_message and "busy" in error_message.lower():
            raise HTTPException(
                status_code=status.HTTP_423_LOCKED,
                detail=error_message
            )
        
        return LabelResponse(
            id=request_log.id,
            input_text=request.text,
            model_name=request.model_name,
            predicted_label=predicted_label,
            processing_time=processing_time,
            error_message=error_message
        )
        
    except HTTPException:
        raise
    except Exception as e:
        # Update request log with error
        request_log.error_message = str(e)
        session.add(request_log)
        session.commit()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@app.post("/feedback")
async def submit_feedback(
    request: FeedbackRequest,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Submit user feedback on prediction"""
    
    account_id = get_account_id(current_user)
    
    # Validate that the request exists and belongs to the user
    request_log = session.get(RequestLog, request.request_id)
    if not request_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Request not found"
        )
    
    if request_log.account_id != account_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to provide feedback for this request"
        )
    
    # Validate corrected label if provided
    if request.corrected_label and request.corrected_label not in LABELS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid corrected label"
        )
    
    # Create feedback log
    feedback_log = FeedbackLog(
        request_id=request.request_id,
        account_id=account_id,
        is_supported=request.is_supported,
        corrected_label=request.corrected_label
    )
    
    session.add(feedback_log)
    session.commit()
    
    return {"status": "success", "message": "Feedback submitted successfully"}

@app.get("/labels")
async def get_labels():
    """Get all available labels"""
    return {"labels": LABELS}

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "AI Labeling API is running", "status": "healthy"}

@app.get("/download-logs")
async def download_logs(current_user: str = Depends(get_current_user)):
    """Download database logs (admin only)"""
    # Only allow admin to download logs
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can download logs"
        )
    
    db_path = "app.db"
    if not os.path.exists(db_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Database file not found"
        )
    
    return FileResponse(
        path=db_path,
        filename="ai_labeling_logs.db",
        media_type="application/octet-stream"
    )

@app.get("/logs-summary")
async def get_logs_summary(current_user: str = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get summary of logs (admin only)"""
    # Only allow admin to view logs summary
    if current_user != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can view logs summary"
        )
    
    from sqlmodel import select, func
    
    # Get request logs count by account
    request_logs_query = select(RequestLog.account_id, func.count(RequestLog.id).label("count")).group_by(RequestLog.account_id)
    request_logs_result = session.exec(request_logs_query).all()
    
    # Get feedback logs count by account
    feedback_logs_query = select(FeedbackLog.account_id, func.count(FeedbackLog.id).label("count")).group_by(FeedbackLog.account_id)
    feedback_logs_result = session.exec(feedback_logs_query).all()
    
    # Get total counts
    total_requests = session.exec(select(func.count(RequestLog.id))).first()
    total_feedback = session.exec(select(func.count(FeedbackLog.id))).first()
    
    return {
        "total_requests": total_requests,
        "total_feedback": total_feedback,
        "requests_by_account": [{"account_id": r[0], "count": r[1]} for r in request_logs_result],
        "feedback_by_account": [{"account_id": r[0], "count": r[1]} for r in feedback_logs_result]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 