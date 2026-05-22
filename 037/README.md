# 奶茶店点单系统后端

基于 Python + Django + Django REST Framework + MySQL 实现的奶茶店点单系统后端。

## 功能特性

- ✅ 商品管理（分类、增删改查）
- ✅ 在线点单（创建订单、选择商品、自定义规格）
- ✅ 订单支付（模拟支付流程）
- ✅ 制作排队（订单状态管理）
- ✅ 取餐核销（取餐码验证）
- ✅ 自动生成订单号和取餐码
- ✅ 订单状态流转：待制作 → 制作中 → 待取餐 → 已完成
- ✅ 多条件组合筛选（订单号+商品+状态、价格区间、日期等）
- ✅ 库存校验（下单时扣减库存、库存不足提示）
- ✅ 必填信息校验（顾客姓名、手机号、商品数量等）
- ✅ 分页功能（默认每页10条）
- ✅ 金额合法性校验（价格>0、订单总金额限制）
- ✅ 制作完成自动提醒（待取餐订单通知）
- ✅ 取餐核销后自动归档
- ✅ 收银员/制作员/管理员三级权限隔离
- ✅ JWT 身份认证

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- Django REST Framework SimpleJWT 5.3
- MySQL 5.7+ / 8.0+
- mysqlclient 2.2

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+
- pip

### 2. 数据库配置

在 MySQL 中创建数据库：

```sql
CREATE DATABASE milky_tea CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `.env` 文件中的数据库配置：

```
DB_NAME=milky_tea
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 6. 初始化示例数据

```bash
python init_data.py
```

### 7. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

服务启动后访问：
- API 根地址：http://localhost:8000/api/
- Django 后台：http://localhost:8000/admin/

## API 接口文档

### 商品分类接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/categories/ | 获取所有分类 |
| GET | /api/categories/{id}/ | 获取单个分类 |
| POST | /api/categories/ | 创建分类 |
| PUT | /api/categories/{id}/ | 更新分类 |
| DELETE | /api/categories/{id}/ | 删除分类 |

### 商品接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/products/ | 获取所有商品 |
| GET | /api/products/?category=1 | 按分类筛选商品 |
| GET | /api/products/?is_available=true | 获取上架商品 |
| GET | /api/products/?name=奶茶 | 按商品名称模糊搜索 |
| GET | /api/products/?min_price=10&max_price=30 | 按价格区间筛选 |
| GET | /api/products/?has_stock=true | 只显示有库存的商品 |
| GET | /api/products/?page=2&page_size=20 | 分页查询 |
| GET | /api/products/{id}/ | 获取单个商品 |
| POST | /api/products/ | 创建商品 |
| PUT | /api/products/{id}/ | 更新商品 |
| DELETE | /api/products/{id}/ | 删除商品 |

### 订单接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/orders/ | 获取所有订单 |
| GET | /api/orders/?status=pending | 按状态筛选订单 |
| GET | /api/orders/?status=pending,making | 多状态筛选（逗号分隔） |
| GET | /api/orders/?is_paid=true | 筛选已支付订单 |
| GET | /api/orders/?order_no=NT17000 | 按订单号模糊搜索 |
| GET | /api/orders/?product_name=奶茶 | 按商品名称筛选 |
| GET | /api/orders/?product_id=1 | 按商品ID筛选 |
| GET | /api/orders/?customer_name=张三 | 按顾客姓名搜索 |
| GET | /api/orders/?customer_phone=13800138000 | 按手机号搜索 |
| GET | /api/orders/?start_date=2024-01-01&end_date=2024-12-31 | 按日期范围筛选 |
| GET | /api/orders/?min_amount=50&max_amount=200 | 按金额范围筛选 |
| GET | /api/orders/?is_archived=true | 筛选已归档订单 |
| GET | /api/orders/?page=2&page_size=20 | 分页查询 |
| GET | /api/orders/{id}/ | 获取单个订单 |
| POST | /api/orders/ | 创建订单 |
| POST | /api/orders/pay/ | 支付订单 |
| POST | /api/orders/{id}/update_status/ | 更新订单状态 |
| POST | /api/orders/verify/ | 取餐核销（自动归档） |
| GET | /api/orders/queue/ | 获取制作队列 |
| GET | /api/orders/notifications/ | 获取待取餐提醒 |
| POST | /api/orders/{id}/mark_notified/ | 标记单个通知已读 |
| POST | /api/orders/mark_all_notified/ | 标记全部通知已读 |
| POST | /api/orders/{id}/archive/ | 手动归档订单 |
| GET | /api/orders/archived/ | 获取已归档订单 |
| GET | /api/orders/{order_no}/detail_by_no/ | 按订单号查询 |

