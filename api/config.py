# iMPORTS #
# ------- #
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# base config
class Config():

    SECRET_KEY = os.environ.get("SECRET_KEY")
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT")

    @staticmethod
    def init_app(app):
        pass

# development config
class DevelopmentConfig(Config):

    DEBUG = True
    MONGO_URI = os.environ.get("MONGODB_URI")

# testing config
class TestingConfig(Config):

    MONGO_URI = os.environ.get("MONGODB_URI")

# production config
class ProductionConfig(Config):

    MONGO_URI = os.environ.get("MONGODB_URI")


# environment config
env_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
    }
