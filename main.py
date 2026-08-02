
from fastapi import FastAPI
from database import engine, Base
import app.models 
from app.routers import api_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Supermarket POS Modular System",
    
)


app.include_router(api_router)

