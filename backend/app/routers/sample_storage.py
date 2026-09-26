"""样品留存接口：维护留存样品，覆盖确认处置、申请延期、登记处置等动作。"""
from __future__ import annotations

from app.modules import MODULES
from app.routers.base import build_router

CONFIG = MODULES["sample_storage"]

router = build_router(CONFIG)

# 保留原有模块级常量，字段口径统一由 app.modules.MODULES 维护
LIST_FIELDS = list(CONFIG.list_fields)
STATUSES = list(CONFIG.statuses)
