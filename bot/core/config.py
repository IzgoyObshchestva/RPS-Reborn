import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
BOT_API_SECRET = os.getenv('BOT_API_SECRET')
API_V1_URL = os.getenv('API_V1_URL')