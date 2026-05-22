# 酒店管理系统后端

基于 Python + Django + MySQL 实现的酒店管理系统后端API，支持多条件筛选、超时费用自动计算、三级权限隔离。

## 功能特性

- 客房管理（CRUD）
- 客人信息登记
- 预订管理
- 入住办理
- 退房结算
- 订单状态管理（待入住、已入住、已退房、已取消）
- 自动生成订单号
- 数据统计
- **多条件组合筛选**（房间号、客人姓名、订单状态等）
- **预订时段冲突校验**
- **完善的必填字段校验**
- **分页功能**
- **金额合法性校验**
- **超时费用自动计算**
- **退房后房间状态自动释放并标记为待清洁**
- **三级权限隔离**（前台/客房/管理员）

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.15
- MySQL 5.7+ / 8.0+

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+ 或 8.0+
- pip

### 2. 创建并激活虚拟环境

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

#### 方法一：手动创建数据库

1. 登录MySQL：
```bash
mysql -u root -p
```

2. 执行初始化脚本：
```sql
source init_db.sql;
```

或者手动创建数据库：
```sql
CREATE DATABASE hotel_management DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 方法二：修改配置

编辑 `.env` 文件，修改数据库连接信息：

```env
DB_NAME=hotel_management
DB_USER=root
DB_PASSWORD=你的密码
DB_HOST=localhost
DB_PORT=3306
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

按照提示输入用户名、邮箱和密码。

### 7. 初始化用户角色（推荐）

```bash
python manage.py shell < init_roles.py
```

这将创建三个测试用户：
- 管理员：admin / admin123
- 前台：receptionist / receptionist123
- 客房：housekeeper / housekeeper123

### 8. 导入初始客房数据（可选）

```bash
mysql -u root -p hotel_management < init_db.sql
```

### 9. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

服务启动后，访问：
- 管理后台：http://localhost:8000/admin/
- API接口：http://localhost:8000/api/

## 权限说明

### 三级角色权限

| 角色 | 权限范围 |
|------|----------|
| 管理员(admin) | 所有权限，包括用户管理、房间增删改、订单管理等 |
| 前台(receptionist) | 客人登记、订单预订/取消、入住办理、退房结算 |
| 客房(housekeeper) | 查看房间信息、标记房间清洁状态 |

## API 接口文档

### 通用参数

#### 分页参数
所有列表接口均支持分页：
- `page`: 页码（默认1）
- `page_size`: 每页条数（默认10，最大100）

