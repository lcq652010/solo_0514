# 机场自助行李托运机运维管理系统 v3.0 - API文档

## 版本更新说明

### v3.0 新增功能

| 功能模块 | 新增特性 |
|---------|---------|
| **设备模块** | 增加航站楼、值机岛字段 |
| **故障模块** | 增加故障等级字段（轻微/一般/严重/致命） |
| **设备工单联动** | 设备详情接口自动关联工单列表 |
| **维修日志增强** | 增加维修工时、更换配件记录 |
| **多维度筛选** | 支持按航站楼、值机岛、故障等级筛选 |
| **优先级排序** | 工单按优先级自动排序，紧急工单优先 |
| **统一接口格式** | 标准响应格式、统一分页封装 |
| **设备完好率** | 全局及按航站楼设备完好率统计 |

---

## 快速开始

### 启动服务

```bash
# 数据库迁移（从旧版本升级）
python migrate_db.py

# 启动服务
python app.py
```

服务地址: http://localhost:5000

---

## 统一响应格式

### 成功响应

```json
{
  "code": 200,
  "message": "操作成功",
  "data": { ... },
  "timestamp": "2024-05-15T10:30:00.000000"
}
```

### 错误响应

```json
{
  "code": 400,
  "message": "错误信息",
  "data": null,
  "timestamp": "2024-05-15T10:30:00.000000"
}
```

### 分页格式

```json
{
  "list": [...],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10,
    "has_next": true,
    "has_prev": false
  }
}
```

---

## API 接口列表

### 1. 设备管理

#### 1.1 设备录入
- **接口**: `POST /api/devices`
- **说明**: 录入新设备，支持航站楼、值机岛字段

**请求体**:
```json
{
  "device_code": "BAG-T1-A001",
  "device_name": "T1航站楼A区1号托运机",
  "device_model": "BAG-2024-PRO",
  "communication_mode": "5G",
  "terminal": "T1",
  "checkin_island": "A岛",
  "location": "T1航站楼A区1号机位",
  "install_date": "2024-01-15",
  "activation_date": "2024-02-01",
  "operator": "管理员"
}
```

**字段说明**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| device_code | string | 是 | 设备编号，唯一标识 |
| device_name | string | 是 | 设备名称 |
| device_model | string | 否 | 设备型号 |
| communication_mode | string | 否 | 通信方式（5G/WiFi/有线） |
| terminal | string | 否 | 所属航站楼 |
| checkin_island | string | 否 | 所属值机岛 |
| location | string | 是 | 具体位置 |
| install_date | string | 是 | 安装日期 (YYYY-MM-DD) |
| activation_date | string | 否 | 启用日期 (YYYY-MM-DD) |
| operator | string | 否 | 操作人 |

---

#### 1.2 设备列表查询
- **接口**: `GET /api/devices`
- **说明**: 查询设备列表，支持多维度筛选

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认1 |
| per_page | int | 每页数量，默认10 |
| status | string | 设备状态（正常/故障/维修中/已修复） |
| terminal | string | 按航站楼筛选 |
| checkin_island | string | 按值机岛筛选 |
| device_model | string | 按型号模糊搜索 |
| communication_mode | string | 按通信方式筛选 |

**示例**:
```
GET /api/devices?terminal=T1&checkin_island=A岛&status=正常
```

---

#### 1.3 设备详情查询（含关联工单）
- **接口**: `GET /api/devices/{device_id}`
- **说明**: 查询单个设备详情，自动关联该设备的工单列表和运维记录数

**响应数据包含**:
- 设备基本信息（航站楼、值机岛等）
- work_orders: 该设备关联的工单列表（最近5条）
- maintenance_count: 运维记录总数

---

#### 1.4 更新设备信息
- **接口**: `PUT /api/devices/{device_id}`
- **说明**: 更新设备的基本信息

**请求体**（支持部分更新）:
```json
{
  "device_name": "更新后的设备名称",
  "terminal": "T2",
  "checkin_island": "B岛"
}
```

---

#### 1.5 更新设备状态
- **接口**: `PUT /api/devices/{device_id}/status`
- **说明**: 更新设备运行状态

**请求体**:
```json
{
  "status": "维修中",
  "operator": "张工程师"
}
```

---

### 2. 工单管理

#### 2.1 故障上报
- **接口**: `POST /api/work-orders`
- **说明**: 上报设备故障，支持优先级和故障等级

**请求体**:
```json
{
  "device_code": "BAG-T1-A001",
  "fault_type": "硬件故障",
  "priority": "紧急",
  "fault_level": "严重",
  "fault_description": "行李传送带电机烧坏，影响航班出港",
  "reporter": "李操作员"
}
```

**字段说明**:
| 字段 | 类型 | 必填 | 可选值 |
|------|------|------|--------|
| fault_type | string | 否 | 硬件故障/软件故障/通信故障/机械故障/传感器故障/电源故障/其他（默认） |
| priority | string | 否 | 紧急/高/普通（默认）/低 |
| fault_level | string | 否 | 轻微/一般（默认）/严重/致命 |

**优先级说明**:
- **紧急**: 严重影响航班运行，需立即处理
- **高**: 影响较大，需优先处理
- **普通**: 常规故障，按正常流程处理
- **低**: 不影响正常使用，可延后处理

---

