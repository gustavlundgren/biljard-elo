import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")