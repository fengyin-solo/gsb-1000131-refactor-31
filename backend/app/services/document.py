"""体系文档业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="document",
    label="体系文档",
    entry_name="体系文档",
    code_field="文档编号",
    required_fields=["文档编号", "文档名称", "文档类型"],
    status_order=["草案", "审批中", "正式发布", "已作废"],
    action_rules={"提交审批": "审批中", "正式发布": "正式发布", "作废文档": "已作废"},
    negative_actions=["作废文档"],
    list_doc="按文档编号与状态过滤体系文档列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条体系文档明细；不存在时给出可读的错误说明。",
    create_doc="登记一条体系文档，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条体系文档执行提交审批、正式发布、作废文档；不允许的动作会被拦下并说明原因。",
    export_doc="导出体系文档清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
