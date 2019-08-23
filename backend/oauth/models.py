from django.db import models
from . import config
from django.utils import timezone
from .extensions import format_time, encrypt_code, decrypt_code, encrypt_token, decrypt_token, get_md5, aes, now
import random


class User(models.Model):
    username = models.CharField(max_length=128)  # 用户名
    password = models.CharField(max_length=128)  # 密码
    email = models.CharField(max_length=128)  # 邮箱地址
    nickname = models.CharField(max_length=128)  # 昵称
    create_time = models.DateTimeField()  # 创建时间
    user_type = models.PositiveSmallIntegerField(default=0, choices=[(0, 'student'), (1, 'teacher'), (2, 'others')])  # 用户类型 student, teacher, others
    permission = models.PositiveSmallIntegerField(default=0, choices=[(0, 'normal'), (1, 'admin'), (2, 'superadmin')])  # 用户权限类别 normal, admin, superadmin

    def __str__(self):
        return self.username

    @property
    def p_user_type(self):
        if self.user_type == 0:
            return 'student'
        elif self.user_type == 1:
            return 'teacher'
        else:
            return 'others'

    @p_user_type.setter
    def p_user_type(self, value):
        if value == 'student':
            self.user_type = 0
        elif value == 'teacher':
            self.user_type = 1
        elif value == 'others':
            self.user_type = 2
        else:
            raise ValueError('Value is out of choice(student, teacher, others)')

    @property
    def p_permission(self):
        if self.permission == 0:
            return 'normal'
        elif self.permission == 1:
            return 'admin'
        elif self.permission == 2:
            return 'superadmin'

    @p_permission.setter
    def p_permission(self, value):
        if value == 'normal':
            self.permission = 0
        elif value == 'admin':
            self.permission = 1
        elif value == 'superadmin':
            self.permission = 2
        else:
            raise ValueError('Value is out of choice(normal, admin, superadmin)')

    @staticmethod
    def get(username):
        sets = User.objects.filter(username=username)
        if len(sets) > 0:
            return sets.first()
        else:
            return None

    @staticmethod
    def create_stu(username, password, email):
        user = User(username=username, password=password, email=email, nickname='default', create_time=timezone.datetime.now())
        user.save()
        return user

    def to_dic(self):
        return {
            'username': self.username,
            'email': self.email,
            'nickname': self.nickname,
            'create_time': format_time(self.create_time),
            'user_type': self.p_user_type,
            'permission': self.p_permission
        }

    @staticmethod
    def checkpw(username, password):
        return len(User.objects.filter(username=username, password=password)) > 0