### 用户与认证接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/auth/login/ | JWT登录获取token |
| POST | /api/auth/refresh/ | 刷新access token |
| GET | /api/users/ | 获取用户列表（仅管理员） |
| POST | /api/users/ | 创建用户（仅管理员） |
| GET | /api/users/{id}/ | 获取用户详情（仅管理员） |
| PUT | /api/users/{id}/ | 更新用户（仅管理员） |
| DELETE | /api/users/{id}/ | 删除用户（仅管理员） |

## 订单状态说明

| 状态码 | 状态名称 | 说明 |
|--------|----------|------|
| pending | 待制作 | 订单已创建，等待制作 |
| making | 制作中 | 正在制作中 |
| ready | 待取餐 | 制作完成，等待取餐 |
| completed | 已完成 | 已取餐，订单完成 |

## 状态流转规则

```
待制作(pending) → 制作中(making) → 待取餐(ready) → 已完成(completed)
```

## API 使用示例

### 1. 创建订单

```bash
POST /api/orders/
Content-Type: application/json

{
    "customer_name": "张三",
    "customer_phone": "13800138000",
    "remark": "少冰",
    "items": [
        {
            "product": 1,
            "quantity": 2,
            "sugar": "半糖",
            "ice": "少冰",
            "toppings": "珍珠"
        },
        {
            "product": 3,
            "quantity": 1,
            "sugar": "全糖",
            "ice": "正常冰",
            "toppings": ""
        }
    ]
}
```

响应示例：
```json
{
    "id": 1,
    "order_no": "NT17000000001234",
    "customer_name": "张三",
    "customer_phone": "13800138000",
    "total_amount": "52.00",
    "status": "pending",
    "status_display": "待制作",
    "is_paid": false,
    "take_code": "1234",
    "remark": "少冰",
    "items": [...]
}
```

### 2. 支付订单

```bash
POST /api/orders/pay/
Content-Type: application/json

{
    "order_no": "NT17000000001234"
}
```

### 3. 更新订单状态（制作中）

```bash
POST /api/orders/1/update_status/
Content-Type: application/json

{
    "status": "making"
}
```

### 4. 更新订单状态（待取餐）

```bash
POST /api/orders/1/update_status/
Content-Type: application/json

{
    "status": "ready"
}
```

### 5. 取餐核销

```bash
POST /api/orders/verify/
Content-Type: application/json

{
    "take_code": "1234"
}
```

### 6. 获取制作队列

```bash
GET /api/orders/queue/
```

返回所有已支付且未完成的订单，按创建时间排序。

## 项目结构

```
.
├── manage.py                 # Django 管理脚本
├── requirements.txt          # 依赖包列表
├── .env                      # 环境配置文件
├── init_data.py              # 初始化数据脚本
├── README.md                 # 项目说明文档
├── milky_tea/               # 项目配置目录
│   ├── __init__.py
│   ├── settings.py          # Django 配置
│   ├── urls.py              # 主路由
│   └── wsgi.py              # WSGI 配置
└── api/                     # API 应用目录
    ├── __init__.py
    ├── apps.py              # 应用配置
    ├── admin.py             # 后台管理配置
    ├── models.py            # 数据模型
    ├── serializers.py       # 序列化器
    ├── views.py             # 视图
    └── urls.py              # API 路由
```

## 数据模型说明

### Category（商品分类）
- name: 分类名称
- description: 分类描述
- created_at: 创建时间
- updated_at: 更新时间

### Product（商品）
- name: 商品名称
- category: 所属分类
- price: 价格
- stock: 库存数量
- image: 商品图片
- description: 商品描述
- is_available: 是否上架
- created_at: 创建时间
- updated_at: 更新时间

### Order（订单）
- order_no: 订单号（自动生成）
- customer_name: 顾客姓名
- customer_phone: 顾客电话
- total_amount: 订单总金额
- status: 订单状态
- is_paid: 是否已支付
- paid_at: 支付时间
- take_code: 取餐码（自动生成）
- remark: 订单备注
- created_at: 创建时间
- updated_at: 更新时间

