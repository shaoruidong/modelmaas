"""
认证 & 用户路由
自动挂载到 PREFIX 指定的路径
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from maas_core.apps.users.views import (
    LoginView,
    ResetPasswordView,
    UserProfileView,
    AvatarUploadView,
)

PREFIX = 'api/auth/'

urlpatterns = [
    path('login/',          LoginView.as_view(),         name='auth-login'),
    path('reset-password/', ResetPasswordView.as_view(), name='auth-reset-password'),
    path('token/refresh/',  TokenRefreshView.as_view(),  name='token-refresh'),
    path('profile/',        UserProfileView.as_view(),   name='user-profile'),
    path('avatar/',         AvatarUploadView.as_view(),  name='user-avatar'),
]
