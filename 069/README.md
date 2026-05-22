# 港口集装箱RFID识别终端运维管理系统

基于 Python + Flask + SQLite 的后端服务系统，实现终端设备管理、识别异常上报、设备状态监控和工单管理功能。

## 功能特性

### 1. 终端设备管理
- 设备录入、编辑、删除
- 设备状态管理（正常、故障、离线、信号异常）
- 设备信息扩展：码头编号、桥吊/龙门吊位置、设备SN码、安装日期、作业区域
- 支持按作业区域、码头编号筛选设备
- 设备心跳上报
- 设备列表查询（支持分页、状态筛选、关键字搜索（含SN码））

### 2. 异常上报管理
- RFID识别异常上报
- 异常类型分为：漏读、误读、通信中断、供电异常
- 记录异常开始/结束时间，自动计算持续时长
- 异常记录查询和筛选
- 异常处理标记
- 异常自动触发设备状态变更

### 3. 工单管理
- 工单自动编号（WO + 日期 + 4位序号）
- 工单创建、编辑、状态更新
- 工单与异常、设备关联
- 工单优先级管理（低、中、高、紧急）

### 4. 识别记录与统计
- RFID识别记录上报（成功/失败）
- 日识别成功率统计
- 月识别成功率统计
- 综合作业效率评分
- 支持按作业区域筛选统计数据

### 5. 重点运维设备清单
- 按作业效率排名
- 综合计算成功率、可用率、稳定性得分
- 运维优先级分类（高/中/低）
- 支持自定义统计周期和阈值

## 项目结构

```
.
├── app.py              # Flask主应用，包含所有API路由
├── models.py           # 数据库模型定义
├── init_data.py        # 测试数据初始化脚本
├── requirements.txt    # 项目依赖
├── README.md          # 项目说明文档
└── rfid_terminal.db   # SQLite数据库文件（自动生成）
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化测试数据（可选）

```bash
python init_data.py
```

### 3. 启动服务

```bash
python app.py
```

服务将在 `http://localhost:5000` 启动

## API接口文档

### 基础信息
- **基础URL**: `http://localhost:5000`
- **数据格式**: JSON
- **字符编码**: UTF-8

### 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

- `code`: 0表示成功，非0表示失败
- `message`: 响应消息
- `data`: 响应数据

---

### 1. 设备管理接口

#### 获取设备列表
```
GET /api/devices
```
**参数**:
- `page`: 页码（默认1）
- `per_page`: 每页数量（默认10）
- `status`: 状态筛选（normal/fault/offline/signal_error）
- `work_zone`: 作业区域筛选
- `wharf_code`: 码头编号筛选
- `keyword`: 关键字搜索（设备编号/名称/SN码）

#### 获取单个设备
```
GET /api/devices/{device_id}
```

#### 创建设备
```
POST /api/devices
```
**请求体**:
```json
{
  "device_code": "RFID-005",
  "device_name": "E区入口识别终端",
  "wharf_code": "WH-001",
  "crane_location": "Q05#桥吊",
  "sn_code": "SN202405005",
  "work_zone": "E作业区",
  "location": "港口E区入口闸口",
  "install_date": "2024-05-01",
  "status": "normal",
  "signal_strength": 90,
  "remarks": "备注信息"
}
```

#### 更新设备
```
PUT /api/devices/{device_id}
```

#### 删除设备
```
DELETE /api/devices/{device_id}
```

#### 更新设备状态
```
PUT /api/devices/{device_id}/status
```
**请求体**:
```json
{
  "status": "normal"
}
```

#### 设备心跳上报
```
POST /api/devices/{device_id}/heartbeat
```
**请求体**:
```json
{
  "signal_strength": 85
}
```

---

### 2. 异常上报接口

#### 获取异常列表
```
GET /api/exceptions
```
**参数**:
- `page`: 页码
- `per_page`: 每页数量
- `device_id`: 设备ID筛选
- `handled`: 是否已处理（true/false）

#### 上报异常
```
POST /api/exceptions
```
**请求体**:
```json
{
  "device_id": 1,
  "exception_type": "miss_read",
  "description": "连续3次漏读RFID标签",
  "container_code": "CONT-20240501-001",
  "rfid_data": "EPC:1234567890,TID:0987654321"
}
```
**异常类型说明**:
- `miss_read`: 漏读
- `wrong_read`: 误读
- `comm_interrupt`: 通信中断
- `power_failure`: 供电异常

#### 处理异常
```
PUT /api/exceptions/{exception_id}/handle
```
**请求体**:
```json
{
  "handler": "张工"
}
```

#### 结束异常并计算时长
```
PUT /api/exceptions/{exception_id}/end
```
**请求体**:
```json
{
  "handler": "张工"
}
```
**响应包含**:
- `start_time`: 异常开始时间
- `end_time`: 异常结束时间
- `duration`: 持续时长（秒）
- `duration_text`: 格式化时长（如"2小时30分0秒"）

---

### 3. 识别记录接口

#### 上报识别记录
```
POST /api/recognition/record
```
**请求体**:
```json
{
  "device_id": 1,
  "container_code": "CONT-20240501-001",
  "success": true,
  "fail_reason": null
}
```

