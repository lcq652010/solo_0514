# 机场自助行李托运机运维管理系统 v2.0 - API测试说明

## 版本更新说明

v2.0 新增功能:
- 设备模块新增: 设备型号、通信方式、启用日期字段
- 故障模块新增: 故障类型分类、紧急优先级标记
- 工单按优先级自动排序（紧急工单优先）
- 支持按故障类型、优先级筛选工单
- 统计面板新增故障类型和优先级统计

## 启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 数据库迁移（升级旧版本数据库）
python migrate_db.py

# 启动服务
python app.py
```

服务启动后访问: http://localhost:5000

---

## API 接口列表

### 1. 设备录入
- **接口**: POST /api/devices
- **说明**: 录入新的自助行李托运机

**请求示例**:
```json
{
  "device_code": "BAG-001",
  "device_name": "T1航站楼1号自助托运机",
  "device_model": "BAG-2024-PRO",
  "communication_mode": "5G",
  "location": "T1航站楼A区",
  "install_date": "2024-01-15",
  "activation_date": "2024-02-01",
  "operator": "管理员"
}
```

**字段说明**:
- `device_model`: 设备型号（可选）
- `communication_mode`: 通信方式（可选），如: 5G、WiFi、有线
- `activation_date`: 启用日期（可选）

### 2. 设备列表查询
- **接口**: GET /api/devices
- **参数**:
  - page: 页码（默认1）
  - per_page: 每页数量（默认10）
  - status: 按状态筛选（正常/故障/维修中/已修复）
  - device_model: 按设备型号模糊搜索
  - communication_mode: 按通信方式筛选

**示例**:
```
GET /api/devices?page=1&per_page=10&status=正常&communication_mode=5G
```

### 3. 设备详情查询
- **接口**: GET /api/devices/<device_id>

**示例**:
```
GET /api/devices/1
```

### 4. 更新设备状态
- **接口**: PUT /api/devices/<device_id>/status

**请求示例**:
```json
{
  "status": "维修中",
  "operator": "张工程师"
}
```

### 5. 故障上报
- **接口**: POST /api/work-orders
- **说明**: 上报设备故障，自动生成工单

**请求示例**:
```json
{
  "device_code": "BAG-001",
  "fault_type": "硬件故障",
  "priority": "紧急",
  "fault_description": "行李传送带电机烧坏，影响航班出港行李托运",
  "reporter": "李操作员"
}
```

**字段说明**:
- `fault_type`: 故障类型，可选值: 硬件故障、软件故障、通信故障、机械故障、传感器故障、电源故障、其他（默认）
- `priority`: 紧急优先级，按机场航班运行影响程度: 紧急、高、普通（默认）、低

### 6. 工单列表查询
- **接口**: GET /api/work-orders
- **参数**:
  - page: 页码
  - per_page: 每页数量
  - status: 工单状态（待处理/处理中/已完成）
  - fault_type: 按故障类型筛选
  - priority: 按优先级筛选

**说明**: 工单默认按优先级排序（紧急 > 高 > 普通 > 低），相同优先级按时间倒序

### 7. 处理工单
- **接口**: PUT /api/work-orders/<order_no>/handle

**请求示例**:
```json
{
  "handler": "王工程师",
  "handle_result": "已更换传送带电机，设备恢复正常",
  "action": "修复完成"
}
```

**action 可选值**:
- "开始维修" - 将工单设为"处理中"，设备设为"维修中"
- "修复完成" - 将工单设为"已完成"，设备设为"已修复"

### 8. 运维记录查询
- **接口**: GET /api/maintenance-records
- **参数**:
  - page: 页码
  - per_page: 每页数量
  - device_code: 按设备编号筛选
  - record_type: 按记录类型筛选（设备录入/状态变更/故障上报/运维处理）

### 9. 统计数据
- **接口**: GET /api/dashboard/statistics

**返回数据包含**:
- 设备总数及各状态设备数
- 工单状态统计（待处理、处理中、已完成）
- 待处理紧急工单数量
- 待处理高优先级工单数量
- 各故障类型统计（硬件、软件、通信、机械、传感器、电源）

---

## 设备状态说明

| 状态 | 说明 |
|------|------|
| 正常 | 设备正常运行中 |
| 故障 | 设备出现故障，待处理 |
| 维修中 | 设备正在维修中 |
| 已修复 | 设备故障已修复 |

---

## 工单自动编号规则

工单编号格式: WO + 日期(8位) + 序号(4位)

示例: WO202405150001

---

## 响应格式说明

所有接口统一响应格式:

```json
{
  "code": 200,
  "message": "操作说明",
  "data": { ... }
}
```

- code: 状态码（200成功，400参数错误，404资源不存在，500服务器错误）
- message: 操作结果说明
- data: 返回数据
