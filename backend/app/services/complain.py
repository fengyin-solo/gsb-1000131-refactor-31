"""客户申诉业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="complain",
    label="客户申诉",
    entry_name="申诉记录",
    code_field="申诉编号",
    required_fields=["申诉编号", "申诉单位", "涉及报告"],
    status_order=["待受理", "受理中", "已答复", "已撤诉", "升级仲裁"],
    action_rules={"受理申诉": "受理中", "提交答复": "已答复", "升级仲裁": "升级仲裁"},
    negative_actions=[],
    list_doc="按申诉编号与状态过滤客户申诉列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条申诉记录明细；不存在时给出可读的错误说明。",
    create_doc="登记一条申诉记录，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条申诉记录执行受理申诉、提交答复、升级仲裁；不允许的动作会被拦下并说明原因。",
    export_doc="导出客户申诉清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
