"""
数据库配置模块
支持 MySQL / PostgreSQL，通过 .env 切换，不使用 SQLite。
Docker 部署时直接通过环境变量注入，无需修改代码。
"""
from decouple import config

DB_ENGINE   = config('DB_ENGINE',   default='django.db.backends.mysql')
DB_NAME     = config('DB_NAME',     default='maas_db')
DB_USER     = config('DB_USER',     default='root')
DB_PASSWORD = config('DB_PASSWORD', default='')
DB_HOST     = config('DB_HOST',     default='127.0.0.1')
DB_PORT     = config('DB_PORT',     default='3306')

DATABASES = {
    'default': {
        'ENGINE':   DB_ENGINE,
        'NAME':     DB_NAME,
        'USER':     DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST':     DB_HOST,
        'PORT':     DB_PORT,
        'OPTIONS': {
            'charset': 'utf8mb4',
            # MySQL 连接超时重连
            'connect_timeout': 10,
        },
        'CONN_MAX_AGE': 60,  # 连接复用 60 秒
    }
}
