from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database.database import DataBase
from api.models.historical import Historical
from api.models.historical_training import HistoricalTraining
from api.models.training import Training
from api.models.user import User
from api.controllers.user import router as user_router
from api.controllers.auth import router as auth_router
from api.controllers.training import router as training_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.on_event("startup")
async def startup():
    database = DataBase()
    database.MODELS = [
            User,
            # HistoricalTraining,
            Historical,
            Training
        ]
    await database.init()

# # Inclui router
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(training_router)
