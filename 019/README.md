# 汽车租赁管理系统后端

基于 Python + Django + MySQL 实现的汽车租赁管理系统后端 API。

## 功能特性

- 车辆管理（增删改查、状态管理）
- 客户登记（客户信息管理）
- 订单预订（创建订单、自动生成订单号）
- 取还车登记（状态流转）
- 租金结算（自动计算租金）

## 订单状态

- 待取车 (pending)
- 已取车 (picked_up)
- 已还车 (returned)
- 已取消 (cancelled)

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- MySQL 5.7+
- mysqlclient 2.2

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+
- pip

### 2. 创建 MySQL 数据库

```sql
CREATE DATABASE car_rental CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

编辑 `.env` 文件，修改数据库配置：

```
DB_NAME=car_rental
DB_USER=root
DB_PASSWORD=你的密码
DB_HOST=localhost
DB_PORT=3306
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 7. 初始化测试数据（可选）

```bash
python manage.py initdata
```

### 8. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

## API 接口文档

### 基础地址

- API 根地址：http://localhost:8000/api/
- 管理后台：http://localhost:8000/admin/

### 分页说明

所有列表接口默认支持分页，分页参数：
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认10，最大100）

分页响应格式：
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/orders/?page=2",
  "previous": null,
  "results": [...]
}
```

### 车辆管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/cars/ | 获取车辆列表（支持筛选） |
| POST | /api/cars/ | 创建车辆 |
| GET | /api/cars/{id}/ | 获取车辆详情 |
| PUT | /api/cars/{id}/ | 更新车辆 |
| DELETE | /api/cars/{id}/ | 删除车辆 |
| GET | /api/cars/available/ | 获取可租用车辆 |

**车辆列表筛选参数（支持多条件组合）：**
- `status`: 状态（可用逗号分隔多选，如 "available,rented"）
- `brand`: 品牌（模糊匹配）
- `model`: 型号（模糊匹配）
- `car_type`: 车型（模糊匹配，如 SUV、轿车）
- `plate_number`: 车牌号（模糊匹配）
- `min_daily_rent`: 最低日租金
- `max_daily_rent`: 最高日租金

### 客户管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/customers/ | 获取客户列表（支持筛选） |
| POST | /api/customers/ | 创建客户 |
| GET | /api/customers/{id}/ | 获取客户详情 |
| PUT | /api/customers/{id}/ | 更新客户 |
| DELETE | /api/customers/{id}/ | 删除客户 |
| GET | /api/customers/search/?keyword=xxx | 搜索客户 |

**客户列表筛选参数：**
- `name`: 姓名（模糊匹配）
- `phone`: 手机号（模糊匹配）
- `gender`: 性别（male/female）

### 订单管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/orders/ | 获取订单列表（支持多条件筛选） |
| POST | /api/orders/ | 创建订单 |
| GET | /api/orders/{id}/ | 获取订单详情 |
| PUT | /api/orders/{id}/ | 更新订单 |
| DELETE | /api/orders/{id}/ | 删除订单 |
| POST | /api/orders/pick_up/ | 取车 |
| POST | /api/orders/return_car/ | 还车（自动结算费用） |
| POST | /api/orders/cancel/ | 取消订单 |
| GET | /api/orders/statistics/ | 订单统计数据 |
| GET | /api/orders/pending/ | 待取车订单 |
| GET | /api/orders/picked_up/ | 已取车订单 |
| GET | /api/orders/returned/ | 已还车订单 |
| GET | /api/orders/cancelled/ | 已取消订单 |

**订单列表多条件筛选参数（支持组合使用）：**
- `status`: 订单状态（可用逗号分隔多选，如 "pending,picked_up"）
- `customer_name`: 客户姓名（模糊匹配）
- `customer_phone`: 客户手机号（模糊匹配）
- `car_brand`: 车辆品牌（模糊匹配）
- `car_model`: 车辆型号（模糊匹配）
- `car_type`: 车辆车型（模糊匹配，如 SUV）
- `plate_number`: 车牌号（模糊匹配）
- `start_date`: 取车日期起（>=）
- `end_date`: 还车日期止（<=）
- `is_overdue`: 是否超时（true），仅筛选超时未还车订单

## API 调用示例

### 创建客户

```bash
curl -X POST http://localhost:8000/api/customers/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试用户",
    "gender": "male",
    "phone": "13900139000",
    "id_card": "110101199001010001",
    "driver_license": "110101199001010001",
    "address": "测试地址",
    "email": "test@example.com"
  }'
