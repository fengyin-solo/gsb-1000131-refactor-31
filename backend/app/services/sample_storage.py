"""样品留存业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="sample_storage",
    label="样品留存",
    entry_name="留存样品",
    code_field="留存编号",
    required_fields=["留存编号", "样品编号", "留存位置"],
    status_order=["留存中", "即将到期", "已处置", "已延期"],
    action_rules={"确认处置": "已处置", "申请延期": "已延期", "登记处置": "已处置"},
    negative_actions=[],
    list_doc="按留存编号与状态过滤样品留存列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条留存样品明细；不存在时给出可读的错误说明。",
    create_doc="登记一条留存样品，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条留存样品执行确认处置、申请延期、登记处置；不允许的动作会被拦下并说明原因。",
    export_doc="导出样品留存清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
