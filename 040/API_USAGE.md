# 维修管理系统API使用说明

## 1. 多条件组合筛选 - 增强版

### 维修工单筛选参数
| 参数 | 说明 | 示例 |
|------|------|------|
| customer_name | 客户姓名（模糊搜索） | ?customer_name=张三 |
| customer_phone | 客户电话（模糊搜索） | ?customer_phone=138 |
| device_brand | 设备品牌（模糊搜索） | ?device_brand=苹果 |
| device_model | 设备型号（模糊搜索） | ?device_model=iPhone |
| device_type | 设备类型（单选） | ?device_type=phone |
| device_type_in | 设备类型（多选，逗号分隔） | ?device_type_in=phone,laptop |
| status | 工单状态（单选） | ?status=repairing |
| status_in | 工单状态（多选，逗号分隔） | ?status_in=pending,repairing |
| created_at_start | 创建时间开始 | ?created_at_start=2024-01-01 |
| created_at_end | 创建时间结束 | ?created_at_end=2024-12-31 |
| completed_at_start | 完成时间开始 | ?completed_at_start=2024-01-01 |
| completed_at_end | 完成时间结束 | ?completed_at_end=2024-12-31 |
| picked_up_at_start | 取机时间开始 | ?picked_up_at_start=2024-01-01 |
| picked_up_at_end | 取机时间结束 | ?picked_up_at_end=2024-12-31 |
| assigned_to | 分配工程师ID | ?assigned_to=2 |
| assigned_to_isnull | 是否未分配 | ?assigned_to_isnull=true |
| created_by | 创建人ID | ?created_by=1 |
| min_cost | 最小费用 | ?min_cost=100 |
| max_cost | 最大费用 | ?max_cost=500 |
| has_cost | 是否有费用 | ?has_cost=true |
| search | 综合搜索（工单号、客户、设备、故障） | ?search=屏幕 |
| order_number | 工单号（模糊） | ?order_number=WO2024 |
| fault_keyword | 故障关键词 | ?fault_keyword=黑屏 |
| is_overdue | 是否超期（7天未完成） | ?is_overdue=true |
| days_old | 创建天数 | ?days_old=30 |
| ordering | 排序字段 | ?ordering=-created_at |

### 客户筛选参数
| 参数 | 说明 | 示例 |
|------|------|------|
| name | 姓名（模糊） | ?name=张 |
| phone | 电话（模糊） | ?phone=138 |
| email | 邮箱（模糊） | ?email=@qq.com |
| address | 地址（模糊） | ?address=北京 |
| search | 综合搜索 | ?search=张三 |
| created_at_start | 创建时间开始 | ?created_at_start=2024-01-01 |
| created_at_end | 创建时间结束 | ?created_at_end=2024-12-31 |
| has_device | 是否有设备 | ?has_device=true |
| has_active_order | 是否有活跃工单 | ?has_active_order=true |
| min_devices | 最少设备数 | ?min_devices=2 |

### 设备筛选参数
| 参数 | 说明 | 示例 |
|------|------|------|
| customer_name | 客户姓名（模糊） | ?customer_name=张 |
| customer_phone | 客户电话（模糊） | ?customer_phone=138 |
| brand | 品牌（模糊） | ?brand=苹果 |
| model | 型号（模糊） | ?model=iPhone 15 |
| serial_number | 序列号（模糊） | ?serial_number=ABC123 |
| device_type | 设备类型（单选） | ?device_type=phone |
| device_type_in | 设备类型（多选） | ?device_type_in=phone,laptop |
| has_active_order | 是否有活跃工单 | ?has_active_order=true |
| description | 设备描述关键词 | ?description=全新 |
| search | 综合搜索 | ?search=苹果 |

### 通知筛选参数
| 参数 | 说明 | 示例 |
|------|------|------|
| is_read | 是否已读 | ?is_read=false |
| notification_type | 通知类型 | ?notification_type=repair_completed |
| notification_type_in | 通知类型多选 | ?notification_type_in=repair_completed,system |
| created_at_start | 创建时间开始 | ?created_at_start=2024-01-01 |
| created_at_end | 创建时间结束 | ?created_at_end=2024-12-31 |
| search | 搜索标题内容 | ?search=工单 |

### 示例组合查询
```
GET /api/repair-orders/?customer_name=张&device_type_in=phone,laptop&status_in=pending,repairing&is_overdue=true&ordering=-created_at
```

## 2. 分页功能

### 分页参数
| 参数 | 说明 | 默认值 | 最大值 |
|------|------|--------|--------|
| page | 页码 | 1 | - |
| page_size | 每页数量 | 10 | 100 |

### 响应格式
```json
{
  "count": 100,
  "page_count": 10,
  "current_page": 1,
  "page_size": 10,
  "next": "http://localhost:8000/api/repair-orders/?page=2",
  "previous": null,
  "results": [...]
}
```

