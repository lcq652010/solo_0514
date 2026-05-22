# 车管所自助违章处理终端运维管理系统后端

## 技术栈
- Python 3.x
- Flask 3.0.0
- SQLite

## 安装依赖
```bash
pip install -r requirements.txt
```

## 数据库迁移（如果已有旧版本数据库）
```bash
python migrate_db.py
```

## 运行项目
```bash
python app.py
```

服务将在 http://localhost:5000 启动

---

## 统一接口返回格式

所有 API 接口统一返回以下格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "success": true,
    "timestamp": "2024-05-16 10:30:00",
    "data": {}
}
```

- `code`: HTTP 状态码
- `message`: 操作结果描述
- `success`: 是否成功
- `timestamp`: 响应时间戳
- `data`: 返回数据（可选）

---

## API 接口文档

### 1. 基础数据接口

#### 获取服务大厅列表
- **GET** `/api/service-halls`
- 返回示例：
```json
{
    "code": 200,
    "message": "操作成功",
    "success": true,
    "timestamp": "2024-05-16 10:30:00",
    "data": [
        {"code": "A", "name": "A服务大厅"},
        {"code": "B", "name": "B服务大厅"},
        {"code": "C", "name": "C服务大厅"},
        {"code": "D", "name": "D服务大厅"}
    ]
}
```

#### 获取故障等级列表
- **GET** `/api/fault-levels`
- 返回示例：
```json
{
    "code": 200,
    "message": "操作成功",
    "success": true,
    "timestamp": "2024-05-16 10:30:00",
    "data": [
        {"code": "紧急", "name": "紧急", "description": "系统完全瘫痪，所有业务无法办理"},
        {"code": "严重", "name": "严重", "description": "核心功能故障，主要业务受影响"},
        {"code": "一般", "name": "一般", "description": "部分功能故障，不影响主要业务"},
        {"code": "轻微", "name": "轻微", "description": "轻微问题，不影响业务运行"}
    ]
}
```

#### 获取故障分类列表
- **GET** `/api/fault-categories`

#### 获取优先级列表
- **GET** `/api/priorities`

---

### 2. 设备管理

#### 添加设备
- **POST** `/api/devices`
- 请求体：
```json
{
    "device_code": "DEV001",
    "device_name": "自助违章终端1号",
    "device_model": "HT-2000",
    "communication_protocol": "TCP/IP",
    "service_hall": "A",
    "location": "车管所大厅A区1号窗口",
    "install_date": "2024-01-15",
    "enable_date": "2024-01-20"
}
```

#### 获取设备列表（支持筛选）
- **GET** `/api/devices`
- 查询参数：
  - `service_hall`: 服务大厅（A/B/C/D）
  - `status`: 设备状态（正常、故障、维修中、已修复）
- 示例：`/api/devices?service_hall=A&status=正常`

#### 获取单个设备
- **GET** `/api/devices/{device_id}`

#### 更新设备信息
- **PUT** `/api/devices/{device_id}`

#### 更新设备状态
- **PUT** `/api/devices/{device_id}/status`
- 请求体：
```json
{
    "status": "正常"
}
```

#### 删除设备
- **DELETE** `/api/devices/{device_id}`

---

### 3. 工单管理

#### 故障上报（创建工单）
- **POST** `/api/work-orders`
- 请求体：
```json
{
    "device_id": 1,
    "fault_type": "触摸屏无响应",
    "fault_category": "硬件故障",
    "fault_level": "严重",
    "priority": "高",
    "fault_description": "用户点击屏幕无任何反应，重启后问题依旧，无法办理违章缴费业务",
    "reporter": "张三",
    "reporter_phone": "13800138000"
}
```

#### 获取工单列表（支持多维度筛选）
- **GET** `/api/work-orders`
- 查询参数：
  - `status`: 处理状态（待处理、处理中、已完成）
  - `device_id`: 设备ID
  - `fault_category`: 故障分类
  - `fault_level`: 故障等级（紧急、严重、一般、轻微）
  - `priority`: 优先级（高、中、低）
  - `service_hall`: 服务大厅
  - `handle_user`: 处理人
- 示例：`/api/work-orders?status=待处理&service_hall=A&fault_level=紧急`
- 按优先级从高到低排序

#### 获取单个工单
- **GET** `/api/work-orders/{order_id}`

#### 处理工单
- **PUT** `/api/work-orders/{order_id}/handle`
- 请求体：
```json
{
    "status": "处理中",
    "handle_user": "李工",
    "handle_desc": "正在检查触摸屏硬件，已更换触控模块"
}
```

---

### 4. 运维记录管理

#### 添加运维记录
- **POST** `/api/maintain-records`

#### 获取运维记录列表（支持筛选）
- **GET** `/api/maintain-records`
- 查询参数：
  - `device_id`: 设备ID
  - `service_hall`: 服务大厅

---

### 5. 仪表盘统计

#### 获取统计数据
- **GET** `/api/dashboard`
- 返回数据：
```json
{
    "code": 200,
    "message": "操作成功",
    "success": true,
    "timestamp": "2024-05-16 10:30:00",
    "data": {
        "total_devices": 20,
        "normal_devices": 16,
        "fault_devices": 2,
        "repairing_devices": 2,
        "repaired_devices": 0,
        "online_health_rate": 80.00,
        "pending_orders": 3,
        "processing_orders": 2,
        "completed_orders": 10,
        "priority_distribution": {
            "高": 1,
            "中": 2,
            "低": 0
        },
        "category_distribution": {
            "硬件故障": 2,
            "软件故障": 1,
            "其他": 0
        },
        "level_distribution": {
            "紧急": 1,
            "严重": 1,
            "一般": 1,
            "轻微": 0
        },
        "hall_distribution": [
            {
                "service_hall": "A",
                "total": 5,
                "normal_count": 4,
                "health_rate": 80.00
            },
            {
                "service_hall": "B",
                "total": 5,
                "normal_count": 5,
                "health_rate": 100.00
            }
        ]
    }
}
```

---

## 数据库表结构

### devices（设备表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| device_code | TEXT | 设备编号（唯一） |
| device_name | TEXT | 设备名称 |
| device_model | TEXT | 设备型号 |
| communication_protocol | TEXT | 通信协议 |
| service_hall | TEXT | 服务大厅 |
| location | TEXT | 安装位置 |
| status | TEXT | 设备状态（正常/故障/维修中/已修复） |
| install_date | TEXT | 安装日期 |
| enable_date | TEXT | 启用日期 |
| last_maintain_date | TEXT | 最后维护日期 |
| create_time | TEXT | 创建时间 |
| update_time | TEXT | 更新时间 |

### work_orders（工单表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| order_no | TEXT | 工单编号（唯一，自动生成） |
| device_id | INTEGER | 关联设备ID |
| fault_type | TEXT | 故障类型 |
| fault_category | TEXT | 故障分类（硬件/软件/网络/系统/支付/打印/其他） |
| fault_level | TEXT | 故障等级（紧急/严重/一般/轻微） |
| priority | TEXT | 紧急优先级（高/中/低） |
| fault_description | TEXT | 故障描述 |
| reporter | TEXT | 上报人 |
| reporter_phone | TEXT | 上报人电话 |
| status | TEXT | 工单状态（待处理/处理中/已完成） |
| handle_user | TEXT | 处理人 |
| handle_desc | TEXT | 处理描述 |
| create_time | TEXT | 创建时间 |
| handle_time | TEXT | 处理时间 |

### maintain_records（运维记录表）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| device_id | INTEGER | 关联设备ID |
| maintain_type | TEXT | 维护类型 |
| maintain_desc | TEXT | 维护描述 |
| maintain_user | TEXT | 维护人员 |
| maintain_time | TEXT | 维护时间 |
| create_time | TEXT | 创建时间 |

---

## 核心功能说明

### 1. 多维度筛选
- **设备筛选**：按服务大厅、设备状态筛选
- **工单筛选**：按处理状态、服务大厅、故障分类、故障等级、优先级、处理人等多维度筛选
- **运维记录筛选**：按设备、服务大厅筛选

### 2. 设备在线完好率统计
- 全局在线完好率 = 正常设备数 / 总设备数 × 100%
- 按服务大厅统计各大厅的设备完好率
- 仪表盘实时展示各大厅完好率分布

### 3. 故障等级与优先级
- **故障等级**：紧急 > 严重 > 一般 > 轻微
- **优先级**：高 > 中 > 低
- 工单列表自动按优先级排序，紧急工单优先处理

### 4. 统一接口格式
- 所有接口统一返回格式，便于前端统一处理
- 包含响应时间戳，便于问题追踪
- 明确的成功/失败标识和状态码

---

## 故障分类说明

| 分类 | 说明 | 典型场景 |
|------|------|----------|
| 硬件故障 | 终端硬件设备故障 | 触摸屏、读卡器、打印机、电源等 |
| 软件故障 | 应用程序、操作系统故障 | APP崩溃、系统死机、界面异常等 |
| 网络故障 | 网络连接、通信故障 | 无法连接服务器、网络超时等 |
| 系统故障 | 核心业务系统故障 | 业务系统接口异常、数据同步失败等 |
| 支付故障 | 支付模块故障 | 银联/支付宝/微信支付失败、扫码异常等 |
| 打印故障 | 凭证打印故障 | 票据打印失败、打印格式异常等 |
| 其他 | 其他类型故障 | 未归类的其他问题 |

---

## 优先级与车管业务影响说明

| 优先级 | 业务影响 | 响应要求 |
|--------|----------|----------|
| 高 | 严重影响车管业务办理，终端完全不可用，影响缴费、上牌、违章处理等核心业务 | 2小时内响应，4小时内到场处理 |
| 中 | 部分功能受影响，终端部分业务可办理，非核心功能故障 | 4小时内响应，8小时内到场处理 |
| 低 | 轻微影响，不影响主要业务办理，仅影响辅助功能或界面显示 | 24小时内响应，预约处理 |
