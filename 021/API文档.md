# 政务不动产自助打证终端运维管理系统 API 文档

## 基础信息
- 服务器地址: `http://localhost:5000`
- API 前缀: `/api`
- 数据格式: JSON

## 统一响应格式

### 成功响应
```json
{
  "code": 200,
  "success": true,
  "message": "操作成功",
  "data": { ... },
  "timestamp": "2024-05-16T10:00:00.000000"
}
```

### 失败响应
```json
{
  "code": 400,
  "success": false,
  "message": "错误信息",
  "errors": null,
  "timestamp": "2024-05-16T10:00:00.000000"
}
```

### 列表分页响应
```json
{
  "code": 200,
  "success": true,
  "message": "操作成功",
  "data": {
    "list": [ ... ],
    "pagination": {
      "page": 1,
      "page_size": 20,
      "total": 100,
      "total_pages": 5
    }
  },
  "timestamp": "..."
}
```

## 系统常量

### 大厅区域
- 一楼大厅
- 二楼大厅
- 三楼大厅
- VIP服务区
- 24小时自助区

### 设备状态
- 正常
- 故障
- 维修中
- 已修复

### 工单状态
- 待处理
- 处理中
- 已完成

### 故障类型分类
| 代码 | 名称 | 说明 |
|------|------|------|
| `hardware` | 硬件故障 | 设备硬件损坏或异常 |
| `software` | 软件故障 | 系统软件、应用程序异常 |
| `network` | 网络故障 | 网络连接异常 |
| `printer` | 打印故障 | 打印机相关问题 |
| `touchscreen` | 触摸屏故障 | 触摸屏不灵敏或损坏 |
| `power` | 电源故障 | 电源或供电问题 |
| `other` | 其他故障 | 其他未分类问题 |

### 紧急优先级（政务服务影响程度）
| 级别 | 颜色 | 影响程度 | 处理要求 |
|------|------|----------|----------|
| `high` | 🔴 #ff4d4f | 高 | 影响政务大厅正常服务，需立即处理 |
| `medium` | 🟡 #faad14 | 中 | 影响部分业务，需4小时内处理 |
| `low` | 🟢 #52c41a | 低 | 不影响主要业务，可安排时间处理 |

### 通信方式
- 以太网
- WiFi
- 4G
- 5G
- 专网

---

## API 接口列表

### 1. 系统常量接口

#### 1.1 获取所有常量
- **接口**: `GET /api/constants`
- **说明**: 获取系统所有枚举常量
- **返回数据**: 设备状态、工单状态、故障类型、紧急级别、通信方式、大厅区域

#### 1.2 获取大厅区域列表
- **接口**: `GET /api/hall-areas`
- **说明**: 获取所有大厅区域

---

### 2. 设备管理（增强版）

#### 2.1 录入新设备
- **接口**: `POST /api/devices`
- **说明**: 录入新的自助打证终端设备
- **请求体**:
```json
{
  "device_code": "BDC-001",
  "device_name": "不动产自助打证终端A",
  "device_model": "HP-ZT2024",
  "location": "1号窗口旁",
  "hall_area": "一楼大厅",
  "communication_mode": "专网",
  "status": "正常",
  "install_date": "2024-01-15",
  "commission_date": "2024-02-01"
}
```

#### 2.2 查询设备列表
- **接口**: `GET /api/devices`
- **说明**: 查询所有设备，支持多维度筛选和分页
- **查询参数**:
  - `status`: 按状态筛选
  - `hall_area`: 按大厅区域筛选
  - `communication_mode`: 按通信方式筛选
  - `keyword`: 关键词搜索（设备编号、名称、型号、位置）
  - `page`: 页码，默认1
  - `page_size`: 每页大小，默认20

#### 2.3 查询单个设备详情
- **接口**: `GET /api/devices/{device_id}`
- **说明**: 根据ID查询设备详情，包含该设备的近期工单和运维记录

