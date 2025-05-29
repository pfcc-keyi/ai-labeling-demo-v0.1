# AI Labeling Platform

A full-stack web application for AI-powered text classification using OpenAI models.

## Tech Stack

### Backend
- **FastAPI** - Python web framework
- **SQLite** - Database for logging
- **SQLModel** - ORM for database operations
- **JWT** - Authentication
- **asyncio.Lock** - Concurrency control

### Frontend
- **React** + **TypeScript** + **Vite** - Frontend framework
- **Chakra UI** - Component library
- **Axios** - HTTP client

### Deployment
- **Render.com** - Backend hosting (free tier)
- **Vercel** - Frontend hosting (free tier)

## Features

1. **Model Selection**: Choose between GPT-4 and GPT-3.5-turbo
2. **Text Classification**: Classify financial services job descriptions
3. **User Feedback**: Support/reject predictions and provide corrections
4. **Authentication**: 5 predefined accounts
5. **Concurrency Control**: Single-user processing with queue mechanism
6. **Logging**: Complete audit trail of all interactions

## Project Structure

```
ai-labeling/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         # FastAPI app
│   │   ├── auth.py         # Authentication
│   │   ├── models.py       # Database models
│   │   ├── labeling.py     # Core labeling logic
│   │   └── accounts.py     # User accounts
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── utils/
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── docker-compose.yml      # Local development
└── README.md
```

## Local Development

1. **Start Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Or use Docker Compose**:
   ```bash
   docker-compose up
   ```

## Environment Variables

Create a `.env` file in the backend directory:

```
OPENAI_API_KEY=your_openai_api_key_here
JWT_SECRET=your_jwt_secret_here
```

## User Accounts

The system has 5 predefined accounts stored in `backend/app/accounts.py`.

## API Endpoints

- `POST /login` - User authentication
- `POST /label` - Text classification
- `POST /feedback` - User feedback
- `GET /status` - Check if system is busy

## Deployment

### Backend (Render.com)
1. Connect GitHub repository
2. Set environment variables
3. Deploy as web service

### Frontend (Vercel)
1. Connect GitHub repository
2. Set build command and output directory
3. Deploy automatically on push 