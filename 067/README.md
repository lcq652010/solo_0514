# 展会管理后端系统

基于 Python + Django + MySQL 实现的展会管理后端系统，支持展位信息维护、企业展位预订、搭建需求提交、进度跟踪、尾款结算等功能。

## 功能特性

- 展会管理：创建和管理展会基本信息
- 展位管理：展位信息维护，支持多种类型和状态
- 企业管理：企业信息注册和管理
- 展位预订：自动生成订单号，支持预订和取消
- 搭建需求：搭建需求提交、审核、进度跟踪
- 付款管理：定金和尾款结算，支持多种支付方式
- REST API：完整的 RESTful API 接口
- 管理后台：Django Admin 管理界面

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework
- MySQL
- django-cors-headers

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+

### 2. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE exhibition_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

修改 `.env` 文件中的数据库配置：

```env
DB_NAME=exhibition_db
DB_USER=root
DB_PASSWORD=你的密码
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=django-insecure-exhibition-management-system-2024
DEBUG=True
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 7. 初始化演示数据（可选）

```bash
python manage.py init_exhibition_data
```

### 8. 启动服务

```bash
python manage.py runserver
```

访问：
- API 根地址：http://127.0.0.1:8000/api/
- 管理后台：http://127.0.0.1:8000/admin/

## API 接口说明

### 展会管理
- `GET /api/exhibitions/` - 获取展会列表
- `POST /api/exhibitions/` - 创建展会
- `GET /api/exhibitions/{id}/` - 获取展会详情
- `PUT /api/exhibitions/{id}/` - 更新展会
- `DELETE /api/exhibitions/{id}/` - 删除展会

### 展位管理
- `GET /api/booths/` - 获取展位列表
- `GET /api/booths/available/` - 获取可用展位
- `GET /api/booths/by_exhibition/?exhibition_id={id}` - 按展会获取展位
- `POST /api/booths/` - 创建展位

### 企业管理
- `GET /api/companies/` - 获取企业列表
- `POST /api/companies/` - 创建企业

### 展位预订
- `GET /api/bookings/` - 获取预订列表
- `POST /api/bookings/` - 创建预订（自动生成订单号）
- `POST /api/bookings/{id}/cancel/` - 取消预订
- `GET /api/bookings/by_company/?company_id={id}` - 按企业获取预订

### 搭建需求
- `GET /api/construction-demands/` - 获取搭建需求列表
- `POST /api/construction-demands/` - 提交搭建需求
- `POST /api/construction-demands/{id}/approve/` - 批准需求
- `POST /api/construction-demands/{id}/reject/` - 拒绝需求
- `POST /api/construction-demands/{id}/start_construction/` - 开始施工
- `POST /api/construction-demands/{id}/complete/` - 完成搭建

### 进度跟踪
- `GET /api/progress/` - 获取进度列表
- `POST /api/progress/` - 创建进度记录
- `GET /api/progress/by_construction/?construction_id={id}` - 按搭建需求获取进度

### 付款管理
- `GET /api/payments/` - 获取付款记录
- `POST /api/payments/` - 记录付款（自动更新订单状态）
- `GET /api/payments/by_booking/?booking_id={id}` - 按订单获取付款

## 订单号生成规则

订单号格式：`EX + YYYYMMDD + 4位序号`

示例：`EX202405160001`

## 业务流程

### 展位预订流程
1. 企业注册
2. 查询可用展位
3. 提交预订申请 → 自动生成订单号
4. 展位状态变为"已预订"
5. 支付定金 → 订单状态变为"已付定金"
6. 支付尾款 → 订单状态变为"已付尾款"

### 搭建需求流程
1. 预订展位后提交搭建需求
2. 管理员审核（批准/拒绝）
3. 开始施工
4. 记录施工进度
5. 搭建完成

## 项目结构

```
exhibition_system/
├── manage.py
├── .env
├── requirements.txt
├── README.md
├── exhibition_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── exhibition/
    ├── __init__.py
    ├── apps.py
    ├── models.py          # 数据模型
    ├── serializers.py     # 序列化器
    ├── views.py           # 视图集
    ├── admin.py           # 管理后台
    └── management/
        └── commands/
            └── init_exhibition_data.py  # 初始化数据脚本
```

## 数据模型

- **Exhibition（展会）**: 展会基本信息
- **Booth（展位）**: 展位信息，包含类型、面积、价格、状态
- **Company（企业）**: 企业基本信息
- **Booking（预订）**: 展位预订订单，自动生成订单号
- **ConstructionDemand（搭建需求）**: 搭建需求和审核状态
- **ProgressTracker（进度跟踪）**: 施工进度记录
- **Payment（付款）**: 定金和尾款付款记录

## 注意事项

1. 确保 MySQL 服务已启动
2. 数据库配置需要正确设置用户名和密码
3. 生产环境请修改 `SECRET_KEY` 并设置 `DEBUG=False`
4. 如需文件上传功能，请配置媒体文件存储路径
