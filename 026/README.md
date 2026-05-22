# 缂丝团扇定制订单管理系统 V2.0

基于 Python + Flask + SQLite 实现的传统缂丝团扇定制订单管理系统后端（增强版）。

## 功能特性

### V2.0 新增功能
- ✅ **统一接口返回格式** - 标准化的成功/错误响应格式
- ✅ **必填字段校验** - 客户姓名、电话、团扇风格、纹样描述等必填验证
- ✅ **规范选项验证** - 团扇风格、丝线品类、扇骨材质、纹样复杂度等选项规范
- ✅ **纹样复杂度自动计价** - 4等级复杂度，自动计算价格和工期
- ✅ **匠人绑定与工期管理** - 匠人状态管理、订单绑定、自动状态流转
- ✅ **多条件筛选查询** - 按风格、进度、匠人、交付日期筛选
- ✅ **灵活分页排序** - 支持多字段排序、完整分页信息

### 基础功能
- 客户提交缂丝团扇定制需求
- 管理员管理订单、修改制作进度
- 订单状态：待接单 → 选线 → 打稿 → 牵经 → 缂丝 → 装框 → 装柄 → 完工
- 订单自动编号（格式：KS + 日期 + 4位序号）
- 丝线品类、纹样图案、扇骨材质、扇面尺寸管理
- 缂丝、装框、装柄三道工序详细记录

## 安装运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 运行应用
python app.py

# 3. 访问地址
http://localhost:5000
```

## 纹样复杂度与计价规则

| 复杂度等级 | 价格(元) | 工期(天) | 颜色数量范围 | 说明 |
|-----------|---------|---------|------------|------|
| simple (简单) | 800 | 7 | 3-8色 | 基础纹样 |
| medium (中等) | 1500 | 14 | 8-15色 | 标准纹样 |
| complex (复杂) | 3000 | 25 | 15-30色 | 精细纹样 |
| master (大师级) | 8000 | 45 | 25-50色 | 精品收藏级 |

## 规范选项列表

| 类型 | 选项 |
|------|------|
| 团扇风格 | 圆形团扇、海棠形团扇、方形团扇、芭蕉形团扇、异形团扇 |
| 丝线品类 | 桑蚕丝、柞蚕丝、天丝线、彩色丝线、金线 |
| 扇骨材质 | 紫竹、湘妃竹、梅鹿竹、紫檀木、红木、鸡翅木 |

## API 接口文档

### 1. 健康检查
```
GET /health
```
返回系统版本和功能列表

### 2. 获取所有配置选项
```
GET /api/statuses
```
返回订单状态、团扇风格、丝线品类、扇骨材质、纹样复杂度等所有配置选项

### 3. 价格试算
```
POST /api/price/calculate
Content-Type: application/json

{
    "pattern_complexity": "complex",
    "kesi_color_count": 20
}
```
返回计算后的价格、工期、预计交付日期

### 4. 匠人管理 - 创建匠人
```
POST /api/craftsmen
Content-Type: application/json

{
    "name": "王师傅",
    "phone": "13800138000",
    "skill_level": "高级",
    "specialty": "山水纹样",
    "status": "空闲",
    "daily_output": 2
}
```

### 5. 匠人管理 - 查询匠人列表
```
GET /api/craftsmen?status=空闲
```

### 6. 匠人管理 - 查询单个匠人
```
GET /api/craftsmen/{id}
```

### 7. 匠人管理 - 更新匠人信息
```
PUT /api/craftsmen/{id}
Content-Type: application/json

{
    "status": "忙碌",
    "specialty": "山水、花鸟纹样"
}
```

### 8. 匠人管理 - 删除匠人
```
DELETE /api/craftsmen/{id}
```

### 9. 客户提交订单（增强版）
```
POST /api/orders
Content-Type: application/json

{
    "customer_name": "张三",
    "customer_phone": "13800138000",
    "customer_address": "北京市朝阳区",
    "fan_style": "圆形团扇",
    "pattern_description": "牡丹花纹",
    "size": "直径30cm",
    "material_requirement": "真丝线",
    "special_requirement": "双面缂丝",
    "remark": "加急订单",
    "silk_thread_type": "桑蚕丝",
    "pattern_design": "传统牡丹纹样",
    "frame_material": "紫竹",
    "fan_size_width": "30cm",
    "fan_size_height": "30cm",
    "pattern_complexity": "complex",
    "kesi_color_count": 20
}
```

### 10. 获取订单列表（支持筛选和分页）
```
GET /api/orders
  ?page=1
  &per_page=10
  &status=缂丝
  &fan_style=圆形团扇
  &craftsman=王师傅
  &delivery_from=2026-05-01
  &delivery_to=2026-06-30
  &sort_by=created_at
  &sort_order=desc
