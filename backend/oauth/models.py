from django.db import models, transaction
from . import config
from django.utils.timezone import datetime
from .extensions import format_time, encrypt_code, decrypt_code, encrypt_token, decrypt_token, get_md5, aes, now, encrypt_refresh_token, decrypt_refresh_token
import random
from .apis import jh_user
from .consts import SHORTCUT


class User(models.Model):

    class Permission:
        NORMAL = 0
        ADMIN = 1
        SUPER_ADMIN = 2

        @staticmethod
        def to_str(arg: int):
            if arg == User.Permission.NORMAL:
                return 'normal'
            elif arg == User.Permission.ADMIN:
                return 'admin'
            elif arg == User.Permission.SUPER_ADMIN:
                return 'superadmin'
            raise ValueError()

        @staticmethod
        def to_value(arg: str):
            if arg == 'normal':
                return User.Permission.NORMAL
            elif arg == 'admin':
                return User.Permission.ADMIN
            elif arg == 'superadmin':
                return User.Permission.SUPER_ADMIN
            raise ValueError()

    username = models.CharField(max_length=128)  # 用户名
    password = models.CharField(max_length=128)  # 密码
    email = models.CharField(max_length=128)  # 邮箱地址
    nickname = models.CharField(max_length=128)  # 昵称
    create_time = models.DateTimeField()  # 创建时间
    permission = models.PositiveSmallIntegerField(default=0, choices=[(0, 'normal'), (1, 'admin'), (2, 'superadmin')])  # 用户权限类别 normal, admin, superadmin

    def __str__(self):
        return self.username

    @staticmethod
    def get(username):
        sets = User.objects.filter(username=username)
        if len(sets) > 0:
            return sets.first()
        else:
            return None

    @staticmethod
    def create_or_update(username, password, email):
        sets = User.objects.filter(username=username)
        if sets.exists():
            user = sets.first()
            user.password = password
            user.email = email
        else:
            user = User(username=username, password=password, email=email, nickname='default', create_time=datetime.now())
        user.save()
        return user

    def to_dic(self):
        return {
            'username': self.username,
            'email': self.email,
            'nickname': self.nickname,
            'create_time': format_time(self.create_time),
            'permission': User.Permission.to_str(self.permission)
        }

    def check_password(self):
        data = jh_user.login(self.username, self.password)
        return data['shortcut']


