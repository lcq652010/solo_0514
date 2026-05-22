# 地铁自动售票机运维系统后端

基于 Python + Flask + SQLite 实现的地铁自动售票机运维管理系统后端。

## 功能特性

- ✅ 设备基础信息录入、修改、查询
- ✅ 故障上报与工单管理
- ✅ 设备状态管理（正常、故障、停用）
- ✅ 工单自动编号
- ✅ 多条件查询功能
- ✅ 统计数据接口

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动，数据库会自动创建。

## API 接口文档

### 设备管理接口

#### 1. 添加设备

**POST** `/api/devices`

请求体：
```json
{
    "device_id": "TVM001",
    "device_name": "自动售票机1号",
    "location": "A口",
    "station": "天安门东站",
    "device_serial": "SN20240001",
    "production_date": "2024-01-15",
    "status": "正常",
    "install_date": "2024-01-20",
    "manufacturer": "ABC公司",
    "model": "TVM-2024"
}
```

必填字段：`device_id`, `device_name`, `location`, `station`

可选字段：`device_serial`（设备序列号）, `production_date`（投产日期）, `status`（默认：正常）, `install_date`, `manufacturer`, `model`

#### 2. 查询设备列表

**GET** `/api/devices`

支持查询参数：
- `status`: 按状态筛选（正常、故障、停用）
- `station`: 按站点模糊搜索
- `device_id`: 按设备ID模糊搜索

示例：
```
GET /api/devices?status=故障&station=天安门
GET /api/devices?device_id=TVM001
```

#### 3. 查询单个设备

**GET** `/api/devices/<device_id>`

#### 4. 更新设备信息

**PUT** `/api/devices/<device_id>`

请求体（可更新任意字段）：
```json
{
    "status": "停用",
    "location": "B口"
}
```

### 工单管理接口

#### 1. 创建工单（故障上报）

**POST** `/api/workorders`

请求体：
```json
{
    "device_id": "TVM001",
    "fault_type": "卡币",
    "fault_description": "硬币卡住在找零口",
    "reporter": "张三",
    "contact": "13800138000"
}
```

必填字段：`device_id`, `fault_type`

预设故障类型：`卡票`、`卡币`、`不找零`、`无法支付`

系统会自动：
- 生成工单号（格式：WO + 日期 + 4位序号）
- 自动将设备状态设为"故障"

#### 2. 查询工单列表

**GET** `/api/workorders`

支持查询参数：
- `status`: 按状态筛选（待处理、处理中、已完成）
- `device_id`: 按设备ID筛选
- `station`: 按站点模糊筛选

示例：
```
GET /api/workorders?station=天安门
GET /api/workorders?status=待处理&station=西单
```

#### 3. 获取故障类型列表

**GET** `/api/fault-types`

返回预设的故障类型列表：
```json
["卡票", "卡币", "不找零", "无法支付"]
```

#### 4. 处理工单

**PUT** `/api/workorders/<order_id>`

请求体：
```json
{
    "status": "处理中",
    "handle_result": "正在更换纸币识别模块"
}
```

当状态设为"已完成"时，系统会自动将对应设备状态恢复为"正常"。

### 统计接口

#### 获取统计数据

**GET** `/api/dashboard/stats`

返回示例：
```json
{
    "total_devices": 10,
    "normal_devices": 7,
    "fault_devices": 2,
    "disabled_devices": 1,
    "pending_orders": 3,
    "processing_orders": 1
}
```

## 数据库结构

### devices 表（设备表）

| 字段 | 类型 | 说明 |
|------|------|------|
| device_id | TEXT | 设备ID（主键） |
| device_name | TEXT | 设备名称 |
| location | TEXT | 位置 |
| station | TEXT | 所属站点 |
| device_serial | TEXT | 设备序列号 |
| production_date | TEXT | 投产日期 |
| status | TEXT | 状态（正常、故障、停用） |
| install_date | TEXT | 安装日期 |
| manufacturer | TEXT | 厂商 |
| model | TEXT | 型号 |
| create_time | TEXT | 创建时间 |
| update_time | TEXT | 更新时间 |

