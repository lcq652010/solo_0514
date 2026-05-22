# 化工园区气体监测终端运维系统后端

基于 Python + Flask + SQLite 实现的化工园区气体监测终端运维系统后端。

## 功能特性

- 设备录入管理（含测量量程、报警上限、安装点位等字段）
- 超标告警上报（工单自动编号，含浓度值和发生时间）
- 告警确认与处置闭环（确认状态、处置结果、处置人）
- 按未确认、已确认、已处置自动分类展示告警列表
- 单设备监测浓度日/周趋势曲线数据接口
- 设备状态查询（正常、故障、离线、告警）
- 按监测气体种类筛选设备
- RESTful API 接口

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动

### 3. 运行测试

```bash
python test_api.py
```

## API 接口说明

### 设备管理

#### 添加设备
- **接口**: `POST /api/devices`
- **请求体**:
```json
{
  "device_code": "GAS-001",
  "device_name": "氨气监测终端-A区",
  "location": "化工园区A区1号厂房",
  "gas_type": "氨气",
  "measure_range": "0-100 ppm",
  "threshold": 25.0,
  "alarm_upper_limit": 50.0,
  "installation_point": "A区-1号反应釜旁",
  "status": "正常"
}
```

#### 获取所有设备
- **接口**: `GET /api/devices`
- **查询参数**: 
  - `status` (可选): 按状态筛选
  - `gas_type` (可选): 按气体类型筛选

#### 获取单个设备
- **接口**: `GET /api/devices/<device_id>`

#### 根据设备编号获取设备
- **接口**: `GET /api/devices/code/<device_code>`

#### 更新设备状态
- **接口**: `PUT /api/devices/<device_id>/status`
- **请求体**:
```json
{
  "status": "离线"
}
```
- **状态值**: 正常、故障、离线、告警

#### 获取所有气体类型
- **接口**: `GET /api/gas-types`

#### 获取设备日趋势曲线
- **接口**: `GET /api/devices/<device_id>/trend/daily`
- **返回**: 过去24小时的浓度监测数据

#### 获取设备周趋势曲线
- **接口**: `GET /api/devices/<device_id>/trend/weekly`
- **返回**: 过去7天的浓度监测数据

### 告警管理

#### 上报超标告警
- **接口**: `POST /api/alarms`
- **请求体**:
```json
{
  "device_code": "GAS-001",
  "gas_value": 30.5,
  "description": "氨气浓度超标"
}
```
- **工单编号**: 自动生成，格式: `GDYYYYMMDDXXXX`

#### 获取所有告警
- **接口**: `GET /api/alarms`
- **查询参数**: `confirm_status` (可选: 未确认/已确认/已处置)

#### 获取分类告警列表
- **接口**: `GET /api/alarms/categorized`
- **返回**: 按未确认、已确认、已处置自动分类的告警列表

#### 确认告警
- **接口**: `PUT /api/alarms/<alarm_id>/confirm`
- **请求体**:
```json
{
  "handler": "张三"
}
```

#### 处置告警（闭环）
- **接口**: `PUT /api/alarms/<alarm_id>/handle`
- **请求体**:
```json
{
  "handler": "李四",
  "handle_result": "已关闭泄漏源，浓度恢复正常。现场通风处理完成。"
}
```

### 仪表盘

#### 获取统计数据
- **接口**: `GET /api/dashboard`

## 数据库结构

### Device 表
- id: 主键
- device_code: 设备编号（唯一）
- device_name: 设备名称
- location: 安装位置
- gas_type: 监测气体类型
- measure_range: 测量量程
- threshold: 告警阈值
- alarm_upper_limit: 报警上限
- installation_point: 安装点位
- status: 设备状态
- created_at: 创建时间
- last_online: 最后在线时间

### Alarm 表
- id: 主键
- ticket_no: 工单编号（唯一）
- device_id: 设备ID
- gas_value: 气体浓度值
- alarm_time: 告警发生时间
- confirm_status: 确认状态（未确认/已确认/已处置）
- handle_result: 处置结果
- handler: 处置人
- handle_time: 处置时间
- description: 告警描述

### GasReading 表
- id: 主键
- device_id: 设备ID
- gas_value: 气体浓度值
- reading_time: 读数时间
