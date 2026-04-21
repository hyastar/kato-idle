import re

def validate_username(username):
    if not username or len(username) < 3:
        return False, "用户名至少3个字符"
    if not re.match(r'^\w+$', username):
        return False, "用户名只能包含字母、数字和下划线"
    return True, ""

def validate_password(password):
    if not password or len(password) < 6:
        return False, "密码长度至少6位"
    return True, ""

def validate_email(email):
    if not email:
        return True, ""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "邮箱格式不正确"
    return True, ""

def validate_phone(phone):
    if not phone:
        return True, ""
    pattern = r'^1[3-9]\d{9}$'
    if not re.match(pattern, phone):
        return False, "手机号格式不正确"
    return True, ""
