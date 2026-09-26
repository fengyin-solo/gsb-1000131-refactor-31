"""检测结果业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="result",
    label="检测结果",
    entry_name="检测结果",
    code_field="结果编号",
    required_fields=["结果编号", "所属任务", "检测项"],
    status_order=["待录入", "已录入", "待审核", "已发布", "已作废"],
    action_rules={"录入结果": "已录入", "提交审核": "待审核", "作废结果": "已作废"},
    negative_actions=["作废结果"],
    list_doc="按结果编号与状态过滤检测结果列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条检测结果明细；不存在时给出可读的错误说明。",
    create_doc="登记一条检测结果，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条检测结果执行录入结果、提交审核、作废结果；不允许的动作会被拦下并说明原因。",
    export_doc="导出检测结果清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
