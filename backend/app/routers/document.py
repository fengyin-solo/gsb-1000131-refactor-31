"""体系文档接口：维护体系文档，覆盖提交审批、正式发布、作废文档等动作。"""
from __future__ import annotations

from app.modules import MODULES
from app.routers.base import build_router

CONFIG = MODULES["document"]

router = build_router(CONFIG)

# 保留原有模块级常量，字段口径统一由 app.modules.MODULES 维护
LIST_FIELDS = list(CONFIG.list_fields)
STATUSES = list(CONFIG.statuses)
