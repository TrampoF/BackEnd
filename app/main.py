"""
This module initializes the FastAPI application and includes the application routers.
"""

from fastapi import FastAPI

from .routers import channels, users


app = FastAPI()
app.include_router(channels.router)
app.include_router(users.router)
