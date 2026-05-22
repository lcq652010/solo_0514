# 二手回收系统后端

基于 Python + Django + MySQL 的二手回收系统后端 API。

## 功能特性

- **物品登记**: 支持多种物品分类登记
- **在线估价**: 对回收物品进行价格评估
- **上门回收**: 上门回收状态管理
- **入库质检**: 回收物品质量检查
- **订单结算**: 完成订单并结算
- **订单状态流转**: 待上门 → 已回收 → 已入库 → 已完成
- **自动生成回收单号**: RC + 日期 + 8位UUID
- **多条件组合筛选**: 支持用户、物品、状态等多条件筛选
- **三级权限隔离**: 客服 / 回收员 / 管理员，不同角色不同权限
- **回收完成自动入库**: 支持一键完成回收并自动入库
- **质检后自动结算**: 入库质检后可自动完成结算
- **JWT身份认证**: 安全的API访问控制

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.15
- Django REST Framework SimpleJWT 5.3
- MySQL 5.7+/8.0+

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=recycle_system
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=3306
```

### 3. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE recycle_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动服务

```bash
python manage.py runserver
```

服务启动后访问：http://127.0.0.1:8000/

## 三级权限说明

| 功能 | 客服 | 回收员 | 管理员 |
|------|------|--------|--------|
| 创建订单 | ✅ | ❌ | ✅ |
| 编辑订单 | ✅ | ❌ | ✅ |
| 删除订单 | ❌ | ❌ | ✅ |
| 分配回收员 | ✅ | ❌ | ✅ |
| 在线估价 | ✅ | ❌ | ✅ |
| 上门回收 | ❌ | ✅ | ✅ |
| 入库质检 | ❌ | ✅ | ✅ |
| 订单结算 | ❌ | ❌ | ✅ |
| 用户管理 | ❌ | ❌ | ✅ |

**回收员数据隔离**: 回收员只能查看分配给自己或未分配的订单

## API 接口

### 认证接口
- `POST /api/token/` - 获取JWT访问令牌
- `POST /api/token/refresh/` - 刷新访问令牌

### 用户管理
- `GET /api/users/` - 获取用户列表
- `GET /api/users/me/` - 获取当前登录用户信息及权限
- `GET /api/users/recyclers/` - 获取所有回收员列表
- `GET /api/users/{id}/` - 获取用户详情

### 物品管理
- `GET /api/items/` - 获取物品列表（支持筛选和分页）
  - 查询参数：`category`(分类), `name`(名称模糊搜索), `min_price`, `max_price`, `page`, `page_size`
- `POST /api/items/` - 创建物品
- `GET /api/items/{id}/` - 获取物品详情
- `PUT /api/items/{id}/` - 更新物品
- `DELETE /api/items/{id}/` - 删除物品

### 订单管理
- `GET /api/orders/` - 获取订单列表（支持多条件组合筛选和分页）
  - 查询参数：
    - `customer_name` - 客户姓名模糊搜索
    - `phone` - 联系电话模糊搜索
    - `status` - 订单状态 (pending_pickup/picked_up/warehoused/completed)
    - `item_category` - 物品分类筛选
    - `start_date` - 上门时间起始日期 (YYYY-MM-DD)
    - `end_date` - 上门时间结束日期 (YYYY-MM-DD)
    - `created_by` - 创建人ID
    - `recycler` - 回收员ID
    - `page` - 页码
    - `page_size` - 每页数量
- `GET /api/orders/my_orders/` - 获取我的订单（根据角色过滤）
- `POST /api/orders/` - 创建订单（物品登记，含上门时间冲突校验）
- `GET /api/orders/{id}/` - 获取订单详情
- `POST /api/orders/{id}/assign_recycler/` - 分配回收员
- `POST /api/orders/{id}/estimate/` - 在线估价（含价格校验）
- `POST /api/orders/{id}/pickup/` - 上门回收（支持自动入库）
- `POST /api/orders/{id}/warehouse/` - 入库质检（支持自动结算）
- `POST /api/orders/{id}/complete/` - 订单结算

### 质检管理
- `GET /api/quality-checks/` - 获取质检列表（支持筛选和分页）
  - 查询参数：`result`(质检结果), `checker`(质检人), `order_no`, `page`, `page_size`
- `POST /api/quality-checks/` - 创建质检
- `GET /api/quality-checks/{id}/` - 获取质检详情

### 结算管理
- `GET /api/settlements/` - 获取结算列表（支持筛选和分页）
  - 查询参数：`operator`(操作员), `order_no`, `start_date`, `end_date`, `page`, `page_size`
- `POST /api/settlements/` - 创建结算
- `GET /api/settlements/{id}/` - 获取结算详情

## API 使用示例

### 1. 获取 JWT Token

```bash
POST /api/token/
Content-Type: application/json

{
    "username": "admin",
    "password": "your-password"
}
```

响应：
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**后续请求在 Header 中添加**: `Authorization: Bearer {access_token}`

### 2. 创建订单（物品登记）

```bash
POST /api/orders/
Content-Type: application/json
Authorization: Bearer {access_token}

