"""检测任务业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="task",
    label="检测任务",
    entry_name="检测任务单",
    code_field="任务编号",
    required_fields=["任务编号", "所属样品", "检测项目"],
    status_order=["待分配", "已分配", "检测中", "已完成", "已复核"],
    action_rules={"分配任务": "已分配", "开始检测": "检测中", "提交复核": "已复核"},
    negative_actions=[],
    list_doc="按任务编号与状态过滤检测任务列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测任务单明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测任务单，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测任务单执行分配任务、开始检测、提交复核；不允许的动作会被拦下并说明原因。",
    export_doc="导出检测任务清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
