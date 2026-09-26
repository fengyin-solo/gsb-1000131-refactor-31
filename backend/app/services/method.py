"""检测方法业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="method",
    label="检测方法",
    entry_name="检测方法",
    code_field="方法编号",
    required_fields=["方法编号", "方法名称", "适用标准"],
    status_order=["草案", "验证中", "现行有效", "已废止"],
    action_rules={"发起验证": "验证中", "确认有效": "现行有效", "废止方法": "已废止"},
    negative_actions=[],
    list_doc="按方法编号与状态过滤检测方法列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测方法明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测方法，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测方法执行发起验证、确认有效、废止方法；不允许的动作会被拦下并说明原因。",
    export_doc="导出检测方法清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