#### 2.4 更新设备信息
- **接口**: `PUT /api/devices/{device_id}`
- **说明**: 更新设备的任意字段信息
- **请求体**: 支持以下字段的部分或全部更新
```json
{
  "device_name": "更新后的名称",
  "device_model": "新型号",
  "location": "新位置",
  "hall_area": "VIP服务区",
  "communication_mode": "5G",
  "status": "正常",
  "install_date": "2024-01-15",
  "commission_date": "2024-02-01"
}
```

#### 2.5 更新设备状态
- **接口**: `PUT /api/devices/{device_id}/status`
- **说明**: 单独更新设备运行状态
- **请求体**:
```json
{
  "status": "维修中"
}
```

#### 2.6 获取设备关联的工单列表
- **接口**: `GET /api/devices/{device_id}/work-orders`
- **说明**: 设备工单联动，获取指定设备的所有工单
- **查询参数**:
  - `status`: 按工单状态筛选
  - `page`: 页码，默认1
  - `page_size`: 每页大小，默认20

---

### 3. 故障工单管理（增强版）

#### 3.1 上报故障（创建工单）
- **接口**: `POST /api/work-orders`
- **说明**: 上报设备故障，自动生成工单编号，支持故障分类和优先级标记
- **请求体**:
```json
{
  "device_id": 1,
  "fault_type": "printer",
  "urgency_level": "high",
  "fault_description": "打印机完全不工作，证书无法打印，严重影响窗口业务",
  "reporter": "张三",
  "reporter_phone": "13800138000"
}
```
- **工单编号格式**: `WOYYYYMMDDXXXX`，例如: `WO202405160001`

#### 3.2 查询工单列表
- **接口**: `GET /api/work-orders`
- **说明**: 查询所有工单，支持多维度筛选，按优先级排序（高优在前）
- **查询参数**:
  - `status`: 按状态筛选
  - `device_id`: 按设备筛选
  - `fault_type`: 按故障类型筛选
  - `urgency_level`: 按紧急级别筛选
  - `hall_area`: 按大厅区域筛选
  - `page`: 页码，默认1
  - `page_size`: 每页大小，默认20
- **排序规则**: 高优先级工单排在前面，同优先级按创建时间倒序

#### 3.3 查询单个工单详情
- **接口**: `GET /api/work-orders/{order_id}`
- **说明**: 根据ID查询工单详情，包含关联的设备信息和维修日志

#### 3.4 处理工单
- **接口**: `PUT /api/work-orders/{order_id}/handle`
- **说明**: 管理员处理工单，自动更新设备状态，自动记录维修日志
- **请求体**:
```json
{
  "status": "处理中",
  "handler": "李工程师",
  "handle_description": "已到达现场，正在检查打印机"
}
```
- **状态流转说明**:
  - 设为`处理中` → 设备状态自动变为`维修中`，自动添加开始处理日志
  - 设为`已完成` → 设备状态自动变为`已修复`，自动生成运维记录和完成日志

#### 3.5 添加维修日志
- **接口**: `POST /api/work-orders/{order_id}/logs`
- **说明**: 为工单添加维修进度日志
- **请求体**:
```json
{
  "log_type": "progress",
  "content": "已拆下打印机主板，发现电路板有烧毁痕迹，正在联系供应商申请配件",
  "operator": "李工程师"
}
```

---

### 4. 运维记录管理

#### 4.1 创建运维记录
- **接口**: `POST /api/maintenance-records`
- **说明**: 创建设备运维记录（日常巡检、保养等）
- **请求体**:
```json
{
  "device_id": 1,
  "work_order_id": 1,
  "maintenance_type": "日常巡检",
  "description": "清洁设备外观，检查系统运行状态，更新杀毒软件",
  "parts_used": "无",
  "operator": "王技术员",
  "duration_minutes": 30
}
```

