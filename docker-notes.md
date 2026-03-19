# MaaS 项目 Docker 技术笔记

本文档结合项目中的实际配置文件，解释所有用到的 Docker 技术点。

---

## 一、核心概念

Docker 有三个核心对象：

| 对象 | 说明 | 类比 |
|------|------|------|
| **镜像 Image** | 只读的模板，包含运行环境和代码 | 安装包 / 光盘 |
| **容器 Container** | 镜像运行起来的实例 | 安装后跑起来的程序 |
| **网络 Network** | 容器之间通信的虚拟局域网 | 内网交换机 |
| **数据卷 Volume** | 容器外部的持久化存储 | 外挂硬盘 |

---

## 二、Dockerfile 详解

Dockerfile 是构建镜像的"菜谱"，每一行是一个指令，从上到下执行。

### 2.1 后端 Dockerfile（`maas-backend/Dockerfile`）

```dockerfile
# ── 阶段1：安装依赖 ────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder   # 基础镜像，AS builder 给这个阶段起名

WORKDIR /app                       # 设置工作目录，后续命令都在 /app 下执行

RUN apt-get update && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/* # RUN 执行 shell 命令，安装 gcc 编译器

COPY requirements.txt .            # 把宿主机的 requirements.txt 复制进镜像
RUN pip install --no-cache-dir -r requirements.txt  # 安装 Python 依赖

# ── 阶段2：运行镜像 ────────────────────────────────────────────────────────────
FROM python:3.11-slim              # 重新用一个干净的基础镜像（不含 gcc 等编译工具）

WORKDIR /app

# 从 builder 阶段把安装好的包复制过来（不用重新安装）
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .                           # 把项目代码复制进镜像

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh        # 给启动脚本加执行权限

EXPOSE 8000                        # 声明容器监听 8000 端口（仅文档作用，不会自动映射）

ENTRYPOINT ["/entrypoint.sh"]      # 容器启动时执行的命令
```

**为什么用两阶段构建？**

- 阶段1（builder）：需要 gcc 来编译某些 Python 包，但 gcc 很大
- 阶段2（运行）：只需要编译好的包，不需要 gcc
- 结果：最终镜像体积更小，不含编译工具，更安全

### 2.2 前端 Dockerfile（`maas-front/Dockerfile`）

```dockerfile
# ── 阶段1：构建前端 ────────────────────────────────────────────────────────────
FROM node:22-alpine AS builder     # alpine 是极简 Linux，体积很小

WORKDIR /app

COPY package*.json ./              # 先只复制 package.json（利用缓存层）
RUN npm ci --prefer-offline        # npm ci 比 npm install 更严格，适合 CI/CD

COPY . .                           # 再复制源代码
RUN npm run build-only             # 执行 vite build，产物在 /app/dist

# ── 阶段2：Nginx 托管静态文件 ──────────────────────────────────────────────────
FROM nginx:1.27-alpine

RUN rm /etc/nginx/conf.d/default.conf          # 删除 nginx 默认配置

COPY nginx.conf /etc/nginx/conf.d/default.conf # 放入我们自己的配置
COPY --from=builder /app/dist /usr/share/nginx/html  # 把构建产物复制进来

EXPOSE 5713

CMD ["nginx", "-g", "daemon off;"]  # 前台运行 nginx（容器要求进程不能退出）
```

**为什么 `COPY package*.json` 要单独一行？**

Docker 构建有缓存机制：每一行指令如果输入没变，就复用上次的缓存。
把 `package.json` 单独复制，只要依赖没变，`npm ci` 就走缓存，不用重新下载，大幅加速构建。

### 2.3 常用 Dockerfile 指令速查

| 指令 | 作用 | 示例 |
|------|------|------|
| `FROM` | 指定基础镜像 | `FROM python:3.11-slim` |
| `WORKDIR` | 设置工作目录 | `WORKDIR /app` |
| `COPY` | 复制文件到镜像 | `COPY . .` |
| `RUN` | 构建时执行命令 | `RUN pip install -r requirements.txt` |
| `ENV` | 设置环境变量 | `ENV DEBUG=False` |
| `EXPOSE` | 声明端口（文档用） | `EXPOSE 8000` |
| `ENTRYPOINT` | 容器启动命令（不可被覆盖） | `ENTRYPOINT ["/entrypoint.sh"]` |
| `CMD` | 容器启动命令（可被覆盖） | `CMD ["nginx", "-g", "daemon off;"]` |
| `ARG` | 构建时参数 | `ARG NODE_ENV=production` |

