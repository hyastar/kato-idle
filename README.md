# 🏫 kato-idle — 校园二手物品信息展示平台

> 基于 Python Flask + Vue3 的前后端分离校园二手交易信息平台，专为高校师生提供便捷的二手物品发布、检索与交易信息服务。

---

## ✨ 功能特性

- 🔐 **用户系统** — 注册 / 登录 / JWT 鉴权 / 个人信息管理 / 头像上传
- 📦 **物品发布** — 多图上传 / 分类选择 / 价格填写 / 新旧程度标注
- 🔍 **搜索筛选** — 关键词搜索 / 分类筛选 / 价格区间 / 多种排序
- ❤️ **收藏功能** — 收藏 / 取消收藏 / 我的收藏列表
- 🛒 **购物车** — 加入 / 移除 / 清空购物车
- 👤 **个人中心** — 查看 / 编辑个人资料 / 管理我发布的物品

---

## 🛠️ 技术栈

| 层次 | 技术 |
|------|------|
| 后端语言 | Python 3.10+ |
| 后端框架 | Flask + Flask-CORS + Flask-JWT-Extended |
| 数据库 | SQLite（零配置，文件型） |
| ORM | Flask-SQLAlchemy |
| 虚拟环境 | Conda |
| 前端框架 | Vue 3（Composition API） |
| 构建工具 | Vite |
| 状态管理 | Pinia |
| 前端路由 | Vue Router 4 |
| UI 组件库 | Element Plus |
| HTTP 客户端 | Axios |
| 包管理器 | pnpm |

---

## 📁 项目结构

```
kato-idle/
├── backend/                    # Flask 后端
│   ├── app/
│   │   ├── __init__.py         # Flask 工厂函数
│   │   ├── models/             # 数据库模型
│   │   ├── routes/             # API 路由
│   │   ├── services/           # 业务逻辑层
│   │   └── utils/              # 工具函数
│   ├── config.py               # 配置文件
│   ├── run.py                  # 启动入口
│   ├── requirements.txt        # Python 依赖
│   └── .env                    # 环境变量（需手动创建，见下方说明）
│
└── frontend/                   # Vue3 前端
    ├── src/
    │   ├── api/                # Axios 接口封装
    │   ├── components/         # 复用组件
    │   ├── router/             # 路由配置
    │   ├── stores/             # Pinia 状态管理
    │   └── views/              # 页面组件
    ├── vite.config.js
    └── package.json
```

---

## 🚀 本地运行指南

### 前置要求

- [Anaconda](https://www.anaconda.com/) 或 [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Node.js 18+
- pnpm（`npm install -g pnpm`）

---

### 第一步 — 克隆项目

```bash
git clone https://github.com/hyastar/kato-idle.git
cd kato-idle
```

---

### 第二步 — 配置后端

#### 1. 创建并激活 conda 虚拟环境

```bash
conda create -n kato-web python=3.10 -y
conda activate kato-web
```

#### 2. 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

> 国内网络慢可以换清华源：
> `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

#### 3. 创建 `.env` 文件

在 `backend/` 目录下新建 `.env` 文件，内容如下：

```env
SECRET_KEY=kato-web-secret-key-change-in-prod
JWT_SECRET_KEY=kato-jwt-super-secret
```

> ⚠️ `.env` 文件已被 `.gitignore` 忽略，不会提交到仓库，每次拉取后需手动创建。
> 两个 Key 的值可以自己随意修改，保持私密即可。

#### 4. 启动后端

```bash
python run.py
```

首次运行会自动在 `backend/` 目录下生成 `kato_web.db` 数据库文件，并初始化分类数据。

后端运行在：`http://localhost:5000`

---

### 第三步 — 配置前端

新开一个终端：

```bash
cd frontend
pnpm install
pnpm dev
```

> 国内网络慢可以先换源：
> `pnpm config set registry https://registry.npmmirror.com`

前端运行在：`http://localhost:5173`

---

### 第四步 — 访问项目

浏览器打开 [http://localhost:5173](http://localhost:5173)，注册账号后即可使用全部功能。

---

## 🔧 环境变量说明

| 变量名 | 说明 | 是否必填 |
|--------|------|---------|
| `SECRET_KEY` | Flask Session 密钥，生产环境请修改为随机字符串 | ✅ |
| `JWT_SECRET_KEY` | JWT Token 签名密钥，生产环境请修改为随机字符串 | ✅ |

> 数据库无需配置，SQLite 会自动在 `backend/` 目录下创建 `kato_web.db` 文件。

---

## 📌 注意事项

- 数据库文件 `kato_web.db` 不会提交到 Git，每次 clone 后首次运行 `python run.py` 会自动创建
- 用户上传的图片存储在 `backend/app/static/uploads/` 目录，同样不会提交到 Git
- 如果修改了数据库 Model，直接删除 `kato_web.db` 后重启 `run.py` 即可重建

---

## 📄 License

MIT
