"""检测任务接口：由通用路由工厂生成。"""
from __future__ import annotations

from app.routers.common import build_router
from app.services.task import CONFIG

router = build_router(CONFIG)
