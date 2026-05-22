# 校园超市管理系统后端

基于 Python + Django + MySQL 实现的校园超市管理系统后端 API。

## 功能特性

- **商品管理**：商品建档、分类管理、库存查询
- **采购入库**：创建采购订单、自动更新库存、库存日志
- **收银结账**：自动生成收银单号、支持会员积分抵扣、库存自动扣减
- **会员管理**：会员注册、积分管理、积分日志
- **订单管理**：订单状态（待结账、已完成、已退款、已作废）、退款、作废
- **库存管理**：库存调整、库存变动日志

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.15
- MySQL 5.7+ / 8.0+
- pymysql / mysqlclient

## 快速开始

### 1. 环境要求

- Python 3.8 或更高版本
- MySQL 5.7 或更高版本

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置数据库

编辑 `.env` 文件，配置数据库连接信息：

```env
DB_NAME=campus_supermarket
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DEBUG=True
SECRET_KEY=your-secret-key
```

### 4. 创建数据库

```bash
python init_db.py
```

### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 初始化测试数据（可选）

```bash
python init_data.py
```

### 7. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 8. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

服务启动后访问：
- API 文档：http://localhost:8000/api/
- 管理后台：http://localhost:8000/admin/

## API 接口说明

### 商品管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/products/` | 获取商品列表 |
| POST | `/api/products/` | 创建商品 |
| GET | `/api/products/{id}/` | 获取商品详情 |
| PUT | `/api/products/{id}/` | 更新商品 |
| DELETE | `/api/products/{id}/` | 删除商品 |
| POST | `/api/products/{id}/adjust_stock/` | 调整库存 |

**查询参数（支持多条件组合筛选）：**
- `category`: 按分类筛选 (food/drink/snack/daily/stationery)
- `keyword`: 按商品名称或商品编号搜索
- `barcode`: 按条形码搜索
- `supplier`: 按供应商搜索
- `is_active`: 是否上架 (true/false)
- `stock_status`: 按库存状态筛选 (out_of_stock-缺货/low-库存不足/normal-库存正常/sufficient-库存充足)
- `min_stock`: 最小库存数量
- `max_stock`: 最大库存数量
- `min_price`: 最低价格
- `max_price`: 最高价格
- `page`: 页码
- `page_size`: 每页数量（默认10，最大100）

**库存校验接口：**
- GET `/api/products/check_stock/?product_ids=1&product_ids=2` - 批量校验库存
- GET `/api/products/low_stock_alert/?threshold=10` - 低库存预警列表

### 会员管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/members/` | 获取会员列表 |
| POST | `/api/members/` | 创建会员 |
| GET | `/api/members/{id}/` | 获取会员详情 |
| GET | `/api/members/by_phone/?phone=xxx` | 按手机号查询会员 |

### 采购订单

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/purchase-orders/` | 获取采购订单列表 |
| POST | `/api/purchase-orders/create_purchase/` | 创建采购订单并入库 |

**采购入库示例：**
```json
{
    "supplier": "供应商A",
    "items": [
        {"product_id": 1, "quantity": 50, "unit_price": 2.5},
        {"product_id": 2, "quantity": 100, "unit_price": 1.2}
    ],
    "remark": "备注信息"
}
```

### 销售订单（收银）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/sales-orders/` | 获取销售订单列表 |
| POST | `/api/sales-orders/checkout/` | 收银结账 |
| POST | `/api/sales-orders/{id}/refund/` | 退款 |
| POST | `/api/sales-orders/{id}/cancel/` | 作废订单 |

**收银结账示例：**
```json
{
    "member_id": 1,
    "items": [
        {"product_id": 1, "quantity": 2},
        {"product_id": 3, "quantity": 1}
    ],
    "points_used": 5,
    "cashier": "收银员A",
    "remark": "备注信息"
}
```

**查询参数：**
- `status`: 订单状态 (pending/completed/refunded/cancelled)
- `start_date`: 开始日期
- `end_date`: 结束日期

### 库存日志

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stock-logs/` | 获取库存变动日志 |

**查询参数：**
- `product_id`: 商品ID
- `type`: 变动类型 (purchase/sale/refund/adjust)

### 积分日志

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/points-logs/` | 获取积分变动日志 |

**查询参数：**
- `member_id`: 会员ID

## 订单状态说明

- `pending`: 待结账
- `completed`: 已完成
- `refunded`: 已退款
- `cancelled`: 已作废

## 收银单号生成规则

格式：`SK` + 时间戳(YYYYMMDDHHMMSS) + 4位随机数

示例：`SK202401151234561234`

## 项目结构

```
campus_supermarket/
├── campus_supermarket/     # 项目配置目录
│   ├── __init__.py
│   ├── settings.py        # 项目配置
│   ├── urls.py            # 主路由
│   ├── wsgi.py
│   └── asgi.py
├── supermarket/           # 超市管理应用
│   ├── __init__.py
│   ├── admin.py           # 管理后台配置
│   ├── apps.py
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── views.py           # 视图函数
│   └── urls.py            # API路由
├── .env                   # 环境变量配置
├── requirements.txt       # 依赖包列表
├── manage.py              # Django管理脚本
├── init_db.py             # 数据库初始化脚本
└── init_data.py           # 测试数据脚本
```

## 注意事项

1. 确保 MySQL 服务已启动
2. 确保数据库用户有创建数据库的权限
3. 生产环境请修改 `SECRET_KEY` 并设置 `DEBUG=False`
4. 建议使用虚拟环境运行项目
