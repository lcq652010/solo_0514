# 传统锡制茶叶罐定制订单管理系统 - API文档 v2.0

## 服务信息
- 服务地址: http://127.0.0.1:5000
- 默认管理员账号: admin / admin123

## 统一响应格式

### 成功响应
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        // 具体数据
    },
    "timestamp": "2026-05-16T00:00:00.000000"
}
```

### 失败响应
```json
{
    "code": 400,
    "message": "操作失败",
    "errors": [
        "参数校验失败1",
        "参数校验失败2"
    ],
    "timestamp": "2026-05-16T00:00:00.000000"
}
```

## 系统配置常量

### 订单状态 (ORDER_STATUSES)
```
1. 待接单 (进度: 0%)
2. 熔锡 (进度: 12.5%)
3. 制坯 (进度: 25%)
4. 锻打 (进度: 37.5%) - 关键工艺
5. 雕花 (进度: 50%) - 关键工艺
6. 打磨 (进度: 62.5%)
7. 抛光 (进度: 75%) - 关键工艺
8. 完工 (进度: 100%)
```

### 罐口样式 (MOUTH_STYLES)
```
- 直口
- 翻口
- 螺旋口
- 宽口
```

### 雕刻花纹 (PATTERN_TYPES) 及 难度系数
```
- 传统龙纹 (难度系数: 2.0) - 最复杂
- 山水图 (难度系数: 1.8)
- 花鸟图案 (难度系数: 1.6)
- 梅兰竹菊 (难度系数: 1.4)
- 祥云纹 (难度系数: 1.2)
- 几何纹样 (难度系数: 1.0) - 最简单
- 其他 (难度系数: 1.0)
```

### 锡料纯度 (TIN_PURITIES) 及 溢价系数
```
- 99.9%纯锡 (溢价: 1.5x)
- 99%纯锡 (溢价: 1.0x)
- 97%锡合金 (溢价: 0.8x)
```

### 尺寸档位
```
- 小 (< 200ml): 系数 1.0x
- 中 (200-400ml): 系数 1.3x
- 大 (> 400ml): 系数 1.6x
```

### 计价公式
```
单价 = 基础价格(200元) × 锡料溢价 × 花纹难度 × 尺寸系数
总价 = 单价 × 数量
```

### 工期计算
```
简单花纹: 5天
中等花纹: 7天
复杂花纹: 10天
```

## API 接口列表

### 1. 用户注册
```
POST /api/register
Content-Type: application/json

请求体:
{
    "username": "customer1",
    "password": "123456",
    "role": "customer",        // 可选: customer/craftsman/admin
    "phone": "13800138000",   // 可选
    "skills": "锻打,雕花"     // 匠人专用，可选
}
```

### 2. 用户登录
```
POST /api/login
Content-Type: application/json

请求体:
{
    "username": "admin",
    "password": "admin123"
}
```

### 3. 预计算订单价格 (新增)
```
POST /api/orders/calculate
Content-Type: application/json

请求体:
{
    "tin_purity": "99.9%纯锡",
    "carving_pattern": "传统龙纹",
    "capacity": "250ml",
    "quantity": 2
}

响应:
{
    "code": 200,
    "message": "价格计算成功",
    "data": {
        "unit_price": 780.0,
        "total_price": 1560.0,
        "work_days": 10,
        "estimated_delivery": "2026-05-26T00:00:00"
    }
}
```

### 4. 提交定制订单 (必填校验 + 自动计价)
```
POST /api/orders
Content-Type: application/json

请求体:
{
    "customer_id": 2,
    "capacity": "250ml",
    "tin_purity": "99.9%纯锡",
    "body_height": "12cm",
    "body_diameter": "8cm",
    "body_thickness": "2.5mm",
    "mouth_style": "螺旋口",
    "mouth_diameter": "5cm",
    "carving_pattern": "传统龙纹",
    "carving_position": "罐体正面环绕",
    "engraving_text": "福如东海",
    "design_desc": "传统中式风格，龙纹环绕罐体",
    "material": "云南个旧锡矿",
    "quantity": 1
}
```

### 5. 获取订单列表 (多条件筛选 + 分页排序) (升级)
```
GET /api/orders

查询参数:
- 状态筛选: status=锻打
- 客户筛选: customer_id=2
- 匠人筛选: craftsman_id=1
- 款式筛选: carving_pattern=传统龙纹
- 材质筛选: tin_purity=99.9%纯锡
- 罐口筛选: mouth_style=螺旋口
- 进度筛选: progress_min=25&progress_max=75
- 交期筛选: delivery_date_from=2026-05-20&delivery_date_to=2026-06-01
- 分页参数: page=1&per_page=10
- 排序参数: sort_by=total_price&sort_order=desc

