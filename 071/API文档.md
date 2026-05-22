# 砚台定制后端 API 文档

## 基础信息
- 基础 URL: `http://localhost:5000/api`
- 数据格式: JSON
- 数据库: SQLite (inkstone.db)
- 文件上传目录: `uploads/`

## 订单状态流转
```
待分配 → 采石 → 切坯 → 凿池 → 刻砚 → 细磨 → 封蜡 → 已完成
```

## 石质密度表
| 石材类型 | 密度 (g/cm³) |
|---------|-------------|
| 端溪石 | 2.75 |
| 歙石 | 2.8 |
| 洮河石 | 2.65 |
| 澄泥砚 | 2.4 |
| 红丝石 | 2.7 |
| 松花石 | 2.6 |
| 其他 | 2.7 |

---

## 客户管理

### 创建客户
- **接口**: `POST /customers`
- **请求体**:
```json
{
    "name": "客户姓名",
    "phone": "联系电话",
    "address": "地址（可选）"
}
```

### 查询所有客户
- **接口**: `GET /customers`

---

## 匠人管理

### 创建匠人
- **接口**: `POST /craftsmen`
- **请求体**:
```json
{
    "name": "匠人姓名",
    "phone": "联系电话",
    "skill_level": "技能等级（可选）",
    "status": "available（可选，默认空闲）"
}
```

### 查询所有匠人
- **接口**: `GET /craftsmen`

---

## 重量预估计算

### 预估砚台重量
- **接口**: `POST /calculate-weight`
- **说明**: 根据石材类型和尺寸自动计算预估体积和重量
- **请求体**:
```json
{
    "material": "端溪石",
    "length": 20,
    "width": 15,
    "thickness": 3
}
```
- **返回示例**:
```json
{
    "material": "端溪石",
    "stone_density": 2.75,
    "length_cm": 20,
    "width_cm": 15,
    "thickness_cm": 3,
    "estimated_volume_cm3": 0.9,
    "estimated_weight_g": 247.5,
    "estimated_weight_kg": 0.248,
    "unit": "密度单位: g/cm³, 体积单位: cm³, 重量单位: g"
}
```

---

## 订单管理

### 创建订单（客户下单）
- **接口**: `POST /orders`
- **说明**: 系统自动生成唯一订单编号，并根据尺寸和材质自动计算预估重量
- **请求体**:
```json
{
    "customer_id": 1,
    "inkstone_type": "端砚",
    "size": "20cm x 15cm x 3cm（可选）",
    "length": 20,
    "width": 15,
    "thickness": 3,
    "material": "端溪石",
    "stone_origin": "石料产地（可选，如：广东肇庆端溪）",
    "hardness": "硬度标注（可选，如：摩氏硬度 3.5-4.0）",
    "inscription_text": "定制落款文字（可选，如：宁静致远）",
    "design_description": "设计描述（可选）"
}
```

### 分配匠人（管理员）
- **接口**: `POST /orders/{order_id}/assign`
- **请求体**:
```json
{
    "craftsman_id": 1
}
```

### 开始工序
- **接口**: `POST /orders/{order_id}/process/{process_code}/start`
- **说明**: 记录工序开始时间，工序状态变为"进行中"
- **工序代码**: quarrying(采石), cutting(切坯), carving_pool(凿池), engraving(刻砚), polishing(细磨), waxing(封蜡)

### 完成工序
- **接口**: `POST /orders/{order_id}/process/{process_code}/complete`
- **说明**: 记录工序完成时间，自动计算耗时，并流转到下一工序
- **请求体**:
```json
{
    "notes": "工序备注（可选）"
}
```

### 流转到下一状态（快速方式）
- **接口**: `POST /orders/{order_id}/next-status`
- **说明**: 按采石→切坯→凿池→刻砚→细磨→封蜡顺序自动流转，自动记录工序时间

### 查询所有订单
- **接口**: `GET /orders`

