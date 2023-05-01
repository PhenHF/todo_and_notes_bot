from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    def __init__(self, token) -> None:
        self.token = token

def load_config():
    return Config(token = os.getenv('API_TOKEN'))