---

## 三、docker-compose.yml 详解

`docker-compose.yml` 是编排多个容器的配置文件，一个文件定义整个系统。

### 3.1 顶层结构

```yaml
networks:   # 定义网络
volumes:    # 定义数据卷
services:   # 定义各个容器服务
```

### 3.2 自建网络

```yaml
networks:
  maas-network:
    driver: bridge       # bridge 是最常用的网络模式，类似虚拟交换机
    name: maas-network   # 网络的实际名称
```

**为什么要自建网络？**

默认情况下 docker compose 会创建一个随机名称的网络。自建网络的好处：
1. 名称固定，便于管理
2. 同一网络内的容器可以**直接用服务名互相访问**，不需要知道 IP
3. 网络隔离，外部无法直接访问内部容器

**容器间通信示例：**
```
maas-frontend 容器  →  访问 http://maas-backend:8000  →  maas-backend 容器
```
`maas-backend` 就是服务名，Docker 内置 DNS 会自动解析成对应容器的 IP。

### 3.3 数据卷

```yaml
volumes:
  mysql_data:       # MySQL 数据永久保存
  backend_static:   # Django 静态文件
```

```yaml
# 在服务中挂载
volumes:
  - mysql_data:/var/lib/mysql        # 命名卷：卷名:容器内路径
  - ./docker/mysql/conf:/etc/mysql/conf.d  # 绑定挂载：宿主机路径:容器内路径
```

**两种挂载方式的区别：**

| 类型 | 格式 | 特点 |
|------|------|------|
| 命名卷 | `卷名:容器路径` | Docker 管理，数据在 `/var/lib/docker/volumes/` |
| 绑定挂载 | `./宿主机路径:容器路径` | 直接映射宿主机目录，开发时常用 |

**为什么 MySQL 要用命名卷？**

容器删除后，命名卷的数据依然保留。如果不挂载卷，容器一删数据就全没了。

### 3.4 服务配置详解

```yaml
services:
  maas-db:
    image: mysql:8.0           # 直接用现成镜像，不需要 build
    container_name: maas-db    # 固定容器名称
    restart: unless-stopped    # 崩溃自动重启，除非手动停止
    networks:
      - maas-network           # 加入自建网络
    environment:               # 注入环境变量
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}  # ${} 读取 .env 文件的值
      MYSQL_DATABASE: ${DB_NAME}
    ports:
      - "3307:3306"            # 宿主机端口:容器端口
    healthcheck:               # 健康检查
      test: ["CMD", "mysqladmin", "ping", ...]
      interval: 5s             # 每 5 秒检查一次
      retries: 20              # 失败 20 次才算不健康
```

```yaml
  maas-backend:
    build:
      context: ./maas-backend  # Dockerfile 所在目录
      dockerfile: Dockerfile   # Dockerfile 文件名
    env_file:
      - .env                   # 从文件批量注入环境变量
    environment:
      DB_HOST: maas-backend    # 单独覆盖某个变量（优先级高于 env_file）
    depends_on:
      maas-db:
        condition: service_healthy  # 等 maas-db 健康检查通过才启动
```

### 3.5 端口映射

```
宿主机端口:容器端口
   3307  :  3306    ← 宿主机 3306 被占用，所以映射到 3307
   8000  :  8000
   5713  :  5713
```

外部访问 `服务器IP:3307` → 实际进入容器的 3306 端口。
容器内部服务之间通信**不走端口映射**，直接用服务名+容器内端口。

---

## 四、容器内 Nginx 反向代理

### 4.1 为什么需要 Nginx？

前端 Vue 项目 `npm run build` 后只是一堆静态文件（HTML/JS/CSS），需要一个 Web 服务器来托管。
同时，前端需要调用后端 API，如果直接从浏览器访问 `http://maas-backend:8000`，浏览器不认识这个域名（它是容器内网地址）。

解决方案：让 Nginx 同时做两件事：
1. 托管静态文件
2. 把 `/api/` 请求转发给后端容器

### 4.2 nginx.conf 详解（`maas-front/nginx.conf`）

