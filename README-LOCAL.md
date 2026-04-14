# MaaS 平台 — 本地开发指南

本文档面向开发者，介绍如何在本地搭建开发环境并运行前后端服务。  
生产部署请参考 [README.md](./README.md)。

---

## 目录

- [环境要求](#环境要求)
- [项目结构概览](#项目结构概览)
- [第一步：克隆仓库](#第一步克隆仓库)
- [第二步：配置环境变量](#第二步配置环境变量)
- [第三步：启动后端（Django）](#第三步启动后端django)
- [第四步：启动前端（Vue）](#第四步启动前端vue)
- [数据库迁移操作](#数据库迁移操作)
- [常用开发命令](#常用开发命令)
- [注意事项与常见问题](#注意事项与常见问题)

---

## 环境要求

| 工具 | 版本要求 | 说明 |
|------|---------|------|
| Python | 3.11+ | 后端运行环境 |
| Node.js | ^20.19.0 或 >=22.12.0 | 前端运行环境 |
| npm | 随 Node 安装 | 前端包管理 |
| Git | 最新版 | 版本控制 |

> **注意**：本地开发无需安装 MySQL，直接连接远程服务器上已部署的数据库。

---

## 项目结构概览

```
modelmaas/
├── maas-front/              # Vue 3 前端
│   ├── src/                 # 前端源码
│   ├── vite.config.ts       # Vite 配置（开发端口 5713，API 代理到 8000）
│   └── package.json
├── maas-backend/            # Django 后端
│   ├── maas_core/           # Django 项目主模块
│   │   ├── apps/            # 业务 App（users 等）
│   │   ├── settings.py      # 配置入口（导入 config/ 下各模块）
│   │   ├── urls.py          # URL 入口
│   │   └── wsgi.py
│   ├── config/              # 分模块配置
│   │   ├── base.py          # 基础配置（SECRET_KEY、APPS、MIDDLEWARE 等）
│   │   ├── database.py      # 数据库配置
│   │   ├── auth.py          # DRF + JWT 认证配置
│   │   ├── cors.py          # 跨域配置
│   │   └── router.py        # 路由自动发现
│   ├── requirements.txt     # Python 依赖
│   └── manage.py            # Django 管理命令入口
├── docker/                  # Docker 相关配置（MySQL 配置等）
├── docker-compose.yml       # Docker Compose 编排（生产部署用）
├── .env.example             # 环境变量模板（生产/Docker 部署用）
├── .env.local               # 本地开发环境变量（不提交到 Git）
└── .env                     # 实际生效的环境变量文件（不提交到 Git）
```

---

## 第一步：克隆仓库

```bash
git clone https://github.com/shaoruidong/modelmaas.git
cd modelmaas
```

> 国内服务器如果 GitHub 连接超时，可使用镜像加速：
> ```bash
> git clone https://ghproxy.com/https://github.com/shaoruidong/modelmaas.git
> ```

---

## 第二步：配置环境变量

项目提供了两个环境变量模板：

| 文件 | 用途 | 数据库连接 |
|------|------|-----------|
| `.env.docker` | 生产 / Docker 部署 | `DB_HOST=maas-db`（Docker 容器服务名） |
| `.env.local` | 本地开发调试 | `DB_HOST=远程服务器IP`（直连远程数据库） |

**本地开发使用 `.env.local`**：

```bash
cp .env.local .env
```

`.env.local` 内容示例：

```ini
# ── Django ──
SECRET_KEY=django-dev-insecure-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# ── 数据库（直连远程服务器 MySQL）──
DB_ENGINE=django.db.backends.mysql
DB_NAME=maas_db
DB_USER=root
DB_PASSWORD=<远程数据库密码>
DB_HOST=<远程服务器IP>
DB_PORT=3306

# ── 跨域（本地前端 Vite 开发服务器）──
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5713

# ── JWT ──
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=120
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
```

**关键说明**：

- `.env.local` 中 `DB_HOST` 填远程服务器 IP，本地直连远程已部署的 MySQL，不需要在本地安装数据库
- `.env.example` 中 `DB_HOST=maas-db` 是 Docker 容器间通信的服务名，**本地开发不要用这个**
- `.env.local` 和 `.env` 都已在 `.gitignore` 中忽略，不会被提交到仓库，密码信息安全

---

## 第三步：启动后端（Django）

### 3.1 创建 Python 虚拟环境

```bash
cd maas-backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
.\venv\Scripts\activate.bat
# Linux / macOS:
source venv/bin/activate
```

### 3.2 安装依赖

```bash
pip install -r requirements.txt
```

> PyMySQL 是纯 Python 的 MySQL 驱动，无需额外安装系统级 MySQL 客户端库。

### 3.3 执行数据库迁移

由于本地连接的是远程数据库，迁移操作会直接作用于远程数据库，**请谨慎操作**。

```bash
# 生成迁移文件（如果有模型变更）
python manage.py makemigrations

# 执行迁移
python manage.py migrate
```

> ⚠️ 如果远程数据库已经通过 Docker 部署执行过迁移，本地一般不需要再次执行 `migrate`，Django 会自动跳过已执行的迁移。

### 3.4 启动开发服务器

```bash
python manage.py runserver 0.0.0.0:8000
```

后端启动后访问：
- API 地址：http://127.0.0.1:8000/api/
- Admin 后台：http://127.0.0.1:8000/admin/

---

## 第四步：启动前端（Vue）

打开 **新的终端窗口**：

```bash
cd maas-front

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问：http://localhost:5713

Vite 开发服务器已配置 API 代理（`vite.config.ts`），所有 `/api/*` 请求会自动转发到 `http://127.0.0.1:8000`，开发时前后端联调无需额外配置。

---

## 数据库迁移操作

### ⚠️ 重要：本地连接的是远程数据库

本地开发环境直连远程服务器的 MySQL，所有迁移操作会**直接影响远程数据库**。请遵循以下规范：

- **不要随意执行** `migrate` 命令，除非你确认需要更新数据库结构
- **不要执行** 回滚或 `migrate zero` 等破坏性操作
- 先用 `showmigrations` 检查状态，确认需要执行后再操作

### 日常开发流程

修改了 Django 模型（`models.py`）后：

```bash
cd maas-backend

# 1. 生成迁移文件（只在本地生成文件，不影响数据库）
python manage.py makemigrations

# 2. 查看将要执行的 SQL（可选，用于检查确认）
python manage.py sqlmigrate <app_name> <migration_name>
# 例如：python manage.py sqlmigrate users 0002

# 3. 查看当前迁移状态（[X] 已执行，[ ] 未执行）
python manage.py showmigrations

# 4. 确认无误后，执行迁移
python manage.py migrate
```

### 常用迁移命令

```bash
# 查看所有迁移状态
python manage.py showmigrations

# 只迁移指定 App
python manage.py migrate users

# 生成空迁移文件（用于数据迁移）
python manage.py makemigrations users --empty --name describe_what_it_does
```

### 迁移冲突处理

多人协作时可能出现迁移冲突：

```bash
# 合并冲突的迁移文件
python manage.py makemigrations --merge
```

### Docker 部署时的迁移

Docker 部署不需要手动执行迁移。后端容器启动时，`entrypoint.sh` 会自动执行：

```bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
```

所以只要你的迁移文件提交到了 Git，部署时会自动应用。

---

## 常用开发命令

### 后端

```bash
cd maas-backend

# 启动开发服务器
python manage.py runserver 0.0.0.0:8000

# 进入 Django Shell（调试用）
python manage.py shell

# 创建超级管理员
python manage.py createsuperuser

# 收集静态文件（本地开发一般不需要，Docker 部署时自动执行）
python manage.py collectstatic
```

### 前端

```bash
cd maas-front

# 启动开发服务器（热更新）
npm run dev

# 构建生产版本
npm run build

# 快速构建（跳过类型检查）
npm run build:fast

# 预览构建结果
npm run preview

# 代码格式化
npm run format

# 代码检查
npm run lint

# 单元测试
npm run test:unit

# E2E 测试
npm run test:e2e
```

---

## 注意事项与常见问题

### 1. 环境变量文件说明

| 文件 | 用途 | 是否提交 Git |
|------|------|-------------|
| `.env.example` | Docker/生产部署模板 | ✅ 提交 |
| `.env.local` | 本地开发配置模板 | ❌ 不提交 |
| `.env` | 实际生效的配置（从上面两个复制而来） | ❌ 不提交 |

本地开发：`cp .env.local .env`  
Docker 部署：`cp .env.example .env`（再修改密码等）

### 2. 前端 API 代理

本地开发时，Vite 配置了代理（`vite.config.ts`）：

```
/api/* → http://127.0.0.1:8000
```

前端请求通过 Vite 代理转发到本地后端，不存在跨域问题。`.env` 中的 `CORS_ALLOWED_ORIGINS` 配置是为了某些直接访问后端的场景（如 Postman 或 curl 测试）。

### 3. 自定义用户模型

项目使用 `CustomUser` 模型（`AUTH_USER_MODEL = 'users.CustomUser'`），以 **手机号** 作为用户标识，不使用 Django 默认的 username。创建超级管理员时注意按提示填写手机号。

### 4. 路由自动发现

后端路由采用自动发现机制（`config/router.py`），新增接口只需：

1. 在 `maas-backend/maas_core/apps/<app>/routes/` 下新建 `.py` 文件
2. 定义 `PREFIX` 和 `urlpatterns`
3. 重启后端服务，路由自动挂载

无需手动修改 `urls.py`。

### 5. CSRF 已禁用

项目是纯 API 服务，使用 JWT 认证，已在 `config/base.py` 中注释掉 `CsrfViewMiddleware`。前端请求不需要携带 CSRF Token。

### 6. Windows 开发注意

- 虚拟环境激活：PowerShell 用 `.\venv\Scripts\Activate.ps1`
- 如果 PowerShell 提示脚本执行策略限制，先执行：
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### 7. 端口占用

| 服务 | 端口 |
|------|------|
| 前端 Vite | 5713 |
| 后端 Django | 8000 |

如果端口被占用：

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux / macOS
lsof -i :8000
kill -9 <pid>
```

### 8. 迁移文件需要提交

`makemigrations` 生成的迁移文件（`migrations/*.py`）**必须提交到 Git**，这样团队成员和 Docker 部署才能同步数据库结构变更。

---

## 快速启动清单（TL;DR）

```bash
# 1. 克隆 & 配置
git clone https://github.com/shaoruidong/modelmaas.git
cd modelmaas
cp .env.local .env

# 2. 启动后端
cd maas-backend
python -m venv venv
.\venv\Scripts\Activate.ps1          # Windows
# source venv/bin/activate           # Linux/macOS
pip install -r requirements.txt
python manage.py migrate             # 远程数据库已有表则可跳过
python manage.py runserver 0.0.0.0:8000

# 3. 启动前端（新终端）
cd maas-front
npm install
npm run dev

# 4. 打开浏览器访问 http://localhost:5713
```
