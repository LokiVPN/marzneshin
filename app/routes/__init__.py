from fastapi import APIRouter

from . import (
    admin,
    node,
    service,
    inbounds,
    subscription,
    system,
    user,
    telegram_bot,
    telegram_web_app,
    notification,
)

api_router = APIRouter()

api_router.include_router(admin.router, prefix="/api")
api_router.include_router(node.router, prefix="/api")
api_router.include_router(service.router, prefix="/api")
api_router.include_router(inbounds.router, prefix="/api")
api_router.include_router(subscription.router)
api_router.include_router(system.router, prefix="/api")
api_router.include_router(user.router, prefix="/api")
api_router.include_router(notification.router, prefix="/api")
api_router.include_router(telegram_bot.router, prefix="/bot")
api_router.include_router(telegram_web_app.router, prefix="/web")

__all__ = ["api_router"]