#### 获取识别记录列表
```
GET /api/recognition/records
```
**参数**:
- `page`: 页码
- `per_page`: 每页数量
- `device_id`: 设备ID筛选
- `success`: 是否成功（true/false）
- `start_date`: 开始日期
- `end_date`: 结束日期

---

### 4. 统计接口

#### 获取日统计数据
```
GET /api/stats/daily
```
**参数**:
- `page`: 页码
- `per_page`: 每页数量
- `device_id`: 设备ID筛选
- `work_zone`: 作业区域筛选
- `start_date`: 开始日期
- `end_date`: 结束日期

**响应数据**:
- `total_recognitions`: 总识别次数
- `success_recognitions`: 成功识别次数
- `fail_recognitions`: 失败识别次数
- `success_rate`: 识别成功率（%）
- `exception_count`: 异常次数
- `total_exception_duration`: 异常总时长（秒）
- `efficiency_score`: 效率综合得分

#### 获取月统计数据
```
GET /api/stats/monthly
```
**参数**:
- `page`: 页码
- `per_page`: 每页数量
- `device_id`: 设备ID筛选
- `work_zone`: 作业区域筛选
- `year`: 统计年份

#### 获取重点运维设备清单（按作业效率排名）
```
GET /api/stats/maintenance-devices
```
**参数**:
- `days`: 统计周期天数（默认7天）
- `limit`: 返回设备数量（默认10台）
- `work_zone`: 作业区域筛选
- `min_success_rate`: 最低成功率阈值，低于此阈值的设备列入运维清单

**响应包含**:
- `avg_success_rate`: 平均识别成功率
- `total_exception_count`: 总异常次数
- `total_exception_duration`: 异常总时长
- `efficiency_score`: 综合效率得分
- `maintenance_priority`: 运维优先级（高/中/低）

#### 刷新历史统计数据
```
POST /api/stats/refresh
```
**请求体**:
```json
{
  "days": 7
}
```

---

### 5. 工单管理接口

#### 获取工单列表
```
GET /api/work-orders
```
**参数**:
- `page`: 页码
- `per_page`: 每页数量
- `device_id`: 设备ID筛选
- `status`: 状态筛选（pending/processing/completed/closed）

#### 获取单个工单
```
GET /api/work-orders/{order_id}
```

#### 创建工单
```
POST /api/work-orders
```
**请求体**:
```json
{
  "device_id": 1,
  "exception_id": 1,
  "title": "设备故障维修",
  "description": "详细描述...",
  "priority": "high",
  "assign_to": "张工",
  "created_by": "管理员"
}
```

#### 更新工单
```
PUT /api/work-orders/{order_id}
```

#### 更新工单状态
```
PUT /api/work-orders/{order_id}/status
```
**请求体**:
```json
{
  "status": "processing"
}
```

---

### 4. 统计接口

#### 获取统计数据
```
GET /api/dashboard/statistics
```

---

## 设备字段说明

| 字段名 | 类型 | 说明 |
|--------|------|------|
| device_code | String | 设备编号，唯一标识 |
| device_name | String | 设备名称 |
| wharf_code | String | 码头编号 |
| crane_location | String | 桥吊/龙门吊位置 |
| sn_code | String | 设备SN码（序列号） |
| work_zone | String | 作业区域 |
| location | String | 详细位置描述 |
| install_date | Date | 安装日期 |
| status | Enum | 设备状态（见下文） |
| signal_strength | Integer | 信号强度 |
| last_heartbeat | DateTime | 最后心跳时间 |
| remarks | Text | 备注信息 |

## 设备状态说明

| 状态值 | 状态名称 | 说明 |
|--------|----------|------|
| normal | 正常 | 设备运行正常 |
| fault | 故障 | 设备硬件或功能故障 |
| offline | 离线 | 设备网络连接中断 |
| signal_error | 信号异常 | RFID信号强度异常 |

## 工单状态说明

| 状态值 | 状态名称 | 说明 |
|--------|----------|------|
| pending | 待处理 | 工单已创建，未开始处理 |
| processing | 处理中 | 工单正在处理中 |
| completed | 已完成 | 工单已完成处理 |
| closed | 已关闭 | 工单已关闭归档 |

## 工单优先级说明

| 优先级值 | 优先级名称 | 说明 |
|----------|------------|------|
| low | 低 | 常规维护 |
| medium | 中 | 一般问题 |
| high | 高 | 重要问题 |
| urgent | 紧急 | 紧急故障 |

## 技术栈

- **Python 3.8+**
- **Flask 2.3.3** - Web框架
- **Flask-SQLAlchemy 3.1.1** - ORM框架
- **SQLite** - 嵌入式数据库
- **Flask-CORS 4.0.0** - 跨域支持

## 注意事项

1. 首次运行 `app.py` 会自动创建数据库和表结构
2. 工单编号自动生成，格式为：WO + YYYYMMDD + 4位序号
3. 异常上报会自动根据异常类型更新设备状态
4. 所有API接口支持CORS跨域访问