class UserActivity(models.Model):

    class State:
        SUCCESS = 0
        FAIL = 1
        BANNED = 2

        @staticmethod
        def to_str(arg: int):
            if arg == UserActivity.State.SUCCESS:
                return 'success'
            elif arg == UserActivity.State.FAIL:
                return 'fail'
            elif arg == UserActivity.State.BANNED:
                return 'banned'
            raise ValueError()

        @staticmethod
        def to_value(arg: str):
            if arg == 'success':
                return UserActivity.State.SUCCESS
            elif arg == 'fail':
                return UserActivity.State.FAIL
            elif arg == 'banned':
                return UserActivity.State.BANNED
            raise ValueError()

    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)  # 用户
    software = models.CharField(max_length=64)  # 对应的软件名称，默认为'index'
    access_ip = models.CharField(max_length=64)  # 最后活动的ip地址
    access_id = models.CharField(max_length=64, default='')  # 用户访问识别码
    device_type = models.CharField(max_length=64)  # 设备类型名称
    access_time = models.DateTimeField()  # 最后活动的时间
    code = models.CharField(max_length=128, default='')  # 第三方验证需要的code
    state = models.PositiveSmallIntegerField(default=0, choices=[(0, 'success'), (1, 'fail'), (2, 'banned')])

    def __str__(self):
        return f'{self.user.username} {self.software} {self.device_type}'

    def generate_code(self, appkey):
        self.code = encrypt_code(self.software, appkey, self.access_id)

    @property
    def token(self):
        return encrypt_token(self.user.username, self.access_id, self.software, self.device_type)

    @property
    def refresh_token(self):
        return encrypt_refresh_token(self.user.username, self.access_id, self.software, self.device_type)

    @property
    def alive(self):
        return (now() - self.access_time.astimezone()).days < config.STABLE_TIME and self.state == UserActivity.State.SUCCESS

    def generate_id(self):
        id_raw = f'{self.user.username}::{self.software}::{self.access_time}::{random.randrange(10,100)}'
        self.access_id = get_md5(id_raw)

    def update(self, access_ip):
        self.access_time = datetime.now()
        self.access_ip = access_ip
        self.save()

    @staticmethod
    def assert_one_login(act):
        with transaction.atomic():
            # TODO 使用批量事务进行处理
            acts = UserActivity.objects.filter(user=act.user, software='index', device_type=act.device_type)
            for item in acts:
                if item.access_id != act.access_id:
                    item.state = UserActivity.State.FAIL
                else:
                    item.p_state = UserActivity.State.SUCCESS
                item.save()

    @staticmethod
    def create_or_update(user: User, software: str, device_type: str, access_ip: str, access_id):
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
        act.access_time = datetime.now()
        act.access_ip = access_ip
        act.save()
        UserActivity.assert_one_login(act)
        return act

    @staticmethod
    def code_effect(code, appkey):
        """
        判断code是否存在，如果存在，请返回True并清空code，防止被盗用
        :param code:
        :param appkey:
        :return:
        """
        code_raw = decrypt_code(code)
        app = AppScheme.get(code_raw['name'])
        if app is None:
            raise KeyError(f'app {app} is not found.')
        elif app.appkey != appkey:
            raise ValueError(f'appkey is invalid')
        else:
            sets = UserActivity.objects.filter(code=code)
            if sets.exists():
                sets[0].code = ""
                return sets[0]
        return None

    def to_dic(self, token):
        dic = self.user.to_dic()
        dic['access_time'] = format_time(self.access_time)
        dic['token'] = token
        return dic

    def to_dic_oauth(self, token, refresh_token):
        dic = self.to_dic(token)
        dic['refresh_token'] = refresh_token
        return dic

    def to_dic_state(self):
        dic = self.user.to_dic()
        dic['access_time'] = format_time(self.access_time)
        dic['state'] = UserActivity.State.to_str(self.state)
        return dic

    def to_dic_simple(self):
        dic = {
            'software': self.software,
            'device_type': self.device_type,
            'access_time': format_time(self.access_time),
            'access_ip': self.access_ip,
            'access_id': self.access_id,
            'state': UserActivity.State.to_str(self.state),
        }
        return dic

    @staticmethod
    def get(token):
        data_raw = decrypt_token(token)
        if data_raw is None:
            return None
        users = User.objects.filter(username=data_raw['uid'])
        if users.exists():
            software = data_raw['software']
            access_id = data_raw['access_id']
            device_type = data_raw['device_type']
            sets = UserActivity.objects.filter(user=users[0], software=software, access_id=access_id, device_type=device_type)
            if sets.exists():
                return sets[0]
        return None

    @staticmethod
    def get_index_of(token):
        act = UserActivity.get(token)
        if act is not None:
            sets = UserActivity.objects.filter(user=act.user, software='index', access_id=act.access_id, device_type=act.device_type)
            if sets.exists():
                return sets[0]
        return None

    @staticmethod
    def from_refresh_token(refresh_token):
        token_raw = decrypt_refresh_token(refresh_token)
        uid = token_raw['uid']
        software = token_raw['software']
        access_id = token_raw['access_id']
        device_type = token_raw['device_type']
        sets = UserActivity.objects.filter(user=User.get(uid), software=software, access_id=access_id, device_type=device_type)
        if sets.exists():
            return sets.first()
        return None


class AppScheme(models.Model):

    class State:
        WAIT = 0
        SUCCESS = 1
        FAIL = 2

        @staticmethod
        def to_str(arg: int):
            if arg == AppScheme.State.WAIT:
                return 'wait'
            elif arg == AppScheme.State.SUCCESS:
                return 'success'
            elif arg == AppScheme.State.FAIL:
                return 'fail'
            raise ValueError()

        @staticmethod
        def to_value(arg: str):
            if arg == 'wait':
                return AppScheme.State.SUCCESS
            elif arg == 'success':
                return AppScheme.State.SUCCESS
            elif arg == 'fail':
                return AppScheme.State.FAIL
            raise ValueError()

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

    @staticmethod
    def create(owner: User, appname: str, title, description):
        sets = AppScheme.objects.filter(name=appname)
        if sets.exists():
            return None
        app = AppScheme(owner=owner, name=appname, create_time=datetime.now(), title=title, description=description)
        app.generate_appkey()
        app.save()
        return app

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

    @staticmethod
    def get(name):
        sets = AppScheme.objects.filter(name=name)
        if sets.exists():
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
            'state': AppScheme.State.to_str(self.state),
        }

    def generate_appkey(self):
        self.appkey = aes.encrypt(f'{self.name}::{self.owner.username}')

