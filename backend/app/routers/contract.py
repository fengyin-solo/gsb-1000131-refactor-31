"""委托合同接口：由通用路由工厂生成。"""
from __future__ import annotations

from app.routers.common import build_router
from app.services.contract import CONFIG

router = build_router(CONFIG)
