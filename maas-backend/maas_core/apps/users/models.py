from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('手机号不能为空')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [('admin', '管理员'), ('user', '普通用户')]

    phone      = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    nickname   = models.CharField(max_length=32, blank=True, default='', verbose_name='昵称')
    avatar     = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    role       = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user', verbose_name='角色')
    is_active  = models.BooleanField(default=True, verbose_name='是否启用')
    is_staff   = models.BooleanField(default=False, verbose_name='是否管理员')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    USERNAME_FIELD  = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        return self.phone
