# 宠物寄养平台后端

基于 Python + Django + MySQL 实现的宠物寄养平台 RESTful API 后端服务。

## 功能特性

- 宠物信息登记管理（含疫苗有效期自动校验、体型分类）
- 寄养房间分配管理（含容量上限控制、体型自动匹配、自动分配房间）
- 每日喂食记录管理（支持批量导入）
- 寄养费用自动计算（含超时费用自动核算）
- 离店结算功能
- 订单状态管理（待入住、照料中、待接走、已完成、已取消）
- 自动生成寄养单号
- 多维度筛选功能（宠物品种、体型、寄养时长、房间类型等）
- 分页支持和异常数据过滤
- 疫苗过期预警
- 寄养到期前自动提醒查询接口
- 管理后台批量操作支持

## 环境要求

- Python 3.8+
- MySQL 5.7+ 或 8.0+

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 创建数据库

首先确保 MySQL 服务已启动，然后执行：

```bash
python init_db.py
```

默认数据库配置：
- 数据库名: pet_fostering
- 用户名: root
- 密码: 123456

如需修改，请编辑 `pet_fostering/settings.py` 中的 DATABASES 配置。

### 3. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 初始化房间数据

```bash
python init_data.py
```

### 5. 创建超级管理员（可选）

```bash
python manage.py createsuperuser
```

### 6. 启动服务

```bash
python manage.py runserver
```

服务启动后，访问以下地址：
- API 文档: http://127.0.0.1:8000/api/
- 管理后台: http://127.0.0.1:8000/admin/

## API 接口说明

### 宠物管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/pets/ | 获取宠物列表（支持筛选和分页） |
| POST | /api/pets/ | 创建宠物信息 |
| GET | /api/pets/{id}/ | 获取宠物详情 |
| PUT | /api/pets/{id}/ | 更新宠物信息 |
| DELETE | /api/pets/{id}/ | 删除宠物信息 |

**宠物筛选参数：**
- `species`: 宠物种类 (dog/cat/other)
- `size`: 宠物体型 (small/medium/large)
- `breed`: 品种（模糊搜索）
- `min_age`: 最小年龄
- `max_age`: 最大年龄
- `owner_name`: 主人姓名
- `vaccine_warning`: 疫苗即将过期预警（7天内）
- `search`: 关键词搜索
- `ordering`: 排序字段

### 房间管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/rooms/ | 获取房间列表（支持筛选和分页） |
| POST | /api/rooms/ | 创建房间 |
| GET | /api/rooms/available/ | 获取空闲房间列表 |
| GET | /api/rooms/with_capacity/ | 获取尚有容量的房间列表 |
| GET | /api/rooms/suitable_for_pet/ | 获取适合指定宠物的房间列表 |

**房间筛选参数：**
- `room_type`: 房间类型 (standard/deluxe/vip)
- `suitable_size`: 适用体型 (small/small_medium/all)
- `status`: 房间状态
- `min_price`: 最低日租金
- `max_price`: 最高日租金
- `pet_id`: 查询适合指定宠物的房间
- `search`: 关键词搜索
- `ordering`: 排序字段

### 订单管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/orders/ | 获取订单列表（支持筛选和分页） |
| POST | /api/orders/ | 创建订单 |
| GET | /api/orders/{id}/ | 获取订单详情 |
| POST | /api/orders/{id}/checkin/ | 宠物入住（校验疫苗和房间容量） |
| POST | /api/orders/{id}/checkout/ | 宠物离店结算（自动计算超时费用） |
| POST | /api/orders/{id}/complete/ | 完成订单 |
| POST | /api/orders/{id}/cancel/ | 取消订单 |
| POST | /api/orders/{id}/auto_assign_room/ | 自动分配房间 |
| GET | /api/orders/pending_checkin/ | 待入住订单 |
| GET | /api/orders/in_care/ | 照料中订单 |
| GET | /api/orders/pending_pickup/ | 待接走订单 |
| GET | /api/orders/completed/ | 已完成订单 |
| GET | /api/orders/needing_reminder/ | 寄养即将到期需要提醒的订单 |
| POST | /api/orders/{id}/mark_reminder/ | 标记提醒状态 |

**订单筛选参数：**
- `status`: 订单状态
- `room_type`: 房间类型
- `pet_species`: 宠物种类
- `pet_size`: 宠物体型
- `pet_breed`: 宠物品种（模糊搜索）
- `min_expected_days`: 最小预计寄养天数
- `max_expected_days`: 最大预计寄养天数
- `min_stay_days`: 最小实际寄养天数
- `max_stay_days`: 最大实际寄养天数
- `checkin_date_from`: 入住开始日期
- `checkin_date_to`: 入住结束日期
- `expected_checkout_date_from`: 预计离店开始日期
- `expected_checkout_date_to`: 预计离店结束日期
- `days`: 到期前N天的订单（仅用于needing_reminder接口）
- `search`: 关键词搜索
- `ordering`: 排序字段

### 喂食记录管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/feeding-records/ | 获取喂食记录列表（支持筛选和分页） |
| POST | /api/feeding-records/ | 创建喂食记录 |
| POST | /api/feeding-records/batch_import/ | 批量导入喂食记录 |
| GET | /api/feeding-records/?order_id={id} | 获取指定订单的喂食记录 |

**喂食记录筛选参数：**
- `order_id`: 订单ID
- `record_date_from`: 记录开始日期
- `record_date_to`: 记录结束日期
- `created_by`: 创建人
- `search`: 关键词搜索
- `ordering`: 排序字段

**批量导入请求格式：**
```json
{
  "order_id": 1,
  "records": [
    {
      "record_date": "2024-01-15",
      "morning_feeding": true,
      "morning_notes": "食欲良好",
      "afternoon_feeding": true,
      "evening_feeding": false,
      "health_notes": "精神良好",
      "created_by": "李护士"
    }
  ]
}
```

