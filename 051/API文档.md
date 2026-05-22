# 校园一卡通自助充值圈存机运维管理系统 API 文档

## 基础地址
`http://127.0.0.1:5000/api`

## 统一返回格式
```json
{
    "code": 200,
    "data": {},
    "msg": "success"
}
```

---

## 一、设备管理接口

### 1.1 设备录入
- **接口**: `POST /devices`
- **说明**: 新增圈存机设备

**请求参数**:
```json
{
    "device_id": "DEV001",
    "device_name": "一号教学楼圈存机",
    "location": "一号教学楼大厅",
    "status": "正常",
    "install_date": "2024-01-15"
}
```

### 1.2 获取所有设备
- **接口**: `GET /devices`
- **说明**: 获取所有设备列表

### 1.3 获取单个设备
- **接口**: `GET /devices/{device_id}`
- **说明**: 获取指定设备详情

### 1.4 更新设备状态
- **接口**: `PUT /devices/{device_id}/status`
- **说明**: 更新设备状态

**请求参数**:
```json
{
    "status": "维修中"
}
```
- 状态可选值: `正常`、`故障`、`维修中`、`已修复`

### 1.5 删除设备
- **接口**: `DELETE /devices/{device_id}`
- **说明**: 删除指定设备

---

## 二、工单管理接口

### 2.1 故障上报（创建工单）
- **接口**: `POST /work-orders`
- **说明**: 上报设备故障，自动生成工单编号

**请求参数**:
```json
{
    "device_id": "DEV001",
    "fault_type": "硬件故障",
    "fault_description": "触摸屏幕无响应",
    "reporter": "张三",
    "reporter_phone": "13800138000"
}
```

**返回示例**:
```json
{
    "code": 200,
    "data": {
        "order_id": "WO202405160001"
    },
    "msg": "工单创建成功"
}
```

### 2.2 获取工单列表
- **接口**: `GET /work-orders`
- **说明**: 获取所有工单，可按状态筛选

**查询参数**:
- `status` (可选): 工单状态（待处理、处理中、已完成）

### 2.3 开始处理工单
- **接口**: `PUT /work-orders/{order_id}/handle`
- **说明**: 管理员开始处理工单

**请求参数**:
```json
{
    "handler": "李工程师",
    "handle_note": "已安排人员上门维修"
}
```

### 2.4 完成工单
- **接口**: `PUT /work-orders/{order_id}/complete`
- **说明**: 完成工单维修，更新设备状态为"已修复"

**请求参数**:
```json
{
    "handle_note": "更换触摸屏模块，设备恢复正常"
}
```

---

## 三、运维记录接口

### 3.1 获取运维记录
- **接口**: `GET /maintain-records`
- **说明**: 获取所有运维记录，可按设备筛选

**查询参数**:
- `device_id` (可选): 设备编号

---

## 四、统计接口

### 4.1 获取统计数据
- **接口**: `GET /statistics`
- **说明**: 获取系统统计数据

**返回示例**:
```json
{
    "code": 200,
    "data": {
        "total_devices": 10,
        "normal_devices": 8,
        "fault_devices": 1,
        "repairing_devices": 1,
        "total_orders": 15,
        "pending_orders": 2
    },
    "msg": "success"
}
```
