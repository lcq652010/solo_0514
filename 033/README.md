# 智能水表远程采集终端运维管理系统

基于 Python + Flask + SQLite 的后端API服务。

## 功能特性

- **设备管理**：设备录入、查询、更新、删除
- **故障上报**：自动生成工单号，设备状态自动更新
- **工单处理**：管理员受理、完成工单
- **运维记录**：记录查询、添加、更新、删除
- **设备状态**：正常、故障、维修中、已修复

## 项目结构

```
├── app.py                 # 应用入口
├── config.py              # 配置文件
├── requirements.txt       # 依赖包
├── init_data.py           # 初始化演示数据
├── models/                # 数据模型
│   ├── __init__.py
│   ├── device.py         # 设备模型
│   ├── fault.py          # 故障模型
│   └── maintenance.py    # 运维记录模型
└── routes/                # API路由
    ├── __init__.py
    ├── device.py         # 设备API
    ├── fault.py          # 故障API
    └── maintenance.py    # 运维记录API
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化演示数据（可选）

```bash
python init_data.py
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动。

## API 接口文档

### 设备管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/devices | 获取所有设备 |
| POST | /api/devices | 创建设备 |
| GET | /api/devices/{id} | 获取单个设备 |
| PUT | /api/devices/{id} | 更新设备 |
| DELETE | /api/devices/{id} | 删除设备 |

**创建设备请求示例：**
```json
{
    "device_code": "WM004",
    "device_name": "智能水表-C区1号楼",
    "install_location": "C区1号楼1单元101",
    "install_date": "2024-05-01",
    "status": "normal"
}
```

### 故障管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/faults | 获取所有故障工单 |
| POST | /api/faults | 上报故障 |
| GET | /api/faults/{id} | 获取单个工单 |
| DELETE | /api/faults/{id} | 删除工单 |
| POST | /api/faults/{id}/handle | 处理工单 |

**上报故障请求示例：**
```json
{
    "device_id": 1,
    "fault_type": "通信故障",
    "fault_desc": "设备频繁离线，通信不稳定",
    "reporter": "王五"
}
```

**处理工单请求示例：**
```json
{
    "action": "accept",
    "handler": "李工"
}
```

或标记完成：
```json
{
    "action": "complete",
    "handle_note": "已更换通信模块，设备恢复正常"
}
```

### 运维记录

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/maintenance | 获取运维记录（支持筛选） |
| POST | /api/maintenance | 添加运维记录 |
| GET | /api/maintenance/{id} | 获取单条记录 |
| PUT | /api/maintenance/{id} | 更新记录 |
| DELETE | /api/maintenance/{id} | 删除记录 |

**查询参数：**
- `device_id`: 按设备ID筛选
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)

**添加运维记录请求示例：**
```json
{
    "device_id": 1,
    "fault_id": 1,
    "maintenance_type": "故障维修",
    "operator": "王工",
    "maintenance_date": "2024-05-10 14:30:00",
    "maintenance_content": "更换传感器模块",
    "parts_replaced": "流量传感器 x1",
    "cost": 280.00,
    "notes": "设备恢复正常运行"
}
```

## 设备状态说明

| 状态码 | 状态文本 | 说明 |
|--------|----------|------|
| normal | 正常 | 设备正常运行 |
| fault | 故障 | 设备发生故障，待处理 |
| repairing | 维修中 | 工单已受理，正在维修 |
| fixed | 已修复 | 工单已完成，设备修复 |

## 工单状态说明

| 状态码 | 状态文本 | 说明 |
|--------|----------|------|
| pending | 待处理 | 故障已上报，未受理 |
| processing | 处理中 | 管理员已受理工单 |
| completed | 已完成 | 工单处理完成 |

## 工单编号规则

格式：`WO + 日期(YYYYMMDD) + 序号(4位)`

示例：`WO202605160001`