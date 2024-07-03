import os
import dotenv

dotenv.load_dotenv()


class Config:
    DEBUG = False
    ELASTIC_PASSWORD = os.getenv("ELASTIC_PASSWORD", "changeme")
    ELASTIC_HOST = os.getenv("ELASTIC_HOST", "https://localhost:9200")
