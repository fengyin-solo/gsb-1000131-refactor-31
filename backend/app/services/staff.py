"""检测人员业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="staff",
    label="检测人员",
    entry_name="检测员",
    code_field="员工编号",
    required_fields=["员工编号", "姓名", "技术职称"],
    status_order=["在岗", "培训中", "离岗", "停岗"],
    action_rules={"安排培训": "培训中", "确认离岗": "离岗", "恢复在岗": "在岗"},
    negative_actions=[],
    list_doc="按员工编号与状态过滤检测人员列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测员明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测员，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测员执行安排培训、确认离岗、恢复在岗；不允许的动作会被拦下并说明原因。",
    export_doc="导出检测人员清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
