# 港口集装箱识别终端运维管理系统 - API文档

## 基础信息
- **基础URL**: `http://localhost:5000/api`
- **数据格式**: JSON
- **字符编码**: UTF-8
- **版本**: v3.0
- **统一响应格式**: 
  ```json
  {
    "success": true,
    "code": 200,
    "message": "操作成功",
    "timestamp": "2024-05-15T10:00:00",
    "data": {}
  }
  ```

---

## 数据库迁移说明

### 从旧版本升级到 v3.0

如果您已有旧版本数据库，请运行迁移脚本：
```bash
python migrate_db.py
```

**迁移脚本功能**:
- 自动备份原数据库
- 设备表新增：`harbor_area`、`work_area`、`is_online`、`last_online_time`
- 工单表新增：`fault_level`、`handle_duration`、`before_status`、`after_status`
- 运维记录表新增：港区、作业区域、故障等级、上报人、上报时间、处理时长、维修前后状态

---

## 枚举接口

### 获取所有枚举值
```
GET /enums
```
**响应数据**:
```json
{
  "fault_types": ["硬件故障", "软件故障", "网络故障", "电源故障", "传感器故障", "机械故障", "其他故障"],
  "priority_levels": ["紧急", "高", "一般", "低"],
  "device_status": ["正常", "故障", "维修中", "已修复"],
  "harbor_areas": ["港区A", "港区B", "港区C", "港区D"],
  "work_areas": ["集装箱堆场", "码头作业区", "闸口通道", "海关查验区", "冷藏箱区"],
  "fault_levels": ["轻微", "一般", "严重", "致命"]
}
```

---

## 一、设备管理接口

### 1.1 获取设备列表
```
GET /devices?harbor_area={港区}&work_area={作业区}&status={状态}&is_online={在线状态}
```
**查询参数（可选）**:
| 参数 | 类型 | 说明 |
|------|------|------|
| harbor_area | string | 按港区筛选 |
| work_area | string | 按作业区域筛选 |
| status | string | 按设备状态筛选 |
| is_online | boolean | 按在线状态筛选 |

**响应数据说明**:
- `priority_weight`: 优先级权重（紧急=4, 高=3, 一般=2, 低=1）
- `has_pending_order`: 是否有待处理工单

### 1.2 获取单个设备详情
```
GET /devices/{device_id}
```
**响应数据说明**:
- `pending_orders`: 待处理工单列表（按优先级排序）
- `has_pending_order`: 是否有待处理工单
- `recent_maintenance`: 最近5条维修记录

### 1.3 添加设备
```
POST /devices
```
**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| device_code | string | 是 | 设备编号（唯一） |
| device_name | string | 是 | 设备名称 |
| device_type | string | 是 | 设备类型 |
| device_model | string | 否 | 设备型号 |
| protection_level | string | 否 | 防护等级 |
| serial_number | string | 否 | 设备序列号 |
| commission_date | string | 否 | 投用日期 |
| harbor_area | string | 否 | 所属港区 |
| work_area | string | 否 | 作业区域 |
| location | string | 是 | 安装位置 |
| install_date | string | 是 | 安装日期 |

### 1.4 更新设备信息
```
PUT /devices/{device_id}
```
**支持更新的字段**:
`device_code`, `device_name`, `device_type`, `device_model`, `protection_level`, `serial_number`, `commission_date`, `harbor_area`, `work_area`, `location`, `install_date`, `status`, `is_online`

### 1.5 删除设备
```
DELETE /devices/{device_id}
```

### 1.6 更新设备状态
```
PUT /devices/{device_id}/status
```
**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| status | string | 是 | 状态：正常/故障/维修中/已修复 |

### 1.7 设备心跳更新
```
PUT /devices/{device_id}/heartbeat
```
**说明**: 更新设备在线状态和最后在线时间

---

## 二、工单管理接口

### 2.1 获取工单列表
```
GET /work-orders?harbor_area={港区}&work_area={作业区}&fault_type={故障类型}&fault_level={故障等级}&priority={优先级}&status={状态}&device_id={设备ID}
```
**查询参数（可选）**:
| 参数 | 类型 | 说明 |
|------|------|------|
| harbor_area | string | 按港区筛选 |
| work_area | string | 按作业区域筛选 |
| fault_type | string | 按故障类型筛选 |
| fault_level | string | 按故障等级筛选 |
| priority | string | 按优先级筛选 |
| status | string | 按工单状态筛选 |
| device_id | int | 按设备ID筛选 |

**排序规则**:
1. 按优先级排序（紧急→高→一般→低）
2. 同优先级按上报时间倒序

**响应数据说明**:
- `priority_weight`: 优先级权重
- `is_high_priority`: 是否高优先级（紧急/高），可用于前端高亮显示

### 2.2 获取单个工单详情
```
GET /work-orders/{order_no}
```

### 2.3 故障上报（创建工单）
```
POST /work-orders
```
**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| device_id | int | 是 | 设备ID |
| fault_type | string | 是 | 故障类型 |
| fault_level | string | 否 | 故障等级（默认：一般） |
| priority | string | 否 | 紧急优先级（默认：一般） |
| fault_description | string | 是 | 故障描述 |
| reporter | string | 是 | 上报人 |

**设备工单联动**:
- 创建工单时自动记录当前设备状态（`before_status`）
- 设备状态自动更新为"故障"

### 2.4 处理工单
```
PUT /work-orders/{order_no}/handle
```
**请求参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| handler | string | 是 | 处理人 |
| handle_result | string | 是 | 处理结果 |
| device_status | string | 是 | 维修后设备状态 |
| cost | float | 否 | 维修费用 |
| remark | string | 否 | 备注 |

