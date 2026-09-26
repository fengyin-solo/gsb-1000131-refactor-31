"""通用接口：列表、详情、登记、动作与导出只在这里写一遍，按模块配置生成路由。

分支判断（分页上限、记录不存在、缺字段、非法动作）与提示文案都收在这一个文件里，
各业务模块只保留 app.modules 中的一条配置和一行路由绑定。
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query

from app.config import settings
from app.modules import ModuleConfig
from app.schemas import ActionResult, EntryPayload, PageResult
from app.services.base import EntryService


def build_router(config: ModuleConfig) -> APIRouter:
    """按模块配置生成一套标准接口：列表、详情、登记、动作、导出。"""
    service = EntryService(config)
    router = APIRouter(prefix=f"/api/{config.name}", tags=[config.label])

    @router.get(
        "",
        response_model=PageResult[dict],
        description=f"按{config.keyword_field}与状态过滤{config.label}列表；没有数据时返回空页，不报错。",
    )
    def list_entries(
        keyword: str | None = Query(default=None, description=f"按{config.keyword_field}检索"),
        status: str | None = Query(default=None, description="、".join(config.statuses)),
        page: int = 1,
        size: int = 20,
    ) -> PageResult[dict]:
        if size > settings.page_size_max:
            raise HTTPException(status_code=400, detail=f"每页最多 {settings.page_size_max} 条，请缩小分页范围")
        items, total = service.list_entries(keyword=keyword, status=status, page=page, size=size)
        return PageResult(items=items, total=total, page=page, size=size)

    @router.get(
        "/{entry_id}",
        response_model=dict,
        description=f"读取单条{config.entity}明细；不存在时给出可读的错误说明。",
    )
    def get_entry(entry_id: int) -> dict:
        entry = service.get_entry(entry_id)
        if entry is None:
            raise HTTPException(status_code=404, detail=service.not_found_message(entry_id))
        return entry

    @router.post(
        "",
        response_model=ActionResult,
        description=f"登记一条{config.entity}，缺字段时说明原因而不是静默丢弃。",
    )
    def create_entry(payload: EntryPayload) -> ActionResult:
        entry, missing = service.create_entry(payload.values)
        if missing:
            return ActionResult(ok=False, message=f"缺少必填字段：{'、'.join(missing)}")
        return ActionResult(ok=True, message=f"{config.entity}已登记", entry=entry)

    @router.post(
        "/{entry_id}/actions",
        response_model=ActionResult,
        description=f"对单条{config.entity}执行{'、'.join(config.action_rules)}；不允许的动作会被拦下并说明原因。",
    )
    def run_action(entry_id: int, payload: EntryPayload) -> ActionResult:
        action = str(payload.values.get("action") or "").strip()
        entry, message = service.run_action(entry_id, action)
        if entry is None:
            return ActionResult(ok=False, message=message)
        return ActionResult(ok=True, message=message, entry=entry)

    @router.get(
        "/export",
        description=f"导出{config.label}清单：返回当前过滤条件下的全量数据。",
    )
    def export_entries() -> dict[str, Any]:
        items, total = service.list_entries(page=1, size=10000)
        return {"module": config.name, "total": total, "items": items}

    return router
