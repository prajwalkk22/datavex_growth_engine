from fastapi import FastAPI

from backend.app.api.routes import router
from backend.app.agents.signal_discovery import discover_signals

app = FastAPI(title="DataVex Growth Intelligence Engine")

app.include_router(router)