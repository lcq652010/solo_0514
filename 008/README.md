# 传统毛笔定制订单管理系统后端

基于 Python + Flask + SQLite 实现的传统毛笔定制订单管理系统后端。

## 功能特性

- 客户提交毛笔定制订单
- 订单自动编号（格式：MB + 日期 + 4位序号，如 MB202605150001）
- 管理员查看和管理所有订单
- 修改订单制作进度（7种状态）
- **必填校验与数值规范** - 完善的表单验证
- **自动计价** - 按材料与工艺难度自动计算价格
- **匠人绑定** - 支持分配匠人及工期管理
- **筛选分页** - 按款式、进度、交付日期筛选，支持分页排序
- **统一接口返回格式** - 标准的成功/错误响应

## 订单状态

- 待接单、选料、理毛、修毫、装杆、整笔、完工

## 难度等级

- 简单、普通、中等、复杂、极难

## 毫毛类型及基础价格

| 类型 | 价格（元） |
|------|-----------|
| 狼毫 | 50 |
| 羊毫 | 30 |
| 兼毫 | 40 |
| 紫毫 | 80 |
| 鸡毫 | 25 |
| 鼠毫 | 60 |
| 鹿毫 | 45 |

## 笔杆材质及基础价格

| 材质 | 价格（元） |
|------|-----------|
| 竹制 | 20 |
| 红木 | 80 |
| 紫檀 | 150 |
| 牛角 | 100 |
| 象牙 | 200 |
| 檀木 | 120 |
| 鸡翅木 | 60 |

## 安装运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py
```

服务将在 http://localhost:5000 启动

## 统一接口返回格式

### 成功响应
```json
{
  "success": true,
  "code": 200,
  "message": "操作成功",
  "data": { ... },
  "timestamp": "2026-05-15 12:00:00"
}
```

### 错误响应
```json
{
  "success": false,
  "code": 400,
  "message": "数据验证失败",
  "errors": ["客户姓名不能为空", "客户电话格式不正确"],
  "timestamp": "2026-05-15 12:00:00"
}
```

## API 接口

### 1. 创建订单
- **POST** `/api/orders`
- 请求体示例：
```json
{
  "customer_name": "张三",
  "customer_phone": "13800138000",
  "customer_address": "北京市朝阳区",
  "brush_type": "大楷笔",
  "brush_size": "大号",
  "hair_type": "狼毫",
  "tip_length": "4.5cm",
  "handle_material": "红木",
  "handle_size": "25cm",
  "grooming_spec": "按毫毛长短分层梳理，去除杂毛，保证毛锋顺直",
  "trimming_spec": "修毫时保持锋尖尖锐，锋长误差控制在±1mm内",
  "mounting_spec": "笔杆与笔头接合处需牢固，涂胶均匀，外观平整",
  "quantity": 10,
  "difficulty": "中等",
  "requirements": "适合楷书练习，手感舒适"
}
```

**必填字段校验**：
- `customer_name` - 客户姓名不能为空
- `customer_phone` - 客户电话不能为空，且格式为11位手机号
- `brush_type` - 毛笔款式不能为空
- `hair_type` - 毫毛类型不能为空
- `handle_material` - 笔杆材质不能为空
- `quantity` - 数量不能为空，必须是1-100之间的正整数

### 2. 获取订单列表（支持筛选、分页、排序）
- **GET** `/api/orders`

**查询参数**：
| 参数 | 说明 | 示例 |
|------|------|------|
| `page` | 页码，默认1 | ?page=2 |
| `per_page` | 每页数量，默认10，最大100 | ?per_page=20 |
| `brush_type` | 按款式筛选 | ?brush_type=大楷 |
| `status` | 按进度筛选 | ?status=理毛 |
| `delivery_date_start` | 交付日期起始 | ?delivery_date_start=2026-05-20 |
| `delivery_date_end` | 交付日期结束 | ?delivery_date_end=2026-06-01 |
| `sort_by` | 排序字段 | ?sort_by=total_price |
| `sort_order` | 排序方向：asc/desc | ?sort_order=asc |

**示例**：
```
GET /api/orders?page=1&per_page=20&status=理毛&sort_by=delivery_date&sort_order=asc
```

**响应数据**：
```json
{
  "success": true,
  "code": 200,
  "message": "获取订单列表成功",
  "data": {
    "orders": [...],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 100,
      "pages": 10,
      "has_next": true,
      "has_prev": false
    }
  },
  "timestamp": "2026-05-15 12:00:00"
}
```

### 3. 获取单个订单详情
- **GET** `/api/orders/<order_no>`

### 4. 更新订单状态
- **PUT** `/api/orders/<order_no>/status`
- 请求体：`{"status": "选料"}`

### 5. 绑定匠人
- **PUT** `/api/orders/<order_no>/craftsman`
- 请求体：`{"craftsman_id": 1}`

### 6. 更新订单信息
- **PUT** `/api/orders/<order_no>`
- 支持更新所有字段，修改材料/难度/数量时会自动重新计价

### 7. 删除订单
- **DELETE** `/api/orders/<order_no>`

### 8. 获取所有状态列表
- **GET** `/api/statuses`

### 9. 获取匠人列表
- **GET** `/api/craftsmen`

### 10. 获取价格配置
- **GET** `/api/price-config`

## 自动计价规则

```
单价 = (毫毛价格 + 笔杆价格) × 难度系数
总价 = 单价 × 数量
```

| 难度 | 系数 | 基础工期 |
|------|------|---------|
| 简单 | 1.0 | 3天 |
| 普通 | 1.2 | 5天 |
| 中等 | 1.5 | 7天 |
| 复杂 | 2.0 | 10天 |
| 极难 | 2.5 | 15天 |

**工期额外增加**：每增加5支，工期增加1天
