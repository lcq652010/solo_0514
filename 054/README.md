# 影院自助取票售检票一体机运维管理系统后端

基于 Python + Flask + SQLite 实现的影院设备运维管理系统。

## 功能特性

### 1. 设备管理
- 设备录入（设备编号、名称、类型、位置、状态）
- 设备查询（支持分页、按状态/类型筛选）
- 设备信息更新
- 设备删除

### 2. 故障工单管理
- 故障上报（创建工单）
- 工单自动编号（格式：WO+日期+4位序号，如 WO202605160001）
- 工单查询（支持分页、按状态/设备筛选）
- 工单处理（开始维修、完成维修）

### 3. 运维记录管理
- 运维记录查询（支持分页、按设备/工单筛选）
- 添加运维记录

### 4. 设备状态
- normal（正常）
- fault（故障）
- repairing（维修中）
- repaired（已修复）

### 5. 仪表盘统计
- 设备总数、各状态设备数量
- 工单总数、待处理/处理中工单数量

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行服务
```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 3. 测试 API
```bash
python test_api.py
```

## API 接口文档

### 设备管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/devices | 添加设备 |
| GET | /api/devices | 获取设备列表（支持分页筛选） |
| GET | /api/devices/{id} | 获取单个设备详情 |
| PUT | /api/devices/{id} | 更新设备信息 |
| DELETE | /api/devices/{id} | 删除设备 |

**添加设备请求示例：**
```json
{
    "device_code": "DEV001",
    "device_name": "一号厅自助取票机",
    "device_type": "ticket_machine",
    "location": "一号厅入口",
    "status": "normal"
}
```

### 工单管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/workorders | 创建故障工单（故障上报） |
| GET | /api/workorders | 获取工单列表（支持分页筛选） |
| GET | /api/workorders/{id} | 获取单个工单详情 |
| PUT | /api/workorders/{id}/handle | 处理工单 |

**创建工单请求示例：**
```json
{
    "device_id": 1,
    "fault_type": "打印机故障",
    "fault_description": "自助取票机打印机卡纸",
    "reporter": "张三"
}
```

**处理工单请求示例：**
```json
{
    "handler": "王工程师",
    "action": "start_repair"  // 或 "complete"
}
```

完成维修时需要额外提供：
```json
{
    "handler": "王工程师",
    "action": "complete",
    "handle_result": "已更换打印机滚轴"
}
```

### 运维记录接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/maintenance | 添加运维记录 |
| GET | /api/maintenance | 获取运维记录列表（支持分页筛选） |

**添加运维记录请求示例：**
```json
{
    "device_id": 1,
    "maintenance_type": "定期保养",
    "description": "设备清洁、传感器校准",
    "operator": "赵师傅",
    "result": "成功",
    "remarks": "设备运行状态良好"
}
```

### 统计接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/dashboard/stats | 获取仪表盘统计数据 |

## 数据库表结构

### devices 设备表
- id: 主键
- device_code: 设备编号（唯一）
- device_name: 设备名称
- device_type: 设备类型
- location: 安装位置
- status: 设备状态
- install_date: 安装日期
- last_maintenance: 上次维护时间
- created_at: 创建时间
- updated_at: 更新时间

### work_orders 工单表
- id: 主键
- order_no: 工单编号（唯一，自动生成）
- device_id: 关联设备ID
- fault_type: 故障类型
- fault_description: 故障描述
- reporter: 上报人
- report_time: 上报时间
- status: 工单状态（pending/processing/completed）
- handler: 处理人
- handle_time: 处理时间
- handle_result: 处理结果
- created_at: 创建时间
- updated_at: 更新时间

### maintenance_records 运维记录表
- id: 主键
- device_id: 关联设备ID
- work_order_id: 关联工单ID（可选）
- maintenance_type: 维护类型
- description: 维护描述
- operator: 操作人
- maintenance_time: 维护时间
- result: 维护结果
- remarks: 备注
- created_at: 创建时间
