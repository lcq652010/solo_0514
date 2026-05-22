# 车管所自助体检拍照一体机运维管理系统 - API文档

## 基础信息
- 基础URL: `http://localhost:5000/api`
- 数据格式: JSON
- 字符编码: UTF-8

## 设备管理 API

### 1. 获取设备列表
- **接口**: `GET /devices`
- **说明**: 获取所有设备信息
- **返回示例**:
```json
{
  "code": 200,
  "data": [
    {
      "id": 1,
      "device_code": "TZJ-001",
      "device_name": "自助体检一体机A1",
      "location": "车管所一楼大厅",
      "status": "正常",
      "install_date": "2024-01-15",
      "last_maintain_date": "2024-05-10",
      "remark": "主力设备",
      "create_time": "2024-05-16 10:00:00"
    }
  ],
  "message": "success"
}
```

### 2. 获取单个设备
- **接口**: `GET /devices/{id}`
- **说明**: 根据ID获取设备详情

### 3. 添加设备
- **接口**: `POST /devices`
- **请求参数**:
```json
{
  "device_code": "TZJ-003",
  "device_name": "自助体检一体机A3",
  "location": "车管所三楼",
  "status": "正常",
  "install_date": "2024-05-01",
  "remark": "新设备"
}
```

### 4. 更新设备
- **接口**: `PUT /devices/{id}`
- **说明**: 更新设备信息

### 5. 删除设备
- **接口**: `DELETE /devices/{id}`
- **说明**: 删除指定设备

### 6. 更新设备状态
- **接口**: `PUT /devices/{id}/status`
- **请求参数**:
```json
{
  "status": "维修中"
}
```
- **状态说明**: 正常、故障、维修中、已修复

## 工单管理 API

### 1. 获取工单列表
- **接口**: `GET /work-orders`
- **查询参数**: `status` (可选) - 按状态筛选

### 2. 获取单个工单
- **接口**: `GET /work-orders/{id}`

### 3. 创建工单（故障上报）
- **接口**: `POST /work-orders`
- **请求参数**:
```json
{
  "device_id": 1,
  "device_code": "TZJ-001",
  "fault_type": "硬件故障",
  "fault_desc": "触摸屏无响应",
  "reporter": "王五",
  "reporter_phone": "13900139000"
}
```
- **说明**: 工单编号自动生成，格式为：YYYYMMDD + 4位序号

### 4. 处理工单
- **接口**: `PUT /work-orders/{id}/handle`
- **请求参数**:
```json
{
  "handle_user": "赵六",
  "handle_desc": "更换触摸屏模块",
  "status": "已完成"
}
```
- **状态说明**: 待处理、处理中、已完成

## 运维记录 API

### 1. 获取运维记录
- **接口**: `GET /maintain-records`
- **查询参数**: `device_id` (可选) - 按设备筛选

### 2. 添加运维记录
- **接口**: `POST /maintain-records`
- **请求参数**:
```json
{
  "device_id": 1,
  "device_code": "TZJ-001",
  "maintain_type": "例行维护",
  "maintain_desc": "清洁设备、检查硬件",
  "maintain_user": "李四",
  "maintain_time": "2024-05-16",
  "remark": "设备正常"
}
```

## 仪表盘 API

### 1. 获取统计数据
- **接口**: `GET /dashboard`
- **返回示例**:
```json
{
  "code": 200,
  "data": {
    "total_devices": 3,
    "normal_devices": 2,
    "fault_devices": 1,
    "repairing_devices": 0,
    "pending_orders": 1,
    "total_orders": 1
  },
  "message": "success"
}
```
