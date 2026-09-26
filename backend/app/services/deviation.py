"""偏离处理业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="deviation",
    label="偏离处理",
    entry_name="偏离记录",
    code_field="偏离编号",
    required_fields=["偏离编号", "偏离描述", "涉及样品"],
    status_order=["已发现", "调查中", "已处理", "已关闭"],
    action_rules={"发起调查": "调查中", "执行处理": "已处理", "关闭偏离": "已关闭"},
    negative_actions=[],
    list_doc="按偏离编号与状态过滤偏离处理列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条偏离记录明细；不存在时给出可读的错误说明。",
    create_doc="登记一条偏离记录，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条偏离记录执行发起调查、执行处理、关闭偏离；不允许的动作会被拦下并说明原因。",
    export_doc="导出偏离处理清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
