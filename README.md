# 🥫 猫罐头营养分析管理系统

用于管理猫罐头品牌、口味、营养成分，并依据营养标准自动计算合格指标的分析系统。

---

## 功能模块

### 品牌管理 `/brands`
- 新增 / 编辑 / 删除品牌
- 支持字段：品牌名称、通俗名（alias）、Logo（Base64 图片）、简介、国家（国内/国外）
- Logo 可上传预览，删除时自动清除

### 口味管理 `/flavors`
- 新增 / 编辑 / 删除口味
- 关联所属品牌（brand_code）
- 支持口味图片（Base64）和创建人自动记录

### 罐头管理 `/can-foods`
- 录入罐头营养成分，系统**自动计算**所有派生指标
- 支持罐头图片上传
- 批量重新计算所有罐头指标

### 营养标准管理 `/standards`
- 可视化配置合格指标规则（数据库驱动）
- 支持操作符：`>=`、`<=`、`>`、`<`、`range`
- 修改规则后自动影响所有罐头判定结果，无需重新录入

### 查询 `/query`
- 按品牌、口味、罐头简介关键字筛选
- 按蛋白合格状态筛选
- 按创建人筛选

### 数据统计 `/dashboard`
- 品牌总数、国内/国外品牌数量
- 口味总数、罐头总数
- 蛋白合格率、脂肪合格率、纤维合格率

### 用户管理 `/users`
- 管理员可新增用户、设置角色（admin / user）
- 可禁用/启用用户

---

## 系统架构

```
┌──────────────────────────────────────────────────────────────┐
│                      浏览器 (Vue 3 SPA)                     │
│   axios baseURL = /api    ←→   JWT Token 存储在 localStorage │
└────────────────────────────┬───────────────────────────────┘
                             │ nginx:80
              ┌──────────────┴──────────────┐
              │  /api/*  →  后端 FastAPI:8001 │
              │  /*      →  Vue SPA 静态文件 │
              └─────────────────────────────┘
                             │
          ┌───────────────────┴───────────────────┐
          │           FastAPI 后端 (:8001)          │
          │  JWT 认证 | CRUD | 营养计算引擎         │
          └───────────────────┬───────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │    SQLite DB       │
                    │  can_food.db       │
                    │  (品牌/口味/罐头/用户/标准) │
                    └───────────────────┘
```

---

## 营养计算引擎

### 干物质换算
用户只需录入**湿基**成分，系统自动换算干基：
- `干物质 = 1 - 水分`
- `某成分干基 = 某成分湿基 / 干物质`

### 代谢能计算
按 NRC 公式计算（单位：kcal/kg）：
- 蛋白代谢能 = 蛋白 × 3.5 × 100 × 10
- 脂肪代谢能 = 脂肪 × 8.5 × 100 × 10
- 碳水代谢能 = NFE × 3.5 × 100 × 10
- 总热量 = 三者之和

### 衍生指标
| 指标 | 计算公式 |
|------|---------|
| 钙磷比 | 钙(湿基) / 磷(湿基) |
| 钙mg/1000kcal | 钙(湿基) × 1000 × 10 / 总热量 |
| 磷mg/1000kcal | 磷(湿基) × 1000 × 10 / 总热量 |
| 蛋白:脂肪 | 蛋白(湿基) / 脂肪(湿基) |

### 合格指标规则（存储于数据库）

| 规则名称 | 字段 | 操作符 | 阈值 | 说明 |
|---------|------|--------|------|------|
| 粗蛋白合格 | protein | >= | 0.10 | 蛋白质 ≥ 10% |
| 粗脂肪合格 | fat | <= | 0.09 | 脂肪 ≤ 9% |
| 粗纤维合格 | fiber | <= | 0.03 | 纤维 ≤ 3% |
| 粗灰分合格 | ash | <= | 0.02 | 灰分 ≤ 2% |
| 含水量合格 | moisture | <= | 0.80 | 水分 ≤ 80% |
| 钙磷比合格 | ca_ph_ratio | range | 1.1~1.4 | 钙磷比在 [1.1, 1.4] 区间（含边界）|
| 磷含量-高 | phosphorus_per_1000kal | > | 2400 | > 2400 mg/1000kcal |
| 磷含量-低 | phosphorus_per_1000kal | < | 1800 | < 1800 mg/1000kcal |
| 蛋白质:脂肪-优秀 | protein_fat_ratio | > | 3.0 | 比值 > 3.0 |
| 蛋白质:脂肪-一般 | protein_fat_ratio | > | 1.5 | 比值 > 1.5（不含边界）|

### 蛋白水平判定逻辑
```
protein_fat_ratio > 3.0  →  优秀
protein_fat_ratio ∈ (1.5, 3.0]  →  一般
protein_fat_ratio ≤ 1.5  →  不合格
```

