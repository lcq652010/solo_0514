# 婚纱摄影管理系统后端

基于 Python + Django + MySQL 实现的婚纱摄影管理系统后端 API。

## 功能模块

- **套餐管理**: 套餐的增删改查，启用/禁用状态管理
- **客户管理**: 客户信息管理，支持搜索
- **摄影师管理**: 摄影师信息、档期查询、可用摄影师查询
- **客户预约**: 预约创建、确认、取消流程，档期冲突校验
- **拍摄订单**: 订单管理，支持四种状态流转，自动生成订单编号，档期冲突校验
- **尾款结算**: 订单尾款结算，自动计算尾款金额

## 核心特性

### ✅ 多条件组合筛选
- **订单筛选**: 客户姓名、套餐类型、摄影师、订单状态、日期范围、订单号
- **预约筛选**: 客户姓名、摄影师、预约状态、日期范围
- **结算筛选**: 订单号、支付方式、日期范围

### ✅ 档期冲突校验
- 创建/更新预约时，校验摄影师在同一时间段是否已有预约或拍摄订单
- 创建/更新订单时，校验摄影师在同一时间段是否已有订单或预约
- 防止重复预约和重复安排拍摄

### ✅ 表单必填校验
- 套餐：名称、价格、拍摄天数、精修数量
- 客户：姓名、电话
- 摄影师：姓名、电话、级别
- 预约：客户、套餐、摄影师、预约日期、预约时间
- 订单：客户、套餐、摄影师、拍摄日期、拍摄时间、拍摄地点、总金额
- 结算：支付方式

### ✅ 金额合法性校验
- 套餐价格不能为负数
- 订单总金额不能为负数
- 定金不能为负数
- 定金不能大于订单总金额
- 尾款金额不能为负数

### ✅ 分页功能
- 所有列表接口支持分页
- 默认每页 20 条
- 支持自定义每页数量（`page_size` 参数）

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- MySQL 5.7+
- mysqlclient 2.2.0

## 安装与运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

确保 MySQL 服务已启动，创建数据库：

```sql
CREATE DATABASE wedding_photo_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

根据实际情况修改 `wedding_photo_system/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wedding_photo_db',
        'USER': 'root',
        'PASSWORD': '你的密码',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 3. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 5. 启动服务

```bash
python manage.py runserver
```

服务启动后访问：
- 后台管理: http://localhost:8000/admin/
- API 接口: http://localhost:8000/api/

## API 接口列表

### 套餐管理
- `GET /api/packages/` - 套餐列表（支持筛选：`name`, `is_active`）
- `POST /api/packages/` - 创建套餐
- `GET /api/packages/{id}/` - 套餐详情
- `PUT /api/packages/{id}/` - 更新套餐
- `DELETE /api/packages/{id}/` - 删除套餐
- `GET /api/packages/active/` - 启用的套餐列表

**分页参数**: `page` (页码), `page_size` (每页数量)

### 客户管理
- `GET /api/customers/` - 客户列表（支持筛选：`keyword`）
- `POST /api/customers/` - 创建客户
- `GET /api/customers/{id}/` - 客户详情
- `PUT /api/customers/{id}/` - 更新客户
- `DELETE /api/customers/{id}/` - 删除客户
- `GET /api/customers/search/?keyword=xxx` - 搜索客户

**分页参数**: `page` (页码), `page_size` (每页数量)

### 摄影师管理
- `GET /api/photographers/` - 摄影师列表（支持筛选：`name`, `level`, `is_active`）
- `POST /api/photographers/` - 创建摄影师
- `GET /api/photographers/{id}/` - 摄影师详情
- `PUT /api/photographers/{id}/` - 更新摄影师
- `DELETE /api/photographers/{id}/` - 删除摄影师
- `GET /api/photographers/active/` - 在职摄影师列表
- `GET /api/photographers/{id}/schedule/?start_date=2024-01-01&end_date=2024-01-31` - 摄影师档期
- `GET /api/photographers/available/?date=2024-01-01&time=10:00` - 可用摄影师查询

