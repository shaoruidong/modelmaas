from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    LoginSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    AvatarUploadSerializer,
)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id':       user.id,
                'phone':    user.phone,
                'nickname': user.nickname,
                'role':     user.role,
                'avatar_url': (
                    request.build_absolute_uri(user.avatar.url)
                    if user.avatar else None
                ),
            },
        })


class ResetPasswordView(APIView):
    """忘记密码：手机号 + 新密码，无需验证码"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({'detail': '密码重置成功'})


class UserProfileView(APIView):
    """获取 / 更新当前用户信息（需登录）"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(
            request.user, context={'request': request}
        )
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AvatarUploadView(APIView):
    """上传头像（需登录）"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.FILES)
        serializer.is_valid(raise_exception=True)

        user = request.user
        # 删除旧头像文件
        if user.avatar:
            user.avatar.delete(save=False)

        user.avatar = serializer.validated_data['avatar']
        user.save()

        return Response({
            'avatar_url': request.build_absolute_uri(user.avatar.url)
        }, status=status.HTTP_200_OK)
