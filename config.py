from dotenv import load_dotenv
import os


load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
ASYNC_DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')
SECRET = os.getenv('SECRET')
