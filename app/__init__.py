from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import gemini_router, service_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

app.include_router(gemini_router)
app.include_router(service_router)