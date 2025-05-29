import pandas as pd
from autolabel import LabelingAgent, AutolabelDataset
import tempfile
import os
import csv
from typing import Tuple, Optional
import asyncio
import time

# Global lock for concurrency control
_processing_lock = asyncio.Lock()
_current_user = None
_processing_start_time = None

# Labels and descriptions from the original script
LABELS = [
    "Investment Banking - Mergers & Acquisitions (M&A)",
    "Investment Banking - Capital Markets (ECM&DCM)",
    "Global Markets (including Sales & Trading) - Equities",
    "Global Markets (including Sales & Trading) - FICC",
    "Global Markets (including Sales & Trading) - Structured Products",
    "Global Markets (including Sales & Trading) - Prime Brokerage",
    "Securities Services - Custody / funding services",
    "Research - Equity research",
    "Research - FI research",
    "Commercial Banking - Core Lending & Credit Solutions",
    "Commercial Banking - Deposit & Cash Management (Treasury)",
    "Commercial Banking - Payment & Merchant Services",
    "Commercial Banking - Trade & Supply Chain Finance",
    "Retail banking - Core retail banking products",
    "Retail banking - Wealth & investment services",
    "Retail banking - Digital & Mobile Banking",
    "Private Banking - Private wealth",
    "Business services - Bank level support functions",
    "Asset Management - Hedge fund",
    "Asset Management - Mutual fund",
    "Asset Management - Private Equity (PE)",
    "Insurance - Core insurance products",
    "Insurance - Value added services"
]

LABEL_DESCRIPTIONS = {
    "Investment Banking - Mergers & Acquisitions (M&A)": "Advises companies on buying, selling, or merging with other businesses. Works on leveraged buyouts (LBOs), hostile takeovers, and strategic deals.",
    "Investment Banking - Capital Markets (ECM&DCM)": "Equity Capital Markets (ECM): Helps companies raise capital through IPOs, follow-on offerings, and private placements. Debt Capital Markets (DCM): Assists in issuing corporate bonds, government debt, and structured financing.",
    "Global Markets (including Sales & Trading) - Equities": "Deals with stocks, ETFs, and equity derivatives.",
    "Global Markets (including Sales & Trading) - FICC": "Covers bonds, interest rate products, FX, and commodities.",
    "Global Markets (including Sales & Trading) - Structured Products": "Creates complex financial instruments like derivatives, swaps, and securitized products.",
    "Global Markets (including Sales & Trading) - Prime Brokerage": "Services for hedge funds (leverage, securities lending, execution).",
    "Securities Services - Custody / funding services": "Provides custody, clearing, settlement, and asset-servicing solutions to institutional clients.",
    "Research - Equity research": "Covers public companies, earnings forecasts, and stock recommendations.",
    "Research - FI research": "Analyzes bonds, credit risk, and macroeconomic trends.",
    "Commercial Banking - Core Lending & Credit Solutions": "Business loans, credit facilities, and small business banking.",
    "Commercial Banking - Deposit & Cash Management (Treasury)": "Responsible for cash management, liquidity, and treasury functions.",
    "Commercial Banking - Payment & Merchant Services": "Business Credit/Debit Cards – Corporate cards, purchasing cards (P-cards). Merchant Acquiring – Payment processing for retailers (POS, e-commerce). B2B Payments – Automated vendor payments, virtual cards.",
    "Commercial Banking - Trade & Supply Chain Finance": "Import/Export Financing – Letters of credit, documentary collections. Supply Chain Finance – Early payment programs for suppliers. Foreign Exchange (FX) Services – Hedging against currency risk.",
    "Retail banking - Core retail banking products": "Deposit accounts, Lending products, payment services.",
    "Retail banking - Wealth & investment services": "Basic investment products and advisory services.",
    "Retail banking - Digital & Mobile Banking": "Mobile apps, AI chatbots.",
    "Private Banking - Private wealth": "Manages investments for high-net-worth individuals (HNWIs), families, and institutions.",
    "Business services - Bank level support functions": "Bank level risk, finance, IT, and others.",
    "Asset Management - Hedge fund": "A type of investment fund that uses high-risk strategies to generate returns for its investors.",
    "Asset Management - Mutual fund": "A pooled investment fund that collects money from many investors to invest in a diversified portfolio of stocks, bonds, or other assets.",
    "Asset Management - Private Equity (PE)": "Investment in private companies or buyouts of public companies, typically aiming to improve them and eventually sell them at a profit.",
    "Insurance - Core insurance products": "Life insurance, health insurance, and others.",
    "Insurance - Value added services": "Risk Assessment & Consulting, Claims Management."
}

