"""内审管理业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="audit",
    label="内审管理",
    entry_name="内审记录",
    code_field="内审编号",
    required_fields=["内审编号", "审核范围", "审核组长"],
    status_order=["计划中", "执行中", "已完成", "跟踪中"],
    action_rules={"开始内审": "执行中", "完成内审": "已完成", "跟踪验证": "跟踪中"},
    negative_actions=[],
    list_doc="按内审编号与状态过滤内审管理列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条内审记录明细；不存在时给出可读的错误说明。",
    create_doc="登记一条内审记录，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条内审记录执行开始内审、完成内审、跟踪验证；不允许的动作会被拦下并说明原因。",
    export_doc="导出内审管理清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
