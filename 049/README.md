# 农产品批发管理系统后端

基于 Python + Django + MySQL 实现的农产品批发管理系统后端 API。

## 功能特性

### 核心功能
- **商品建档**：商品分类、商品信息管理
- **采购入库**：供应商管理、采购订单、入库确认
- **批发下单**：客户管理、批发订单创建
- **出库结算**：配送管理、订单完成、结算支付
- **库存预警**：库存查询、库存变动记录、低库存预警

### 新增功能
- **组合筛选**：支持按商品名称、分类、库存状态多条件筛选
- **库存自动扣减**：出库时自动扣减库存，库存不足时提示
- **预警自动提示**：低于预警线自动创建预警消息，支持分级预警
- **角色权限管理**：开单员/库管/老板三级权限体系

## 订单状态

批发订单包含以下四种状态：
- 待出库 (pending)
- 配送中 (delivering)
- 已完成 (completed)
- 已作废 (cancelled)

## 角色权限体系

| 权限 | 开单员 | 库管 | 老板 |
|------|--------|------|------|
| 订单管理 | ✅ | ❌ | ✅ |
| 库存管理 | ❌ | ✅ | ✅ |
| 商品管理 | ✅ | ✅ | ✅ |
| 供应商管理 | ❌ | ✅ | ✅ |
| 客户管理 | ✅ | ❌ | ✅ |
| 结算管理 | ❌ | ❌ | ✅ |
| 查看报表 | ❌ | ❌ | ✅ |
| 用户管理 | ❌ | ❌ | ✅ |

## 技术栈

- Python 3.8+
- Django 4.2.7
- Django REST Framework 3.14.0
- MySQL 5.7+
- django-cors-headers

## 安装配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 MySQL 数据库

创建数据库：
```sql
CREATE DATABASE wholesale_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `wholesale_system/settings.py` 中的数据库配置：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wholesale_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 初始化测试用户角色

```bash
python init_roles.py
```

### 5. 运行开发服务器

```bash
python manage.py runserver
```

访问地址：
- 后台管理：http://127.0.0.1:8000/admin/
- API 文档：http://127.0.0.1:8000/docs/

### 测试账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 老板 | admin | admin123 |
| 开单员 | order_clerk | order123 |
| 库管 | warehouse | warehouse123 |
| 老板 | boss | boss123 |

## API 接口列表

### 认证与权限
- `POST /api/auth/login/` - 用户登录
- `GET /api/auth/users/me/` - 获取当前用户信息
- `GET /api/auth/users/` - 用户列表
- `POST /api/auth/users/create_user/` - 创建用户
- `GET /api/auth/stock-alerts/unread_count/` - 未读预警数量
- `POST /api/auth/stock-alerts/{id}/mark_read/` - 标记预警已读
- `POST /api/auth/stock-alerts/mark_all_read/` - 标记所有预警已读

### 商品管理
- `GET /api/products/categories/` - 商品分类列表
- `POST /api/products/categories/` - 创建商品分类
- `GET /api/products/products/` - 商品列表（支持name/category/is_active/stock_status筛选）
- `POST /api/products/products/` - 创建商品

### 采购管理
- `GET /api/purchases/suppliers/` - 供应商列表（支持name/is_active筛选）
- `POST /api/purchases/purchase-orders/` - 创建采购订单
- `POST /api/purchases/purchase-orders/{id}/confirm_receipt/` - 确认入库
- `POST /api/purchases/purchase-orders/{id}/cancel/` - 作废订单

### 订单管理
- `GET /api/orders/customers/` - 客户列表（支持name/is_active筛选）
- `POST /api/orders/wholesale-orders/` - 创建批发订单
- `POST /api/orders/wholesale-orders/{id}/start_delivery/` - 开始配送（自动扣减库存）
- `POST /api/orders/wholesale-orders/{id}/complete/` - 完成订单
- `POST /api/orders/wholesale-orders/{id}/cancel/` - 作废订单
- `GET /api/orders/settlements/` - 结算单列表
- `POST /api/orders/settlements/{id}/confirm_payment/` - 确认付款

### 库存管理
- `GET /api/inventory/inventory/` - 库存列表（支持product_name/stock_status筛选）
- `GET /api/inventory/inventory/low_stock_alerts/` - 低库存预警
- `GET /api/inventory/inventory/statistics/` - 库存统计
- `GET /api/inventory/stock-records/` - 库存变动记录
- `GET /api/inventory/stock-alerts/` - 库存预警列表
- `POST /api/inventory/stock-alerts/{id}/handle_alert/` - 处理预警

## 订单编号规则

系统自动生成订单编号，规则如下：
- 采购订单：PO + 年月日 + 4位序号（如：PO202401150001）
- 批发订单：WO + 年月日 + 4位序号（如：WO202401150001）
- 结算单号：ST + 年月日 + 4位序号（如：ST202401150001）

## 项目结构

```
wholesale_system/
├── manage.py
├── requirements.txt
├── init_roles.py       # 初始化用户角色脚本
├── wholesale_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── pagination.py    # 自定义分页
│   ├── permissions.py   # 权限装饰器
│   └── exceptions.py    # 异常处理
├── accounts/          # 用户权限应用
├── products/          # 商品管理应用
├── purchases/         # 采购管理应用
├── orders/            # 订单管理应用
└── inventory/         # 库存管理应用
    └── services.py    # 库存服务（入库/出库/预警检查）
```
