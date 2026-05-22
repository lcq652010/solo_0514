# 智能燃气表远程采集终端运维管理系统 - API文档 (v3.0)

## 启动方式
```bash
python app.py
```
服务器启动在 `http://localhost:5000`

## 统一响应格式
所有接口返回统一的JSON格式：
```json
{
  "code": 200,
  "msg": "成功/失败信息",
  "data": {}
}
```
- `code`: 状态码，200表示成功，其他表示失败
- `msg`: 响应消息
- `data`: 响应数据对象

---

## 版本升级说明
### v3.0 新功能
1. **区域楼栋管理**：设备新增区域、楼栋字段，支持按区域楼栋筛选
2. **数据上传统计**：新增数据上传记录模型，统计上传成功率
3. **设备完好率**：统计设备完好率，支持按区域统计完好率
4. **统一接口格式**：所有接口返回统一的响应格式
5. **筛选增强**：工单支持按区域、楼栋筛选查询
6. **区域楼栋列表**：新增获取区域列表、楼栋列表接口

---

## 设备管理 API

### 1. 添加设备
- **URL**: `POST /api/devices`
- **请求体**:
```json
{
  "device_no": "GAS001",
  "device_name": "智能燃气表-1号",
  "device_model": "G4-GPRS",
  "communication_protocol": "MQTT",
  "region": "东城区",
  "building": "A栋",
  "location": "1单元101室",
  "install_date": "2024-01-15",
  "enable_date": "2024-01-20"
}
```

### 2. 查询设备列表
- **URL**: `GET /api/devices`
- **参数**: 
  - `page`: 页码（默认1）
  - `page_size`: 每页数量（默认10）
  - `status`: 状态筛选（正常/故障/维修中/已修复）
  - `device_model`: 设备型号筛选
  - `communication_protocol`: 通信协议筛选
  - `region`: 区域筛选
  - `building`: 楼栋筛选
  - `keyword`: 关键词搜索（设备编号/名称/位置/区域/楼栋）

### 3. 更新设备
- **URL**: `PUT /api/devices/{device_id}`
- **请求体**: 同上（字段可选）

### 4. 删除设备
- **URL**: `DELETE /api/devices/{device_id}`

### 5. 获取区域列表
- **URL**: `GET /api/devices/regions`
- **说明**: 获取所有已登记的区域列表

### 6. 获取楼栋列表
- **URL**: `GET /api/devices/buildings`
- **参数**:
  - `region`: 可选，按区域筛选楼栋

---

## 数据上传记录 API

### 1. 上报数据上传状态
- **URL**: `POST /api/data-upload`
- **请求体**:
```json
{
  "device_id": 1,
  "status": "成功",
  "data_type": "计量数据",
  "error_msg": ""
}
```
- `status`: 成功/失败
- `error_msg`: 失败时填写错误信息

### 2. 查询上传记录
- **URL**: `GET /api/data-upload`
- **参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `device_id`: 设备ID筛选
  - `status`: 状态筛选（成功/失败）
  - `start_date`: 开始日期
  - `end_date`: 结束日期

---

## 故障类型配置 API

### 获取故障类型配置
- **URL**: `GET /api/fault-types`
- **说明**: 获取系统支持的故障类型、分类映射、优先级规则

---

## 工单管理 API

### 1. 故障上报（创建工单）
- **URL**: `POST /api/workorders`
- **请求体**:
```json
{
  "device_id": 1,
  "fault_type": "燃气泄漏",
  "fault_description": "检测到微量燃气泄漏，浓度持续上升",
  "reporter": "张三"
}
```
- **说明**: 
  - 工单自动编号，格式为 `WO + 日期 + 4位序号`
  - 系统自动根据故障类型分配**故障分类**和**紧急优先级**

