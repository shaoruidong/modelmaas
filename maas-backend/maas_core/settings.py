"""
Django 配置入口
所有配置分模块管理，统一在此导入。
新增配置项请在 config/ 对应模块中修改，不要在此文件直接添加。
"""
# 兼容 PyMySQL
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

from config.base     import *   # noqa: F401,F403  基础配置
from config.database import *   # noqa: F401,F403  数据库
from config.auth     import *   # noqa: F401,F403  DRF + JWT
from config.cors     import *   # noqa: F401,F403  跨域
