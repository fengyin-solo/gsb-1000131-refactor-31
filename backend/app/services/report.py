"""检测报告业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="report",
    label="检测报告",
    entry_name="检测报告",
    code_field="报告编号",
    required_fields=["报告编号", "委托单位", "样品名称"],
    status_order=["待编制", "编制中", "待批准", "已签发", "已撤回"],
    action_rules={"编制报告": "编制中", "提交批准": "待批准", "撤回报告": "已撤回"},
    negative_actions=[],
    list_doc="按报告编号与状态过滤检测报告列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测报告明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测报告，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测报告执行编制报告、提交批准、撤回报告；不允许的动作会被拦下并说明原因。",
    export_doc="导出检测报告清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
