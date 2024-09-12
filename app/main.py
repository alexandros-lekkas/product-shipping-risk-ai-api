from config import Config

from fastapi import FastAPI

config = Config()
app = FastAPI(debug=config.debug)