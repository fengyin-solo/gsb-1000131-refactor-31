"""通用业务规则：列表筛选、登记校验与状态流转只在这里写一遍。

各模块的差异（字段、状态序列、动作规则、文案称呼）都由 app.modules.ModuleConfig 提供，
不再每个模块各抄一份。
"""
from __future__ import annotations

from typing import Any

from app.modules import ModuleConfig
from app.store import store


class EntryService:
    """按模块配置驱动的通用服务，覆盖列表、详情、登记与动作处理。"""

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
        rows = store.rows(self.config.name)
        if keyword:
            field = self.config.keyword_field
            rows = [row for row in rows if keyword in str(row.get(field, ""))]
        if status:
            rows = [row for row in rows if row.get("status") == status]
        total = len(rows)
        start = max(page - 1, 0) * size
        return rows[start:start + size], total

    def get_entry(self, entry_id: int) -> dict[str, Any] | None:
        return store.find(self.config.name, entry_id)

    def not_found_message(self, entry_id: int) -> str:
        """详情 404 与动作处理共用的提示文案。"""
        return f"{self.config.entity} {entry_id} 不存在或已归档"

    def create_entry(self, values: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
        required = self.config.required_fields
        missing = [field for field in required if not str(values.get(field) or "").strip()]
        if missing:
            return None, missing
        rows = store.rows(self.config.name)
        entry = {"id": max((int(row.get("id", 0)) for row in rows), default=0) + 1}
        entry.update({field: values.get(field) for field in required})
        entry["status"] = self.config.statuses[0]
        entry["pending"] = True
        entry["abnormal"] = False
        rows.append(entry)
        return entry, []

    def run_action(self, entry_id: int, action: str) -> tuple[dict[str, Any] | None, str]:
        entry = self.get_entry(entry_id)
        if entry is None:
            return None, self.not_found_message(entry_id)
        rules = self.config.action_rules
        if action not in rules:
            return None, f"动作「{action}」不属于{self.config.label}可执行范围"
        target = rules[action]
        if target not in self.config.statuses:
            return None, f"目标状态「{target}」不在允许的状态序列里"
        entry["status"] = target
        entry["pending"] = target != self.config.statuses[-1]
        entry["abnormal"] = action in self.config.negative_actions
        return entry, f"{self.config.entity}已{action}"
