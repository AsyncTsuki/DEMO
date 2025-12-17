import re
from typing import Any, Dict, List, Optional, Tuple


class ValidationError(Exception):
    """验证错误异常"""
    def __init__(self, message: str, field: str = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


def validate_required(data: Dict, fields: List[str]) -> Optional[str]:
    """验证必填字段"""
    for field in fields:
        if field not in data or data[field] is None or data[field] == '':
            return f'缺少必填字段: {field}'
    return None


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_username(username: str) -> Tuple[bool, str]:
    """验证用户名格式"""
    if len(username) < 3:
        return False, '用户名长度不能少于3个字符'
    if len(username) > 50:
        return False, '用户名长度不能超过50个字符'
    if not re.match(r'^[a-zA-Z0-9_\u4e00-\u9fa5]+$', username):
        return False, '用户名只能包含字母、数字、下划线和中文'
    return True, ''


def validate_password(password: str) -> Tuple[bool, str]:
    """验证密码强度"""
    if len(password) < 6:
        return False, '密码长度不能少于6个字符'
    if len(password) > 128:
        return False, '密码长度不能超过128个字符'
    return True, ''


def validate_positive_number(value: Any, field_name: str) -> Tuple[bool, str]:
    """验证正数"""
    try:
        num = float(value)
        if num <= 0:
            return False, f'{field_name}必须大于0'
        return True, ''
    except (TypeError, ValueError):
        return False, f'{field_name}必须是数字'


def validate_non_negative_number(value: Any, field_name: str) -> Tuple[bool, str]:
    """验证非负数"""
    try:
        num = float(value)
        if num < 0:
            return False, f'{field_name}不能为负数'
        return True, ''
    except (TypeError, ValueError):
        return False, f'{field_name}必须是数字'


def validate_range(value: Any, min_val: float, max_val: float, field_name: str) -> Tuple[bool, str]:
    """验证数值范围"""
    try:
        num = float(value)
        if num < min_val or num > max_val:
            return False, f'{field_name}必须在{min_val}到{max_val}之间'
        return True, ''
    except (TypeError, ValueError):
        return False, f'{field_name}必须是数字'


def validate_in_list(value: Any, allowed: List, field_name: str) -> Tuple[bool, str]:
    """验证值是否在允许列表中"""
    if value not in allowed:
        return False, f'{field_name}必须是以下值之一: {", ".join(map(str, allowed))}'
    return True, ''


def validate_time_format(time_str: str) -> Tuple[bool, str]:
    """验证时间格式 HH:MM"""
    pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$'
    if not re.match(pattern, time_str):
        return False, '时间格式必须为 HH:MM'
    return True, ''


def sanitize_string(value: str, max_length: int = 255) -> str:
    """清理字符串，去除首尾空格并限制长度"""
    if not isinstance(value, str):
        return str(value)[:max_length]
    return value.strip()[:max_length]
