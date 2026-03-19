# 兼容旧引用，实际路由已迁移到 routes/auth.py
from maas_core.apps.users.routes.auth import urlpatterns  # noqa: F401
