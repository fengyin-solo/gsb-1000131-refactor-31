"""仪器管理业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="instrument",
    label="仪器管理",
    entry_name="检测仪器",
    code_field="仪器编号",
    required_fields=["仪器编号", "仪器名称", "型号规格"],
    status_order=["在用", "待校准", "校准中", "已停用", "已报废"],
    action_rules={"发起校准": "校准中", "完成校准": "在用", "停用仪器": "已停用"},
    negative_actions=["停用仪器"],
    list_doc="按仪器编号与状态过滤仪器管理列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测仪器明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测仪器，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测仪器执行发起校准、完成校准、停用仪器；不允许的动作会被拦下并说明原因。",
    export_doc="导出仪器管理清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
