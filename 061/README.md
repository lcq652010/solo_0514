# 运动场馆管理后端系统

基于 Python + Django + MySQL 实现的运动场馆管理后端系统，包含场地信息维护、用户在线预约、入场计时、时段计费、订单结算等功能。

## 功能特性

### 核心功能
- **场地信息维护**: 支持场地类型、场地信息的增删改查
- **用户在线预约**: 用户可查询场地可用性，在线预约场地
- **入场计时**: 支持预约单号扫码/输入入场，自动记录入场时间
- **时段计费**: 按实际使用时长自动计算费用，支持半小时起步
- **订单结算**: 离场时自动结算费用，生成支付记录

### 新增增强功能（V2.0）
- **多维度场地筛选**: 支持按运动类型、场地大小、价格范围、空闲时段筛选
- **单日最长预约时长限制**: 每个场地可设置单日最长预约时长，创建预约时自动校验
- **预约人实名核验**: 支持身份证号核验，入场前必须完成实名核验
- **时段重叠自动检测**: 创建预约时自动检测时段冲突，返回详细冲突信息

### 订单状态
- **待使用 (pending)**: 预约已创建，尚未入场
- **使用中 (in_use)**: 已入场，正在使用
- **已超时 (timeout)**: 超过预约结束时间未使用
- **已完结 (completed)**: 已离场，订单完成

### 核验状态
- **未核验 (unverified)**: 尚未提交实名信息
- **已核验 (verified)**: 实名核验通过
- **核验失败 (failed)**: 实名核验未通过

### 场地大小
- **小型 (small)**: 适合1-2人使用
- **中型 (medium)**: 适合3-6人使用
- **大型 (large)**: 适合7-15人使用
- **超大型 (extra_large)**: 适合15人以上使用

### 支持的运动类型
- badminton: 羽毛球
- basketball: 篮球
- table_tennis: 乒乓球
- tennis: 网球
- swimming: 游泳
- fitness: 健身
- yoga: 瑜伽
- other: 其他

### 其他特性
- 自动生成预约单号 (BK + 日期 + 随机码)
- 自动生成支付单号 (PY + 日期 + 随机码)
- 预约时段冲突检测（返回冲突详情）
- 实时超时检测
- 数据统计看板

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- MySQL 5.7+
- mysqlclient 2.2

## 安装与运行

### 前置准备

1. 安装 Python 3.8+
2. 安装并启动 MySQL 服务
3. 创建数据库 `stadium_db`

```sql
CREATE DATABASE stadium_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 安装步骤

1. 进入项目目录
```bash
cd 061
```

2. 创建虚拟环境（可选）
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库连接

编辑 `.env` 文件，修改数据库配置：
```
DB_NAME=stadium_db
DB_USER=root
DB_PASSWORD=你的密码
DB_HOST=localhost
DB_PORT=3306
```

5. 执行数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

6. 初始化测试数据
```bash
python init_data.py
```

初始化后会创建：
- 管理员账号: `admin` / `admin123`
- 测试用户: `testuser` / `test123`
- 7个场地类型
- 6个测试场地

7. 启动服务
```bash
python manage.py runserver
```

服务启动后访问:
- API 主页: http://127.0.0.1:8000/api/
- 管理后台: http://127.0.0.1:8000/admin/

## API 接口说明

### 场地管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/venues/ | 获取场地列表（支持按状态、类型、运动类型、大小、价格筛选） |
| POST | /api/venues/ | 创建场地 |
| GET | /api/venues/{id}/ | 获取场地详情 |
| PUT | /api/venues/{id}/ | 更新场地 |
| DELETE | /api/venues/{id}/ | 删除场地 |
| GET | /api/venues/{id}/availability/ | 查询场地可用性（支持按日期范围查询） |
| POST | /api/venues/{id}/check_time_slot/ | 检查指定时段是否可用 |
| GET | /api/venues/filter_by_availability/ | 按可用性、运动类型、大小筛选场地 |

### 预约订单
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/bookings/ | 获取预约列表（支持按状态、用户、场地、日期、核验状态筛选） |
| POST | /api/bookings/ | 创建预约（自动检测时段冲突和单日时长限制） |
| GET | /api/bookings/{id}/ | 获取预约详情 |
| PUT | /api/bookings/{id}/ | 更新预约 |
| POST | /api/bookings/verify/ | 实名核验 |
| POST | /api/bookings/check_in/ | 入场（需先完成实名核验） |
| POST | /api/bookings/check_out/ | 离场（自动结算） |
| POST | /api/bookings/{id}/cancel/ | 取消预约 |
| POST | /api/bookings/check_time_conflict/ | 检查时段冲突 |
| GET | /api/bookings/user_daily_hours/ | 查询用户当日已预约时长 |

### 支付管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/payments/ | 获取支付记录 |
| POST | /api/payments/ | 创建支付记录 |
| POST | /api/payments/{id}/confirm_payment/ | 确认支付 |
| POST | /api/payments/{id}/refund/ | 退款 |

### 数据看板
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/dashboard/stats/ | 获取统计数据 |
| GET | /api/dashboard/recent_bookings/ | 获取最近预约 |

## API 使用示例

### 1. 场地筛选查询
```bash
# 按运动类型和场地大小筛选
GET /api/venues/?sport_type=badminton&size=medium