### work_orders 表（工单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| order_id | TEXT | 工单号（主键） |
| device_id | TEXT | 设备ID（外键） |
| fault_type | TEXT | 故障类型 |
| fault_description | TEXT | 故障描述 |
| reporter | TEXT | 上报人 |
| contact | TEXT | 联系方式 |
| status | TEXT | 状态（待处理、处理中、已完成） |
| report_time | TEXT | 上报时间 |
| fault_hour | INTEGER | 故障发生小时（0-23） |
| period_type | TEXT | 时段类型（高峰/平峰） |
| handle_time | TEXT | 处理时间 |
| handle_result | TEXT | 处理结果 |

## 状态说明

### 设备状态
- **正常**: 设备运行正常
- **故障**: 设备存在故障，待维修
- **停用**: 设备已停用

### 工单状态
- **待处理**: 工单已创建，等待处理
- **处理中**: 工单正在处理
- **已完成**: 工单已处理完成

### 时段类型
- **高峰**: 早高峰(7:00-9:00)、晚高峰(17:00-19:00)
- **平峰**: 其他时段

### 统计接口

#### 1. 故障类型频次统计

**GET** `/api/stats/fault-type-frequency`

查询参数：
- `start_date`: 开始日期（格式：YYYY-MM-DD），可选
- `end_date`: 结束日期（格式：YYYY-MM-DD），可选

返回示例：
```json
[
    {"fault_type": "卡票", "count": 15},
    {"fault_type": "卡币", "count": 10},
    {"fault_type": "无法支付", "count": 8},
    {"fault_type": "不找零", "count": 5}
]
```

#### 2. 高峰/平峰时段统计

**GET** `/api/stats/period-type`

查询参数：
- `start_date`: 开始日期（格式：YYYY-MM-DD），可选
- `end_date`: 结束日期（格式：YYYY-MM-DD），可选

返回示例：
```json
{
    "period_stats": {
        "高峰": 28,
        "平峰": 10
    },
    "hour_distribution": [
        {"hour": 7, "count": 5},
        {"hour": 8, "count": 12},
        {"hour": 9, "count": 8},
        {"hour": 17, "count": 3}
    ]
}
```

#### 3. 设备月度故障次数排行

**GET** `/api/stats/device-monthly-rank`

查询参数：
- `year`: 年份，可选（默认当前年份）
- `month`: 月份，可选（默认当前月份）
- `top_n`: 返回前N名，可选（默认10）

返回示例：
```json
{
    "year": 2026,
    "month": 5,
    "ranking": [
        {"rank": 1, "device_id": "TVM001", "device_name": "自动售票机1号", "station": "天安门东站", "fault_count": 8},
        {"rank": 2, "device_id": "TVM003", "device_name": "自动售票机3号", "station": "西单站", "fault_count": 5},
        {"rank": 3, "device_id": "TVM002", "device_name": "自动售票机2号", "station": "天安门东站", "fault_count": 3}
    ]
}
```

## 测试示例

使用 curl 测试接口：

```bash
# 添加设备
curl -X POST http://localhost:5000/api/devices \
  -H "Content-Type: application/json" \
  -d '{"device_id":"TVM001","device_name":"售票机1号","location":"A口","station":"天安门东站"}'

# 查询所有设备
curl http://localhost:5000/api/devices

# 创建工单
curl -X POST http://localhost:5000/api/workorders \
  -H "Content-Type: application/json" \
  -d '{"device_id":"TVM001","fault_type":"纸币模块故障","reporter":"张三"}'

# 查询所有工单
curl http://localhost:5000/api/workorders

# 获取统计数据
curl http://localhost:5000/api/dashboard/stats
```
