import os

from app.config import Config
from app.routes.routes import router as api_router

from fastapi import FastAPI

current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, '..', 'config.yaml')
config = Config(config_path)

app = FastAPI(debug=config.debug)
app.include_router(api_router)