# 按价格范围筛选
GET /api/venues/?min_price=50&max_price=100

# 按可用时段筛选
GET /api/venues/filter_by_availability/?start_time=2026-05-17T10:00:00&end_time=2026-05-17T12:00:00&sport_type=badminton
```

### 2. 检查时段冲突
```bash
POST /api/bookings/check_time_conflict/
{
    "venue_id": 1,
    "start_time": "2026-05-17T10:00:00",
    "end_time": "2026-05-17T12:00:00"
}

# 响应示例：
{
    "is_available": false,
    "overlapping_slots": [
        {
            "booking_no": "BK20260516XXXXXX",
            "start_time": "2026-05-17T09:00:00",
            "end_time": "2026-05-17T11:00:00",
            "contact_name": "李四"
        }
    ]
}
```

### 3. 创建预约（自动检测冲突和时长限制）
```bash
POST /api/bookings/
{
    "user": 1,
    "venue": 1,
    "start_time": "2026-05-17T10:00:00",
    "end_time": "2026-05-17T12:00:00",
    "contact_name": "张三",
    "contact_phone": "13800138000",
    "id_card": "110101199001011234",
    "remarks": ""
}
```

### 4. 实名核验
```bash
POST /api/bookings/verify/
{
    "booking_no": "BK20260516XXXXXX",
    "id_card": "110101199001011234"
}
```

### 5. 查询用户当日预约时长
```bash
GET /api/bookings/user_daily_hours/?user_id=1&date=2026-05-17
```

### 6. 入场（需先完成实名核验）
```bash
POST /api/bookings/check_in/
{
    "booking_no": "BK20260516XXXXXX"
}
```

### 7. 离场（自动结算）
```bash
POST /api/bookings/check_out/
{
    "booking_no": "BK20260516XXXXXX"
}
```

### 8. 确认支付
```bash
POST /api/payments/
{
    "booking": 1,
    "amount": 100.00,
    "payment_method": "wechat"
}

POST /api/payments/{id}/confirm_payment/
```

## 项目结构

```
061/
├── manage.py                    # Django 管理脚本
├── requirements.txt             # 依赖包列表
├── .env                         # 环境变量配置
├── init_data.py                 # 初始化数据脚本
├── README.md                    # 说明文档
├── stadium_management/          # 项目配置目录
│   ├── __init__.py
│   ├── settings.py              # 项目设置
│   ├── urls.py                  # 主路由
│   ├── asgi.py
│   └── wsgi.py
└── stadium/                     # 应用目录
    ├── __init__.py
    ├── apps.py
    ├── models.py                # 数据模型
    ├── serializers.py           # 序列化器
    ├── views.py                 # 视图
    ├── urls.py                  # 路由
    └── admin.py                 # 后台管理
