import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Configuration variables
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"  # convert string to boolean