**自动处理**:
- 自动计算处理时长（`handle_duration`，分钟）
- 自动更新设备状态
- 自动生成完整维修履历（包含维修前后状态）

---

## 三、运维记录接口

### 3.1 获取运维记录列表
```
GET /maintenance-records?harbor_area={港区}&work_area={作业区}&fault_type={故障类型}&fault_level={故障等级}&device_id={设备ID}
```
**查询参数（可选）**:
| 参数 | 类型 | 说明 |
|------|------|------|
| harbor_area | string | 按港区筛选 |
| work_area | string | 按作业区域筛选 |
| fault_type | string | 按故障类型筛选 |
| fault_level | string | 按故障等级筛选 |
| device_id | int | 按设备ID筛选 |

### 3.2 获取单个运维记录
```
GET /maintenance-records/{record_id}
```

### 3.3 获取指定设备的运维记录
```
GET /maintenance-records/device/{device_id}
```

---

## 四、统计接口

### 4.1 获取仪表板统计数据
```
GET /dashboard/stats
```
**响应数据**:
```json
{
  "total_devices": 100,
  "online_devices": 95,
  "online_rate": 95.0,
  "normal_devices": 85,
  "health_rate": 85.0,
  "fault_devices": 10,
  "repairing_devices": 5,
  "pending_orders": 8,
  "urgent_orders": 2,
  "total_maintenance_records": 150,
  "harbor_stats": [
    {"harbor_area": "港区A", "total": 30, "normal_count": 25, "health_rate": 83.33}
  ],
  "fault_type_stats": [
    {"fault_type": "硬件故障", "count": 45}
  ]
}
```

### 4.2 获取设备完好率统计
```
GET /dashboard/availability
```
**响应数据**:
```json
{
  "total_devices": 100,
  "online_devices": 95,
  "online_rate": 95.0,
  "normal_devices": 85,
  "health_rate": 85.0,
  "availability_rate": 90.0,
  "area_stats": [
    {"work_area": "集装箱堆场", "total": 30, "online": 28, "online_rate": 93.33, "normal": 25, "health_rate": 83.33}
  ]
}
```
**指标说明**:
- `online_rate`: 设备在线率
- `health_rate`: 设备完好率（正常状态占比）
- `availability_rate`: 综合可用率

### 4.3 获取30天趋势数据
```
GET /dashboard/trend
```
**响应数据**:
```json
{
  "daily_orders": [{"date": "2024-05-01", "count": 5}],
  "daily_repairs": [{"date": "2024-05-01", "count": 3}]
}
```

---

## 状态与优先级说明

### 设备状态
| 状态 | 说明 |
|------|------|
| 正常 | 设备正常运行 |
| 故障 | 设备出现故障待处理 |
| 维修中 | 设备正在维修 |
| 已修复 | 设备已修复完成 |

### 工单状态
| 状态 | 说明 |
|------|------|
| 待处理 | 工单已创建未处理 |
| 已处理 | 工单已处理完成 |

### 故障类型
| 类型 | 说明 |
|------|------|
| 硬件故障 | 硬件设备损坏 |
| 软件故障 | 系统软件问题 |
| 网络故障 | 网络连接问题 |
| 电源故障 | 供电系统问题 |
| 传感器故障 | 传感器异常 |
| 机械故障 | 机械结构问题 |
| 其他故障 | 其他未分类故障 |

### 故障等级
| 等级 | 说明 |
|------|------|
| 轻微 | 不影响正常使用 |
| 一般 | 部分功能受影响 |
| 严重 | 主要功能受影响 |
| 致命 | 完全无法使用 |

### 优先级（按港口作业影响程度）
| 优先级 | 权重 | 影响程度 | 前端显示建议 |
|--------|------|----------|--------------|
| 紧急 | 4 | 严重影响船舶作业，需立即处理 | 红色高亮 |
| 高 | 3 | 影响作业效率，需优先处理 | 橙色高亮 |
| 一般 | 2 | 不影响主要作业，按常规处理 | 正常显示 |
| 低 | 1 | 轻微问题，可延后处理 | 灰色显示 |

---

## 港区与作业区域

### 港区
- 港区A
- 港区B
- 港区C
- 港区D

### 作业区域
- 集装箱堆场
- 码头作业区
- 闸口通道
- 海关查验区
- 冷藏箱区

---

## 版本更新日志

### v3.0 (2024-05-15)
- ✅ **设备工单联动**: 创建工单时自动更新设备状态，工单自动关联设备详情
- ✅ **统一响应格式**: 所有接口统一 success/code/message/data 结构
- ✅ **多维度筛选**: 支持按港区、作业区域、故障类型、故障等级、优先级筛选
- ✅ **优先级高亮排序**: 工单按优先级自动排序，返回权重和高亮标识
- ✅ **维修履历增强**: 完整记录维修前后状态、处理时长、维修费用等
- ✅ **设备在线状态**: 新增设备在线/离线状态，支持心跳更新
- ✅ **设备完好率统计**: 在线率、完好率、综合可用率，按区域统计
- ✅ **趋势分析**: 30天工单和维修趋势数据
- ✅ **港区作业区域管理**: 设备归属港区和作业区域
- ✅ **故障等级分类**: 轻微/一般/严重/致命四级故障等级

### v2.0 (2024-05-15)
- ✅ 设备模块新增：设备型号、防护等级、设备序列号、投用日期
- ✅ 故障模块新增：按故障类型分类（7种类型）
- ✅ 故障模块新增：按港口作业影响程度标记紧急优先级（4级）
- ✅ 工单查询支持按故障类型、优先级、状态筛选
- ✅ 工单自动按优先级排序显示
- ✅ 新增故障类型和优先级枚举查询接口
- ✅ 运维记录同步保存故障类型和优先级信息
- ✅ 提供数据库迁移脚本，支持无缝升级
