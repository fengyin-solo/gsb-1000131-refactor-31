"""业务模块通用路由工厂：列表、详情、登记、动作与导出只实现一遍。

各模块用同一份 ModuleConfig + ModuleService 生成路由，
分页口径、分支判断与提示文案统一从这里出，避免每个模块各写一套。
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.schemas import ActionResult, EntryPayload, PageResult
from app.services.common import ModuleConfig, ModuleService

PAGE_SIZE_TOO_LARGE = "每页最多 {max_size} 条，请缩小分页范围"
MISSING_FIELDS = "缺少必填字段：{fields}"
CREATED = "{entry_name}已登记"


def build_router(config: ModuleConfig, *, service: ModuleService | None = None) -> APIRouter:
    """按模块配置生成标准 CRUD/动作路由。"""
    service = service or ModuleService(config)
    status_text = "、".join(config.status_order)
    router = APIRouter(prefix=f"/api/{config.module}", tags=[config.label])

    @router.get("", response_model=PageResult[dict])
    def list_entries(
        keyword: str | None = Query(default=None, description=f"按{config.code_field}检索"),
        status: str | None = Query(default=None, description=status_text),
        page: int = 1,
        size: int = settings.page_size_default,
    ) -> PageResult[dict]:
        if size > settings.page_size_max:
            raise HTTPException(
                status_code=400,
                detail=PAGE_SIZE_TOO_LARGE.format(max_size=settings.page_size_max),
            )
        items, total = service.list_entries(keyword=keyword, status=status, page=page, size=size)
        return PageResult(items=items, total=total, page=page, size=size)

    list_entries.__doc__ = config.list_doc

    @router.get("/{entry_id}", response_model=dict)
    def get_entry(entry_id: int) -> dict:
        entry = service.get_entry(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=config.not_found_message(entry_id))
        return entry

    get_entry.__doc__ = config.detail_doc

    @router.post("", response_model=ActionResult)
    def create_entry(payload: EntryPayload) -> ActionResult:
        entry, missing = service.create_entry(payload.values)
        if missing:
            return ActionResult(ok=False, message=MISSING_FIELDS.format(fields="、".join(missing)))
        return ActionResult(
            ok=True, message=CREATED.format(entry_name=config.entry_name), entry=entry
        )

    create_entry.__doc__ = config.create_doc

    @router.post("/{entry_id}/actions", response_model=ActionResult)
    def run_action(entry_id: int, payload: EntryPayload) -> ActionResult:
        action = str(payload.values.get("action") or "").strip()
        entry, message = service.run_action(entry_id, action)
        if entry is None:
            return ActionResult(ok=False, message=message)
        return ActionResult(ok=True, message=message, entry=entry)

    run_action.__doc__ = config.action_doc

    @router.get("/export")
    def export_entries() -> dict[str, Any]:
        items, total = service.list_entries(page=1, size=10000)
        return {"module": config.module, "total": total, "items": items}

    export_entries.__doc__ = config.export_doc

    return router