### 查询单个订单详情
- **接口**: `GET /orders/{order_id}`
- **返回字段说明**:
  - `stone_origin`: 石料产地
  - `hardness`: 硬度标注
  - `stone_density`: 石质密度
  - `estimated_volume_cm3`: 预估体积
  - `estimated_weight_g`: 预估重量（克）
  - `estimated_weight_kg`: 预估重量（千克）
  - `inscription_text`: 定制落款文字
  - `sketch_filename`: 设计草图文件名
  - `sketch_url`: 设计草图访问地址
  - `process_records`: 工序记录列表

### 查询订单状态流程
- **接口**: `GET /orders/{order_id}/status`

### 查看单个订单工时报表
- **接口**: `GET /orders/{order_id}/work-report`
- **返回示例**:
```json
{
    "order_id": 1,
    "order_number": "YAN202605160001",
    "inkstone_type": "端砚",
    "craftsman_name": "李四",
    "status": "已完成",
    "estimated_weight_g": 247.5,
    "estimated_weight_kg": 0.248,
    "total_processes": 6,
    "completed_processes": 6,
    "total_duration_hours": 0.02,
    "total_duration_text": "0.02 小时",
    "process_records": [
        {
            "process_code": "quarrying",
            "process_name": "采石",
            "status": "completed",
            "status_text": "已完成",
            "start_time": "2026-05-16T03:06:40.123456",
            "end_time": "2026-05-16T03:06:41.123456",
            "duration_hours": 0.0003,
            "duration_text": "0.0003 小时",
            "notes": "采石完成，石材质量优良"
        }
    ],
    "generated_at": "2026-05-16T03:06:50.123456"
}
```

### 查询所有订单工时报表
- **接口**: `GET /work-reports`
- **查询参数（可选）**:
  - `start_date`: 开始日期（ISO格式）
  - `end_date`: 结束日期（ISO格式）
- **返回示例**:
```json
{
    "total_orders": 1,
    "reports": [
        {
            "order_id": 1,
            "order_number": "YAN202605160001",
            "inkstone_type": "端砚",
            "craftsman_name": "李四",
            "status": "已完成",
            "estimated_weight_kg": 0.248,
            "total_processes": 6,
            "completed_processes": 6,
            "total_duration_hours": 0.02,
            "created_at": "2026-05-16T03:06:39.123456"
        }
    ]
}
```

---

## 设计草图管理

### 上传设计草图
- **接口**: `POST /orders/{order_id}/upload-sketch`
- **Content-Type**: `multipart/form-data`
- **请求参数**:
  - `sketch`: 图片文件（支持 png, jpg, jpeg, gif, bmp 格式，最大 16MB）

### 访问设计草图
- **接口**: `GET /orders/{order_id}/sketch`
- **说明**: 直接返回图片文件，可在浏览器中显示

### 删除设计草图
- **接口**: `DELETE /orders/{order_id}/sketch`
- **说明**: 删除订单关联的设计草图文件

---

## Order 表新增字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| length | Float | 长度 (cm) |
| width | Float | 宽度 (cm) |
| thickness | Float | 厚度 (cm) |
| stone_origin | VARCHAR(200) | 石料产地，如"广东肇庆端溪" |
| hardness | VARCHAR(50) | 硬度标注，如"摩氏硬度 3.5-4.0" |
| stone_density | Float | 石质密度 (g/cm³) |
| estimated_weight | Float | 预估重量 (g) |
| actual_weight | Float | 实际重量 (g) |
| estimated_volume | Float | 预估体积 (cm³) |
| inscription_text | VARCHAR(200) | 定制落款文字 |
| sketch_filename | VARCHAR(255) | 设计草图文件名 |

---

## ProcessRecord 表结构

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | Integer | 主键 |
| order_id | Integer | 订单ID（外键） |
| process_name | VARCHAR(50) | 工序名称 |
| process_code | VARCHAR(50) | 工序代码 |
| start_time | DateTime | 开工时间 |
| end_time | DateTime | 完工时间 |
| duration_hours | Float | 耗时（小时） |
| craftsman_id | Integer | 匠人ID（外键） |
| notes | Text | 工序备注 |
| status | VARCHAR(20) | 状态: pending(待开始), in_progress(进行中), completed(已完成) |
| created_at | DateTime | 创建时间 |
