
class REQUEST:
    TIMEOUT = 10


class RESPONSE:
    OK = 200


class SHORTCUT:
    AE = 'ae'
    AFE = 'afe'
    OK = 'ok'
    PWE = 'pwe'  # 密码错误
    UNE = 'une'  # 用户不存在
    PE = 'pe'  # 权限不足
    TOKEN_ERROR = 'te'  # token错误
    TLE = 'tle'  # 用户的token处于过期的状态
    SE = 'se'  # 软件没有具有该项权限
    ANE = 'ane'  # 软件不存在
    AKE = 'ake'  # 软件的密钥不正确
    CE = 'ce'  # code错误

