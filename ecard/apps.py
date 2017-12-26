from django.apps import AppConfig


class EcardConfig(AppConfig):
    name = 'ecard'

class ErrorCode():
    """
    名字定义格式：
    方法名_干什么_成功(y)/失败(n)
    """
    'check_u_s':10000,
    'check_us_no_ek':10001,
    'session_ss':100002,
    'session_no':100003,

