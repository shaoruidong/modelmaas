# MaaS 大模型平台

## 服务说明

| 服务 | 端口 | 说明 |
|------|------|------|
| maas-frontend | 5713 | Vue3 前端，Nginx 托管 |
| maas-backend | 8000 | Django REST API |
| maas-db | 3307 | MySQL 8.0（宿主机端口，容器内 3306） |

所有容器通过 `maas-network` 内部网络通信。

---

## 部署（服务器上）

### 前置条件
```bash
# 安装 Docker（Ubuntu）
curl -fsSL https://get.docker.com | sh
apt install docker-compose-plugin -y
```

### 首次部署
```bash
# 1. 拉取代码
git clone <your-repo> /opt/maas && cd /opt/maas

# 2. 配置环境变量（只需改 DB_PASSWORD 和 SECRET_KEY）
cp .env.example .env
vi .env

# 3. 一键构建并启动
docker compose up -d --build

# 4. 查看日志
docker compose logs -f
```

### 更新部署
```bash
git pull
docker compose down
docker compose up -d --build
docker image prune -f   # 清理旧镜像层
```

---

## 配置说明（.env）

只需关心这几项：

```ini
SECRET_KEY=          # Django 密钥，生产环境必须改
DB_PASSWORD=         # MySQL 密码，容器初始化时自动设置
ALLOWED_HOSTS=       # 服务器 IP 或域名
CORS_ALLOWED_ORIGINS= # 前端地址
```

---

## 常用命令

```bash
docker compose ps                          # 查看容器状态
docker compose logs -f maas-backend        # 查看后端日志
docker compose exec maas-backend bash      # 进入后端容器
docker compose exec maas-db mysql -uroot -p  # 连接数据库
docker compose down                        # 停止所有容器（数据不丢失）
docker compose down -v                     # 停止并删除数据（慎用）
```

---

## 新增接口

在 `maas-backend/maas_core/apps/<app>/routes/` 下新建 `.py` 文件：

```python
PREFIX = 'api/xxx/'
urlpatterns = [path('...', MyView.as_view())]
```

重启后端自动挂载，无需修改其他文件：
```bash
docker compose restart maas-backend
```

---

## 当前接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login/ | 登录即注册（手机号+密码） |
| POST | /api/auth/token/refresh/ | 刷新 Token |
