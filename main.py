from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller.intent_controller import router as intent_router

app = FastAPI(title="Smart-X FAQ Bot")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(intent_router)
