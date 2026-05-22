# 传统木雕香盒定制订单管理系统后端

## 功能特性

- 客户提交香盒定制需求
- 管理员管理订单、修改制作进度
- 订单状态包含：待接单、选料、开坯、挖膛、雕花、打磨、上蜡、完工
- 订单自动编号（格式：年月日+4位序号，如 202605160001）
- **必填校验与数值规范验证
- **按木料与雕刻难度自动计价
- **绑定匠人与工期管理
- **按风格、进度、交付日期筛选
- **分页排序
- **统一接口返回格式

## 技术栈

- Python 3
- Flask 2.3.3
- SQLite
- Flask-CORS

## 安装与运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

3. 服务启动后访问：http://localhost:5000

## 统一接口返回格式

### 成功响应
```json
{
  "success": true,
  "message": "操作成功",
  "code": 200,
  "data": { ... }
}
```

### 失败响应
```json
{
  "success": false,
  "message": "操作失败",
  "code": 400,
  "errors": { ... }
}
```

## 价格计算规则

- 价格 = 木料基础价格 × 体积(立方分米) × 难度系数

### 木料基础价格
| 木料 | 价格（元/立方分米） |
|------|-------------------|
| 紫檀木 | 800 |
| 黄花梨 | 1200 |
| 楠木 | 300 |
| 红木 | 500 |
| 鸡翅木 | 200 |
| 酸枝木 | 600 |
| 乌木 | 400 |
| 榉木 | 150 |

### 雕刻难度系数
| 风格 | 系数 |
|------|------|
| 简约 | 1.0 |
| 传统 | 1.3 |
| 繁复 | 1.8 |
| 现代 | 1.2 |
| 复古 | 1.5 |

### 工期计算（单位：天）
| 工序 | 天数 |
|------|------|
| 选料 | 1 |
| 开坯 | 2 |
| 挖膛 | 3 |
| 雕花 | 5 |
| 打磨 | 2 |
| 上蜡 | 1 |
| **总计** | **14天** |

## API 接口文档

### 1. 获取所有状态枚举
```
GET /api/statuses
```

响应：
- `order_statuses` - 订单状态列表
- `pattern_styles` - 图案风格列表
- `pattern_types` - 图案类型列表

### 2. 计算订单价格（预计算）
```
POST /api/price/calculate
Content-Type: application/json

{
    "wood_type": "紫檀木",
    "pattern_style": "传统",
    "outer_length": 10,
    "outer_width": 8,
    "outer_height": 5
}
```

### 3. 提交订单（客户）
```
POST /api/orders
Content-Type: application/json

{
    "customer_name": "张三",
    "customer_phone": "13800138000",
    "customer_address": "北京市东城区",
    "wood_type": "紫檀木",
    "wood_origin": "印度",
    "wood_grade": "A级",
    "wood_density": "高",
    "box_size": "10x8x5cm",
    "outer_length": 10,
    "outer_width": 8,
    "outer_height": 5,
    "inner_length": 8,
    "inner_width": 6,
    "inner_depth": 3.5,
    "wall_thickness": 1,
    "lid_height": 1.5,
    "pattern": "龙凤呈祥",
    "pattern_type": "浮雕",
    "pattern_position": "顶盖+四面",
    "pattern_style": "传统",
    "pattern_detail": "龙在上凤在下，祥云环绕四周，鳞片清晰",
    "description": "希望图案更加精致"
}
```

### 4. 获取订单列表（支持筛选、分页、排序）
```
GET /api/orders
GET /api/orders?page=1&page_size=10
GET /api/orders?status=待接单
GET /api/orders?pattern_style=传统
GET /api/orders?delivery_date_start=2026-05-01&delivery_date_end=2026-05-31
GET /api/orders?sort_by=price&sort_order=DESC
```

参数说明：
- `page` - 页码，默认1
- `page_size` - 每页数量，默认10
- `status` - 按状态筛选
- `pattern_style` - 按风格筛选
- `delivery_date_start` - 交付日期开始
- `delivery_date_end` - 交付日期结束
- `sort_by` - 排序字段：created_at, price, delivery_date, order_no
- `sort_order` - 排序方向：ASC, DESC

### 5. 获取单个订单详情
```
GET /api/orders/{order_no}
```

### 6. 更新订单详情
```
PUT /api/orders/{order_no}
Content-Type: application/json

{
    "inner_depth": 3.8,
    "pattern_detail": "调整图案细节..."
}
```

### 7. 更新订单状态（管理员）
```
PUT /api/orders/{order_no}/status
Content-Type: application/json

{
    "status": "选料"
}
```

### 8. 分配匠人
```
PUT /api/orders/{order_no}/assign
Content-Type: application/json

{
    "craftsman_id": 1
}
```

### 9. 删除订单
```
DELETE /api/orders/{order_no}
```

### 10. 创建匠人
```
POST /api/craftsmen
Content-Type: application/json

{
    "name": "李师傅",
    "phone": "13900139000",
    "skill_level": "高级",
    "specialty": "传统浮雕",
    "status": "空闲"
}
```

### 11. 获取匠人列表
```
GET /api/craftsmen
GET /api/craftsmen?status=空闲
```

### 12. 更新匠人信息
```
PUT /api/craftsmen/{craftsman_id}
Content-Type: application/json

{
    "status": "忙碌"
}
```

### 13. 删除匠人
```
DELETE /api/craftsmen/{craftsman_id}
```

### 14. 获取统计数据
```
GET /api/statistics
```

## 数据校验说明

### 必填字段校验
- 客户姓名、手机号、木料类型、尺寸等必填项校验
- 手机号格式校验（1开头11位手机号）

### 数值范围校验
- 所有尺寸字段必须大于0且小于等于100厘米

### 枚举值校验
- 图案风格必须是：传统、简约、繁复、现代、复古
- 图案类型必须是：浮雕、透雕、阴刻、圆雕

## 订单状态说明

1. 待接单 - 客户刚提交订单
2. 选料 - 选择合适的木材（根据 wood_origin、wood_grade、wood_density）
3. 开坯 - 根据 outer_length、outer_width、outer_height 切割木材成基本形状
4. 挖膛 - 根据 inner_length、inner_width、inner_depth、wall_thickness 挖空香盒内部
5. 雕花 - 根据 pattern、pattern_type、pattern_position、pattern_style、pattern_detail 雕刻花纹
6. 打磨 - 表面打磨光滑
7. 上蜡 - 上蜡保护
8. 完工 - 订单完成
