#!/bin/sh
set -e

echo ">>> 等待 MySQL 就绪..."
python - <<'PYEOF'
import time, sys
import pymysql
from decouple import config

host     = config('DB_HOST',     default='maas-db')
port     = config('DB_PORT',     default='3306', cast=int)
user     = config('DB_USER',     default='root')
password = config('DB_PASSWORD', default='')
db_name  = config('DB_NAME',     default='maas_db')

for i in range(40):
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=password,
                               connect_timeout=5)
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
                f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        conn.close()
        print(f"[OK] MySQL 已就绪，数据库 `{db_name}` 已确认")
        sys.exit(0)
    except Exception as e:
        print(f"[{i+1}/40] 等待 MySQL... {e}")
        time.sleep(3)

print("[ERROR] MySQL 连接超时，退出")
sys.exit(1)
PYEOF

echo ">>> 执行数据库迁移..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo ">>> 收集静态文件..."
python manage.py collectstatic --noinput

echo ">>> 启动 Gunicorn (workers=4)..."
exec gunicorn maas_core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
