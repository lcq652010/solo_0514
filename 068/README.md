# 传统椰壳雕手把件定制订单管理系统

基于 Python + Flask + SQLite 的后端API服务 v2.0。

## 功能特性

- 客户提交定制订单
- 自动生成订单编号（格式：YKD + 日期 + 6位随机码）
- 8种订单状态管理：待接单 → 选椰壳 → 开坯 → 粗磨 → 浮雕 → 精修 → 抛光 → 完工
- 订单状态变更历史记录
- 订单列表分页查询
- 订单统计信息
- **新增：完整的专业字段**
  - 椰壳规格（8种）
  - 外形尺寸（8种）
  - 浮雕纹样（13种）
  - 表面处理（9种）
  - 开坯规格、雕刻深度、抛光等级

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动，数据库会自动初始化。

### 3. 运行API测试（可选）

```bash
pip install requests
python api_examples.py
```

## API 接口文档

### 1. 获取系统信息
```
GET /
```

### 2. 获取所有规格选项
```
GET /api/specifications
```
返回：椰壳规格、外形类型、浮雕纹样、表面处理、订单状态

### 3. 获取所有订单状态
```
GET /api/statuses
```

### 4. 创建订单
```
POST /api/orders
Content-Type: application/json

{
    "customer_name": "张三",
    "phone": "13800138000",
    "design_requirements": "雕刻龙凤图案，传统风格",
    "coconut_specification": "老椰壳(壁厚3-5mm)",
    "shape_type": "圆形",
    "outer_dimensions": "直径6cm，厚度1.5cm",
    "carving_pattern": "龙凤呈祥",
    "surface_treatment": "烫蜡工艺",
    "size": "6cm x 6cm x 1.5cm",
    "material_preference": "海南老椰壳",
    "blank_spec": "正圆形，壁厚均匀，无裂纹",
    "carving_depth": "浅浮雕(0.5-1mm)",
    "polishing_grade": "3000目精抛",
    "remark": "加急"
}
```

### 5. 获取订单列表
```
GET /api/orders?status=待接单&page=1&per_page=20
```

### 6. 获取订单详情
```
GET /api/orders/{order_no}
```

### 7. 更新订单信息
```
PUT /api/orders/{order_no}
Content-Type: application/json

{
    "phone": "13900139000",
    "blank_spec": "正圆形，边缘整齐",
    "carving_depth": "浅浮雕(0.8mm)",
    "remark": "修改备注"
}
```

### 8. 更新订单状态
```
PUT /api/orders/{order_no}/status
Content-Type: application/json

{
    "status": "开坯",
    "operator": "王师傅",
    "remark": "开坯完成，正圆形，壁厚均匀"
}
```

### 9. 删除订单
```
DELETE /api/orders/{order_no}
```

### 10. 获取统计信息
```
GET /api/stats
```

## 数据库结构

### orders 订单表
| 字段 | 说明 |
|------|------|
| id | 主键 |
| order_no | 订单编号（唯一） |
| customer_name | 客户姓名 |
| phone | 联系电话 |
| design_requirements | 设计要求 |
| **coconut_specification** | **椰壳规格** |
| **shape_type** | **外形类型** |
| **outer_dimensions** | **外形尺寸** |
| **carving_pattern** | **浮雕纹样** |
| **surface_treatment** | **表面处理** |
| size | 尺寸 |
| material_preference | 材料偏好 |
| **blank_spec** | **开坯规格** |
| **carving_depth** | **雕刻深度** |
| **polishing_grade** | **抛光等级** |
| status | 订单状态 |
| created_at | 创建时间 |
| updated_at | 更新时间 |
| remark | 备注 |

### status_logs 状态变更记录表
- id: 主键
- order_id: 订单ID
- status: 状态
- operator: 操作人
- remark: 备注
- created_at: 创建时间

## 专业字段选项说明

### 椰壳规格（8种）
1. 小椰壳(直径5-7cm)
2. 中椰壳(直径7-9cm)
3. 大椰壳(直径9-12cm)
4. 特大椰壳(直径12cm以上)
5. 老椰壳(壁厚3-5mm)
6. 嫩椰壳(壁厚1-2mm)
7. 天然原色
8. 碳化处理

### 外形类型（8种）
- 圆形、椭圆形、方形、长方形
- 不规则形、随形、葫芦形、平安扣形

### 浮雕纹样（13种）
1. 龙凤呈祥
2. 山水风景
3. 花鸟虫鱼
4. 人物肖像
5. 吉祥文字
6. 几何图案
7. 图腾纹样
8. 佛教题材
9. 道教题材
10. 生肖图案
11. 梅兰竹菊
12. 松鹤延年
13. 自定义图案

### 表面处理（9种）
1. 原色打磨
2. 上清漆
3. 上木蜡油
4. 烫蜡工艺
5. 碳化处理
6. 做旧处理
7. 光面抛光
8. 磨砂质感
9. 纹理保留

## 订单状态流程说明

1. **待接单** - 客户已提交，等待管理员确认
2. **选椰壳** - 选择合适的椰壳材料（参考：椰壳规格字段）
3. **开坯** - 初步成型（参考：开坯规格、外形尺寸字段）
4. **粗磨** - 粗加工打磨
5. **浮雕** - 雕刻图案（参考：浮雕纹样、雕刻深度字段）
6. **精修** - 精细修整
7. **抛光** - 表面抛光处理（参考：抛光等级字段）
8. **完工** - 制作完成，可交付（参考：表面处理字段）