### OrderItem（订单项）
- order: 所属订单
- product: 商品
- quantity: 数量
- price: 单价
- sugar: 糖度
- ice: 冰度
- toppings: 配料

## 校验规则说明

### 必填校验
- 分类名称：不能为空，至少2个字符
- 商品名称：不能为空，至少2个字符
- 商品价格：不能为空，必须大于0
- 库存数量：不能为空，不能为负数
- 顾客姓名：不能为空，至少2个字符
- 联系电话：不能为空，必须是有效的手机号
- 订单项：订单至少包含一个商品

### 库存校验
- 下单时自动校验商品库存是否充足
- 库存不足时返回具体商品的库存信息
- 下单成功后自动扣减对应商品的库存数量

### 金额校验
- 商品价格：0 < price ≤ 99999
- 订单总金额：0 < total_amount ≤ 999999
- 商品数量：0 < quantity ≤ 100

### 分页说明
- 默认每页10条数据
- 可通过 `page` 参数指定页码
- 可通过 `page_size` 参数自定义每页数量
- 响应格式包含：count（总数）、next（下一页链接）、previous（上一页链接）、results（数据列表）

## 三级权限隔离说明

### 角色说明

| 角色 | 权限范围 |
|------|----------|
| 管理员 (admin) | 所有权限，包括用户管理、商品管理、订单管理、分类管理 |
| 收银员 (cashier) | 创建订单、支付订单、取餐核销、查看订单列表、查看商品 |
| 制作员 (maker) | 更新订单状态（制作中/待取餐）、查看制作队列、查看订单通知 |

### 权限矩阵

| 功能 | 管理员 | 收银员 | 制作员 |
|------|--------|--------|--------|
| 用户管理 | ✅ | ❌ | ❌ |
| 分类增删改 | ✅ | ❌ | ❌ |
| 商品增删改 | ✅ | ❌ | ❌ |
| 创建订单 | ✅ | ✅ | ❌ |
| 支付订单 | ✅ | ✅ | ❌ |
| 取餐核销 | ✅ | ✅ | ❌ |
| 更新订单状态 | ✅ | ❌ | ✅ |
| 查看制作队列 | ✅ | ❌ | ✅ |
| 查看订单通知 | ✅ | ❌ | ✅ |
| 查看订单列表 | ✅ | ✅ | ✅ |
| 查看商品列表 | ✅ | ✅ | ✅ |

## 自动提醒与归档功能

### 制作完成自动提醒
- 当订单状态从「制作中」变为「待取餐」时，自动标记为未通知
- 制作员可通过 `/api/orders/notifications/` 查看待取餐提醒
- 支持单个标记已读和全部标记已读

### 取餐核销后自动归档
- 取餐核销（验证取餐码）时，订单状态变为「已完成」
- 同时自动将订单标记为已归档
- 归档订单通过 `/api/orders/archived/` 查看

## 多条件组合筛选

### 商品筛选参数
- `name`: 商品名称模糊搜索
- `category`: 分类ID
- `is_available`: 是否上架
- `min_price`: 最低价格
- `max_price`: 最高价格
- `has_stock`: 是否有库存

### 订单筛选参数
- `order_no`: 订单号模糊搜索
- `status`: 订单状态（支持逗号分隔多选）
- `is_paid`: 是否已支付
- `product_name`: 订单包含的商品名称（模糊搜索）
- `product_id`: 订单包含的商品ID
- `customer_name`: 顾客姓名
- `customer_phone`: 顾客电话
- `start_date`: 创建开始日期
- `end_date`: 创建结束日期
- `min_amount`: 最低金额
- `max_amount`: 最高金额
- `is_archived`: 是否归档
- `is_notified`: 是否已通知

## 认证说明

### JWT 认证
- 登录接口: `POST /api/auth/login/`
- 刷新令牌: `POST /api/auth/refresh/`
- 请求时在 Header 中添加: `Authorization: Bearer <token>`

### 默认测试账号
| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| cashier | cashier123 | 收银员 |
| maker | maker123 | 制作员 |

## 注意事项

1. 确保 MySQL 服务已启动
2. 确保数据库字符集为 utf8mb4
3. 生产环境请修改 SECRET_KEY 和 DEBUG=False
4. 建议使用虚拟环境运行项目
5. 数据库迁移后记得运行 `python init_data.py` 初始化示例数据

## 许可证

MIT License
