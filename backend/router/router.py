from fastapi import APIRouter
from controller import health_controller, marker_controller, contract_create_controller

api_router = APIRouter()

api_router.include_router(health_controller.router, prefix="/health", tags=["health"])
# api_router.include_router(marker_controller.router, prefix="/markers", tags=["marker"])
api_router.include_router(contract_create_controller.router, prefix="/contracts", tags=["create-contract"])