### 磷水平判定逻辑
```
phosphorus_per_1000kal > 2400  →  高磷
phosphorus_per_1000kal < 1800  →  低磷
phosphorus_per_1000kal ∈ [1800, 2400]  →  中磷
```

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端框架 | Python 3 + FastAPI + SQLAlchemy |
| 前端框架 | Vue 3 + Element Plus + Vite |
| 数据库 | SQLite |
| 认证 | JWT（HS256，7天有效期）|
| 部署 | Nginx 反向代理 + Uvicorn |
| 服务器 | 阿里云（公网 IP: 8.146.233.134）|

---

## 快速启动

### 前端开发
```bash
cd frontend
npm install
npm run dev
# 访问 http://localhost:5173
```

### 后端开发
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
# API 文档: http://localhost:8001/docs
```

### 生产部署（阿里云）
```bash
# 1. 构建前端
cd frontend && npm install && npm run build

# 2. 部署前端到 nginx
tar -czf dist.tar.gz dist
scp -i ~/Downloads/openclaw.pem dist.tar.gz root@8.146.233.134:/www/wwwroot/can-food/

# 3. 部署后端
cd backend && tar -czf app.tar.gz app/
scp -i ~/Downloads/openclaw.pem app.tar.gz root@8.146.233.134:/root/can-food-manager/backend/

# 4. 服务器上重启后端
ssh -i ~/Downloads/openclaw.pem root@8.146.233.134
pkill -f uvicorn
cd /root/can-food-manager/backend
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001 > /tmp/uvicorn.log 2>&1 &
```

---

## 页面路由

| 路径 | 页面 | 权限 |
|------|------|------|
| `/login` | 登录页 | 公开 |
| `/dashboard` | 数据概览 | 需登录 |
| `/brands` | 品牌管理 | 需登录 |
| `/flavors` | 口味管理 | 需登录 |
| `/can-foods` | 罐头管理 | 需登录 |
| `/query` | 组合查询 | 需登录 |
| `/standards` | 营养标准 | 需登录 |
| `/users` | 用户管理 | 仅管理员 |

---

## API 接口

> 所有需要写权限的接口（POST/PUT/DELETE）均需在 Header 中携带 JWT Token：
> `Authorization: Bearer <token>`

### 认证 `/auth`
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/login` | 登录，返回 JWT token |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 品牌 `/brands`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/brands/` | 品牌列表 |
| GET | `/api/brands/{code}` | 品牌详情 |
| POST | `/api/brands/` | 新增品牌 |
| PUT | `/api/brands/{code}` | 更新品牌 |
| DELETE | `/api/brands/{code}` | 删除品牌 |

### 口味 `/flavors`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/flavors/` | 口味列表（支持 brand_code 过滤）|
| GET | `/api/flavors/{code}` | 口味详情 |
| POST | `/api/flavors/` | 新增口味 |
| PUT | `/api/flavors/{code}` | 更新口味 |
| DELETE | `/api/flavors/{code}` | 删除口味 |

### 罐头 `/can-foods`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/can-foods/` | 罐头列表（支持多条件过滤、分页）|
| GET | `/api/can-foods/{code}` | 罐头详情 |
| POST | `/api/can-foods/` | 新增罐头 |
| PUT | `/api/can-foods/{code}` | 更新罐头（湿基营养变更时自动重算）|
| DELETE | `/api/can-foods/{code}` | 删除罐头 |
| POST | `/api/can-foods/{code}/recalc` | 重新计算单条指标 |
| POST | `/api/can-foods/recalc-all` | 重新计算所有罐头指标 |

**GET 列表过滤参数：**
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认 1 |
| page_size | int | 每页数量，默认 50 |
| brand_code | int | 品牌 ID |
| flavor_code | int | 口味 ID |
| keyword | string | 罐头简介关键字（模糊）|
| protein_pass | string | 蛋白合格状态（合格/不合格）|
| creator | string | 创建人关键字（模糊）|

### 营养标准 `/standards`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/standards/` | 标准列表 |
| PUT | `/api/standards/{id}` | 更新标准（支持修改阈值、操作符）|
| POST | `/api/standards/init` | 初始化默认标准（共10条）|

### 数据统计 `/stats`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats/` | 统计数据（需登录）|

