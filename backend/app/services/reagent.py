"""试剂耗材业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="reagent",
    label="试剂耗材",
    entry_name="试剂耗材",
    code_field="试剂编号",
    required_fields=["试剂编号", "试剂名称", "规格等级"],
    status_order=["在库", "已领用", "已用完", "已过期"],
    action_rules={"领用试剂": "已领用", "登记用完": "已用完", "标记过期": "已过期"},
    negative_actions=[],
    list_doc="按试剂编号与状态过滤试剂耗材列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条试剂耗材明细；不存在时给出可读的错误说明。",
    create_doc="登记一条试剂耗材，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条试剂耗材执行领用试剂、登记用完、标记过期；不允许的动作会被拦下并说明原因。",
    export_doc="导出试剂耗材清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
