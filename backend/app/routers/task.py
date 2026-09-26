"""检测任务接口：维护检测任务单，覆盖分配任务、开始检测、提交复核等动作。"""
from __future__ import annotations

from app.modules import MODULES
from app.routers.base import build_router

CONFIG = MODULES["task"]

router = build_router(CONFIG)

# 保留原有模块级常量，字段口径统一由 app.modules.MODULES 维护
LIST_FIELDS = list(CONFIG.list_fields)
STATUSES = list(CONFIG.statuses)
