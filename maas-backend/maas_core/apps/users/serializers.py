import re
from rest_framework import serializers
from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    phone    = serializers.CharField(max_length=11)
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_phone(self, value):
        if not re.fullmatch(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('请输入有效的 11 位手机号')
        return value

    def validate(self, attrs):
        phone    = attrs['phone']
        password = attrs['password']

        user, created = CustomUser.objects.get_or_create(phone=phone)

        if created:
            # 首次登录：自动注册，设置密码
            user.set_password(password)
            user.save()
        else:
            # 已注册：校验密码
            if not user.check_password(password):
                raise serializers.ValidationError({'detail': '密码错误'})

        attrs['user'] = user
        return attrs
