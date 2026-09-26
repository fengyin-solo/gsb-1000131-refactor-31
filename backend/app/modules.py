"""业务模块注册表：各模块的字段、状态序列与动作规则全部收拢在这里。

列表、详情、登记、动作等处理逻辑只写一遍（见 app.services.base 与 app.routers.base），
模块之间的差异都用 ModuleConfig 表达；新增模块时在这里加一条配置即可。
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleConfig:
    """一个业务模块的全部差异点。

    name: 模块键，同时用作接口前缀 /api/{name} 与仓库存储键。
    label: 模块名称，用于路由标签与动作范围提示。
    entity: 单条记录的称呼，用于详情、登记与动作提示文案。
    required_fields: 登记必填字段；第一个字段同时作为列表检索关键字。
    list_fields: 列表展示字段（原各路由的 LIST_FIELDS）。
    statuses: 允许的状态序列（原 STATUSES / STATUS_ORDER），末位为终态。
    action_rules: 可执行动作到目标状态的映射。
    negative_actions: 执行后把记录标记为异常的动作。
    """

    name: str
    label: str
    entity: str
    required_fields: tuple[str, ...]
    list_fields: tuple[str, ...]
    statuses: tuple[str, ...]
    action_rules: dict[str, str]
    negative_actions: tuple[str, ...] = ()

    @property
    def keyword_field(self) -> str:
        """列表检索关键字固定取第一个必填字段（各模块的编号字段）。"""
        return self.required_fields[0]


MODULES: dict[str, ModuleConfig] = {config.name: config for config in [
    ModuleConfig(
        name="sample",
        label="样品接收",
        entity="检测样品",
        required_fields=("样品编号", "样品名称", "委托单位"),
        list_fields=("样品编号", "样品名称", "委托单位", "样品类型", "接收日期", "保存条件", "送样人员", "接收状态"),
        statuses=("待接收", "已接收", "已退回", "已废弃"),
        action_rules={"确认接收": "已接收", "退回样品": "已退回", "废弃样品": "已废弃"},
    ),
    ModuleConfig(
        name="task",
        label="检测任务",
        entity="检测任务单",
        required_fields=("任务编号", "所属样品", "检测项目"),
        list_fields=("任务编号", "所属样品", "检测项目", "检测标准", "指定检测员", "截止日期", "优先级", "任务状态"),
        statuses=("待分配", "已分配", "检测中", "已完成", "已复核"),
        action_rules={"分配任务": "已分配", "开始检测": "检测中", "提交复核": "已复核"},
    ),
    ModuleConfig(
        name="instrument",
        label="仪器管理",
        entity="检测仪器",
        required_fields=("仪器编号", "仪器名称", "型号规格"),
        list_fields=("仪器编号", "仪器名称", "型号规格", "所属实验室", "校准周期", "上次校准日", "下次校准日", "仪器状态"),
        statuses=("在用", "待校准", "校准中", "已停用", "已报废"),
        action_rules={"发起校准": "校准中", "完成校准": "在用", "停用仪器": "已停用"},
        negative_actions=("停用仪器",),
    ),
    ModuleConfig(
        name="calibration",
        label="校准记录",
        entity="校准记录单",
        required_fields=("记录编号", "仪器编号", "校准机构"),
        list_fields=("记录编号", "仪器编号", "校准机构", "校准日期", "校准结果", "偏差值", "校准证书号", "记录状态"),
        statuses=("待校准", "校准中", "已合格", "不合格"),
        action_rules={"执行校准": "校准中", "标记合格": "已合格", "标记不合格": "不合格"},
    ),
    ModuleConfig(
        name="reagent",
        label="试剂耗材",
        entity="试剂耗材",
        required_fields=("试剂编号", "试剂名称", "规格等级"),
        list_fields=("试剂编号", "试剂名称", "规格等级", "生产厂家", "有效期至", "存放位置", "领用人员", "使用状态"),
        statuses=("在库", "已领用", "已用完", "已过期"),
        action_rules={"领用试剂": "已领用", "登记用完": "已用完", "标记过期": "已过期"},
    ),
    ModuleConfig(
        name="result",
        label="检测结果",
        entity="检测结果",
        required_fields=("结果编号", "所属任务", "检测项"),
        list_fields=("结果编号", "所属任务", "检测项", "实测值", "标准限值", "判定结论", "检测日期", "结果状态"),
        statuses=("待录入", "已录入", "待审核", "已发布", "已作废"),
        action_rules={"录入结果": "已录入", "提交审核": "待审核", "作废结果": "已作废"},
        negative_actions=("作废结果",),
    ),
    ModuleConfig(
        name="report",
        label="检测报告",
        entity="检测报告",
        required_fields=("报告编号", "委托单位", "样品名称"),
        list_fields=("报告编号", "委托单位", "样品名称", "报告类型", "编制人", "批准人", "签发日期", "报告状态"),
        statuses=("待编制", "编制中", "待批准", "已签发", "已撤回"),
        action_rules={"编制报告": "编制中", "提交批准": "待批准", "撤回报告": "已撤回"},
    ),
    ModuleConfig(
        name="qc",
        label="质量控制",
        entity="质控样品",
        required_fields=("质控编号", "质控类别", "标准值"),
        list_fields=("质控编号", "质控类别", "标准值", "允许偏差", "实测值", "判定结果", "检测日期", "质控状态"),
        statuses=("待检测", "检测中", "受控", "失控"),
        action_rules={"检测质控": "检测中", "确认受控": "受控", "标记失控": "失控"},
    ),
    ModuleConfig(
        name="deviation",
        label="偏离处理",
        entity="偏离记录",
        required_fields=("偏离编号", "偏离描述", "涉及样品"),
        list_fields=("偏离编号", "偏离描述", "涉及样品", "发现人", "发现日期", "处理措施", "验证结果", "偏离状态"),
        statuses=("已发现", "调查中", "已处理", "已关闭"),
        action_rules={"发起调查": "调查中", "执行处理": "已处理", "关闭偏离": "已关闭"},
    ),
    ModuleConfig(
        name="sample_storage",
        label="样品留存",
        entity="留存样品",
        required_fields=("留存编号", "样品编号", "留存位置"),
        list_fields=("留存编号", "样品编号", "留存位置", "留存期限", "到期日期", "保管人员", "处理方式", "留存状态"),
        statuses=("留存中", "即将到期", "已处置", "已延期"),
        action_rules={"确认处置": "已处置", "申请延期": "已延期", "登记处置": "已处置"},
    ),
    ModuleConfig(
        name="contract",
        label="委托合同",
        entity="委托检验合同",
        required_fields=("合同编号", "委托单位", "联系人"),
        list_fields=("合同编号", "委托单位", "联系人", "样品数量", "检测项目", "合同金额", "签约日期", "合同状态"),
        statuses=("待签约", "执行中", "已完成", "已终止"),
        action_rules={"签约合同": "执行中", "终止合同": "已终止", "确认完成": "已完成"},
    ),
    ModuleConfig(
        name="staff",
        label="检测人员",
        entity="检测员",
        required_fields=("员工编号", "姓名", "技术职称"),
        list_fields=("员工编号", "姓名", "技术职称", "资质证书", "授权项目", "在岗状态", "考核日期", "考核结果"),
        statuses=("在岗", "培训中", "离岗", "停岗"),
        action_rules={"安排培训": "培训中", "确认离岗": "离岗", "恢复在岗": "在岗"},
    ),
    ModuleConfig(
        name="method",
        label="检测方法",
        entity="检测方法",
        required_fields=("方法编号", "方法名称", "适用标准"),
        list_fields=("方法编号", "方法名称", "适用标准", "检测范围", "检出限", "方法版本", "批准日期", "方法状态"),
        statuses=("草案", "验证中", "现行有效", "已废止"),
        action_rules={"发起验证": "验证中", "确认有效": "现行有效", "废止方法": "已废止"},
    ),
    ModuleConfig(
        name="environment",
        label="环境监测",
        entity="环境记录",
        required_fields=("记录编号", "监测区域", "温度值"),
        list_fields=("记录编号", "监测区域", "温度值", "湿度值", "压差值", "记录时间", "记录人员", "环境状态"),
        statuses=("正常", "预警", "超标", "已恢复"),
        action_rules={"登记预警": "预警", "确认超标": "超标", "标记恢复": "已恢复"},
    ),
    ModuleConfig(
        name="complain",
        label="客户申诉",
        entity="申诉记录",
        required_fields=("申诉编号", "申诉单位", "涉及报告"),
        list_fields=("申诉编号", "申诉单位", "涉及报告", "申诉内容", "受理日期", "处理结果", "回复日期", "申诉状态"),
        statuses=("待受理", "受理中", "已答复", "已撤诉", "升级仲裁"),
        action_rules={"受理申诉": "受理中", "提交答复": "已答复", "升级仲裁": "升级仲裁"},
    ),
    ModuleConfig(
        name="audit",
        label="内审管理",
        entity="内审记录",
        required_fields=("内审编号", "审核范围", "审核组长"),
        list_fields=("内审编号", "审核范围", "审核组长", "审核日期", "不符合项", "纠正期限", "跟踪验证", "内审状态"),
        statuses=("计划中", "执行中", "已完成", "跟踪中"),
        action_rules={"开始内审": "执行中", "完成内审": "已完成", "跟踪验证": "跟踪中"},
    ),
    ModuleConfig(
        name="equipment_repair",
        label="仪器维修",
        entity="维修记录",
        required_fields=("维修编号", "仪器编号", "故障描述"),
        list_fields=("维修编号", "仪器编号", "故障描述", "报修人", "报修日期", "维修单位", "修复日期", "维修状态"),
        statuses=("已报修", "维修中", "已修复", "无法修复"),
        action_rules={"派工维修": "维修中", "确认修复": "已修复", "标记报废": "无法修复"},
    ),
    ModuleConfig(
        name="document",
        label="体系文档",
        entity="体系文档",
        required_fields=("文档编号", "文档名称", "文档类型"),
        list_fields=("文档编号", "文档名称", "文档类型", "编制人", "版本号", "生效日期", "分发范围", "文档状态"),
        statuses=("草案", "审批中", "正式发布", "已作废"),
        action_rules={"提交审批": "审批中", "正式发布": "正式发布", "作废文档": "已作废"},
        negative_actions=("作废文档",),
    ),
]}
