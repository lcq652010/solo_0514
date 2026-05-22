# 电影院管理系统后端

基于 Python + Django + MySQL 实现的电影院管理系统后端API，支持三级权限隔离、多条件组合筛选、完整的票务流程管理。

## 功能特性

- ✅ 影片管理（增删改查，多条件筛选）
- ✅ 影厅管理（座位自动生成，冲突检测）
- ✅ 影厅排期管理（时间冲突检测，多状态筛选）
- ✅ 座位管理与选座（数据库行级锁，防止超卖）
- ✅ 订单管理（影片+场次+状态多条件组合筛选）
- ✅ 检票入场（检票员权限控制，防止重复检票）
- ✅ 订单结算与退票（事务保证数据一致性，座位自动释放）
- ✅ 订单统计（多维度统计，支持按影片/影厅/时间筛选）
- ✅ 三级权限隔离（管理员/售票员/检票员）
- ✅ 统一分页配置
- ✅ 完整的数据合法性校验

## 三级权限隔离说明

| 角色 | 权限说明 |
|------|---------|
| 管理员 | 系统所有权限，包括用户管理、影片/影厅/排期的增删改查 |
| 售票员 | 查看影片/影厅/排期，创建订单、退票、完结订单，查看统计数据 |
| 检票员 | 查看影片/影厅/排期，执行检票操作 |

## 订单状态流转

```
待检票 (pending) → 已检票 (checked) → 已完结 (completed)
    ↓
已退票 (refunded)
```

## 环境要求

- Python 3.8+
- MySQL 5.7+ 或 8.0+

## 安装步骤

### 1. 创建MySQL数据库

```sql
CREATE DATABASE cinema_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 修改数据库配置

编辑 `cinema_system/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cinema_db',
        'USER': 'root',
        'PASSWORD': '你的密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
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

### 6. 初始化用户组（可选）

登录Django后台，创建三个用户组：
- 管理员
- 售票员
- 检票员

将用户添加到对应的用户组即可获得相应权限。

### 7. 运行项目

```bash
python manage.py runserver
```

访问地址: http://127.0.0.1:8000/

## 认证说明

系统使用Token认证，登录成功后获取token，后续请求在Header中携带：

```
Authorization: Token <your-token>
```

## API 接口文档

### 分页说明

所有列表接口默认支持分页，请求参数：
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认10，最大100）

返回格式：
```json
{
    "count": 100,
    "next": "http://...?page=2",
    "previous": null,
    "results": [...]
}
```

### 基础URL: `/api/`

---

### 1. 认证接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/auth/login/` | 用户登录 | 公开 |
| POST | `/api/auth/logout/` | 用户登出 | 已认证 |
| GET | `/api/auth/permissions/` | 获取当前用户权限 | 已认证 |

**登录请求:**
```json
POST /api/auth/login/
{
    "username": "admin",
    "password": "password"
}
```

**登录返回:**
```json
{
    "token": "abcdefghijklmnopqrstuvwxyz1234567890",
    "user": {
        "id": 1,
        "username": "admin",
        "group_names": ["管理员"],
        "is_admin": true,
        "is_seller": true,
        "is_checker": true
    }
}
```

---

### 2. 用户管理（仅管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET/POST | `/api/users/` | 用户列表/创建用户 |
| GET/PUT/DELETE | `/api/users/{id}/` | 用户详情/更新/删除 |
| GET | `/api/users/me/` | 获取当前用户信息 |
| POST | `/api/users/change_password/` | 修改密码 |
| POST | `/api/users/{id}/toggle_active/` | 启用/禁用用户 |

**创建用户请求:**
```json
POST /api/users/
{
    "username": "seller01",
    "password": "password123",
    "email": "seller01@example.com",
    "first_name": "张",
    "last_name": "三",
    "groups": ["售票员"]
}
```

**筛选参数:**
- `username`: 用户名（模糊查询）
- `group`: 用户组

---

### 3. 影片管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/movies/` | 影片列表 | 所有已认证用户 |
| GET | `/api/movies/showing/` | 正在上映的影片 | 所有已认证用户 |
| GET | `/api/movies/{id}/` | 影片详情 | 所有已认证用户 |
| POST | `/api/movies/` | 新增影片 | 仅管理员 |
| PUT/DELETE | `/api/movies/{id}/` | 更新/删除影片 | 仅管理员 |

**筛选参数:**
- `title`: 影片名称（模糊查询）
- `genre`: 类型（模糊查询）
- `director`: 导演（模糊查询）
- `is_showing`: 是否上映（true/false）
- `min_rating`: 最低评分
- `max_rating`: 最高评分

---

### 4. 影厅管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/halls/` | 影厅列表 | 所有已认证用户 |
| GET | `/api/halls/{id}/` | 影厅详情 | 所有已认证用户 |
| POST | `/api/halls/` | 新增影厅 | 仅管理员 |
| PUT/DELETE | `/api/halls/{id}/` | 更新/删除影厅 | 仅管理员 |
| POST | `/api/halls/{id}/generate_seats/` | 生成影厅座位 | 仅管理员 |

**筛选参数:**
- `name`: 影厅名称（模糊查询）
- `hall_no`: 影厅编号（模糊查询）
- `is_3d`: 是否3D厅（true/false）
- `is_active`: 是否启用（true/false）
- `min_seats`: 最少座位数
- `max_seats`: 最多座位数

---

