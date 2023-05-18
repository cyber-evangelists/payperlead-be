import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ["DB_HOST"]
SMTP_PWD = os.environ["SMTP_PWD"]
SERVICE_AK_PATH = os.environ["SERVICE_AK_PATH"]
CONNECTION = os.environ["CONNECTION"]
UPLOAD_IMAGE_PATH = os.environ["UPLOAD_IMAGE_PATH"]