**分页参数**: `page` (页码), `page_size` (每页数量)

### 客户预约
- `GET /api/appointments/` - 预约列表（支持筛选：`customer_name`, `photographer_id`, `status`, `start_date`, `end_date`）
- `POST /api/appointments/` - 创建预约（档期冲突校验）
- `GET /api/appointments/{id}/` - 预约详情
- `PUT /api/appointments/{id}/` - 更新预约（档期冲突校验）
- `DELETE /api/appointments/{id}/` - 取消预约
- `GET /api/appointments/pending/` - 待确认预约列表
- `POST /api/appointments/{id}/confirm/` - 确认预约
- `POST /api/appointments/{id}/cancel/` - 取消预约

**分页参数**: `page` (页码), `page_size` (每页数量)

### 拍摄订单
- `GET /api/orders/` - 订单列表（支持筛选：`customer_name`, `package_id`, `photographer_id`, `status`, `start_date`, `end_date`, `order_number`）
- `POST /api/orders/` - 创建订单（自动生成订单号，档期冲突校验）
- `GET /api/orders/{id}/` - 订单详情
- `PUT /api/orders/{id}/` - 更新订单（档期冲突校验）
- `DELETE /api/orders/{id}/` - 删除订单
- `GET /api/orders/pending/` - 待拍摄订单
- `GET /api/orders/shooting/` - 拍摄中订单
- `GET /api/orders/selected/` - 已选片订单
- `GET /api/orders/completed/` - 已完成订单
- `POST /api/orders/{id}/start_shooting/` - 开始拍摄
- `POST /api/orders/{id}/finish_shooting/` - 拍摄完成（已选片）
- `POST /api/orders/{id}/complete/` - 订单完成
- `GET /api/orders/filter/?customer_name=xxx&package_id=1&status=pending` - 多条件筛选订单
- `GET /api/orders/search/?keyword=xxx` - 搜索订单

**分页参数**: `page` (页码), `page_size` (每页数量)

### 尾款结算
- `GET /api/settlements/` - 结算列表（支持筛选：`order_number`, `payment_method`, `start_date`, `end_date`）
- `POST /api/settlements/` - 创建结算（自动计算尾款，金额校验）
- `GET /api/settlements/{id}/` - 结算详情
- `PUT /api/settlements/{id}/` - 更新结算
- `DELETE /api/settlements/{id}/` - 删除结算

**分页参数**: `page` (页码), `page_size` (每页数量)

## 订单状态流转

```
待拍摄 (pending)
    ↓ 开始拍摄
拍摄中 (shooting)
    ↓ 完成拍摄
已选片 (selected)
    ↓ 完成订单
已完成 (completed)
```

## 订单编号规则

订单编号自动生成，格式为：`YYYYMMDDXXXX`
- YYYYMMDD: 当前日期
- XXXX: 当日流水号（从 0001 开始）

例如：202401010001

## 档期冲突校验规则

创建或更新预约/订单时，系统会校验：
1. 同一摄影师在同一日期和时间是否已有待确认/已确认的预约
2. 同一摄影师在同一日期和时间是否有待拍摄/拍摄中的订单

如果存在冲突，系统返回错误提示："该摄影师在当前时间段已有预约" 或 "该摄影师在当前时间段已有拍摄订单"

## 项目结构

```
wedding_photo_system/
├── wedding_photo_system/    # 项目配置目录
│   ├── __init__.py
│   ├── settings.py          # 项目配置
│   ├── urls.py              # URL 路由
│   ├── asgi.py
│   └── wsgi.py
├── core/                     # 核心应用
│   ├── __init__.py
│   ├── admin.py             # 后台管理配置
│   ├── apps.py
│   ├── models.py            # 数据模型
│   ├── serializers.py       # 序列化器（包含校验逻辑）
│   ├── urls.py              # API 路由
│   └── views.py             # 视图逻辑（包含筛选和分页）
├── manage.py
├── requirements.txt
└── README.md
```