## 订单状态流转

```
待入住 (pending_checkin)
    ↓ (调用 checkin 接口)
照料中 (in_care)
    ↓ (调用 checkout 接口)
待接走 (pending_pickup)
    ↓ (调用 complete 接口)
已完成 (completed)

(可取消状态: 待入住、待接走)
```

## 核心校验规则

### 疫苗有效期校验
- 入住时自动校验宠物疫苗是否在有效期内
- 疫苗过期前7天自动预警
- 未设置疫苗有效期禁止入住

### 房间容量控制
- 入住时校验房间是否还有剩余容量
- 自动更新房间当前宠物数量
- 达到容量上限时房间自动变更为"已占用"状态
- 宠物离店后自动释放容量

### 宠物体型与房间匹配校验
- 房间支持按体型分类配置（小型/中小型/全体型）
- 入住时自动校验房间是否适合该体型宠物
- 自动分配房间功能自动匹配合适房型

### 超时费用自动核算
- 离店时自动计算实际寄养天数
- 超过预计寄养天数按超时倍率自动计算超时费用
- 费用明细自动分为基础费用和超时费用

### 数据完整性校验
- 年龄、体重、寄养天数必须大于0
- 离店日期不能早于入住日期
- 喂食记录日期不能晚于今天
- 超时费率必须大于等于1

## 使用示例

### 1. 创建宠物信息（含体型）

```bash
curl -X POST http://127.0.0.1:8000/api/pets/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "旺财",
    "species": "dog",
    "size": "large",
    "breed": "金毛",
    "age": 3,
    "weight": 25.5,
    "owner_name": "张三",
    "owner_phone": "13800138000",
    "vaccine_expiry": "2025-06-15",
    "health_status": "健康",
    "special_requirements": "喜欢玩球"
  }'
```

### 2. 创建支持体型匹配的房间

```bash
curl -X POST http://127.0.0.1:8000/api/rooms/ \
  -H "Content-Type: application/json" \
  -d '{
    "room_number": "VIP001",
    "room_type": "vip",
    "suitable_size": "all",
    "daily_price": 200,
    "overtime_multiplier": 1.5,
    "status": "available",
    "max_pets": 2,
    "description": "豪华VIP套房，适合所有体型宠物"
  }'
```

### 3. 创建寄养订单（自动计算预计离店日期）

```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -d '{
    "pet": 1,
    "room": 1,
    "checkin_date": "2024-01-15T09:00:00",
    "expected_checkout_date": "2024-01-22T09:00:00",
    "expected_days": 7,
    "daily_price": 80
  }'
```

### 4. 自动分配房间

```bash
curl -X POST http://127.0.0.1:8000/api/orders/1/auto_assign_room/
```

### 5. 宠物入住（自动校验疫苗、房间容量、体型匹配）

```bash
curl -X POST http://127.0.0.1:8000/api/orders/1/checkin/
```

### 6. 查询适合指定宠物的房间

```bash
curl "http://127.0.0.1:8000/api/rooms/suitable_for_pet/?pet_id=1"
```

### 7. 按条件筛选订单

```bash
# 按宠物体型筛选
curl "http://127.0.0.1:8000/api/orders/?pet_size=large"

# 按房间类型筛选
curl "http://127.0.0.1:8000/api/orders/?room_type=vip"

# 按宠物品种筛选
curl "http://127.0.0.1:8000/api/orders/?pet_breed=金毛"

# 按寄养天数筛选
curl "http://127.0.0.1:8000/api/orders/?min_stay_days=3&max_stay_days=10"

# 组合筛选
curl "http://127.0.0.1:8000/api/orders/?status=in_care&room_type=standard"
```

### 8. 查询即将到期需要提醒的订单

```bash
# 到期前3天的订单
curl "http://127.0.0.1:8000/api/orders/needing_reminder/?days=3"

# 标记提醒已发送
curl -X POST http://127.0.0.1:8000/api/orders/1/mark_reminder/ \
  -H "Content-Type: application/json" \
  -d '{"status": "sent"}'
```

### 9. 批量导入喂食记录

```bash
curl -X POST http://127.0.0.1:8000/api/feeding-records/batch_import/ \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": 1,
    "records": [
      {
        "record_date": "2024-01-15",
        "morning_feeding": true,
        "morning_notes": "食欲良好",
        "afternoon_feeding": true,
        "evening_feeding": true,
        "health_notes": "精神状态良好",
        "created_by": "李护士"
      },
      {
        "record_date": "2024-01-16",
        "morning_feeding": true,
        "afternoon_feeding": true,
        "evening_feeding": true,
        "health_notes": "一切正常",
        "created_by": "王护士"
      }
    ]
  }'
```

### 10. 离店结算（自动计算超时费用）

```bash
curl -X POST http://127.0.0.1:8000/api/orders/1/checkout/
```

返回结果包含费用明细：
```json
{
  "order_no": "F20240115XXXX",
  "expected_days": 7,
  "actual_days": 10,
  "overtime_days": 3,
  "base_amount": 560.00,
  "overtime_amount": 360.00,
  "total_amount": 920.00
}
```

### 11. 完成订单

```bash
curl -X POST http://127.0.0.1:8000/api/orders/1/complete/
```

## 管理后台功能

宠物寄养平台管理后台支持丰富的批量操作：
- 批量办理入住
- 批量办理离店结算
- 批量完成订单
- 批量取消订单
- 批量自动分配房间
- 批量标记提醒已发送
- 实时显示疫苗状态
- 实时显示房间可用容量
- 费用明细展示（基础费用/超时费用）
- 提醒状态管理
