# 外卖店铺管理系统后端

基于 Python + Django + MySQL 实现的外卖店铺管理系统后端 API。

## 功能特性

- ✅ 店铺管理（增删改查）
- ✅ 商品管理（增删改查、分类筛选）
- ✅ 订单创建（自动生成订单号、自动计算金额）
- ✅ 骑手派单
- ✅ 配送跟踪
- ✅ 订单完成/取消
- ✅ 四种订单状态：待接单、配送中、已完成、已取消

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

在 MySQL 中执行：

```sql
CREATE DATABASE food_delivery DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 修改数据库配置

编辑 `food_delivery/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'food_delivery',
        'USER': 'root',           # 修改为你的数据库用户名
        'PASSWORD': 'password',   # 修改为你的数据库密码
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 5. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 初始化测试数据

```bash
python init_data.py
```

此命令将创建：
- 2 个测试店铺
- 10 个测试商品
- 3 个测试骑手

### 7. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

### 8. 启动服务

```bash
python manage.py runserver
```

服务启动后访问：http://localhost:8000/api/

## API 接口说明

### 店铺接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/shops/ | 获取店铺列表 |
| POST | /api/shops/ | 创建店铺 |
| GET | /api/shops/{id}/ | 获取店铺详情 |
| PUT | /api/shops/{id}/ | 更新店铺 |
| DELETE | /api/shops/{id}/ | 删除店铺 |

### 商品接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/products/ | 获取商品列表 |
| POST | /api/products/ | 创建商品 |
| GET | /api/products/{id}/ | 获取商品详情 |
| PUT | /api/products/{id}/ | 更新商品 |
| DELETE | /api/products/{id}/ | 删除商品 |

查询参数：
- `shop_id`: 按店铺筛选
- `category`: 按分类筛选

### 骑手接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/riders/ | 获取骑手列表 |
| POST | /api/riders/ | 创建骑手 |
| GET | /api/riders/{id}/ | 获取骑手详情 |
| PUT | /api/riders/{id}/ | 更新骑手 |
| DELETE | /api/riders/{id}/ | 删除骑手 |
| GET | /api/riders/available/ | 获取在岗骑手 |

### 订单接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/orders/ | 获取订单列表 |
| POST | /api/orders/ | 创建订单 |
| GET | /api/orders/{id}/ | 获取订单详情 |
| POST | /api/orders/{id}/assign_rider/ | 分配骑手（派单） |
| POST | /api/orders/{id}/complete/ | 完成订单 |
| POST | /api/orders/{id}/cancel/ | 取消订单 |
| POST | /api/orders/{id}/update_tracking/ | 更新配送信息 |
| GET | /api/orders/{id}/tracking/ | 获取配送跟踪记录 |

查询参数：
- `status`: 按状态筛选 (pending/delivering/completed/cancelled)
- `shop_id`: 按店铺筛选
- `rider_id`: 按骑手筛选

### 配送跟踪接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/tracking/ | 获取配送跟踪列表 |
| GET | /api/tracking/{id}/ | 获取配送跟踪详情 |

查询参数：
- `order_id`: 按订单筛选

## API 调用示例

### 1. 创建订单

```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "shop": 1,
    "customer_name": "张三",
    "customer_phone": "13800000000",
    "customer_address": "北京市朝阳区xxx路xxx号",
    "remark": "不要辣",
    "items": [
      {"product": 1, "quantity": 2},
      {"product": 4, "quantity": 2}
    ]
  }'
```

### 2. 分配骑手（派单）

```bash
curl -X POST http://localhost:8000/api/orders/1/assign_rider/ \
  -H "Content-Type: application/json" \
  -d '{"rider_id": 1}'
```

### 3. 更新配送跟踪

```bash
curl -X POST http://localhost:8000/api/orders/1/update_tracking/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "已取餐",
    "description": "骑手已取餐，正在配送中",
    "latitude": "39.9042",
    "longitude": "116.4074"
  }'
```

### 4. 完成订单

```bash
curl -X POST http://localhost:8000/api/orders/1/complete/
```

### 5. 取消订单

```bash
curl -X POST http://localhost:8000/api/orders/1/cancel/
```

## 订单状态流转

```
待接单 (pending)
    ↓
配送中 (delivering)  ← 分配骑手
    ↓
已完成 (completed)    ← 送达
    ↓
（终止状态）

待接单 (pending)
    ↓
已取消 (cancelled)    ← 取消订单
    ↓
（终止状态）
```

## 统一响应格式

所有 API 接口返回统一格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 100,
    "total_pages": 10,
    "current_page": 1,
    "page_size": 10,
    "results": [...]
  }
}
```

## 新功能使用示例

### 1. 多条件组合筛选订单

```bash
# 搜索昵称包含"张"、状态为待接单或配送中、金额10-100元、2024年1月1日之后的订单
curl "http://localhost:8000/api/orders/?customer_name=张&status=pending,delivering&min_amount=10&max_amount=100&start_date=2024-01-01&page=1&page_size=20"
```

### 2. 按商品类型筛选商品

```bash
# 获取热菜分类、有库存、价格20-50元、已上架的商品
curl "http://localhost:8000/api/products/?category=热菜&has_stock=true&min_price=20&max_price=50&is_available=true"
```

### 3. 自定义分页

```bash
# 获取第2页，每页50条数据
curl "http://localhost:8000/api/orders/?page=2&page_size=50"
```

### 4. 下单时的校验说明

下单时系统会自动校验：
- **用户昵称**：长度2-50字符
- **手机号**：11位有效手机号格式
- **配送地址**：长度5-200字符，且包含地址关键词（省/市/区/路/街等）
- **商品库存**：检查每个商品库存是否充足
- **订单金额**：自动计算，确保金额合法

## 项目结构

```
.
├── food_delivery/          # 项目主目录
│   ├── __init__.py
│   ├── settings.py         # 配置文件
│   ├── urls.py             # 主路由
│   ├── asgi.py
│   └── wsgi.py
├── api/                    # API 应用
│   ├── __init__.py
│   ├── admin.py            # 后台管理
│   ├── apps.py
│   ├── models.py           # 数据模型
│   ├── serializers.py      # 序列化器（含校验逻辑）
│   ├── urls.py             # API 路由
│   └── views.py            # 视图（含筛选和分页逻辑）
├── manage.py               # Django 管理脚本
├── init_data.py            # 初始化数据脚本
├── requirements.txt        # 依赖清单
└── README.md               # 说明文档
```

## 管理后台

访问：http://localhost:8000/admin/

使用创建的超级用户登录，可以在后台管理所有数据。