```

### 11. 获取单个订单详情
```
GET /api/orders/{order_no}
```

### 12. 绑定匠人到订单
```
PUT /api/orders/{order_no}/assign
Content-Type: application/json

{
    "craftsman_id": 1
}
```
- 自动将匠人状态设置为「忙碌」
- 订单记录绑定的匠人ID和姓名

### 13. 更新订单状态
```
PUT /api/orders/{order_no}/status
Content-Type: application/json

{
    "status": "缂丝",
    "remark": "开始缂丝工序"
}
```

### 14. 更新订单信息（增强版）
```
PUT /api/orders/{order_no}
Content-Type: application/json

{
    "kesi_color_count": 25,
    "pattern_complexity": "master"
}
```
- 更新颜色数量或复杂度时，自动重新计算价格和工期

### 15. 更新缂丝工序详情
```
PUT /api/orders/{order_no}/kesi
Content-Type: application/json

{
    "kesi_technique": "双面缂丝，平缂+掼缂",
    "kesi_thread_count": "120根/厘米",
    "kesi_color_count": 20,
    "kesi_operator": "王师傅",
    "completed": true
}
```
- 设置 `completed: true` 自动记录完成时间，并将状态推进到「装框」

### 16. 更新装框工序详情
```
PUT /api/orders/{order_no}/frame
Content-Type: application/json

{
    "frame_type": "圆形实木框",
    "frame_size": "外框35cm，内框30cm",
    "frame_material_detail": "优质紫竹，经打磨上漆",
    "frame_operator": "李师傅",
    "completed": true
}
```
- 设置 `completed: true` 自动记录完成时间，并将状态推进到「装柄」

### 17. 更新装柄工序详情
```
PUT /api/orders/{order_no}/handle
Content-Type: application/json

{
    "handle_material": "紫檀木",
    "handle_style": "传统直柄，雕花",
    "handle_length": "18cm",
    "handle_operator": "张师傅",
    "completed": true
}
```
- 设置 `completed: true` 自动记录完成时间，并将状态推进到「完工」
- 自动将绑定的匠人状态重置为「空闲」

### 18. 删除订单
```
DELETE /api/orders/{order_no}
```
- 删除订单时自动释放绑定的匠人（状态重置为空闲）

## 统一响应格式

### 成功响应
```json
{
    "success": true,
    "code": 200,
    "message": "操作成功",
    "timestamp": "2026-05-16 12:00:00",
    "data": { ... }
}
```

### 错误响应
```json
{
    "success": false,
    "code": 400,
    "message": "订单验证失败",
    "timestamp": "2026-05-16 12:00:00",
    "errors": [
        "缺少必填字段: customer_name",
        "手机号格式不正确",
        "团扇风格不支持"
    ]
}
```

## 数据库结构

### Order 订单表（新增字段）
| 字段 | 类型 | 说明 |
|------|------|------|
| pattern_complexity | String | 纹样复杂度 |
| calculated_price | Float | 自动计算价格 |
| estimated_days | Integer | 预计工期(天) |
| estimated_delivery | DateTime | 预计交付日期 |
| assigned_craftsman_id | Integer | 绑定匠人ID |
| assigned_craftsman_name | String | 绑定匠人姓名 |

### Craftsman 匠人表（新增）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 主键 |
| name | String | 匠人姓名 |
| phone | String | 联系电话 |
| skill_level | String | 技能等级 |
| specialty | String | 专长 |
| status | String | 状态(空闲/忙碌) |
| daily_output | Integer | 日产量 |
| created_at | DateTime | 创建时间 |

## 项目文件说明

| 文件 | 说明 |
|------|------|
| app.py | 主应用文件，V2.0完整版 |
| requirements.txt | 依赖包列表 |
| test_v2.py | V2.0完整功能测试脚本 |
| test_enhanced.py | V1.1增强版测试脚本 |
| test_api.py | HTTP API测试脚本 |
| instance/orders.db | SQLite数据库文件 |

## 版本历史

### V2.0 (当前版本)
- 统一接口返回格式
- 增加必填字段校验与规范选项验证
- 实现纹样复杂度自动计价功能（4等级）
- 新增匠人管理模块与绑定功能
- 实现工期自动计算与交付日期管理
- 支持多条件筛选（风格、进度、匠人、交付日期）
- 增强分页排序功能
- 工序完成自动流转与匠人状态释放

### V1.1
- 补充丝线品类、纹样图案、扇骨材质、扇面尺寸字段
- 完善数据库表结构
- 为缂丝、装框、装柄提供明确依据
- 增加三道工序专用API接口
