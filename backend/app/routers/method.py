"""检测方法接口：由通用路由工厂生成。"""
from __future__ import annotations

from app.routers.common import build_router
from app.services.method import CONFIG

router = build_router(CONFIG)