### 5. 排期管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/schedules/` | 排期列表 | 所有已认证用户 |
| GET | `/api/schedules/{id}/` | 排期详情 | 所有已认证用户 |
| POST | `/api/schedules/` | 新增排期 | 仅管理员 |
| PUT/DELETE | `/api/schedules/{id}/` | 更新/删除排期 | 仅管理员 |
| GET | `/api/schedules/{id}/seats/` | 获取排期座位 | 所有已认证用户 |

**筛选参数 (支持影片+场次+状态多条件组合筛选):**
- `movie_title`: 影片名称（模糊查询）
- `movie_id`: 影片ID
- `hall_id`: 影厅ID
- `hall_name`: 影厅名称（模糊查询）
- `hall_no`: 影厅编号（模糊查询）
- `date`: 日期（YYYY-MM-DD）
- `start_date`: 开始日期
- `end_date`: 结束日期
- `min_price`: 最低票价
- `max_price`: 最高票价
- `is_active`: 是否有效（true/false）
- `status`: 场次状态（upcoming-即将开始, ongoing-进行中, ended-已结束）

---

### 6. 座位管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/seats/` | 座位列表 | 所有已认证用户 |
| GET | `/api/seats/{id}/` | 座位详情 | 所有已认证用户 |
| POST | `/api/seats/` | 新增座位 | 仅管理员 |
| PUT/DELETE | `/api/seats/{id}/` | 更新/删除座位 | 仅管理员 |

**筛选参数:**
- `hall_id`: 影厅ID
- `schedule_id`: 排期ID
- `is_available`: 是否可用（true/false）
- `row_number`: 排号

---

### 7. 订单管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/orders/` | 订单列表 | 所有已认证用户 |
| GET | `/api/orders/{id}/` | 订单详情 | 所有已认证用户 |
| POST | `/api/orders/` | 创建订单（购票） | 售票员/管理员 |
| POST | `/api/orders/{id}/refund/` | 订单退票 | 售票员/管理员 |
| POST | `/api/orders/{id}/complete/` | 完结订单 | 售票员/管理员 |

**筛选参数 (支持影片+场次+状态多条件组合筛选):**
- `order_no`: 订单号（模糊查询）
- `status`: 订单状态（多个用逗号分隔：pending,checked,completed,refunded）
- `movie_id`: 影片ID
- `movie_title`: 影片名称（模糊查询）
- `hall_id`: 影厅ID
- `hall_name`: 影厅名称（模糊查询）
- `hall_no`: 影厅编号（模糊查询）
- `schedule_id`: 排期ID
- `customer_name`: 顾客姓名（模糊查询）
- `customer_phone`: 顾客电话（模糊查询）
- `start_date`: 下单开始日期
- `end_date`: 下单结束日期
- `min_amount`: 最低金额
- `max_amount`: 最高金额

**创建订单请求:**
```json
POST /api/orders/
{
    "schedule": 1,
    "seat_ids": [1, 2, 3],
    "customer_name": "张三",
    "customer_phone": "13800138000"
}
```

**校验规则:**
- 手机号码格式校验
- 至少选择1个座位，最多10个座位
- 不能重复选择同一个座位
- 座位必须属于该排期且未被占用
- 已过期场次不能购票
- 并发购票使用数据库行级锁防止超卖

---

### 8. 检票接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/check-ticket/` | 检票入场 | 检票员/管理员 |

**检票请求:**
```json
POST /api/check-ticket/
{
    "order_no": "TK20240101120000ABC12345"
}
```

**检票校验:**
- 订单必须存在
- 订单不能已退票
- 订单不能已检票
- 订单不能已完结
- 场次不能已结束
- 检票后自动更新订单状态为"已检票"，记录检票时间和检票员

---

### 9. 订单统计

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/order-statistics/` | 获取订单统计数据 | 售票员/管理员 |

**筛选参数:**
- `movie_id`: 影片ID
- `hall_id`: 影厅ID
- `schedule_id`: 排期ID
- `start_date`: 开始日期
- `end_date`: 结束日期

**返回示例:**
```json
{
    "total_orders": 100,
    "pending_orders": 20,
    "checked_orders": 30,
    "completed_orders": 45,
    "refunded_orders": 5,
    "total_revenue": 4500.00,
    "today_orders": 12,
    "today_revenue": 540.00
}
```

---

## 状态自动更新与座位自动释放机制

### 检票后状态自动更新
- 检票成功后，订单状态自动从"待检票"变更为"已检票"
- 自动记录检票时间和检票员
- 防止重复检票

### 退票后座位自动释放
- 使用数据库事务确保数据一致性
- 订单状态变更为"已退票"，记录退票时间和操作人
- 订单关联的所有座位自动标记为可用，释放座位资源
- 仅场次开始前允许退票

## 管理后台

访问: http://127.0.0.1:8000/admin/

使用创建的超级管理员账号登录，可管理所有数据，包括：
- 影片管理
- 影厅管理
- 排期管理
- 座位管理
- 订单管理
- 用户管理
- 用户组权限管理

## 快速测试流程

1. 创建超级管理员账号
2. 登录后台，创建三个用户组：管理员、售票员、检票员
3. 创建测试用户并分配到相应用户组
4. 创建影片、影厅数据
5. 创建排期（系统自动检测时间冲突）
6. 生成排期座位
7. 使用售票员账号登录，创建订单（选座购票）
8. 使用检票员账号登录，执行检票操作
9. 使用售票员账号完结订单或退票
10. 查看订单统计数据
