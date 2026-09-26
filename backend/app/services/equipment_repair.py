"""仪器维修业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="equipment_repair",
    label="仪器维修",
    entry_name="维修记录",
    code_field="维修编号",
    required_fields=["维修编号", "仪器编号", "故障描述"],
    status_order=["已报修", "维修中", "已修复", "无法修复"],
    action_rules={"派工维修": "维修中", "确认修复": "已修复", "标记报废": "无法修复"},
    negative_actions=[],
    list_doc="按维修编号与状态过滤仪器维修列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条维修记录明细；不存在时给出可读的错误说明。",
    create_doc="登记一条维修记录，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条维修记录执行派工维修、确认修复、标记报废；不允许的动作会被拦下并说明原因。",
    export_doc="导出仪器维修清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
