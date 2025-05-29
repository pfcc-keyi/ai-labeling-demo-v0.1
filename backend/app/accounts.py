import hashlib

# Predefined user accounts
# In production, these would be stored in a proper database with proper hashing
ACCOUNTS = {
    "admin": {
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "account_id": "admin"
    },
    "user1": {
        "password_hash": hashlib.sha256("user123".encode()).hexdigest(),
        "account_id": "user1"
    },
    "user2": {
        "password_hash": hashlib.sha256("user456".encode()).hexdigest(),
        "account_id": "user2"
    },
    "user3": {
        "password_hash": hashlib.sha256("user789".encode()).hexdigest(),
        "account_id": "user3"
    },
    "demo": {
        "password_hash": hashlib.sha256("demo123".encode()).hexdigest(),
        "account_id": "demo"
    }
}

def verify_account(username: str, password: str) -> bool:
    """Verify if username and password match"""
    if username not in ACCOUNTS:
        return False
    
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    return ACCOUNTS[username]["password_hash"] == password_hash

def get_account_id(username: str) -> str:
    """Get account ID for username"""
    if username in ACCOUNTS:
        return ACCOUNTS[username]["account_id"]
    return None 