### 用户 `/users`
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/users/` | 用户列表（仅管理员）|
| POST | `/api/users/` | 新增用户（仅管理员）|
| PUT | `/api/users/{id}` | 更新用户（仅管理员）|
| DELETE | `/api/users/{id}` | 删除用户（仅管理员）|

---

## 数据库表结构

### brands（品牌）
| 字段 | 类型 | 说明 |
|------|------|------|
| code | INTEGER PK | 品牌 ID |
| name | VARCHAR(100) | 品牌名称（唯一）|
| alias | VARCHAR(100) | 通俗名 |
| logo | TEXT | Logo 图片（Base64）|
| description | TEXT | 品牌简介 |
| country | VARCHAR(20) | 国内 / 国外 |
| created_date | TEXT | 创建日期 |

### flavors（口味）
| 字段 | 类型 | 说明 |
|------|------|------|
| code | INTEGER PK | 口味 ID |
| name | VARCHAR(100) | 口味名称 |
| brand_code | INTEGER FK | 所属品牌 ID |
| photo | TEXT | 口味图片（Base64）|
| creator | VARCHAR(50) | 创建人 |
| created_date | TEXT | 创建日期 |

### can_foods（罐头）
| 分类 | 字段 | 说明 |
|------|------|------|
| 基础 | code, brand_code, flavor_code, description, creator, created_date, photo | |
| 湿基输入 | protein, fat, ash, fiber, moisture, calcium_wet, phosphorus_wet, nfe_wet, labeled_kcal | 用户录入 |
| 干基自动计算 | protein_dm, fat_dm, ash_dm, nfe_dm, calcium_dm, phosphorus_dm | 湿基/干物质 |
| 热量自动计算 | total_energy_kcal, protein_kcal, fat_kcal, carb_kcal, protein_met_energy_pct, fat_met_energy_pct, carb_met_energy_pct | |
| 比例自动计算 | ca_ph_ratio, calcium_per_1000kal, phosphorus_per_1000kal, protein_fat_ratio | |
| 合格判定 | protein_pass, fat_pass, fiber_pass, ash_pass, moisture_pass, ca_ph_pass | 合格/不合格 |
| 等级判定 | protein_level（优秀/一般/不合格）, phosphorus_level（高磷/中磷/低磷）| |

### standards（营养标准）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | |
| name | VARCHAR(100) | 规则名称 |
| field | VARCHAR(50) | 目标字段名 |
| operator | VARCHAR(10) | 操作符：>=, <=, >, <, range |
| threshold | FLOAT | 阈值 |
| threshold_max | FLOAT | 范围上限（range 时使用）|
| unit | VARCHAR(20) | 单位 |
| status | VARCHAR(20) | active / inactive |

### users（用户）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER PK | |
| username | VARCHAR(50) | 用户名（唯一）|
| password_hash | VARCHAR(256) | PBKDF2-SHA256 哈希 |
| role | VARCHAR(20) | admin / user |
| status | VARCHAR(20) | active / inactive |

---

## 默认账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |

---

## 项目结构

```
can-food-manager/
├── README.md
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py              # FastAPI 入口，路由注册，启动事件
│       ├── database.py          # SQLite + SQLAlchemy 配置
│       ├── models/
│       │   └── models.py       # 所有数据表模型
│       ├── schemas/
│       │   └── schemas.py      # Pydantic 请求/响应模型
│       └── routers/
│           ├── auth.py          # JWT 认证（登录/Token 解码/依赖注入）
│           ├── brands.py        # 品牌 CRUD
│           ├── flavors.py       # 口味 CRUD
│           ├── can_foods.py    # 罐头 CRUD + 营养计算引擎
│           ├── standards.py     # 营养标准 CRUD
│           ├── stats.py         # 数据统计
│           └── users.py        # 用户管理
└── frontend/
    ├── vite.config.js
    ├── package.json
    └── src/
        ├── main.js             # Vue 入口
        ├── App.vue             # 根组件
        ├── api/
        │   └── index.js        # axios 实例 + API 方法（统一拦截器）
        ├── router/
        │   └── index.js        # Vue Router（公开/需登录/管理员三级路由守卫）
        └── views/
            ├── Login.vue        # 登录页
            ├── Dashboard.vue    # 数据概览
            ├── Brands.vue       # 品牌管理
            ├── Flavors.vue     # 口味管理
            ├── CanFoods.vue    # 罐头管理（核心，营养计算）
            ├── Query.vue       # 组合查询
            ├── Standards.vue   # 营养标准管理
            └── Users.vue       # 用户管理
```

---

## nginx 配置（生产）

```nginx
server {
    listen 80;
    server_name _;
    root /www/wwwroot/can-food;
    index index.html;

    # SPA fallback
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 反向代理到后端
    location /api/ {
        proxy_pass http://127.0.0.1:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

> ⚠️ 注意：`/brands`、`/flavors`、`/can-foods` 等路径必须由 Vue Router 接管（SPA），不能 proxy 到后端。

---

## GitHub 仓库

https://github.com/hangao0905/can-food-manager

---
