# 物业管理系统后端

基于 Python + Django + MySQL 开发的物业管理系统后端 API。

## 功能模块

### 1. 业主信息管理模块 (owners)
- **楼栋管理**: 楼栋信息的增删改查，支持按名称筛选
- **房屋管理**: 房屋信息管理，支持按楼栋、房号、状态多条件筛选
- **业主管理**: 业主信息管理，支持按姓名、电话、房号、楼栋多条件组合筛选

### 2. 费用管理模块 (bills)
- **收费标准**: 物业费、水电费等收费标准配置，支持按类型、状态筛选
- **账单生成**: 
  - 物业费批量生成
  - 水电费根据抄表记录生成
- **账单管理**: 账单查询，支持按业主、房屋、房号、楼栋、账单类型、状态、时间范围多条件组合筛选
- **抄表记录**: 水电表抄表记录管理，支持按房屋、房号、楼栋、类型、月份筛选

### 3. 在线缴费模块 (payments)
- **支付记录**: 缴费记录管理，支持按业主、房号、楼栋、支付方式、时间范围多条件筛选
- **在线缴费**: 支持单条/多条账单合并支付，自动核销已缴费账单
- **重复缴费校验**: 支付前自动校验账单状态，防止重复支付
- **金额校验**: 验证支付金额必须大于0
- **支付统计**: 按时间段、支付方式统计

### 4. 报修工单模块 (repairs)
- **维修人员**: 维修人员信息和状态管理，支持按技能、状态筛选
- **报修工单**: 
  - 业主提交报修
  - 管理员派单
  - 维修人员接单/完工
  - 业主评价
  - 支持按业主、维修人员、房号、楼栋、类型、状态、时间范围多条件组合筛选
- **自动归档**: 工单完成后自动归档，支持手动归档/取消归档
- **工单日志**: 工单操作历史记录，支持按操作、操作人、时间筛选
- **工单统计**: 按状态、类型统计

### 5. 权限和认证模块
- **三级权限隔离**: 
  - 业主: 只能查看和操作自己的相关数据
  - 维修人员: 只能查看和操作分配给自己的工单
  - 管理员/超级管理员: 拥有全部权限
- **Token认证**: 支持Token和Session两种认证方式
- **用户管理**: 用户信息管理，支持按用户名、邮箱、状态筛选

## 技术栈

- **后端框架**: Django 4.x
- **API 框架**: Django REST Framework
- **数据库**: MySQL
- **跨域处理**: django-cors-headers

## 环境要求

- Python 3.8+
- MySQL 5.7+

## 安装部署

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

修改 `property_management/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'property_management',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 3. 创建数据库

在 MySQL 中执行：

```sql
CREATE DATABASE property_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 6. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

## API 接口文档

### 基础 URL

```
http://localhost:8000/api
```

### 认证说明

- 所有接口（除登录外）都需要在请求头中携带Token: `Authorization: Token <token_value>`

### 认证接口

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/auth/login/` | POST | 用户登录 | 无 |
| `/auth/logout/` | POST | 用户登出 | 已登录 |
| `/auth/current_user/` | GET | 获取当前用户信息 | 已登录 |
| `/users/` | GET/POST | 用户列表/创建 | 管理员 |
| `/users/{id}/` | GET/PUT/DELETE | 用户详情/更新/删除 | 管理员 |

### 多条件筛选参数说明

所有列表接口支持以下通用筛选参数：

- `page`: 页码
- `page_size`: 每页条数
- `start_date`: 开始日期（YYYY-MM-DD）
- `end_date`: 结束日期（YYYY-MM-DD）

各模块专属筛选参数详见接口说明。

### 业主信息管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/owners/buildings/` | GET/POST | 楼栋列表/创建 |
| `/owners/buildings/{id}/` | GET/PUT/DELETE | 楼栋详情/更新/删除 |
| `/owners/houses/` | GET/POST | 房屋列表/创建 |
| `/owners/houses/by_building/?building_id=` | GET | 按楼栋查询房屋 |
| `/owners/owners/` | GET/POST | 业主列表/创建 |
| `/owners/owners/search/?keyword=` | GET | 搜索业主 |
| `/owners/owners/by_house/?house_id=` | GET | 按房屋查询业主 |

### 费用管理

