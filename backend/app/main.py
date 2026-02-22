# 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import router

app = FastAPI(title="DataVex Growth Intelligence Engine")

# ✅ CORS FIX (REQUIRED FOR BROWSER CALLS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],   # allows OPTIONS, POST, etc.
    allow_headers=["*"],   # allows Content-Type, Authorization, etc.
)

app.include_router(router)