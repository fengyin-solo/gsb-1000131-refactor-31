"""样品接收业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="sample",
    label="样品接收",
    entry_name="检测样品",
    code_field="样品编号",
    required_fields=["样品编号", "样品名称", "委托单位"],
    status_order=["待接收", "已接收", "已退回", "已废弃"],
    action_rules={"确认接收": "已接收", "退回样品": "已退回", "废弃样品": "已废弃"},
    negative_actions=[],
    list_doc="按样品编号与状态过滤样品接收列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测样品明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测样品，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测样品执行确认接收、退回样品、废弃样品；不允许的动作会被拦下并说明原因。",
    export_doc="导出样品接收清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
