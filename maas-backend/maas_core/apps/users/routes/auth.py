"""
认证路由
自动挂载到 PREFIX 指定的路径
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from maas_core.apps.users.views import LoginView

# 路由前缀（自动发现时使用）
PREFIX = 'api/auth/'

urlpatterns = [
    path('login/',         LoginView.as_view(),        name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
