# API 使用说明

## 启动服务
```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口列表

### 1. 设备管理

#### 1.1 添加设备
```
POST /api/devices
Content-Type: application/json

{
  "device_code": "POS001",
  "device_name": "自助收银机1号",
  "location": "一楼入口",
  "install_date": "2024-01-15",
  "remark": "主力设备"
}
```

#### 1.2 查询设备列表
```
GET /api/devices?status=正常&keyword=POS

参数：
- status: 设备状态（正常/故障/维修中/已修复），可选
- keyword: 搜索关键词，可选
```

#### 1.3 查询单个设备
```
GET /api/devices/{device_id}
```

#### 1.4 更新设备状态
```
PUT /api/devices/{device_id}/status
Content-Type: application/json

{
  "status": "维修中"
}
```

#### 1.5 删除设备
```
DELETE /api/devices/{device_id}
```

### 2. 工单管理

#### 2.1 创建报修工单
```
POST /api/work-orders
Content-Type: application/json

{
  "device_id": 1,
  "fault_description": "触摸屏无响应",
  "reporter": "张三",
  "reporter_phone": "13800138000"
}
```

*工单自动编号，格式：WOYYYYMMDDXXXX*

#### 2.2 查询工单列表
```
GET /api/work-orders?status=待处理&device_id=1

参数：
- status: 工单状态（待处理/处理中/已完成），可选
- device_id: 设备ID，可选
```

#### 2.3 处理工单
```
PUT /api/work-orders/{order_no}/handle
Content-Type: application/json

{
  "status": "处理中",
  "handle_user": "李工",
  "handle_content": "已到达现场，正在排查问题"
}
```

*状态变更说明：
- 处理中：设备状态变为"维修中"
- 已完成：设备状态变为"已修复"，并自动生成运维记录*

### 3. 运维记录

#### 3.1 查询运维记录
```
GET /api/maintenance-records?device_id=1&start_date=2024-01-01&end_date=2024-12-31

参数：
- device_id: 设备ID，可选
- start_date: 开始日期，可选
- end_date: 结束日期，可选
```

#### 3.2 添加运维记录
```
POST /api/maintenance-records
Content-Type: application/json

{
  "device_id": 1,
  "maintenance_type": "日常保养",
  "content": "清洁设备，检查硬件连接",
  "operator": "王工",
  "remark": "运行正常"
}
```

### 4. 仪表盘统计

#### 4.1 获取统计数据
```
GET /api/dashboard/stats
```

返回：
- total_devices: 设备总数
- normal_devices: 正常设备数
- fault_devices: 故障设备数
- repairing_devices: 维修中设备数
- pending_orders: 待处理工单数

## 设备状态说明
- **正常**: 设备正常运行
- **故障**: 设备出现故障，等待报修处理
- **维修中**: 设备正在维修
- **已修复**: 设备已修复完成

## 工单状态说明
- **待处理**: 工单已创建，等待处理
- **处理中**: 工单正在处理中
- **已完成**: 工单已处理完成

## 快速测试命令

### 添加设备
```bash
curl -X POST http://localhost:5000/api/devices ^
  -H "Content-Type: application/json" ^
  -d "{\"device_code\":\"POS001\",\"device_name\":\"自助收银机1号\",\"location\":\"一楼入口\",\"install_date\":\"2024-01-15\"}"
```

### 查询设备列表
```bash
curl http://localhost:5000/api/devices
```

### 创建报修工单
```bash
curl -X POST http://localhost:5000/api/work-orders ^
  -H "Content-Type: application/json" ^
  -d "{\"device_id\":1,\"fault_description\":\"触摸屏无响应\",\"reporter\":\"张三\"}"
```

### 查询工单列表
```bash
curl http://localhost:5000/api/work-orders
```

### 处理工单
```bash
curl -X PUT http://localhost:5000/api/work-orders/WO202405150001/handle ^
  -H "Content-Type: application/json" ^
  -d "{\"status\":\"已完成\",\"handle_user\":\"李工\",\"handle_content\":\"更换触摸屏模块\"}"
```

### 查询运维记录
```bash
curl http://localhost:5000/api/maintenance-records
```

### 获取统计数据
```bash
curl http://localhost:5000/api/dashboard/stats
```