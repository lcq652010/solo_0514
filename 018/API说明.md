# 医院超声诊断设备运维管理系统 - API文档

## 服务器信息
- 服务器地址：http://localhost:5000
- 数据库：SQLite (hospital_ultrasound.db)
- 跨域支持：已启用

## 统一响应格式
所有API接口返回统一格式：
```json
{
  "success": true,
  "message": "操作成功",
  "timestamp": "2024-05-16T10:30:00.123456",
  "data": {}
}
```

---

## 1. 设备管理接口

### 添加设备
- **POST** `/api/devices`
- 请求体：
```json
{
  "device_code": "US-001",
  "device_name": "彩色多普勒超声诊断仪",
  "model": "GE-E10",
  "probe_count": 4,
  "department": "radiology",
  "location": "门诊楼3楼B超室",
  "purchase_date": "2024-01-15",
  "enable_date": "2024-02-01",
  "status": "正常"
}
```

### 获取设备列表
- **GET** `/api/devices`
- 查询参数：
  - status (可选): 按状态筛选
  - department (可选): 按科室筛选
  - device_code (可选): 按设备编号模糊搜索
- 说明：返回设备状态颜色标记

### 获取单个设备
- **GET** `/api/devices/{device_id}`

### 更新设备信息
- **PUT** `/api/devices/{device_id}`

### 更新设备状态
- **PUT** `/api/devices/{device_id}/status`
- 状态值：正常、故障、维修中、已修复

---

## 2. 基础数据接口

### 获取科室列表
- **GET** `/api/departments`
- 返回预定义的科室列表：
  - radiology: 放射科
  - cardiology: 心内科
  - emergency: 急诊科
  - pediatrics: 儿科
  - obstetrics: 妇产科
  - surgery: 外科
  - internal: 内科
  - icu: ICU

### 获取故障类型列表
- **GET** `/api/fault-types`
- 返回预定义的故障类型：
  - hardware: 硬件故障
  - software: 软件故障
  - probe: 探头故障
  - display: 显示故障
  - power: 电源故障
  - network: 网络故障
  - other: 其他故障

### 获取故障等级列表
- **GET** `/api/fault-levels`
- 返回预定义的故障等级：
  - critical: 严重（设备完全无法使用）
  - major: 较大（主要功能异常）
  - general: 一般（次要功能异常）
  - minor: 轻微（不影响主要功能）

---

## 3. 工单管理接口

### 故障上报
- **POST** `/api/work-orders/report`
- 请求体：
```json
{
  "device_id": 1,
  "fault_type": "probe",
  "fault_description": "探头无法正常工作，图像显示异常",
  "priority": "紧急",
  "fault_level": "critical",
  "reporter": "张医生"
}
```
- 字段说明：
  - priority: 紧急优先级（紧急/高/普通/低）
  - fault_level: 故障等级（严重/较大/一般/轻微）

### 获取工单列表
- **GET** `/api/work-orders`
- 查询参数：
  - status (可选): 按状态筛选
  - fault_type (可选): 按故障类型筛选
  - priority (可选): 按优先级筛选
  - department (可选): 按科室筛选
  - fault_level (可选): 按故障等级筛选
- 说明：工单默认按优先级排序（紧急>高>普通>低），并附带颜色标记

### 处理工单
- **PUT** `/api/work-orders/{order_no}/handle`
- 请求体：
```json
{
  "status": "已完成",
  "handler": "李工程师",
  "handle_result": "更换探头，设备恢复正常",
  "repair_cost": 5000
}
```
- 状态值：待处理、处理中、已完成

---

## 4. 运维记录接口

### 获取运维记录
- **GET** `/api/maintenance-records`
- 查询参数：
  - device_id (可选): 按设备筛选
  - department (可选): 按科室筛选
  - maintenance_type (可选): 按维护类型筛选

### 添加运维记录
- **POST** `/api/maintenance-records`
- 请求体：
```json
{
  "device_id": 1,
  "work_order_no": "WO202405160001",
  "maintenance_type": "日常保养",
  "description": "设备定期清洁和校准",
  "operator": "王工程师",
  "start_time": "2024-05-16 09:00:00",
  "end_time": "2024-05-16 10:30:00",
  "result": "保养完成，设备运行正常",
  "parts_used": "清洁液、棉签",
  "cost": 200
}
```

---

## 5. 设备操作日志接口

### 获取设备操作日志
- **GET** `/api/device-operation-logs`
- 查询参数：device_id (可选) - 按设备筛选
- 说明：记录设备新增、更新、状态变更等操作

---

## 6. 统计接口

### 获取仪表盘统计
- **GET** `/api/dashboard/stats`
- 返回数据：
  - total_devices: 设备总数
  - normal_devices: 正常设备数
  - fault_devices: 故障设备数
  - repairing_devices: 维修中设备数
  - repaired_devices: 已修复设备数
  - pending_orders: 待处理工单数
  - urgent_orders: 紧急工单数（未完成）
  - total_records: 运维记录总数
  - fault_type_stats: 各故障类型统计
  - availability_rate: 设备开机率 (%)
  - intact_rate: 设备完好率 (%)
  - monthly_maintenance: 本月维护次数
  - total_maintenance_cost: 总维护费用

### 获取科室统计
- **GET** `/api/dashboard/department-stats`
- 返回各科室的设备统计：
  - department: 科室名称
  - total_devices: 设备总数
  - available_devices: 可用设备数
  - availability_rate: 开机率 (%)
  - intact_rate: 完好率 (%)

---

## 数据库表结构

### devices (设备表)
- id: 主键
- device_code: 设备编号（唯一）
- device_name: 设备名称
- model: 设备型号
- probe_count: 探头数量
- department: 所属科室
- location: 存放位置
- purchase_date: 购置日期
- enable_date: 启用日期
- status: 状态（正常/故障/维修中/已修复）
- create_time: 创建时间
- update_time: 更新时间

### work_orders (工单表)
- id: 主键
- order_no: 工单号（自动生成）
- device_id: 设备ID
- device_code: 设备编号
- department: 科室
- fault_type: 故障类型
- fault_description: 故障描述
- priority: 紧急优先级
- fault_level: 故障等级
- reporter: 上报人
- report_time: 上报时间
- status: 状态（待处理/处理中/已完成）
- handler: 处理人
- handle_time: 处理时间
- handle_result: 处理结果
- repair_cost: 维修费用

### maintenance_records (运维记录表)
- id: 主键
- device_id: 设备ID
- device_code: 设备编号
- department: 科室
- work_order_no: 关联工单号
- maintenance_type: 运维类型
- description: 描述
- operator: 操作人
- start_time: 开始时间
- end_time: 结束时间
- result: 结果
- parts_used: 使用配件
- cost: 费用
- create_time: 创建时间

### device_operation_logs (设备操作日志表)
- id: 主键
- device_id: 设备ID
- device_code: 设备编号
- operation_type: 操作类型
- operator: 操作人
- remark: 备注
- operation_time: 操作时间