```

### 创建订单

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "car": 1,
    "customer": 1,
    "start_date": "2024-01-01",
    "end_date": "2024-01-05",
    "pickup_location": "总店",
    "return_location": "总店",
    "deposit": 1000
  }'
```

### 取车

```bash
curl -X POST http://localhost:8000/api/orders/pick_up/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

### 还车

```bash
curl -X POST http://localhost:8000/api/orders/return_car/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

### 取消订单

```bash
curl -X POST http://localhost:8000/api/orders/cancel/ \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1}'
```

### 多条件组合筛选订单示例

```bash
# 按客户姓名 + 订单状态筛选
curl "http://localhost:8000/api/orders/?customer_name=张三&status=pending"

# 按车辆品牌 + 日期范围筛选
curl "http://localhost:8000/api/orders/?car_brand=奔驰&start_date=2024-01-01&end_date=2024-12-31"

# 分页查询
curl "http://localhost:8000/api/orders/?page=1&page_size=20"
```

## 校验功能说明

### 身份信息校验
- **手机号校验**: 11位有效手机号格式（1开头，第二位3-9）
- **身份证校验**: 18位格式校验 + 校验位验证算法验证
- **驾驶证校验**: 10-20位字母数字组合

### 金额合法性校验
- **日租金**: 10-10000元
- **押金**: 0-50000元
- **座位数**: 2-20座
- **超时费率**: 1-5倍（默认1.5倍）

### 时段冲突校验
创建/更新订单时自动检查同一车辆在相同时段是否存在未完成（待取车/已取车）的订单，避免重复预订。

### 还车自动结算功能
执行还车操作时自动完成：
1. **更新车辆状态**: 车辆自动从"已出租"变为"可租用"
2. **计算实际租赁天数**: 从实际取车日到还车日（按天计算）
3. **计算超时费用**:
   - 提前/按时还车：无超时费
   - 超时还车：正常租期按日租金计算，超时部分按 `日租金 × 超时费率` 计算
4. **生成费用明细**:
   - `base_rental`: 基础租金（正常租期费用）
   - `overtime_days`: 超时天数
   - `overtime_fee`: 超时费用
   - `actual_amount`: 实际总费用（基础租金+超时费）

### 超时订单查询
- 订单详情包含 `is_overdue`（是否超时）和 `overdue_days`（超时天数）字段
- 支持通过 `is_overdue=true` 参数筛选所有超时未还车订单
- 管理后台有醒目的红色超时标记

## 项目结构

```
car_rental/
├── car_rental_system/          # 项目主目录
│   ├── __init__.py
│   ├── settings.py            # 项目配置
│   ├── urls.py                # 主路由
│   ├── asgi.py
│   └── wsgi.py
├── rental/                     # 租赁应用
│   ├── migrations/            # 数据库迁移
│   ├── management/
│   │   └── commands/
│   │       └── initdata.py   # 初始化数据命令
│   ├── __init__.py
│   ├── admin.py               # 管理后台配置
│   ├── apps.py
│   ├── models.py              # 数据模型
│   ├── serializers.py         # 序列化器
│   ├── views.py               # 视图
│   └── urls.py                # 应用路由
├── manage.py
├── requirements.txt
└── .env                       # 环境变量配置
```

## 注意事项

1. 请确保 MySQL 服务已启动
2. 数据库字符集建议使用 utf8mb4
3. 生产环境请修改 SECRET_KEY 并设置 DEBUG=False
4. 建议使用虚拟环境运行