### 故障类型与优先级映射表
| 故障分类 | 故障类型 | 优先级 | 说明 |
|---------|---------|-------|-----|
| **燃气安全类** | 燃气泄漏、压力异常、阀门故障 | **紧急** | 涉及燃气安全，需立即处理 |
| **计量通讯类** | 数据异常、通讯中断 | **高** | 影响计量准确性，优先处理 |
| **设备状态类** | 电池电量低、传感器故障、显示屏故障 | **中** | 设备状态异常，常规处理 |
| **其他类** | 其他 | **低** | 一般问题，可延后处理 |

### 2. 查询工单列表
- **URL**: `GET /api/workorders`
- **参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `status`: 状态筛选（待处理/维修中/已修复）
  - `device_id`: 设备ID筛选
  - `fault_category`: 故障分类筛选
  - `priority`: 优先级筛选（紧急/高/中/低）
  - `region`: 区域筛选
  - `building`: 楼栋筛选
- **说明**: 结果按优先级自动排序，紧急工单优先显示

### 3. 处理工单
- **URL**: `PUT /api/workorders/{order_id}/handle`
- **请求体**:
```json
{
  "handler": "李工程师",
  "handle_result": "已更换密封垫圈，泄漏点已修复",
  "next_status": "已修复"
}
```
- `next_status`可选值: 维修中、已修复

---

## 运维记录 API

### 1. 添加运维记录
- **URL**: `POST /api/maintenance`
- **请求体**:
```json
{
  "device_id": 1,
  "work_order_id": 1,
  "maintenance_type": "故障维修",
  "maintenance_content": "更换密封垫圈，重新进行气密性测试",
  "maintainer": "李工程师",
  "remark": "设备运行正常，已恢复供气"
}
```

### 2. 查询运维记录
- **URL**: `GET /api/maintenance`
- **参数**:
  - `page`: 页码
  - `page_size`: 每页数量
  - `device_id`: 设备ID筛选
  - `work_order_id`: 工单ID筛选
  - `start_date`: 开始日期
  - `end_date`: 结束日期

---

## 统计面板 API

### 获取统计数据
- **URL**: `GET /api/dashboard`
- **返回数据示例**:
```json
{
  "code": 200,
  "msg": "成功",
  "data": {
    "total_devices": 100,
    "normal_devices": 85,
    "fault_devices": 8,
    "repairing_devices": 5,
    "repaired_devices": 2,
    "device_health_rate": 85.0,
    "pending_orders": 15,
    "processing_orders": 7,
    "completed_orders": 28,
    "category_stats": {
      "燃气安全类": 5,
      "计量通讯类": 12,
      "设备状态类": 25,
      "其他类": 8
    },
    "priority_stats": {
      "紧急": 3,
      "高": 6,
      "中": 4,
      "低": 2
    },
    "upload_stats": {
      "total_uploads": 1000,
      "success_uploads": 985,
      "success_rate": 98.5
    },
    "region_health_stats": [
      {
        "region": "东城区",
        "total_devices": 30,
        "normal_devices": 28,
        "health_rate": 93.33
      },
      {
        "region": "西城区",
        "total_devices": 40,
        "normal_devices": 32,
        "health_rate": 80.0
      }
    ]
  }
}
```

---

## 设备状态说明
- **正常**: 设备运行正常
- **故障**: 设备出现故障待处理
- **维修中**: 设备正在维修
- **已修复**: 设备已修复完成

## 优先级说明
- **紧急**: 涉及燃气安全，可能危及生命财产安全，需立即响应（30分钟内）
- **高**: 影响计量或通讯，影响民生服务，需优先响应（2小时内）
- **中**: 设备状态异常但不影响核心功能，常规响应（24小时内）
- **低**: 一般问题或建议，可延后处理

## 核心KPI指标
1. **设备完好率** = 正常设备数 / 总设备数 × 100%
2. **数据上传成功率** = 成功上传次数 / 总上传次数 × 100%
3. **工单处理及时率**（可按优先级统计）
