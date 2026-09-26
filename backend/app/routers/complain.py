"""客户申诉接口：维护申诉记录，覆盖受理申诉、提交答复、升级仲裁等动作。"""
from __future__ import annotations

from app.modules import MODULES
from app.routers.base import build_router

CONFIG = MODULES["complain"]

router = build_router(CONFIG)

# 保留原有模块级常量，字段口径统一由 app.modules.MODULES 维护
LIST_FIELDS = list(CONFIG.list_fields)
STATUSES = list(CONFIG.statuses)
