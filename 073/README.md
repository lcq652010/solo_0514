# 驾校管理系统后端

基于 Python + Django + MySQL 实现的驾校管理系统后端 API。

## 功能特性

1. **学员信息管理** - 学员的增删改查、状态管理
2. **教练排班管理** - 教练排班、可用时段查询
3. **车辆分配管理** - 车辆信息维护、分配教练
4. **培训预约管理** - 自动生成预约单号、预约确认/取消/完成
5. **学时打卡记录** - 开始/结束打卡、自动计算学时
6. **培训费用结算** - 费用记录、分期支付、支付状态管理

## 技术栈

- Python 3.8+
- Django 4.2+
- Django REST Framework
- MySQL
- django-cors-headers

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `.env` 文件配置 MySQL 数据库连接信息：

```
DB_NAME=driving_school
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 3. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE driving_school DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
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

### 6. 初始化测试数据（可选）

```bash
python init_data.py
```

### 7. 启动服务

```bash
python manage.py runserver
```

服务将在 http://localhost:8000 启动。

## API 接口文档

访问 http://localhost:8000/api/ 可查看所有 API 端点。

### 主要接口列表

| 模块 | 接口路径 | 说明 |
|------|---------|------|
| 学员 | /api/students/ | 学员列表/创建 |
| 学员 | /api/students/{id}/ | 学员详情/更新/删除 |
| 教练 | /api/coaches/ | 教练列表/创建 |
| 车辆 | /api/vehicles/ | 车辆列表/创建 |
| 排班 | /api/coach-schedules/ | 排班列表/创建 |
| 排班 | /api/coach-schedules/available/ | 可用排班查询 |
| 预约 | /api/training-appointments/ | 预约列表/创建 |
| 预约 | /api/training-appointments/{id}/confirm/ | 确认预约 |
| 预约 | /api/training-appointments/{id}/cancel/ | 取消预约 |
| 预约 | /api/training-appointments/{id}/complete/ | 完成预约 |
| 记录 | /api/training-records/ | 学时记录列表/创建 |
| 记录 | /api/training-records/{id}/clock_in/ | 开始打卡 |
| 记录 | /api/training-records/{id}/clock_out/ | 结束打卡 |
| 费用 | /api/fee-settlements/ | 费用结算列表/创建 |
| 费用 | /api/fee-settlements/{id}/pay/ | 支付费用 |

### 管理后台

访问 http://localhost:8000/admin/ 进入 Django 管理后台。

## 预约单号生成规则

预约单号自动生成，格式为：`AP + 日期(8位) + 随机字符(6位)`

示例：`AP20240115ABC123`

## 项目结构

```
driving_school/
├── driving_school/          # 项目配置目录
│   ├── __init__.py
│   ├── settings.py         # 项目设置
│   ├── urls.py             # 主路由
│   ├── asgi.py
│   └── wsgi.py
├── management/              # 应用目录
│   ├── __init__.py
│   ├── admin.py            # 管理后台配置
│   ├── apps.py
│   ├── models.py           # 数据模型
│   ├── serializers.py      # 序列化器
│   ├── views.py            # 视图
│   ├── urls.py             # API 路由
│   └── tests.py
├── manage.py
├── requirements.txt
├── .env                    # 环境变量配置
├── init_data.py            # 测试数据初始化脚本
└── README.md
```

## 注意事项

1. 确保 MySQL 服务已启动
2. 确保数据库字符集使用 utf8mb4
3. 生产环境请修改 DEBUG=False 和 SECRET_KEY