```

## 数据模型说明

### VenueType (场地类型)
- name: 类型名称
- sport_type: 运动类型
- description: 描述

### Venue (场地)
- name: 场地名称
- venue_type: 场地类型
- code: 场地编号
- size: 场地大小 (small/medium/large/extra_large)
- capacity: 容纳人数（团体预约校验依据）
- area: 场地面积(㎡)
- max_booking_hours_per_day: 单日最长预约时长(小时)
- min_billing_minutes: 最低计费时长(分钟)，默认30分钟
- status: 状态 (available/maintenance/closed)
- price_per_hour: 每小时价格
- qr_code: 场地二维码
- description: 描述

### Booking (预约订单)
- booking_no: 预约单号（自动生成）
- user: 用户
- venue: 场地
- booking_type: 预约类型 (individual个人/group团体)
- people_count: 预约人数（自动校验场地人数上限）
- start_time/end_time: 预约起止时间
- actual_start_time/actual_end_time: 实际入场离场时间
- actual_duration_minutes: 实际使用时长(分钟)
- billing_duration_minutes: 计费时长(分钟)（含最低时长）
- status: 订单状态
- total_amount: 总金额（自动计算）
- contact_name/contact_phone: 联系人信息
- id_card: 身份证号
- verification_status: 核验状态 (unverified/verified/failed)
- verification_time: 核验时间
- check_in_method: 入场方式 (scan扫码/manual手动)
- check_out_method: 离场方式 (scan扫码/manual手动)

### Payment (支付记录)
- payment_no: 支付单号（自动生成）
- booking: 关联预约
- amount: 支付金额
- status: 支付状态
- payment_method: 支付方式
- paid_at: 支付时间
- transaction_id: 交易流水号

## 核心增强功能说明

### 1. 扫码入场自动计时
- 支持扫描场地二维码入场/离场
- 入场时自动记录开始时间
- 离场时自动计算使用时长
- 支持扫码自动识别当前预约
- 记录入场/离场操作方式

### 2. 离场自动停止计费
- 离场时立即停止计费
- 精确计算实际使用时长（分钟级）
- 自动计算费用并更新订单
- 返回详细的计费明细

### 3. 超短时长按最低标准计费
- 每个场地可独立设置最低计费时长
- 默认最低计费30分钟
- 实际使用时长低于最低标准时按最低标准计费
- 计费结果中明确标记是否使用最低标准
- 支持灵活配置不同场地的最低计费时长

### 4. 团体预约自动匹配人数上限
- 支持个人预约和团体预约两种类型
- 创建预约时自动校验预约人数是否超出场地容量
- 超出容量时返回明确错误提示
- 支持团体优惠计算框架（可扩展具体折扣规则）
- 实时显示当前预约人数和场地最大容量

### 5. 实时费用查询
- 可随时查询正在使用订单的当前费用
- 显示已使用时长、计费时长、当前预估金额
- 提前告知是否将触发最低计费

## 注意事项

1. 确保 MySQL 服务已启动
2. 确保数据库字符集为 utf8mb4
3. 预约时间不能早于当前时间
4. 结束时间必须晚于开始时间
5. 单次预约时长最少30分钟，最多8小时
6. 单日预约时长不能超过场地设置的上限
7. 只能取消"待使用"状态的预约
8. 入场前必须先完成实名核验
9. 入场操作只能对"待使用"状态的预约执行
10. 离场操作只能对"使用中"状态的预约执行
11. 计费按实际使用时长，不足最低计费时长按最低标准计算
12. 团体预约人数不能超过场地最大容纳人数

## 开发说明

本项目已完整实现所有要求功能，代码可直接运行。如需二次开发，可根据实际业务需求扩展：
- 添加用户认证权限控制
- 集成微信/支付宝支付
- 添加消息通知功能（微信/短信通知入场、计费提醒）
- 开发前端界面（含扫码功能）
- 完善团体优惠具体规则
- 添加更多计费模式（包场、按次计费等）
- 集成电子发票系统
