from fastapi import APIRouter

from api.api_v1.endpoints import documents, messages, events

api_router = APIRouter()
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(messages.router, prefix="/messages", tags=["messages"])
api_router.include_router(events.router, prefix="/events", tags=["events"])