#### 2.2 工单列表查询
- **接口**: `GET /api/work-orders`
- **说明**: 查询工单列表，支持多维度筛选，**按优先级自动排序**

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| per_page | int | 每页数量 |
| status | string | 工单状态（待处理/处理中/已完成） |
| priority | string | 按优先级筛选 |
| fault_type | string | 按故障类型筛选 |
| fault_level | string | 按故障等级筛选 |
| terminal | string | 按航站楼筛选 |
| checkin_island | string | 按值机岛筛选 |
| device_code | string | 按设备编号搜索 |

**排序规则**:
1. 优先级降序（紧急 > 高 > 普通 > 低）
2. 同优先级按上报时间降序

---

#### 2.3 工单详情查询
- **接口**: `GET /api/work-orders/{order_no}`
- **说明**: 查询单个工单的详细信息

---

#### 2.4 处理工单
- **接口**: `PUT /api/work-orders/{order_no}/handle`
- **说明**: 处理工单，支持记录维修工时和更换的配件

**请求体**:
```json
{
  "handler": "王工程师",
  "handle_result": "已更换传送带电机，设备恢复正常",
  "action": "修复完成",
  "duration": 45,
  "parts_used": "传送带电机x1,传动带x1,轴承x2"
}
```

**字段说明**:
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| handler | string | 是 | 处理人 |
| handle_result | string | 是 | 处理结果说明 |
| action | string | 否 | 操作类型（开始维修/修复完成） |
| duration | int | 否 | 维修工时（分钟） |
| parts_used | string | 否 | 更换的配件清单 |

---

### 3. 运维记录

#### 3.1 运维记录查询
- **接口**: `GET /api/maintenance-records`
- **说明**: 查询运维记录列表，支持多维度筛选

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码 |
| per_page | int | 每页数量 |
| record_type | string | 记录类型（设备录入/状态变更/故障上报/运维处理） |
| fault_type | string | 故障类型 |
| fault_level | string | 故障等级 |
| terminal | string | 按航站楼筛选 |
| checkin_island | string | 按值机岛筛选 |
| device_code | string | 按设备编号搜索 |

---

### 4. 统计分析

#### 4.1 综合统计面板
- **接口**: `GET /api/dashboard/statistics`
- **说明**: 获取系统综合统计数据

**返回数据包含**:
```json
{
  "device_statistics": {
    "total": 50,
    "normal": 45,
    "fault": 3,
    "repairing": 2,
    "repaired": 47,
    "availability_rate": 94.0
  },
  "work_order_statistics": {
    "pending": 5,
    "processing": 3,
    "completed": 100,
    "urgent_pending": 1,
    "high_priority_pending": 2,
    "today_reported": 8,
    "today_completed": 6
  },
  "maintenance_statistics": {
    "total_records": 200,
    "avg_repair_duration": 38.5
  },
  "fault_type_statistics": {
    "硬件故障": 45,
    "软件故障": 30,
    "通信故障": 15
  },
  "terminal_statistics": {
    "T1": {
      "total": 25,
      "normal": 23,
      "availability_rate": 92.0
    },
    "T2": {
      "total": 25,
      "normal": 24,
      "availability_rate": 96.0
    }
  }
}
```

---

#### 4.2 设备完好率统计
- **接口**: `GET /api/devices/availability-rate`
- **说明**: 查询设备完好率，支持按航站楼、值机岛筛选

**查询参数**:
| 参数 | 类型 | 说明 |
|------|------|------|
| terminal | string | 按航站楼筛选 |
| checkin_island | string | 按值机岛筛选 |

**返回数据**:
```json
{
  "total_devices": 50,
  "available_devices": 47,
  "availability_rate": 94.0,
  "terminal": "T1",
  "checkin_island": "A岛"
}
```

**完好率计算公式**:
```
完好率 = (正常设备数 + 已修复设备数) / 总设备数 * 100%
```

---

## 数据字典

### 设备状态
| 状态 | 说明 |
|------|------|
| 正常 | 设备正常运行 |
| 故障 | 设备出现故障，待处理 |
| 维修中 | 设备正在维修 |
| 已修复 | 故障已修复，可正常使用 |

### 工单状态
| 状态 | 说明 |
|------|------|
| 待处理 | 已上报，未派工 |
| 处理中 | 维修人员正在处理 |
| 已完成 | 工单处理完毕 |

### 故障等级
| 等级 | 说明 |
|------|------|
| 轻微 | 不影响使用，可延后处理 |
| 一般 | 部分功能受限，正常处理 |
| 严重 | 核心功能受影响，需尽快处理 |
| 致命 | 完全无法使用，严重影响运行 |

---

## 测试工具

运行测试脚本验证所有功能:

```bash
python test_v3.py
```

---

## 升级指南

### 从 v2.0 升级到 v3.0

```bash
# 1. 数据库迁移（添加新字段）
python migrate_db.py

# 2. 启动服务
python app.py

# 3. 验证功能（可选）
python test_v3.py
```

### 数据库变更内容

| 表名 | 新增字段 |
|------|---------|
| devices | terminal, checkin_island |
| work_orders | fault_level, repair_duration, parts_used |
| maintenance_records | work_order_no, fault_type, fault_level, duration, parts_used |

---

## 联系与支持

如有问题，请查看代码注释或运行测试脚本进行验证。