```nginx
server {
    listen 5713;        # 监听 5713 端口
    server_name _;      # _ 表示匹配所有域名/IP

    root /usr/share/nginx/html;  # 静态文件根目录（Dockerfile 里 COPY 进来的）
    index index.html;

    # Vue Router history 模式支持
    # 用户访问 /dashboard，nginx 找不到这个文件，就返回 index.html
    # 让 Vue Router 在前端处理路由
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 反向代理：/api/ 开头的请求转发给后端
    location /api/ {
        proxy_pass http://maas-backend:8000;  # 容器内网，用服务名
        proxy_set_header Host $host;          # 把原始 Host 头传给后端
        proxy_set_header X-Real-IP $remote_addr;  # 传递真实客户端 IP
        proxy_read_timeout 120s;              # 等待后端响应最多 120 秒
    }

    # 静态资源缓存（JS/CSS/图片）
    location ~* \.(js|css|png|jpg|ico|svg)$ {
        expires 30d;                          # 浏览器缓存 30 天
        add_header Cache-Control "public, immutable";
    }

    gzip on;  # 开启 gzip 压缩，减少传输体积
    gzip_types text/plain text/css application/javascript application/json;
}
```

### 4.3 请求流转路径

```
浏览器
  │
  ├── GET /dashboard          → Nginx 返回 index.html → Vue Router 渲染页面
  │
  ├── GET /assets/main.js     → Nginx 直接返回静态文件（走缓存）
  │
  └── POST /api/auth/login/   → Nginx 转发 → maas-backend:8000 → Django 处理
```

---

## 五、entrypoint.sh 启动脚本

容器启动时不能直接跑 `gunicorn`，因为 MySQL 可能还没准备好。`entrypoint.sh` 解决启动顺序问题：

```sh
#!/bin/sh
set -e   # 任何命令失败就立即退出

# 1. 等待 MySQL 就绪（循环尝试连接，最多等 40×3=120 秒）
python - <<'PYEOF'
...循环连接 MySQL，成功才继续...
PYEOF

# 2. 执行数据库迁移（自动创建/更新表结构）
python manage.py migrate --noinput

# 3. 收集静态文件到 /app/staticfiles
python manage.py collectstatic --noinput

# 4. 启动 Gunicorn（Python 生产级 Web 服务器）
exec gunicorn maas_core.wsgi:application \
    --bind 0.0.0.0:8000 \   # 监听所有网卡的 8000 端口
    --workers 4 \            # 4 个工作进程
    --timeout 120            # 请求超时 120 秒
```

`depends_on: condition: service_healthy` 只保证 MySQL 容器启动了，不保证 MySQL 服务真正可用，所以脚本里还要再等一次。

---

## 六、环境变量与 .env 文件

```yaml
# docker-compose.yml 中两种注入方式
env_file:
  - .env              # 批量注入，适合大量配置

environment:
  DB_HOST: maas-db    # 单独设置，会覆盖 env_file 中同名的值
```

`.env` 文件格式：
```
KEY=value
DB_PASSWORD=your_password
```

在 `docker-compose.yml` 中用 `${KEY}` 引用：
```yaml
MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
```

`.env` 包含密码等敏感信息，加入 `.gitignore` 不提交到 git，用 `.env.example` 作为模板。

---

## 七、常用命令速查

```bash
# 构建并启动所有容器（后台运行）
docker compose up -d --build

# 只重建某个服务
docker compose up -d --build maas-frontend

# 查看运行中的容器
docker compose ps

# 查看某个容器的日志
docker compose logs -f maas-backend

# 停止所有容器
docker compose down

# 停止并删除数据卷（危险！会删除数据库数据）
docker compose down -v

# 删除无用镜像（更新后清理旧镜像）
docker image prune -f

# 进入容器内部执行命令
docker exec -it maas-backend sh

# 查看所有镜像
docker images

# 查看所有网络
docker network ls
```

---

## 八、本项目部署流程总结

```
代码更新
    ↓
git pull
    ↓
docker compose up -d --build   ← 重新构建镜像并启动
    ↓
docker image prune -f          ← 清理旧镜像释放磁盘
```

容器启动顺序（由 depends_on 控制）：
```
maas-db 启动
    ↓ healthcheck 通过
maas-backend 启动（entrypoint.sh 等待 MySQL → 迁移 → 启动 gunicorn）
    ↓
maas-frontend 启动（nginx 托管静态文件 + 反代 /api/）
```
