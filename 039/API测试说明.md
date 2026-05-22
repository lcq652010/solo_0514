# 税务大厅自助发票代开终端运维管理系统 - API 接口说明 (v3.0)

## 运行项目

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 启动服务：
```bash
python app.py
```

服务地址：http://127.0.0.1:5000

默认管理员账号：`admin` / `admin123`

---

## 统一接口响应格式

所有接口统一使用以下响应格式：

```json
{
    "code": 200,
    "success": true,
    "message": "操作成功",
    "timestamp": "2024-05-16 10:30:00",
    "data": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | HTTP状态码 (200成功, 400参数错误, 401未授权, 404不存在, 500服务器错误) |
| success | bool | 是否成功 |
| message | string | 操作消息说明 |
| timestamp | string | 响应时间戳 |
| data | any | 响应数据（可选） |

---

## v3.0 新增优化功能

### ✨ 统一接口响应格式
- 标准化返回字段（code、success、message、timestamp、data）
- 全局异常处理（404、500错误统一响应）

### 🏢 按大厅区域筛选
- 设备列表支持按所在区域模糊筛选
- 工单列表支持按设备所在区域筛选
- 运维记录支持按设备所在区域筛选
- 新增 `/api/devices/locations` 获取所有区域列表

### 🚨 多维度组合筛选（工单模块）
- 按故障类型筛选
- 按紧急优先级筛选
- 按处理状态筛选
- 按处理人员筛选
- 按设备编号模糊搜索
- 按大厅区域筛选
- 多条件组合筛选

### 📊 设备可用率统计
- 系统整体设备可用率
- 按区域统计设备可用率
- 工单完成率统计
- 优先级分布统计
- 故障类型分布统计

### 📄 分页查询支持
- 设备列表分页
- 工单列表分页
- 运维记录列表分页
- 支持自定义每页数量

---

## API 接口列表

### 1. 系统配置接口

#### 1.1 获取枚举配置
**GET** `/api/config/enums`

获取系统所有枚举常量定义：
- `device_status_options`: 设备状态选项
- `order_status_options`: 工单状态选项
- `fault_types`: 故障类型列表
- `priority_levels`: 优先级选项
- `communication_methods`: 通信方式选项

### 2. 设备管理

#### 2.1 录入设备
**POST** `/api/devices`

请求体：
```json
{
    "device_code": "DEVICE001",
    "device_name": "自助发票代开终端1号",
    "device_model": "TAX-2024-PRO",
    "communication_method": "有线网络",
    "location": "一楼大厅A区",
    "status": "正常",
    "install_date": "2024-01-01",
    "commission_date": "2024-01-15",
    "remark": "支持电子发票和纸质发票打印"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| device_code | ✅ | 设备编号（唯一） |
| device_name | ✅ | 设备名称 |
| device_model | ⭕ | 设备型号（新增） |
| communication_method | ⭕ | 通信方式：有线网络/无线网络/4G/5G/其他（新增） |
| location | ✅ | 所在区域 |
| status | ⭕ | 状态：正常/故障/维修中/已修复，默认正常 |
| install_date | ⭕ | 安装日期 |
| commission_date | ⭕ | 投用日期（新增） |
| remark | ⭕ | 备注 |

#### 2.2 查询设备列表（支持分页和筛选）
**GET** `/api/devices`

查询参数：
| 参数 | 说明 | 示例 |
|------|------|------|
| status | 设备状态 | ?status=正常 |
| device_code | 设备编号模糊搜索 | ?device_code=DEVICE |
| device_model | 设备型号模糊搜索 | ?device_model=PRO |
| communication_method | 通信方式筛选 | ?communication_method=5G |
| location | 所在区域模糊搜索 | ?location=一楼大厅 |
| page | 页码，默认1 | ?page=2 |
| page_size | 每页数量，默认20 | ?page_size=50 |

**响应数据结构：**
```json
{
    "code": 200,
    "success": true,
    "message": "设备列表查询成功",
    "data": {
        "list": [...],
        "pagination": {
            "page": 1,
            "page_size": 20,
            "total": 100,
            "total_pages": 5
        }
    }
}
```

#### 2.3 获取区域列表
**GET** `/api/devices/locations`

获取系统中所有设备所在的区域列表，用于下拉筛选。

#### 2.4 查询单个设备详情
**GET** `/api/devices/{device_id}`

#### 2.5 更新设备信息
**PUT** `/api/devices/{device_id}`

支持更新所有设备字段，包括设备型号、通信方式、投用日期等新增字段。

#### 2.6 更新设备状态
**PUT** `/api/devices/{device_id}/status`

请求体：
```json
{
    "status": "维修中"
}
```

### 3. 工单管理（故障上报与处理）

#### 3.1 故障上报（创建工单）
**POST** `/api/work-orders`

请求体（增强字段已标记⭐）：
```json
{
    "device_id": 1,
    "fault_type": "打印机故障",
    "fault_description": "打印机卡纸，无法打印发票",
    "priority": "高",
    "business_impact": "导致发票开具业务中断，已影响5名纳税人正常办税",
    "reporter": "张三",
    "reporter_phone": "13800138000"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| device_id | ✅ | 设备ID |
| fault_type | ⭕ | 故障类型：硬件故障/软件故障/网络故障/打印机故障/触摸屏故障/读卡器故障/电源故障/其他故障 |
| fault_description | ✅ | 故障描述 |
| priority | ⭕ | 紧急优先级：高/中/低，默认为"中" |
| business_impact | ⭕ | 税务业务影响程度描述 |
| reporter | ⭕ | 上报人 |
| reporter_phone | ⭕ | 上报人电话 |

**说明**：创建工单后，设备状态自动变为"故障"

#### 3.2 查询工单列表（支持多维度筛选和分页）
**GET** `/api/work-orders`

查询参数：
| 参数 | 说明 | 示例 |
|------|------|------|
| status | 工单状态：待处理/处理中/已完成 | ?status=待处理 |
| device_code | 设备编号模糊搜索 | ?device_code=DEVICE |
| fault_type | 故障类型筛选 | ?fault_type=打印机故障 |
| priority | 优先级筛选 | ?priority=高 |
| location | 设备所在区域模糊搜索 | ?location=一楼大厅 |
| handler | 处理人员模糊搜索 | ?handler=张工程师 |
| page | 页码，默认1 | ?page=2 |
| page_size | 每页数量，默认20 | ?page_size=50 |

**排序规则**：按优先级降序（高→中→低），同优先级按创建时间降序

**示例：组合筛选高优先级打印机故障**
```
/api/work-orders?priority=高&fault_type=打印机故障&location=一楼大厅
```

#### 3.3 查询单个工单详情
**GET** `/api/work-orders/{order_no}`

#### 3.4 处理工单
**PUT** `/api/work-orders/{order_no}/handle`

请求体：
```json
{
    "status": "处理中",
    "handler": "张工程师",
    "handle_result": "正在排查问题，已联系硬件供应商"
}
```

**状态流转说明**：
- 设为"处理中"时，设备状态自动变为"维修中"
- 设为"已完成"时，设备状态自动变为"已修复"，并自动生成运维记录

### 4. 运维记录管理

#### 4.1 查询运维记录
**GET** `/api/maintain-records`

查询参数：
| 参数 | 说明 | 示例 |
|------|------|------|
| device_code | 设备编号模糊搜索 | ?device_code=DEVICE |
| start_date | 开始日期（格式：YYYY-MM-DD） | ?start_date=2024-01-01 |
| end_date | 结束日期 | ?end_date=2024-12-31 |
| maintain_type | 维护类型筛选 | ?maintain_type=故障维修 |
| location | 设备所在区域模糊搜索 | ?location=一楼大厅 |
| page | 页码，默认1 | ?page=2 |
| page_size | 每页数量，默认20 | ?page_size=50 |

#### 4.2 添加运维记录（手动）
**POST** `/api/maintain-records`

请求体：
```json
{
    "device_id": 1,
    "maintain_type": "日常保养",
    "maintain_content": "清洁设备、检查线路、测试打印功能",
    "maintainer": "王师傅",
    "maintain_time": "2024-05-16 10:00:00",
    "remark": "设备运行正常，各项功能测试通过"
}
```

### 5. 统计面板（增强版）
**GET** `/api/dashboard/statistics`

**响应数据（含设备可用率统计）：**
```json
{
    "code": 200,
    "success": true,
    "message": "统计数据查询成功",
    "data": {
        "device_stats": {
            "total": 10,
            "normal": 7,
            "fault": 1,
            "repairing": 2,
            "repaired": 0,
            "availability_rate": 70.00
        },
        "order_stats": {
            "pending": 3,
            "processing": 2,
            "completed": 5,
            "total": 10,
            "completion_rate": 50.00
        },
        "priority_stats": [
            {"priority": "高", "count": 2},
            {"priority": "中", "count": 5},
            {"priority": "低", "count": 3}
        ],
        "fault_type_stats": [
            {"fault_type": "打印机故障", "count": 4},
            {"fault_type": "触摸屏故障", "count": 2},
            {"fault_type": "网络故障", "count": 2}
        ],
        "location_stats": [
            {
                "location": "一楼大厅A区",
                "total": 3,
                "normal": 2,
                "availability_rate": 66.67
            },
            {
                "location": "二楼办税厅",
                "total": 2,
                "normal": 2,
                "availability_rate": 100.00
            }
        ]
    }
}
```

**统计指标说明：**
- `availability_rate`: 设备可用率 = 正常设备数 / 总设备数 × 100%
- `completion_rate`: 工单完成率 = 已完工单数 / 总工单数 × 100%
- `location_stats`: 按区域分组的设备可用率统计

### 6. 管理员登录
**POST** `/api/admins/login`

请求体：
```json
{
    "username": "admin",
    "password": "admin123"
}
```

---

## 枚举值参考

### 设备状态（device_status_options）
| 值 | 说明 |
|----|------|
| 正常 | 设备运行正常 |
| 故障 | 设备出现故障，已上报 |
| 维修中 | 正在处理故障 |
| 已修复 | 故障已处理完成 |

### 工单状态（order_status_options）
| 值 | 说明 |
|----|------|
| 待处理 | 工单创建，未开始处理 |
| 处理中 | 正在处理故障 |
| 已完成 | 工单处理完成 |

### 故障类型（fault_types）
| 值 | 说明 |
|----|------|
| 硬件故障 | 通用硬件问题 |
| 软件故障 | 系统或应用软件问题 |
| 网络故障 | 网络连接问题 |
| 打印机故障 | 打印设备故障 |
| 触摸屏故障 | 触摸显示屏故障 |
| 读卡器故障 | 身份证/读卡器故障 |
| 电源故障 | 电源供电问题 |
| 其他故障 | 其他未分类故障 |

### 优先级（priority_levels）
| 值 | 税务业务影响程度 |
|----|----------------|
| 高 | 导致核心业务中断，严重影响办税大厅正常秩序 |
| 中 | 影响用户体验，但业务尚可继续进行 |
| 低 | 轻微问题，基本不影响正常业务办理 |

### 通信方式（communication_methods）
| 值 | 说明 |
|----|------|
| 有线网络 | 网线连接 |
| 无线网络 | WiFi连接 |
| 4G | 4G移动网络 |
| 5G | 5G移动网络 |
| 其他 | 其他通信方式 |

---

## 工单编号规则

格式：`WO` + 日期(8位) + 序号(4位)

示例：`WO202405160001`

---

## 快速测试

运行自动化测试脚本验证所有功能：

```bash
python test_api.py
```

该脚本会自动测试：
- ✓ 统一接口响应格式
- ✓ 设备新增字段（型号、通信方式、投用日期）
- ✓ 区域列表查询
- ✓ 按区域筛选功能
- ✓ 故障类型和优先级标记
- ✓ 多维度组合筛选
- ✓ 工单按优先级智能排序
- ✓ 设备可用率统计（整体+按区域）
- ✓ 分页查询功能
