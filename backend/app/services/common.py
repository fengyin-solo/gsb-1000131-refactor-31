"""业务模块通用能力：列表筛选、分页、必填校验与状态流转。

各业务模块（检测方法、样品接收等）只有配置差异，处理流程完全一致，
所以流程代码只在这里写一遍，模块文件只保留一份 ModuleConfig 配置。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.store import store


@dataclass(frozen=True)
class ModuleConfig:
    """描述一个业务模块的字段、状态序列、动作与文案口径。"""

    module: str
    label: str                       # 面向用户的模块名，如“检测方法”
    entry_name: str                  # 单条记录的称呼，如“检测方法”“检测任务单”
    code_field: str                  # 列表关键字检索所用编号字段
    required_fields: list[str]
    status_order: list[str]
    action_rules: dict[str, str]     # 动作 -> 目标状态
    negative_actions: list[str] = field(default_factory=list)
    # 各端点在接口文档（OpenAPI）里的描述，缺省回退到通用口径
    list_doc: str = "按编号与状态过滤列表；没有数据时返回空页，不报错。"
    detail_doc: str = "读取单条明细；不存在时给出可读的错误说明。"
    create_doc: str = "登记一条记录，缺字段时说明原因而不是静默丢弃。"
    action_doc: str = "对单条记录执行配置内动作；不允许的动作会被拦下并说明原因。"
    export_doc: str = "导出清单：返回全量数据。"

    def not_found_message(self, entry_id: int) -> str:
        return f"{self.entry_name} {entry_id} 不存在或已归档"

    def illegal_action_message(self, action: str) -> str:
        return f"动作「{action}」不属于{self.label}可执行范围"

    def action_done_message(self, action: str) -> str:
        return f"{self.entry_name}已{action}"


class ModuleService:
    """配置驱动的通用业务服务：流程统一，提示文案统一从配置取。"""

    def __init__(self, config: ModuleConfig) -> None:
        self.config = config

    def list_entries(
        self,
        *,
        keyword: str | None = None,
        status: str | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = store.rows(self.config.module)
        if keyword:
            code_field = self.config.code_field
            rows = [row for row in rows if keyword in str(row.get(code_field, ""))]
        if status:
            rows = [row for row in rows if row.get("status") == status]
        total = len(rows)
        start = max(page - 1, 0) * size
        return rows[start:start + size], total

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        return store.find(self.config.module, entry_id)

    def find_missing_fields(self, values: dict[str, Any]) -> list[str]:
        return [
            name
            for name in self.config.required_fields
            if not str(values.get(name) or "").strip()
        ]

    def create_entry(self, values: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
        missing = self.find_missing_fields(values)
        if missing:
            return None, missing
        rows = store.rows(self.config.module)
        entry: dict[str, Any] = {
            "id": max((int(row.get("id", 0)) for row in rows), default=0) + 1
        }
        entry.update({name: values.get(name) for name in self.config.required_fields})
        entry["status"] = self.config.status_order[0]
        entry["pending"] = True
        entry["abnormal"] = False
        rows.append(entry)
        return entry, []

    def run_action(self, entry_id: int, action: str) -> tuple[dict[str, Any] | None, str]:
        entry = store.find(self.config.module, entry_id)
        if entry is None:
            return None, self.config.not_found_message(entry_id)
        if action not in self.config.action_rules:
            return None, self.config.illegal_action_message(action)
        target = self.config.action_rules[action]
        if target not in self.config.status_order:
            return None, f"目标状态「{target}」不在允许的状态序列里"
        entry["status"] = target
        entry["pending"] = target != self.config.status_order[-1]
        entry["abnormal"] = action in self.config.negative_actions
        return entry, self.config.action_done_message(action)