#### 4.2 查询运维记录
- **接口**: `GET /api/maintenance-records`
- **说明**: 查询运维记录，支持筛选和分页
- **查询参数**:
  - `device_id`: 按设备筛选
  - `maintenance_type`: 按维护类型筛选
  - `start_date`: 开始日期
  - `end_date`: 结束日期
  - `page`: 页码，默认1
  - `page_size`: 每页大小，默认20

---

### 5. 数据统计（增强版）

#### 5.1 仪表盘统计
- **接口**: `GET /api/dashboard`
- **说明**: 获取完整的仪表盘统计数据
- **返回数据**:
```json
{
  "devices": {
    "total": 10,
    "by_status": {
      "正常": 7,
      "故障": 1,
      "维修中": 1,
      "已修复": 1
    },
    "availability_rate": 80.0
  },
  "work_orders": {
    "total": 15,
    "by_status": {
      "待处理": 3,
      "处理中": 2,
      "已完成": 10
    },
    "high_urgency": 2,
    "by_fault_type": {
      "hardware": 3,
      "software": 2,
      "network": 4,
      "printer": 5,
      "touchscreen": 1,
      "power": 0,
      "other": 0
    },
    "today_new": 2,
    "today_completed": 3
  },
  "by_area": {
    "一楼大厅": {
      "device_count": 3,
      "normal_count": 2,
      "availability_rate": 66.67,
      "pending_orders": 1
    }
  }
}
```
- **指标说明**:
  - `availability_rate`: 设备完好率 = (正常设备数 + 已修复设备数) / 总设备数 * 100%
  - `by_area`: 按区域分组的设备和工单统计

---

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务
```bash
python app.py
```

### 3. 运行完整测试（新开一个终端窗口）
```bash
python test_api.py
```

## 数据库表结构

### devices (设备表 - 增强版)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| device_code | TEXT | 设备编号（唯一） |
| device_name | TEXT | 设备名称 |
| device_model | TEXT | 设备型号 |
| location | TEXT | 具体位置 |
| hall_area | TEXT | 所属大厅区域 |
| communication_mode | TEXT | 通信方式 |
| status | TEXT | 设备状态 |
| install_date | TEXT | 安装日期 |
| commission_date | TEXT | 投用日期 |
| last_maintenance_date | TEXT | 最后维护日期 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

### work_orders (工单表 - 增强版)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| order_no | TEXT | 工单编号（唯一，自动生成） |
| device_id | INTEGER | 关联设备ID |
| device_code | TEXT | 设备编号（冗余，方便查询） |
| device_name | TEXT | 设备名称（冗余） |
| hall_area | TEXT | 大厅区域（冗余） |
| fault_type | TEXT | 故障类型代码 |
| fault_category | TEXT | 故障分类名称 |
| urgency_level | TEXT | 紧急优先级 |
| urgency_color | TEXT | 优先级颜色代码 |
| fault_description | TEXT | 故障描述 |
| reporter | TEXT | 上报人 |
| reporter_phone | TEXT | 上报人电话 |
| status | TEXT | 工单状态 |
| handler | TEXT | 处理人 |
| handle_description | TEXT | 处理说明 |
| created_at | TEXT | 创建时间 |
| handled_at | TEXT | 开始处理时间 |
| completed_at | TEXT | 完成时间 |

### maintenance_records (运维记录表 - 增强版)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| device_id | INTEGER | 关联设备ID |
| work_order_id | INTEGER | 关联工单ID |
| order_no | TEXT | 工单编号（冗余） |
| maintenance_type | TEXT | 运维类型 |
| description | TEXT | 运维描述 |
| parts_used | TEXT | 使用的配件 |
| operator | TEXT | 操作人 |
| duration_minutes | INTEGER | 维护时长(分钟) |
| created_at | TEXT | 创建时间 |

### maintenance_logs (维修日志表 - 新增)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| work_order_id | INTEGER | 关联工单ID |
| log_type | TEXT | 日志类型 (create/start/progress/complete) |
| content | TEXT | 日志内容 |
| operator | TEXT | 操作人 |
| created_at | TEXT | 创建时间 |