| 接口 | 方法 | 说明 |
|------|------|------|
| `/bills/fee-standards/` | GET/POST | 收费标准列表/创建 |
| `/bills/bills/` | GET/POST | 账单列表/创建 |
| `/bills/bills/by_owner/?owner_id=` | GET | 按业主查询账单 |
| `/bills/bills/statistics/` | GET | 账单统计 |
| `/bills/bills/generate_property_fees/` | POST | 批量生成物业费账单 |
| `/bills/bills/generate_utility_fees/` | POST | 批量生成水电费账单 |
| `/bills/meter-readings/` | GET/POST | 抄表记录列表/创建 |

### 在线缴费

| 接口 | 方法 | 说明 |
|------|------|------|
| `/payments/payments/` | GET/POST | 缴费记录列表/创建 |
| `/payments/payments/by_owner/?owner_id=` | GET | 按业主查询缴费记录 |
| `/payments/payments/create_payment/` | POST | 创建支付（支持批量账单） |
| `/payments/payments/statistics/` | GET | 缴费统计 |

### 报修工单

| 接口 | 方法 | 说明 | 权限 |
|------|------|------|------|
| `/repairs/workers/` | GET/POST | 维修人员列表/创建 | GET:已登录, POST:管理员 |
| `/repairs/workers/available/` | GET | 查询空闲维修人员 | 已登录 |
| `/repairs/repairs/` | GET/POST | 工单列表/创建 | GET:已登录, POST:业主 |
| `/repairs/repairs/by_owner/?owner_id=` | GET | 按业主查询工单 | 已登录 |
| `/repairs/repairs/by_worker/?worker_id=` | GET | 按维修人员查询工单 | 已登录 |
| `/repairs/repairs/{id}/assign/` | POST | 派单 | 管理员/维修人员 |
| `/repairs/repairs/{id}/start_repair/` | POST | 开始维修 | 管理员/维修人员 |
| `/repairs/repairs/{id}/complete/` | POST | 完成维修（自动归档） | 管理员/维修人员 |
| `/repairs/repairs/{id}/rate/` | POST | 评价工单 | 业主 |
| `/repairs/repairs/{id}/cancel/` | POST | 取消工单 | 业主/管理员 |
| `/repairs/repairs/{id}/archive/` | POST | 手动归档工单 | 管理员 |
| `/repairs/repairs/{id}/unarchive/` | POST | 取消归档工单 | 管理员 |
| `/repairs/repairs/statistics/` | GET | 工单统计 | 管理员 |
| `/repairs/logs/` | GET | 工单日志列表 | 已登录 |
| `/repairs/logs/by_repair/?repair_id=` | GET | 查询工单日志 | 已登录 |

#### 工单筛选参数说明
- `owner_id`: 业主ID
- `worker_id`: 维修人员ID
- `room_number`: 房号（模糊匹配）
- `building_id`: 楼栋ID
- `repair_type`: 工单类型（water/structure/equipment/other）
- `status`: 工单状态（pending/assigned/processing/completed/cancelled）
- `is_archived`: 是否归档（true/false，默认false）

## 管理后台

访问 `http://localhost:8000/admin/` 可以进入 Django 管理后台进行数据管理。

## 项目结构

```
property_management/
├── manage.py
├── property_management/
│   ├── __init__.py
│   ├── settings.py      # 项目配置（数据库、REST Framework、CORS等）
│   ├── urls.py          # 主路由配置
│   ├── views.py         # 认证和用户管理视图
│   ├── serializers.py   # 用户和认证序列化器
│   ├── utils.py         # 通用工具（分页、权限类等）
│   ├── asgi.py
│   └── wsgi.py
├── owners/              # 业主信息管理模块
│   ├── models.py
│   ├── serializers.py   # 含必填校验和数据验证
│   ├── views.py         # 支持多条件筛选和分页
│   └── urls.py
├── bills/               # 费用管理模块
│   ├── models.py
│   ├── serializers.py   # 含必填校验和金额验证
│   ├── views.py         # 支持多条件筛选和分页
│   └── urls.py
├── payments/            # 在线缴费模块
│   ├── models.py
│   ├── serializers.py   # 含必填校验和金额验证
│   ├── views.py         # 重复缴费校验、自动核销、多条件筛选
│   └── urls.py
├── repairs/             # 报修工单模块
│   ├── models.py        # 含归档字段
│   ├── serializers.py   # 含必填校验
│   ├── views.py         # 三级权限隔离、自动归档、多条件筛选
│   └── urls.py
├── requirements.txt
└── README.md
```
