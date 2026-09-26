"""检测人员接口：由通用路由工厂生成。"""
from __future__ import annotations

from app.routers.common import build_router
from app.services.staff import CONFIG

router = build_router(CONFIG)
