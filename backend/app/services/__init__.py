"""业务服务层：通用 EntryService 按模块配置驱动，各模块不再各写一套规则。"""
from app.services.base import EntryService

__all__ = ["EntryService"]
