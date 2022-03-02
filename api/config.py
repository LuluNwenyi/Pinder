# iMPORTS
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# BASE CONFIG
class Config():

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    @staticmethod
    def init_app(app):
        pass

# DEVELOPMENT CONFIG
class DevelopmentConfig(Config):

    DEBUG = True
    MONGO_URI = os.environ.get("MONGODB_URI")

# TESTING CONFIG
class TestingConfig(Config):

    MONGO_URI = os.environ.get("MONGODB_URI")

# PRODUCTION CONFIG
class ProductionConfig(Config):

    MONGO_URI = os.environ.get("MONGODB_URI")


# ENV CONFiG
env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
    }
