"""API v1 router."""
from fastapi import APIRouter
from app.api.v1 import auth, agents, uploads, runtime, logs, api_keys

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api-keys"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
api_router.include_router(runtime.router, prefix="/runtime", tags=["runtime"])
api_router.include_router(logs.router, prefix="/logs", tags=["logs"])

