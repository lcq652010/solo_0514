# 加油站自助收银加油机运维管理系统后端

基于 Python + Flask + SQLite 实现的加油站设备运维管理系统。

## 功能特性

### 设备管理
- 设备录入（设备编号、名称、类型、位置、安装日期等）
- 设备查询（按状态筛选）
- 设备信息修改
- 设备状态更新（正常、故障、维修中、已修复）
- 设备删除

### 故障报修
- 故障上报（自动生成工单号）
- 报修记录查询（按状态筛选）
- 报修处理（开始维修、完成维修、取消报修）

### 运维记录
- 运维记录录入
- 运维记录查询（按设备筛选）
- 仪表盘统计数据

## 技术栈
- Python 3.x
- Flask 3.0.0
- SQLite 3
- Flask-CORS

## 安装运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 初始化数据库（可选，首次运行会自动创建）
```bash
python models.py
```

### 3. 运行应用
```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API 接口文档

### 基础信息
- 基础 URL: `http://localhost:5000`
- 请求格式: JSON
- 响应格式: JSON

### 设备状态说明
| 状态值 | 说明 |
|--------|------|
| normal | 正常 |
| fault | 故障 |
| maintaining | 维修中 |
| repaired | 已修复 |

### 报修状态说明
| 状态值 | 说明 |
|--------|------|
| pending | 待处理 |
| processing | 处理中 |
| completed | 已完成 |
| cancelled | 已取消 |

---

### 1. 设备管理接口

#### 获取设备列表
```
GET /api/devices
```
查询参数:
- `status` (可选): 按状态筛选

响应示例:
```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "device_no": "FUEL-001",
      "device_name": "1号加油机",
      "device_type": "加油机",
      "location": "A区1号机位",
      "status": "normal",
      "install_date": "2024-01-01",
      "description": "正星加油机",
      "create_time": "2024-01-15 10:00:00",
      "update_time": "2024-01-15 10:00:00"
    }
  ],
  "message": "success"
}
```

#### 获取单个设备
```
GET /api/devices/{id}
```

#### 添加设备
```
POST /api/devices
```
请求体:
```json
{
  "device_no": "FUEL-001",
  "device_name": "1号加油机",
  "device_type": "加油机",
  "location": "A区1号机位",
  "status": "normal",
  "install_date": "2024-01-01",
  "description": "设备描述"
}
```

#### 更新设备
```
PUT /api/devices/{id}
```
请求体: 同上（可部分字段）

#### 更新设备状态
```
PUT /api/devices/{id}/status
```
请求体:
```json
{
  "status": "maintaining"
}
```

#### 删除设备
```
DELETE /api/devices/{id}
```

---

### 2. 故障报修接口

#### 获取报修列表
```
GET /api/fault-reports
```
查询参数:
- `status` (可选): 按状态筛选

#### 获取单个报修
```
GET /api/fault-reports/{id}
```

#### 故障上报
```
POST /api/fault-reports
```
请求体:
```json
{
  "device_id": 1,
  "fault_type": "硬件故障",
  "fault_description": "油枪不出油",
  "reporter": "张三",
  "contact": "13800138000"
}
```
响应: 自动生成工单号 `WO202401150001`

#### 处理报修
```
PUT /api/fault-reports/{id}/process
```
请求体:
```json
{
  "action": "processing"
}
```
action 可选值:
- `processing`: 开始维修（设备状态变为 maintaining）
- `completed`: 完成维修（设备状态变为 repaired）
- `cancelled`: 取消报修（设备状态变为 normal）

---

### 3. 运维记录接口

#### 获取运维记录列表
```
GET /api/maintenance-records
```
查询参数:
- `device_id` (可选): 按设备筛选

#### 获取单条运维记录
```
GET /api/maintenance-records/{id}
```

#### 添加运维记录
```
POST /api/maintenance-records
```
请求体:
```json
{
  "device_id": 1,
  "maintenance_type": "定期保养",
  "maintenance_content": "更换滤芯、检查管路",
  "maintenance_person": "李工",
  "start_time": "2024-01-15 14:00:00",
  "end_time": "2024-01-15 16:00:00",
  "cost": 200.00,
  "remark": "保养完成，设备运行正常"
}
```
响应: 自动生成运维单号 `MT202401150001`

---

### 4. 仪表盘接口

#### 获取统计数据
```
GET /api/dashboard/stats
```
响应示例:
```json
{
  "code": 200,
  "data": {
    "total_devices": 10,
    "normal_devices": 7,
    "fault_devices": 1,
    "maintaining_devices": 2,
    "pending_reports": 3,
    "total_maintenance": 25
  },
  "message": "success"
}
```

---

### 首页接口
```
GET /
```
显示所有可用接口列表。

## 工单编号规则
- 故障报修单: `WO` + 日期(8位) + 序号(4位) → 例: WO202401150001
- 运维记录单: `MT` + 日期(8位) + 序号(4位) → 例: MT202401150001

## 数据库结构
- `devices`: 设备表
- `fault_reports`: 故障报修表
- `maintenance_records`: 运维记录表

所有表会在首次运行时自动创建。
