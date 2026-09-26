"""委托合同业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="contract",
    label="委托合同",
    entry_name="委托检验合同",
    code_field="合同编号",
    required_fields=["合同编号", "委托单位", "联系人"],
    status_order=["待签约", "执行中", "已完成", "已终止"],
    action_rules={"签约合同": "执行中", "终止合同": "已终止", "确认完成": "已完成"},
    negative_actions=[],
    list_doc="按合同编号与状态过滤委托合同列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条委托检验合同明细；不存在时给出可读的错误说明。",
    create_doc="登记一条委托检验合同，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条委托检验合同执行签约合同、终止合同、确认完成；不允许的动作会被拦下并说明原因。",
    export_doc="导出委托合同清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
