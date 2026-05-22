# 家政服务平台后端

基于 Python + Django + Django REST Framework + MySQL 实现的家政服务平台后端系统。

## 功能特性

- 服务项目管理（增删改查）
- 阿姨信息管理（技能、状态、评分等）
- 客户下单（自动生成订单号）
- 派单上门功能
- 订单状态管理（待派单、服务中、已完成、已取消）
- 完成评价功能（自动计算平均评分）
- RESTful API 接口

## 项目结构

```
.
├── housekeeping/          # 项目主目录
│   ├── __init__.py
│   ├── settings.py        # 配置文件
│   ├── urls.py            # 主路由
│   └── wsgi.py
├── api/                   # API应用
│   ├── __init__.py
│   ├── admin.py           # 后台管理
│   ├── apps.py
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── urls.py            # API路由
│   └── views.py           # 视图
├── manage.py              # Django管理脚本
├── requirements.txt       # 依赖包
├── init_data.py           # 初始化数据脚本
└── README.md
```

## 环境要求

- Python 3.8+
- MySQL 5.7+ 或 MySQL 8.0+
- pip 包管理器

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建MySQL数据库

在MySQL中执行：

```sql
CREATE DATABASE housekeeping_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置数据库连接

编辑 `housekeeping/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'housekeeping_db',
        'USER': 'root',       # 你的MySQL用户名
        'PASSWORD': '123456', # 你的MySQL密码
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
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

### 7. 启动开发服务器

```bash
python manage.py runserver
```

访问 http://localhost:8000 即可查看项目。

## API 接口文档

启动服务器后，访问 http://localhost:8000/api/ 可以查看DRF提供的API浏览器界面。

### 服务项目接口

- `GET /api/services/` - 获取服务列表（支持分页）
  - 参数：
    - `is_active=true/false` - 按启用状态筛选
    - `name=xxx` - 按服务名称模糊搜索
    - `min_price=xx` - 最低价格筛选
    - `max_price=xx` - 最高价格筛选
    - `page=1` - 页码
    - `page_size=10` - 每页数量
- `POST /api/services/` - 创建服务
  - 必填校验：name, price, duration
  - 金额校验：价格 > 0 且 <= 100000
- `GET /api/services/{id}/` - 获取服务详情
- `PUT /api/services/{id}/` - 更新服务
- `DELETE /api/services/{id}/` - 删除服务

### 阿姨信息接口

- `GET /api/aunts/` - 获取阿姨列表（支持分页）
  - 参数：
    - `status=available/busy/rest` - 按状态筛选
    - `service_id=xx` - 按技能筛选
    - `name=xxx` - 按姓名模糊搜索
    - `gender=male/female` - 按性别筛选
    - `min_age=xx` - 最小年龄
    - `max_age=xx` - 最大年龄
    - `min_experience=xx` - 最小工作年限
    - `min_rating=xx` - 最低评分
    - `page=1` - 页码
    - `page_size=10` - 每页数量
- `POST /api/aunts/` - 创建阿姨
  - 必填校验：name, phone, id_card, age
  - 格式校验：手机号(11位)、身份证号格式
  - 年龄限制：18-70岁
- `GET /api/aunts/{id}/` - 获取阿姨详情
- `PUT /api/aunts/{id}/` - 更新阿姨
- `DELETE /api/aunts/{id}/` - 删除阿姨

### 订单接口

- `GET /api/orders/` - 获取订单列表（支持分页和统计）
  - 参数（支持多条件组合筛选）：
    - `status=pending/servicing/completed/cancelled` - 订单状态
    - `aunt_id=xx` - 按服务阿姨筛选
    - `customer_name=xxx` - 按客户姓名模糊搜索
    - `customer_phone=xxx` - 按客户电话模糊搜索
    - `service_id=xx` - 按服务类型筛选
    - `start_date=YYYY-MM-DD` - 服务开始日期
    - `end_date=YYYY-MM-DD` - 服务结束日期
    - `order_no=xxx` - 按订单号搜索
    - `page=1` - 页码
    - `page_size=10` - 每页数量
  - 返回包含统计信息：订单总数、总金额、各状态数量
- `GET /api/orders/statistics/` - 获取订单全局统计
  - 返回总统计和今日统计数据
- `POST /api/orders/` - 创建订单（下单）
  - 必填校验：customer_name, customer_phone, customer_address, service, service_date, service_time, duration
  - 格式校验：手机号格式
  - 金额校验：自动计算总价，校验金额正确性
  - 日期校验：服务日期不能早于今天
- `GET /api/orders/{id}/` - 获取订单详情
- `POST /api/orders/{id}/dispatch/` - 派单
  - 请求体：`{"aunt_id": 1}`
  - 派单冲突校验：阿姨不能同时有多个进行中订单
  - 时间冲突校验：检查阿姨同一时间段是否已有订单
- `POST /api/orders/{id}/update_status/` - 更新订单状态
  - 请求体：`{"status": "completed"}`

### 评价接口

- `GET /api/reviews/` - 获取评价列表（支持分页）
  - 参数：
    - `aunt_id=xx` - 按阿姨筛选
    - `order_id=xx` - 按订单筛选
    - `min_rating=xx` - 最低评分
    - `max_rating=xx` - 最高评分
    - `page=1` - 页码
    - `page_size=10` - 每页数量
- `POST /api/reviews/` - 创建评价
  - 必填校验：order, aunt, rating
  - 评分范围：1-5星
  - 只能评价已完成的订单
  - 评价的阿姨必须与订单服务阿姨一致
- `GET /api/reviews/{id}/` - 获取评价详情

## 数据模型说明

### 订单状态

- `pending` - 待派单
- `servicing` - 服务中
- `completed` - 已完成
- `cancelled` - 已取消

### 阿姨状态

- `available` - 空闲（可接单）
- `busy` - 服务中
- `rest` - 休息

### 订单号生成规则

`ORD + 时间戳(YYYYMMDDHHMMSS) + 6位随机字符`

例如：`ORD20240115103000A1B2C3`

## 后台管理

访问 http://localhost:8000/admin/ 进入Django后台管理界面，可以管理所有数据。

## 注意事项

1. 确保MySQL服务已启动
2. 派单时会自动将阿姨状态改为"服务中"
3. 订单完成或取消时，阿姨状态会自动变回"空闲"
4. 只有已完成的订单才能评价
5. 评价后会自动更新阿姨的平均评分
6. 派单时有冲突校验：阿姨不能同时服务多个订单
7. 创建订单时自动校验必填字段和数据格式
8. 金额会自动计算并校验正确性
9. 订单列表支持多条件组合筛选，包含统计信息
10. 所有列表接口支持分页，可自定义每页数量

## 技术栈

- Django 4.2.7
- Django REST Framework 3.14.0
- MySQL
- django-cors-headers
