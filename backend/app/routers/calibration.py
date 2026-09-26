"""校准记录接口：维护校准记录单，覆盖执行校准、标记合格、标记不合格等动作。"""
from __future__ import annotations

from app.modules import MODULES
from app.routers.base import build_router

CONFIG = MODULES["calibration"]

router = build_router(CONFIG)

# 保留原有模块级常量，字段口径统一由 app.modules.MODULES 维护
LIST_FIELDS = list(CONFIG.list_fields)
STATUSES = list(CONFIG.statuses)
