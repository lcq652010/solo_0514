# 传统竹雕笔搁定制订单管理系统 - API文档 v2.0

## 启动说明

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

3. 服务启动后访问：http://localhost:5000

## 统一返回格式

### 成功响应
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {},
  "success": true
}
```

### 失败响应
```json
{
  "code": 400,
  "message": "错误信息",
  "data": null,
  "success": false
}
```

## 基础配置说明

### 竹材类型（8种）
| 竹材 | 基础价格 | 难度系数 |
|------|---------|---------|
| 毛竹 | ¥80 | 1.0 |
| 刚竹 | ¥100 | 1.2 |
| 紫竹 | ¥150 | 1.5 |
| 斑竹 | ¥180 | 1.6 |
| 湘妃竹 | ¥220 | 1.8 |
| 罗汉竹 | ¥250 | 2.0 |
| 方竹 | ¥280 | 2.2 |
| 金丝竹 | ¥320 | 2.5 |

### 雕刻纹样（10种）
| 纹样 | 基础价格 | 难度系数 | 工期(天) |
|------|---------|---------|---------|
| 梅兰竹菊 | ¥200 | 2.0 | 3 |
| 山水风景 | ¥350 | 3.0 | 5 |
| 花鸟虫鱼 | ¥280 | 2.5 | 4 |
| 龙凤呈祥 | ¥500 | 4.0 | 7 |
| 福寿图案 | ¥250 | 2.0 | 3 |
| 云纹 | ¥150 | 1.5 | 2 |
| 回纹 | ¥180 | 1.5 | 2 |
| 人物故事 | ¥450 | 4.0 | 6 |
| 书法文字 | ¥200 | 2.0 | 3 |
| 定制图案 | ¥400 | 3.5 | 5 |

### 匠人团队（5人）
| ID | 姓名 | 级别 | 专长 | 日产量 |
|----|------|------|------|--------|
| 1 | 张师傅 | 高级 | 精雕 | 2件 |
| 2 | 李师傅 | 中级 | 打磨 | 3件 |
| 3 | 王师傅 | 高级 | 上漆 | 4件 |
| 4 | 赵师傅 | 中级 | 粗雕 | 3件 |
| 5 | 陈师傅 | 特级 | 全工序 | 1件 |

### 订单状态（8种）
待接单 → 选竹 → 锯坯 → 粗雕 → 精雕 → 打磨 → 上漆 → 完工

## API接口列表

### 1. 获取所有配置选项
- **接口**: `GET /api/options`
- **说明**: 获取竹材类型、雕刻纹样、放置弧度、订单状态、匠人列表等所有配置
- **响应示例**:
```json
{
  "code": 200,
  "message": "获取选项成功",
  "data": {
    "bamboo_types": [{"name": "毛竹", "price": 80, "difficulty": 1}],
    "carving_patterns": [{"name": "梅兰竹菊", "price": 200, "difficulty": 2, "days": 3}],
    "placement_curves": ["平直(0°)", "微弧(5°-10°)"],
    "statuses": ["待接单", "选竹", "锯坯"],
    "craftsmen": [{"id": 1, "name": "张师傅", "skill_level": "高级"}]
  },
  "success": true
}
```

### 2. 订单计价预览
- **接口**: `POST /api/calculate`
- **说明**: 创建订单前预览价格和工期
- **请求参数**:
```json
{
  "bamboo_type": "紫竹",
  "carving_pattern": "龙凤呈祥",
  "quantity": 2
}
```
- **响应示例**:
```json
{
  "code": 200,
  "message": "计价成功",
  "data": {
    "unit_price": 1085.0,
    "total_price": 2170.0,
    "carving_difficulty": 6.0,
    "estimated_days": 7
  },
  "success": true
}
```

### 3. 创建订单（含必填校验）
- **接口**: `POST /api/orders`
- **说明**: 客户提交定制需求，自动计价和计算工期
- **必填字段**: customer_name, customer_phone, design_requirements, bamboo_type, carving_pattern, length_cm, width_cm, thickness_cm
- **请求参数**:
```json
{
  "customer_name": "张三",
  "customer_phone": "13800138000",
  "customer_address": "北京市朝阳区",
  "design_requirements": "精细雕刻，仿古风格",
  "bamboo_type": "紫竹",
  "carving_pattern": "龙凤呈祥",
  "placement_curve": "微弧(5°-10°)",
  "length_cm": 20.5,
  "width_cm": 5.2,
  "thickness_cm": 2.0,
  "quantity": 2,
  "budget": 2500,
  "remark": "加急订单"
}
```
- **验证规则**:
  - 手机号必须为11位数字
  - 尺寸必须为正数且不超过100cm
  - 竹材类型和雕刻纹样必须在可选范围内

### 4. 获取订单列表（支持筛选、分页、排序）
- **接口**: `GET /api/orders`
- **查询参数**:
  | 参数 | 说明 | 示例 |
  |------|------|------|
  | page | 页码 | 1 |
  | page_size | 每页数量 | 10 |
  | status | 按状态筛选 | 精雕 |
  | bamboo_type | 按竹材筛选 | 紫竹 |
  | carving_pattern | 按雕刻题材筛选 | 龙凤呈祥 |
  | delivery_date_start | 交付日期开始 | 2024-01-01 |
  | delivery_date_end | 交付日期结束 | 2024-12-31 |
  | keyword | 搜索关键词（订单号/客户名/手机号） | 张三 |
  | sort_by | 排序字段 | created_at / delivery_date / total_price |
  | sort_order | 排序方式 | asc / desc |
- **示例**:
  - 分页查询: `/api/orders?page=1&page_size=10`
  - 状态筛选 + 按价格排序: `/api/orders?status=精雕&sort_by=total_price&sort_order=desc`
  - 按题材筛选: `/api/orders?carving_pattern=山水风景`
  - 按交付日期范围查询: `/api/orders?delivery_date_start=2024-06-01&delivery_date_end=2024-06-30`

### 5. 获取单个订单详情
- **接口**: `GET /api/orders/<order_no>`
- **示例**: `/api/orders/BD202405160001`

### 6. 更新订单制作进度
- **接口**: `PUT /api/orders/<order_no>/status`
- **请求参数**:
```json
{
  "status": "精雕"
}
```

### 7. 绑定匠人到订单
- **接口**: `PUT /api/orders/<order_no>/craftsman`
- **请求参数**:
```json
{
  "craftsman_id": 1
}
```

### 8. 修改订单信息（自动重新计价）
- **接口**: `PUT /api/orders/<order_no>`
- **说明**: 修改竹材、纹样、数量时会自动重新计算价格和工期
- **请求参数**: 同创建订单的所有可写字段

### 9. 删除订单
- **接口**: `DELETE /api/orders/<order_no>`

### 10. 获取状态列表
- **接口**: `GET /api/statuses`

## 订单编号规则
- 格式: `BD + 日期(8位) + 序号(4位)`
- 示例: `BD202405160001`
- 每天从0001开始递增

## 计价公式
```
综合难度 = 竹材难度 × 纹样难度
单价 = (竹材基础价 + 纹样基础价) × (1 + (综合难度 - 1) × 0.3)
总价 = 单价 × 数量
工期 = 纹样基础工期 × 数量 / 2 (向上取整)
```

## 数据库自动迁移
- 新增字段会自动添加到现有表中
- 无需手动修改数据库结构
- 旧数据兼容运行
