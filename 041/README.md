# 传统珐琅彩鼻烟壶定制订单管理系统后端

基于 Python + Flask + SQLite 实现的订单管理系统。

## 功能特性

- 客户提交鼻烟壶定制需求
- 管理员管理订单、修改制作进度
- 订单自动编号（格式：ENB+日期+4位序号）
- 订单状态流转：待接单 → 制胎 → 施釉 → 绘彩 → 烧造 → 打磨 → 镶口 → 完工

## 安装运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 初始化数据库：
```bash
python init_db.py
```

3. 启动服务：
```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口

### 1. 系统状态
```
GET /
```

### 2. 获取状态列表
```
GET /api/status
```

### 3. 客户提交订单
```
POST /api/orders
Content-Type: application/json

{
    "customer_name": "客户姓名",
    "customer_phone": "联系电话",
    "customer_address": "地址",
    "bottle_shape": "器型",
    "bottle_material": "材质",
    "pattern_design": "图案设计要求",
    "color_requirement": "色彩要求",
    "special_requirement": "特殊要求",
    "quantity": 1,
    "estimated_price": 5000
}
```

### 4. 查询订单列表
```
GET /api/orders?page=1&per_page=20&status=待接单&keyword=
```

### 5. 查询单个订单
```
GET /api/orders/{id}
```

### 6. 更新订单信息
```
PUT /api/orders/{id}
Content-Type: application/json
```

### 7. 更新订单状态
```
PUT /api/orders/{id}/status
Content-Type: application/json

{
    "status": "制胎"
}
```

### 8. 删除订单
```
DELETE /api/orders/{id}
```