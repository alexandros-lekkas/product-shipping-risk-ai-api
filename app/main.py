from config import Config
from routes.routes import router as api_router

from fastapi import FastAPI

config = Config()

app = FastAPI(debug=config.debug)
app.include_router(api_router)