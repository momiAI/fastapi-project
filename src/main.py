import uvicorn
import sys
from fastapi import FastAPI
from pathlib import Path
from contextlib import asynccontextmanager
sys.path.append(str(Path(__file__).parent.parent))
from src import redis_manager
from route.house import route as route_house
from route.auth import route as route_auth
from route.organization import route as route_organization
from route.cottage import route as route_cottage
from route.booking import route as route_booking
from route.facilitiec import route as route_facilities

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    yield
    await redis_manager.close()
   






app = FastAPI(lifespan=lifespan)
app.include_router(route_house)
app.include_router(route_auth)
app.include_router(route_organization)
app.include_router(route_cottage)
app.include_router(route_booking)
app.include_router(route_facilities)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000,reload=True)