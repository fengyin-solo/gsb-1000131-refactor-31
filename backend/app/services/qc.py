"""质量控制业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="qc",
    label="质量控制",
    entry_name="质控样品",
    code_field="质控编号",
    required_fields=["质控编号", "质控类别", "标准值"],
    status_order=["待检测", "检测中", "受控", "失控"],
    action_rules={"检测质控": "检测中", "确认受控": "受控", "标记失控": "失控"},
    negative_actions=[],
    list_doc="按质控编号与状态过滤质量控制列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条质控样品明细；不存在时给出可读的错误说明。",
    create_doc="登记一条质控样品，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条质控样品执行检测质控、确认受控、标记失控；不允许的动作会被拦下并说明原因。",
    export_doc="导出质量控制清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
