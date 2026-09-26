"""环境监测业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="environment",
    label="环境监测",
    entry_name="环境记录",
    code_field="记录编号",
    required_fields=["记录编号", "监测区域", "温度值"],
    status_order=["正常", "预警", "超标", "已恢复"],
    action_rules={"登记预警": "预警", "确认超标": "超标", "标记恢复": "已恢复"},
    negative_actions=[],
    list_doc="按记录编号与状态过滤环境监测列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条环境记录明细；不存在时给出可读的错误说明。",
    create_doc="登记一条环境记录，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条环境记录执行登记预警、确认超标、标记恢复；不允许的动作会被拦下并说明原因。",
    export_doc="导出环境监测清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
