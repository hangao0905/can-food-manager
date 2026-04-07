# 罐头信息管理系统

基于 FastAPI + Vue3 + Element Plus + SQLite 的罐头信息管理系统。

## 功能特性

- **品牌管理**：CRUD 品牌信息
- **口味管理**：CRUD 口味信息，关联品牌
- **罐头管理**：录入营养成分（热量、蛋白质、脂肪、水分、磷、钙等）、合格指标、罐头简介
- **组合查询**：按品牌、口味、营养指标范围等条件查询

## 技术栈

- **后端**：Python 3.11 + FastAPI + SQLAlchemy + SQLite
- **前端**：Vue 3 + Element Plus + Vite
- **部署**：Docker Compose

## 快速启动

### 方式一：Docker 一键部署（推荐）

```bash
cd ~/Desktop/can-food-manager
docker-compose up -d --build
```

启动后访问：
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 方式二：本地开发

**后端**

```bash
cd backend
pip install -r requirements.txt
python -c "from app.database import engine, Base; Base.metadata.create_all(bind=engine)"
uvicorn app.main:app --reload --port 8000
```

**前端**

```bash
cd frontend
npm install
npm run dev
```

## 项目结构

```
can-food-manager/
├── backend/
│   ├── app/
│   │   ├── main.py          # FastAPI 应用入口
│   │   ├── database.py      # 数据库配置
│   │   ├── models/          # SQLAlchemy 模型
│   │   ├── schemas/         # Pydantic schema
│   │   └── routers/        # API 路由
│   ├── sql/
│   │   └── init_db.py       # 初始化数据库脚本
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── views/           # Vue 页面组件
│   │   ├── api/             # API 调用
│   │   └── router/          # 路由配置
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## API 接口

### 品牌管理
- `GET /api/brands/` - 获取品牌列表
- `GET /api/brands/{id}` - 获取品牌详情
- `POST /api/brands/` - 创建品牌
- `PUT /api/brands/{id}` - 更新品牌
- `DELETE /api/brands/{id}` - 删除品牌

### 口味管理
- `GET /api/flavors/` - 获取口味列表
- `GET /api/flavors/{id}` - 获取口味详情
- `POST /api/flavors/` - 创建口味
- `PUT /api/flavors/{id}` - 更新口味
- `DELETE /api/flavors/{id}` - 删除口味

### 罐头管理
- `GET /api/can-foods/` - 获取罐头列表（支持组合查询）
- `GET /api/can-foods/{id}` - 获取罐头详情
- `POST /api/can-foods/` - 创建罐头
- `PUT /api/can-foods/{id}` - 更新罐头
- `DELETE /api/can-foods/{id}` - 删除罐头

### 查询参数

| 参数 | 类型 | 说明 |
|------|------|------|
| brand_id | int | 品牌ID |
| flavor_id | int | 口味ID |
| name | string | 罐头名称（模糊搜索） |
| min_calories | float | 最小热量 |
| max_calories | float | 最大热量 |
| min_protein | float | 最小蛋白质 |
| max_protein | float | 最大蛋白质 |
| min_fat | float | 最小脂肪 |
| max_fat | float | 最大脂肪 |
| is_quality_passed | bool | 是否合格 |
| page | int | 页码 |
| page_size | int | 每页数量 |

## 数据库

使用 SQLite 数据库，文件位于 `backend/can_food.db`

### 初始化样本数据

Docker 部署时会自动初始化样本数据。如需手动初始化：

```bash
docker exec -it can-food-backend python /app/sql/init_db.py
```

## 停止服务

```bash
docker-compose down
```

如需清除数据：

```bash
docker-compose down -v
rm -rf backend/can_food.db
```
