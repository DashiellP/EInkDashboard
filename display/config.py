import os
from dotenv import load_dotenv

class Config():
    def __init__(self):
        load_dotenv("env/server.env")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ICLOUD_USER = os.getenv("ICLOUD_USER")
        self.ICLOUD_PASSWORD = os.getenv("ICLOUD_PASSWORD")
        self.SERVER_URL = os.getenv("SERVER_URL")

        self.OPEN_WEATHER_MAP_API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")

config = Config()