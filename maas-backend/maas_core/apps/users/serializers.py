import re
from rest_framework import serializers
from .models import CustomUser


def validate_phone_number(value):
    if not re.fullmatch(r'1[3-9]\d{9}', value):
        raise serializers.ValidationError('请输入有效的 11 位手机号')
    return value


class LoginSerializer(serializers.Serializer):
    phone    = serializers.CharField(max_length=11)
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_phone(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        phone    = attrs['phone']
        password = attrs['password']

        user, created = CustomUser.objects.get_or_create(phone=phone)

        if created:
            user.set_password(password)
            user.save()
        else:
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')

        attrs['user'] = user
        return attrs


class ResetPasswordSerializer(serializers.Serializer):
    """忘记密码：手机号 + 新密码，无需验证码"""
    phone        = serializers.CharField(max_length=11)
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate_phone(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        phone = attrs['phone']
        try:
            attrs['user'] = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('该手机号未注册')
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """用户信息读取 / 更新"""
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model  = CustomUser
        fields = ['id', 'phone', 'nickname', 'role', 'avatar_url', 'created_at']
        read_only_fields = ['id', 'phone', 'role', 'created_at']

    def get_avatar_url(self, obj):
        if not obj.avatar:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.avatar.url)
        return obj.avatar.url


class AvatarUploadSerializer(serializers.Serializer):
    """头像上传"""
    avatar = serializers.ImageField()