class UserActivity(models.Model):
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)  # 用户
    software = models.CharField(max_length=64)  # 对应的软件名称，默认为'index'
    access_ip = models.CharField(max_length=64)  # 最后活动的ip地址
    access_id = models.CharField(max_length=64, default='')  # 用户访问识别码
    device_type = models.CharField(max_length=64)  # 设备类型名称
    access_time = models.DateTimeField()  # 最后活动的时间
    code = models.CharField(max_length=128)  # 第三方验证需要的code
    state = models.PositiveSmallIntegerField(default=0, choices=[(0, 'success'), (1, 'fail'), (2, 'banned')])

    def __str__(self):
        return f'{self.user.username} {self.software} {self.device_type}'

    @property
    def p_state(self):
        if self.state == 0:
            if (now() - self.access_time.astimezone()).days < config.STABLE_TIME:
                return 'success'
            else:
                return 'fail'
        elif self.state == 1:
            return 'fail'
        elif self.state == 2:
            return 'banned'

    @p_state.setter
    def p_state(self, value):
        if value == 'success':
            self.state = 0
        elif value == 'fail':
            self.state = 1
        elif value == 'banned':
            self.state = 2
        else:
            raise ValueError('Value is out of choice(success, fail, banned)')

    @property
    def token(self):
        return encrypt_token(self.user.username, self.access_id, self.software, self.device_type)

    @property
    def alive(self):
        return (now() - self.access_time.astimezone()).days < config.STABLE_TIME and self.p_state == 'success'

    def generate_id(self):
        id_raw = f'{self.user.username}::{self.software}::{self.access_time}::{random.randrange(10,100)}'
        self.access_id = get_md5(id_raw)

    def update(self, access_ip):
        self.access_time = timezone.datetime.now()
        self.access_ip = access_ip
        self.save()

    @staticmethod
    def x_update(user: User, software: str, device_type: str, access_ip: str, access_id):
        act = None
        if access_id is not None:
            sets = UserActivity.objects.filter(
                user=user,
                software=software,
                device_type=device_type,
                access_id=access_id
            )
            if len(sets) > 0:
                act = sets[0]
        if act is None:
            act = UserActivity(
                user=user,
                software=software,
                device_type=device_type,
                code='',
                state=0
            )
            if access_id is None:
                act.generate_id()
            else:
                act.access_id = access_id
        act.access_time = timezone.datetime.now()
        act.access_ip = access_ip
        act.save()
        return act

    def to_dic(self, token):
        dic = self.user.to_dic()
        dic['access_time'] = format_time(self.access_time)
        dic['token'] = token
        return dic

    def to_dic_state(self):
        dic = self.user.to_dic()
        dic['access_time'] = format_time(self.access_time)
        dic['state'] = self.p_state
        return dic

    def to_dic_simple(self):
        dic = {
            'software': self.software,
            'device_type': self.device_type,
            'access_time': format_time(self.access_time),
            'access_ip': self.access_ip,
            'access_id': self.access_id,
            'state': self.p_state,
        }
        return dic

    @staticmethod
    def get(token):
        data_raw = decrypt_token(token)
        users = User.objects.filter(username=data_raw['uid'])
        if len(users) > 0:
            software = data_raw['software']
            access_id = data_raw['access_id']
            device_type = data_raw['device_type']
            sets = UserActivity.objects.filter(user=users[0], software=software, access_id=access_id, device_type=device_type)
            if len(sets) > 0:
                return sets[0]
        return None


class AppScheme(models.Model):
    name = models.CharField(max_length=64)
    title = models.CharField(max_length=256, default='')
    owner = models.ForeignKey(User, related_name='apps', on_delete=models.CASCADE)
    create_time = models.DateTimeField()
    description = models.TextField(default='')
    tags = models.TextField(default='')
    appkey = models.CharField(max_length=256)
    state = models.PositiveSmallIntegerField(default=0, choices=[(0, 'wait'), (1, 'success'), (2, 'fail')])

    def __str__(self):
        return self.name

    @property
    def code(self):
        return encrypt_code(self.name, self.appkey, timezone.datetime.now())

    @staticmethod
    def alive(code):
        code_raw = decrypt_code(code)
        app = AppScheme.get(code_raw['name'])
        if app is None:
            raise KeyError(f'app {app} is not found.')
        elif (now() - code_raw['time'].astimezone()).total_seconds() < config.CODE_TIME:
            return True
        return False

    @staticmethod
    def allow_login(code):
        code_raw = decrypt_code(code)
        app = AppScheme.get(code_raw['name'])
        if app is None or app.appkey != code_raw['appkey']:
            raise KeyError(f'app {app} is not found.')
        elif (now() - code_raw['time'].astimezone()).total_seconds() < config.CODE_LOGIN_TIME:
            return True
        return False

    @staticmethod
    def from_code(code):
        code_raw = decrypt_code(code)
        return AppScheme.get(code_raw['name'])

    @property
    def p_state(self):
        if self.state == 0:
            return 'wait'
        elif self.state == 1:
            return 'success'
        elif self.state == 2:
            return 'fail'

    @p_state.setter
    def p_state(self, value):
        if value == 'wait':
            self.state = 0
        elif value == 'success':
            self.state = 1
        elif value == 'fail':
            self.state = 2
        else:
            raise ValueError('Value is out of choice(wait, success, fail)')

    @staticmethod
    def get(name):
        sets = AppScheme.objects.filter(name=name)
        if len(sets) > 0:
            return sets[0]
        else:
            return None

    def to_dic(self):
        return {
            'name': self.name,
            'owner': self.owner.username,
            'create_time': format_time(self.create_time),
            'description': self.description,
            'tags': self.tags,
            'state': self.p_state,
        }

    def generate_appkey(self):
        self.appkey = aes.encrypt(f'{self.name}::{self.owner.username}')

