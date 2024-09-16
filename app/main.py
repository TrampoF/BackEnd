from fastapi import FastAPI

from app.routers import channels, profiles


app = FastAPI()
app.include_router(channels.router)
app.include_router(profiles.router)
