from app.config import Config

import os
import uvicorn

config = Config("config.yaml")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=config.reload)