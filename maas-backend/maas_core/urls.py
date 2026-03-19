"""
主路由文件
路由注册逻辑在 config/router.py 中管理，此处只做加载。
"""
from config.router import build_urlpatterns

urlpatterns = build_urlpatterns()
