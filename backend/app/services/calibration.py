"""校准记录业务规则：只声明本模块配置，流程复用 ModuleService。"""
from __future__ import annotations

from app.services.common import ModuleConfig, ModuleService

CONFIG = ModuleConfig(
    module="calibration",
    label="校准记录",
    entry_name="校准记录单",
    code_field="记录编号",
    required_fields=["记录编号", "仪器编号", "校准机构"],
    status_order=["待校准", "校准中", "已合格", "不合格"],
    action_rules={"执行校准": "校准中", "标记合格": "已合格", "标记不合格": "不合格"},
    negative_actions=[],
    list_doc="按记录编号与状态过滤校准记录列表；没有数据时返回空页，不报错。",
    detail_doc="读取单条校准记录单明细；不存在时给出可读的错误说明。",
    create_doc="登记一条校准记录单，缺字段时说明原因而不是静默丢弃。",
    action_doc="对单条校准记录单执行执行校准、标记合格、标记不合格；不允许的动作会被拦下并说明原因。",
    export_doc="导出校准记录清单：返回当前过滤条件下的全量数据。",
)

service = ModuleService(CONFIG)