def create_config(model_name: str = "gpt-4"):
    """Create configuration for the labeling agent"""
    
    label_guidelines = """You are an expert in categorizing the business line or product in financial services roles based on their respective industries and job functions.
    Your task is to categorize each experience from the input text into the appropriate label.
    
        Important rules:
    - Always focus on the business line or product the employee worked on and financial services-related terminology in the text.
    - Don't be distracted by position or company name; focus entirely on the responsibilities and tasks in the experience description.
 
    Choose the most appropriate label from:
    {labels}
    
    Label descriptions:
    """
 
    for label, desc in LABEL_DESCRIPTIONS.items():
        label_guidelines += f"- {label}: {desc}\n"
   
    label_guidelines += "\nImportant: Please return only one of the above labels, without any additional text, punctuation, or explanation."
 
    config = {
        "task_name": "SentimentClassification",
        "task_type": "classification",
        "model": {
            "provider": "openai",
            "name": model_name,
            "parameters": {
                "temperature": 0.2,
                "max_tokens": 15
            }
        },
        "dataset": {
            "text_column": "text",
            "delimiter": ","
        },
        "prompt": {
            "task_guidelines": label_guidelines,
            "output_guidelines": "Return ONLY the exact label from the list above. Do not add any additional text, explanation, or punctuation.",
            "labels": LABELS,
            "label_descriptions": LABEL_DESCRIPTIONS,
            "example_template": "Text: {text}\nLabel:",
            "few_shot_examples": [
                {
                    "text": "Responsible for managing a team of analysts covering the technology sector. Produces detailed research reports on public companies, including financial analysis, industry trends, and stock recommendations.",
                    "label": "Research - Equity research"
                },
                {
                    "text": "Led the execution of multiple IPOs and follow-on offerings for technology companies. Worked closely with clients to structure offerings and coordinate with legal teams and regulators.",
                    "label": "Investment Banking - Capital Markets (ECM&DCM)"
                }
            ]
        }
    }
    return config

async def get_label(text: str, model_name: str = "gpt-4", account_id: str = "unknown") -> Tuple[Optional[str], Optional[str], float]:
    """
    Label a single text with concurrency control
    :param text: Input text
    :param model_name: Model to use (gpt-4 or gpt-3.5-turbo)
    :param account_id: User account ID
    :return: Tuple of (predicted_label, error_message, processing_time)
    """
    global _current_user, _processing_start_time
    
    # Check if system is busy
    if _processing_lock.locked():
        return None, f"System is busy. User '{_current_user}' is currently processing a request.", 0
    
    start_time = time.time()
    
    try:
        async with _processing_lock:
            _current_user = account_id
            _processing_start_time = start_time
            
            # Clean and format the text
            text = text.strip()
            text = text.replace('\n', ' ')  # Replace newlines with spaces
            text = ' '.join(text.split())   # Normalize whitespace
            
            # Create configuration
            config = create_config(model_name)
            
            # Create temporary dataset file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
                # Create DataFrame with text column
                df = pd.DataFrame({"text": [text]})
                
                # Write to CSV with proper quoting and escaping
                df.to_csv(tmp.name, index=False, quoting=csv.QUOTE_ALL, escapechar='\\')
                
                try:
                    # Use file path to initialize dataset
                    dataset = AutolabelDataset(tmp.name, config=config)
                    
                    agent = LabelingAgent(config=config, cache=False)
                    labeled_dataset = agent.run(dataset)
                    
                    # Get the label from the labeled dataset
                    label_column = f"{config['task_name']}_label"
                    if label_column in labeled_dataset.columns():
                        label = labeled_dataset.df[label_column].iloc[0]
                        
                        # If NO_LABEL is returned, get error information
                        if label == "NO_LABEL":
                            error_column = f"{config['task_name']}_error"
                            if error_column in labeled_dataset.columns():
                                error_msg = labeled_dataset.df[error_column].iloc[0]
                                return None, f"Labeling failed: {error_msg}", time.time() - start_time
                            else:
                                return None, "Labeling failed: Unknown error", time.time() - start_time
                        
                        return label, None, time.time() - start_time
                    else:
                        return None, f"Label column not found. Available columns: {labeled_dataset.columns()}", time.time() - start_time
                        
                except Exception as e:
                    return None, f"Labeling error: {str(e)}", time.time() - start_time
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp.name)
                    except:
                        pass
    
    finally:
        _current_user = None
        _processing_start_time = None

def get_processing_status() -> dict:
    """Get current processing status"""
    return {
        "is_busy": _processing_lock.locked(),
        "current_user": _current_user,
        "processing_time": time.time() - _processing_start_time if _processing_start_time else 0
    } 