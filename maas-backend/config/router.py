"""
路由自动发现模块
────────────────────────────────────────────────────────────────────────────
规则：
  扫描 maas_core/apps/<app>/routes/*.py，每个文件只需定义：
    - urlpatterns: list        路由列表
    - PREFIX: str              URL 前缀，如 'api/auth/'（可选，默认用文件名推导）

新增接口只需：
  1. 在对应 app 的 routes/ 目录下新建 .py 文件
  2. 定义 urlpatterns 和 PREFIX
  3. 重启服务，路由自动挂载 ✓

手动注册（优先级高于自动发现）：
  MANUAL_ROUTES 列表，格式同之前
"""
import importlib
import pkgutil
from pathlib import Path
from django.urls import path, include
from django.contrib import admin

# ── 手动路由（特殊情况使用，一般留空）────────────────────────────────────────
MANUAL_ROUTES: list[dict] = []

# ── 自动发现配置 ──────────────────────────────────────────────────────────────
APPS_DIR = Path(__file__).resolve().parent.parent / 'maas_core' / 'apps'


def _discover_routes() -> list[tuple[str, str]]:
    """
    扫描所有 app 下的 routes/ 包，返回 [(prefix, module_path), ...]
    每个 routes/*.py 文件需定义：
        PREFIX = 'api/xxx/'
        urlpatterns = [...]
    """
    found = []
    if not APPS_DIR.exists():
        return found

    for app_dir in sorted(APPS_DIR.iterdir()):
        if not app_dir.is_dir():
            continue
        routes_dir = app_dir / 'routes'
        if not routes_dir.is_dir():
            continue

        # 确保 routes/ 是 Python 包
        init_file = routes_dir / '__init__.py'
        if not init_file.exists():
            init_file.touch()

        app_name = app_dir.name
        pkg_path = f'maas_core.apps.{app_name}.routes'

        try:
            pkg = importlib.import_module(pkg_path)
        except ImportError:
            continue

        for _, module_name, is_pkg in pkgutil.iter_modules([str(routes_dir)]):
            if is_pkg:
                continue
            module_path = f'{pkg_path}.{module_name}'
            try:
                mod = importlib.import_module(module_path)
            except ImportError as e:
                print(f'[router] 跳过 {module_path}: {e}')
                continue

            if not hasattr(mod, 'urlpatterns'):
                continue

            # PREFIX 优先用模块定义，否则推导为 api/<app>/<file>/
            prefix = getattr(mod, 'PREFIX', f'api/{app_name}/{module_name}/')
            found.append((prefix, module_path))
            print(f'[router] 自动挂载: {prefix}  ←  {module_path}')

    return found


def build_urlpatterns():
    """构建完整 urlpatterns：admin + 手动路由 + 自动发现路由"""
    patterns = [path('admin/', admin.site.urls)]

    # 手动路由
    for route in MANUAL_ROUTES:
        kwargs = {}
        if route.get('namespace'):
            kwargs['namespace'] = route['namespace']
        patterns.append(path(route['prefix'], include(route['urlconf'], **kwargs)))

    # 自动发现路由
    for prefix, module_path in _discover_routes():
        patterns.append(path(prefix, include(module_path)))

    return patterns