### 示例
```
GET /api/repair-orders/?page=1&page_size=20
```

## 3. 派单冲突校验

### 查看所有工程师工作负载
```
GET /api/repair-orders/engineer_workload/
```

响应：
```json
[
  {
    "engineer_id": 2,
    "engineer_name": "engineer1",
    "active_orders": 5,
    "max_orders": 10,
    "available_slots": 5
  }
]
```

### 检查特定工单是否可以分配给工程师
```
GET /api/repair-orders/{id}/check_assignment_conflict/?engineer_id=2
```

响应：
```json
{
  "conflict": false,
  "active_orders": 5,
  "max_orders": 10,
  "available_slots": 5,
  "message": "可以分配"
}
```

### 派单规则
- 只能将工单分配给"工程师"角色的用户
- 每个工程师最多同时有10个活跃工单（pending, diagnosing, repairing, waiting_parts）
- 工程师活跃工单达到上限时会自动阻止分配

## 4. 维修完成自动通知

### 通知触发时机
1. **工单状态变为"已完成"**：自动通知前台和管理员
2. **工单分配给工程师**：自动通知被分配的工程师
3. **工单已取机**：自动通知前台和管理员
4. **工单已归档**：自动通知所有管理员

### 通知类型
- `repair_completed`: 维修完成
- `order_assigned`: 工单分配
- `status_changed`: 状态变更
- `system`: 系统通知

## 5. 取机与自动归档功能

### 取机（支持自动归档）
```
POST /api/repair-orders/{id}/pick_up/
```

请求体：
```json
{
  "auto_archive": true
}
```

响应：
```json
{
  "status": "取机成功并已自动归档",
  "archived": true
}
```

### 单个工单归档
```
POST /api/repair-orders/{id}/archive/
```

响应：
```json
{
  "status": "归档成功",
  "order_number": "WO202405160001"
}
```

### 查看待归档工单列表
```
GET /api/repair-orders/archive_candidates/?days=7
```

响应：
```json
{
  "count": 5,
  "days": 7,
  "candidates": [...]
}
```

### 批量自动归档（管理员）
```
POST /api/repair-orders/auto_archive/
```

请求体：
```json
{
  "days": 7
}
```

响应：
```json
{
  "status": "成功归档3个工单",
  "archived_count": 3,
  "archived_orders": ["WO202405100001", "WO202405110002", "WO202405120003"],
  "days": 7
}
```

### 归档规则
- 只有状态为"picked_up"（已取机）的工单才能归档
- 批量归档默认归档已取机超过7天的工单
- 归档天数可以通过`days`参数自定义
- 归档后会创建系统通知告知所有管理员

## 6. 通知管理增强

### 获取未读通知数量
```
GET /api/notifications/unread_count/
```

响应：
```json
{
  "unread_count": 5
}
```

### 获取最近通知（无需分页）
```
GET /api/notifications/recent/?limit=10
```

### 标记单个通知为已读
```
POST /api/notifications/{id}/mark_read/
```

### 标记全部通知为已读
```
POST /api/notifications/mark_all_read/
```

响应：
```json
{
  "status": "全部标记为已读",
  "updated_count": 3
}
```

### 标记选中通知为已读
```
POST /api/notifications/mark_selected_read/
```

请求体：
```json
{
  "ids": [1, 2, 3]
}
```

响应：
```json
{
  "status": "已标记选中通知为已读",
  "updated_count": 3
}
```

## 7. 必填字段校验

### 客户 (Customer)
- `name`: 客户姓名（必填，不能为空）
- `phone`: 联系电话（必填，7-20位）

### 设备 (Device)
- `customer`: 所属客户（必填）
- `device_type`: 设备类型（必填）
- `brand`: 品牌（必填，不能为空）
- `model`: 型号（必填，不能为空）

### 维修工单 (RepairOrder)
- `customer`: 客户（必填）
- `device`: 设备（必填）
- `fault_description`: 故障描述（必填，不能为空）

## 8. 金额合法性校验

### 费用规则
- `estimated_cost`（预估费用）: 不能为负数，最大值 999999.99
- `actual_cost`（实际费用）: 不能为负数，最大值 999999.99

### 错误响应示例
```json
{
  "estimated_cost": ["预估费用不能为负数"],
  "actual_cost": ["实际费用超出最大限制"]
}
```

## 9. 其他校验规则

### 设备-客户一致性
- 创单或更新时会校验设备是否属于所选客户
- 不一致时返回：`{"device": ["该设备不属于所选客户"]}`

### 工程师角色校验
- 只能将工单分配给工程师角色用户
- 错误时返回：`{"assigned_to": ["只能将工单分配给工程师角色的用户"]}`
