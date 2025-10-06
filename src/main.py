import uvicorn
import sys
from fastapi import FastAPI
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from route.house import route as route_house
from route.auth import route as route_auth
from src.config import settings


app = FastAPI()
app.include_router(route_house)
app.include_router(route_auth)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)