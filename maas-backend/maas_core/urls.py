"""
主路由文件
路由注册逻辑在 config/router.py 中管理，此处只做加载。
"""
from django.conf import settings
from django.conf.urls.static import static
from config.router import build_urlpatterns

urlpatterns = build_urlpatterns()

# 媒体文件（头像等）由 Django 直接 serve（生产环境由 nginx 接管）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