{
    "customer_name": "张三",
    "customer_phone": "13800138000",
    "address": "北京市朝阳区xxx街道xxx号",
    "pickup_time": "2024-01-15 14:30:00",
    "remark": "请准时上门",
    "recycler": 2,
    "items": [
        {
            "name": "旧笔记本电脑",
            "category": "electronics",
            "description": "联想ThinkPad，使用5年",
            "quantity": 1,
            "estimated_price": 500
        },
        {
            "name": "旧手机",
            "category": "electronics",
            "description": "iPhone 8",
            "quantity": 2,
            "estimated_price": 300
        }
    ]
}
```

### 3. 在线估价

```bash
POST /api/orders/1/estimate/
Content-Type: application/json
Authorization: Bearer {access_token}

{
    "estimated_prices": [
        {"price": 600},
        {"price": 350}
    ],
    "auto_warehouse": false,
    "auto_settle": false
}
```

### 4. 上门回收（支持自动入库）

```bash
POST /api/orders/1/pickup/
Content-Type: application/json
Authorization: Bearer {access_token}

{
    "auto_warehouse": true,
    "auto_settle": false
}
```

### 5. 入库质检（支持自动结算）

```bash
POST /api/orders/1/warehouse/
Content-Type: application/json
Authorization: Bearer {access_token}

{
    "checker": "质检员李四",
    "result": "pass",
    "actual_amount": 950,
    "issue_description": "物品完好",
    "auto_settle": true
}
```

### 6. 订单结算

```bash
POST /api/orders/1/complete/
Content-Type: application/json
Authorization: Bearer {access_token}

{
    "operator": "财务王五",
    "remark": "已完成结算"
}
```

### 7. 分配回收员

```bash
POST /api/orders/1/assign_recycler/
Content-Type: application/json
Authorization: Bearer {access_token}

{
    "recycler_id": 3
}
```

### 8. 多条件组合筛选订单

```bash
# 筛选待上门状态、电子产品分类的订单
GET /api/orders/?status=pending_pickup&item_category=electronics

# 按客户姓名和电话搜索
GET /api/orders/?customer_name=张三&phone=13800138000

# 按日期范围筛选
GET /api/orders/?start_date=2024-01-01&end_date=2024-01-31

# 按回收员筛选
GET /api/orders/?recycler=3

# 组合筛选
GET /api/orders/?status=pending_pickup&customer_name=张&start_date=2024-01-01&end_date=2024-01-31
```

### 9. 分页查询

```bash
# 第1页，每页10条（默认）
GET /api/orders/?page=1

# 第2页，每页20条
GET /api/orders/?page=2&page_size=20

# 带筛选的分页
GET /api/orders/?status=completed&page=1&page_size=50
```

## 功能特性说明

### 1. 三级权限隔离
- **客服(Customer Service)**: 负责创建订单、分配回收员、物品估价
- **回收员(Recycler)**: 负责上门回收、入库质检，只能查看相关订单
- **管理员(Admin)**: 拥有全部权限，包括订单结算、用户管理

### 2. 数据隔离机制
- 回收员只能查看分配给自己或未分配的订单
- 我的订单接口根据角色自动过滤数据

### 3. 回收完成自动入库
- 上门回收时设置 `auto_warehouse: true`，系统自动完成入库质检
- 自动入库时默认质检结果为通过(pass)
- 可进一步设置 `auto_settle: true` 实现回收-入库-结算一键完成

### 4. 质检后自动结算
- 入库质检时设置 `auto_settle: true`，系统自动完成订单结算
- 结算金额采用质检记录中的实际金额

### 5. 多条件组合筛选
- 支持按客户姓名、联系电话、订单状态、物品分类、日期范围、创建人、回收员等多条件组合筛选
- 所有筛选参数都是可选的，可以灵活组合使用

### 6. 上门时间冲突校验
- 同一时间段（前后1小时内）只能预约一个订单
- 创建订单时自动检测时间冲突
- 避免重复预约，提高回收效率

### 7. 完整的必填字段校验
- 客户姓名、联系电话、回收地址、上门时间、物品列表等均为必填项
- 每个字段都有严格的格式和长度校验
- 手机号格式校验（1开头的11位手机号）

### 8. 价格校验
- 所有金额字段不能为负数
- 单物品价格不超过100,000元
- 订单总金额不超过1,000,000元
- 防止异常数据录入

### 9. 灵活分页
- 默认每页10条记录
- 支持自定义每页数量（1-100条）
- 分页与筛选功能可组合使用

## 物品分类

- `electronics` - 电子产品
- `furniture` - 家具
- `metal` - 金属
- `paper` - 纸品
- `plastic` - 塑料
- `clothing` - 衣物
- `other` - 其他

## 订单状态

- `pending_pickup` - 待上门
- `picked_up` - 已回收
- `warehoused` - 已入库
- `completed` - 已完成

## 用户角色

- `customer_service` - 客服
- `recycler` - 回收员
- `admin` - 管理员

## 管理后台

访问 http://127.0.0.1:8000/admin/ 可以进入 Django 管理后台，使用超级用户登录后可以管理所有数据，包括：

- 用户管理（分配角色）
- 订单管理
- 物品管理
- 质检记录
- 结算记录

### 设置用户角色

在管理后台编辑用户，在"用户资料"部分选择对应的角色保存即可。
