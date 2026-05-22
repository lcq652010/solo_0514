# 徽墨定制订单管理系统后端

基于 Python + Flask + SQLite 实现的传统徽墨定制订单管理系统后端。

## 功能特性

- 客户提交徽墨定制需求（含详细生产参数）
- 管理员管理订单
- 修改制作进度
- 订单自动编号（格式：年月日 + 4位序号）
- 生产指导接口，为和料、压模、描金提供明确依据

## 订单状态

- 待接单
- 和料
- 制墨
- 压模
- 描金
- 阴干
- 打磨
- 完工

## 安装运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python app.py
```

服务将在 http://localhost:5000 启动

## API 接口文档

### 1. 获取所有订单状态

```
GET /api/statuses
```

响应示例：
```json
{
  "statuses": ["待接单", "和料", "制墨", "压模", "描金", "阴干", "打磨", "完工"]
}
```

### 2. 创建订单

```
POST /api/orders
Content-Type: application/json
```

请求体：
```json
{
  "customer_name": "张三",
  "customer_phone": "13800138000",
  "customer_address": "安徽省黄山市歙县",
  "ink_type": "松烟墨",
  "weight": "50g",
  "shape": "长方形",
  "pattern": "龙纹",
  "quantity": 10,
  "description": "需要刻上徽墨传承四个字"
}
```

必填字段：customer_name, customer_phone, ink_type, quantity

### 3. 获取订单列表

```
GET /api/orders?page=1&per_page=20&status=待接单
```

参数：
- page: 页码（默认1）
- per_page: 每页数量（默认20）
- status: 按状态筛选（可选）

### 4. 获取单个订单详情

```
GET /api/orders/{order_no}
```

### 5. 更新订单状态

```
PUT /api/orders/{order_no}/status
Content-Type: application/json
```

请求体：
```json
{
  "status": "和料"
}
```

### 6. 删除订单

```
DELETE /api/orders/{order_no}
```

## 测试 API

运行测试脚本：

```bash
python test_api.py
```

## 数据库结构

orders 表：
- id: 主键
- order_no: 订单编号（唯一）
- customer_name: 客户姓名
- customer_phone: 客户电话
- customer_address: 客户地址
- ink_type: 墨品类型
- material_type: 墨料类型（为和料提供依据）
- weight: 重量
- ink_style: 墨锭款式（为压模提供依据）
- spec_size: 规格尺寸（为压模提供依据）
- shape: 形状
- pattern: 图案
- gilding_pattern: 纹饰描金（为描金提供依据）
- quantity: 数量
- description: 描述
- status: 状态
- created_at: 创建时间
- updated_at: 更新时间