分页返回格式：
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/rooms/?page=2",
  "previous": null,
  "results": []
}
```

### 1. 认证接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /api/auth/ | 用户登录 | 无需认证 |
| DELETE | /api/auth/ | 用户登出 | 已认证 |
| GET | /api/users/me/ | 获取当前用户信息 | 已认证 |

**登录请求示例：**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

### 2. 用户管理（仅管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/users/ | 获取用户列表 |
| POST | /api/users/ | 创建用户 |
| GET | /api/users/{id}/ | 获取用户详情 |
| PUT | /api/users/{id}/ | 修改用户信息 |
| DELETE | /api/users/{id}/ | 删除用户 |

**创建用户请求示例：**
```json
{
  "username": "new_user",
  "password": "password123",
  "email": "user@hotel.com",
  "role": "receptionist",
  "real_name": "新前台",
  "phone": "13800138003"
}
```

### 3. 客房管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/rooms/ | 获取所有客房列表 | 已认证 |
| GET | /api/rooms/{id}/ | 获取单个客房详情 | 已认证 |
| POST | /api/rooms/ | 新增客房 | 管理员 |
| PUT | /api/rooms/{id}/ | 修改客房信息 | 管理员 |
| DELETE | /api/rooms/{id}/ | 删除客房 | 管理员 |
| GET | /api/rooms/available/ | 获取可用（空闲+已清洁）客房列表 | 已认证 |
| POST | /api/rooms/{id}/mark_clean/ | 标记房间为已清洁 | 客房/管理员 |
| POST | /api/rooms/{id}/mark_dirty/ | 标记房间为待清洁 | 客房/管理员 |

#### 客房筛选参数（支持多条件组合）：
- `room_number`: 按房间号模糊搜索
- `room_type`: 按房间类型筛选（single/double/suite/deluxe）
- `status`: 按状态筛选（available/occupied/reserved/maintenance）
- `clean_status`: 按清洁状态筛选（clean/dirty/cleaning）
- `floor`: 按楼层筛选
- `min_price`: 最低价格
- `max_price`: 最高价格

**示例：**
```
GET /api/rooms/?room_number=101&status=available&clean_status=clean&min_price=100&max_price=500&page=1&page_size=10
```

房间类型：
- single: 单人间
- double: 双人间
- suite: 套房
- deluxe: 豪华套房

### 4. 客人管理（前台/管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/guests/ | 获取所有客人列表 |
| GET | /api/guests/{id}/ | 获取单个客人详情 |
| POST | /api/guests/ | 新增客人 |
| PUT | /api/guests/{id}/ | 修改客人信息 |
| DELETE | /api/guests/{id}/ | 删除客人 |
| POST | /api/guests/register/ | 客人登记 |

#### 客人筛选参数（支持多条件组合）：
- `name`: 按姓名模糊搜索
- `phone`: 按手机号模糊搜索
- `id_card`: 按身份证号模糊搜索
- `gender`: 按性别筛选

**示例：**
```
GET /api/guests/?name=张三&phone=138&page=1&page_size=10
```

### 5. 订单管理

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | /api/orders/ | 获取所有订单列表 | 已认证 |
| GET | /api/orders/{id}/ | 获取单个订单详情 | 已认证 |
| POST | /api/orders/ | 创建订单（预订） | 前台/管理员 |
| PUT | /api/orders/{id}/ | 修改订单信息 | 前台/管理员 |
| DELETE | /api/orders/{id}/ | 删除订单 | 前台/管理员 |
| POST | /api/orders/{id}/cancel/ | 取消订单 | 前台/管理员 |
| GET | /api/orders/pending/ | 待入住订单列表 | 已认证 |
| GET | /api/orders/checked_in/ | 已入住订单列表 | 已认证 |
| GET | /api/orders/checked_out/ | 已退房订单列表 | 已认证 |
| GET | /api/orders/cancelled/ | 已取消订单列表 | 已认证 |

#### 订单筛选参数（支持多条件组合）：
- `order_number`: 按订单号模糊搜索
- `guest_name`: 按客人姓名模糊搜索
- `guest_phone`: 按客人手机号模糊搜索
- `room_number`: 按房间号模糊搜索
- `status`: 按订单状态筛选
- `check_in_date_from`: 入住日期起始
- `check_in_date_to`: 入住日期结束

**示例：**
```
GET /api/orders/?guest_name=张三&room_number=101&status=pending&page=1&page_size=10
```

订单状态：
- pending: 待入住
- checked_in: 已入住
- checked_out: 已退房
- cancelled: 已取消

#### 预订时段冲突校验
创建或修改订单时，系统会自动校验：
- 所选房间在入住-退房时段内是否已被预订
- 如果存在冲突，返回错误提示："该房间在所选时段已被预订"

#### 金额校验
- 押金不能为负数
- 押金不能超过100000
- 房间价格必须大于0

### 6. 入住/退房（前台/管理员）

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/check-in/ | 办理入住 |
| POST | /api/check-out/ | 办理退房 |

**办理入住请求示例：**
```json
{
  "order_id": 1
}
```

**办理退房请求示例：**
```json
{
  "order_id": 1
}
```

#### 退房功能特点：
1. 自动计算超时费用（超过12:00退房，按小时计费）
2. 自动更新房间状态为空闲
3. 自动标记房间为待清洁
4. 自动计算退款金额（押金 - 总金额）

### 7. 统计信息

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/statistics/ | 获取系统统计信息 |

返回内容：
- 客房统计（总数、空闲、已入住、已预订、待清洁）
- 订单统计（总数、各状态数量、总金额、总超时费用）
- 今日统计（今日入住、今日退房）

## 使用示例流程

### 完整业务流程

1. **登录系统（前台）**
```bash
POST http://localhost:8000/api/auth/
{
  "username": "receptionist",
  "password": "receptionist123"
}
```

2. **登记客人信息**
```bash
POST http://localhost:8000/api/guests/register/
{
  "name": "张三",
  "id_card": "110101199001011234",
  "phone": "13800138000",
  "gender": "male"
}
```

3. **查询可用客房**
```bash
GET http://localhost:8000/api/rooms/available/
```

4. **创建预订订单**
```bash
POST http://localhost:8000/api/orders/
{
  "guest": 1,
  "room": 1,
  "check_in_date": "2024-01-15",
  "check_out_date": "2024-01-18",
  "deposit": 500,
  "remark": "需要无烟房"
}
```

5. **办理入住**
```bash
POST http://localhost:8000/api/check-in/
{
  "order_id": 1
}
```

6. **客房服务标记清洁**
```bash
POST http://localhost:8000/api/rooms/1/mark_clean/
```

7. **办理退房（自动计算超时费用）**
```bash
POST http://localhost:8000/api/check-out/
{
  "order_id": 1
}
```

## 超时费用计算规则

- 退房时间默认12:00
- 超过12:00退房，按小时计算超时费用
- 超时费率 = 房间日价 / 24小时
- 不足1小时按1小时计算
- 超时费用 = 超时小时数 × 小时费率

## 项目结构

```
.
├── hotel_management/       # 项目配置目录
│   ├── __init__.py
│   ├── settings.py         # 项目配置
│   ├── urls.py             # 主路由配置
│   ├── asgi.py
│   └── wsgi.py
├── hotel/                  # 酒店管理应用
│   ├── __init__.py
│   ├── admin.py            # 管理后台配置
│   ├── apps.py             # 应用配置
│   ├── models.py           # 数据模型
│   ├── serializers.py      # 序列化器
│   ├── views.py            # 视图/API接口
│   ├── urls.py             # 应用路由
│   ├── permissions.py      # 权限控制
│   └── migrations/         # 数据库迁移文件
├── manage.py               # Django管理脚本
├── requirements.txt        # 依赖包列表
├── .env                    # 环境配置文件
├── init_db.sql             # 数据库初始化脚本
├── init_roles.py           # 用户角色初始化脚本
└── README.md               # 说明文档
```

## 注意事项

1. 确保MySQL服务已启动
2. 修改`.env`中的数据库密码为实际密码
3. 生产环境请修改`SECRET_KEY`并设置`DEBUG=False`
4. 建议使用虚拟环境运行
5. 办理入住前确保房间状态为"已清洁"

## 常见问题

**Q: 遇到mysqlclient安装失败怎么办？**

A: Windows用户可以下载预编译的whl包安装，或者使用pymysql替代（已配置好）

**Q: 如何重置数据库？**

A: 删除所有migrations文件，然后重新执行：
```bash
python manage.py makemigrations
python manage.py migrate
```

**Q: 如何查看API接口文档？**

A: 启动服务后直接访问 http://localhost:8000/api/ 可以看到DRF自带的可浏览API界面。

**Q: 如何初始化测试数据？**

A: 执行以下命令：
```bash
mysql -u root -p hotel_management < init_db.sql
python manage.py shell < init_roles.py
```