示例:
GET /api/orders?status=雕花&carving_pattern=传统龙纹&page=1&per_page=10&sort_by=created_at&sort_order=desc

响应:
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "orders": [...],
        "pagination": {
            "total": 100,
            "pages": 10,
            "page": 1,
            "per_page": 10,
            "has_next": true,
            "has_prev": false
        }
    }
}
```

### 6. 获取单个订单详情
```
GET /api/orders/1
```

### 7. 更新订单 (绑定匠人 + 修改工期) (升级)
```
PUT /api/orders/1
Content-Type: application/json

{
    "status": "锻打",
    "craftsman_id": 3,
    "forging_notes": "采用300g铁锤，轻敲500次，注意罐口边缘加固",
    "estimated_delivery": "2026-05-30T00:00:00"
}

更新雕花状态示例:
{
    "status": "雕花",
    "carving_notes": "使用V型刀，深度0.5mm，龙鳞采用鱼鳞刀法"
}

更新抛光状态示例:
{
    "status": "抛光",
    "polishing_notes": "800目→1500目→3000目镜面抛光"
}

完工状态会自动设置实际交付日期:
{
    "status": "完工"
}
```

### 8. 删除订单
```
DELETE /api/orders/1
```

### 9. 获取系统配置常量
```
GET /api/statuses

返回:
{
    "code": 200,
    "data": {
        "statuses": [...],
        "mouth_styles": [...],
        "pattern_types": [...],
        "tin_purities": [...],
        "pricing_config": {...}
    }
}
```

### 10. 获取用户列表
```
GET /api/users?role=craftsman
```

### 11. 获取匠人列表 (新增)
```
GET /api/craftsmen

返回所有活跃的匠人账号
```

## 参数校验规则

系统会自动校验以下参数:

1. **tin_purity**: 必须是 TIN_PURITIES 中的有效值
2. **mouth_style**: 必须是 MOUTH_STYLES 中的有效值
3. **carving_pattern**: 必须是 PATTERN_TYPES 中的有效值
4. **quantity**: 必须是 1-100 之间的整数
5. **尺寸参数** (body_height/body_diameter/body_thickness): 必须包含数值和单位 (如: 12cm, 2.5mm)

校验失败会返回详细的错误信息列表。

## 完整使用流程示例

### 步骤1: 注册客户账号
```bash
curl -X POST http://127.0.0.1:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"customer1","password":"123456","role":"customer"}'
```

### 步骤2: 注册匠人账号
```bash
curl -X POST http://127.0.0.1:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"craftsman1","password":"123456","role":"craftsman","skills":"锻打,雕花"}'
```

### 步骤3: 预计算订单价格
```bash
curl -X POST http://127.0.0.1:5000/api/orders/calculate \
  -H "Content-Type: application/json" \
  -d '{"tin_purity":"99.9%纯锡","carving_pattern":"传统龙纹","capacity":"250ml","quantity":2}'
```

### 步骤4: 提交订单
```bash
curl -X POST http://127.0.0.1:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 2,
    "capacity": "250ml",
    "tin_purity": "99.9%纯锡",
    "body_height": "12cm",
    "body_diameter": "8cm",
    "body_thickness": "2.5mm",
    "mouth_style": "螺旋口",
    "carving_pattern": "传统龙纹",
    "design_desc": "传统中式风格",
    "material": "云南个旧锡矿",
    "quantity": 1
  }'
```

### 步骤5: 管理员绑定匠人并更新进度
```bash
# 接单并分配匠人
curl -X PUT http://127.0.0.1:5000/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"熔锡","craftsman_id":3}'

# 更新到锻打并记录工艺备注
curl -X PUT http://127.0.0.1:5000/api/orders/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"锻打","forging_notes":"采用300g铁锤，轻敲500次"}'
```

### 步骤6: 多条件筛选订单
```bash
# 查询正在雕花且是传统龙纹的订单，按价格降序
curl "http://127.0.0.1:5000/api/orders?status=雕花&carving_pattern=传统龙纹&sort_by=total_price&sort_order=desc"

# 按交付日期范围查询
curl "http://127.0.0.1:5000/api/orders?delivery_date_from=2026-05-20&delivery_date_to=2026-06-01"
```