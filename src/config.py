from dotenv import load_dotenv
import os


load_dotenv()

ASYNC_DATABASE_URL = os.getenv('ASYNC_DATABASE_URL')
SECRET = os.getenv('SECRET')
SMTP_USER=os.getenv('SMTP_USER')
SMTP_PASS=os.getenv('SMTP_PASS')
TEST_DATABASE_URL=os.getenv('TEST_DATABASE_URL')
REDIS_URL=os.getenv('REDIS_URL')
REDIS_HOST=os.getenv('REDIS_HOST')
REDIS_PORT=os.getenv('REDIS_PORT')
DB_NAME=os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')
DB_PORT=os.getenv('DB_PORT')
