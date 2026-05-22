# 宠物医院管理系统后端

基于 Python + Django + Django REST Framework + MySQL 实现的宠物医院管理系统后端API。

## 功能特性

- **宠物建档**: 宠物基本信息录入和管理
- **挂号就诊**: 宠物就诊预约和挂号，自动生成就诊单号
- **病历填写**: 诊疗过程中的病历记录管理
- **药品处方**: 药品管理和处方开具，含库存校验和出库日志
- **收费结算**: 费用计算和支付管理，诊疗结束自动结算
- **多条件筛选**: 按宠物名称、主人姓名、就诊状态、医生、科室等多条件组合筛选
- **数据校验**: 必填字段校验、数据合法性校验、库存校验
- **分页支持**: 灵活的分页配置
- **权限隔离**: 前台/医生/管理员三级角色权限控制

## 就诊状态

- 待诊 (pending)
- 诊疗中 (in_progress)
- 已完成 (completed)
- 已取消 (cancelled)

## 角色权限说明

| 角色 | 权限范围 |
|-----|---------|
| 前台 (receptionist) | 查看所有数据、创建/编辑主人、宠物、挂号、取消就诊、支付费用 |
| 医生 (doctor) | 查看数据（医生只能查看自己的就诊）、开始/完成诊疗、填写病历、开处方 |
| 管理员 (admin) | 所有权限（增删改查） |

## 环境要求

- Python 3.8+
- MySQL 5.7+
- Django 4.2
- Django REST Framework 3.15

## 快速开始

### 1. 数据库准备

创建MySQL数据库：

```sql
CREATE DATABASE pet_hospital CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

> 默认数据库配置：
> - 数据库名: pet_hospital
> - 用户名: root
> - 密码: 123456
> - 主机: localhost
> - 端口: 3306
>
> 如需修改，请编辑 `pet_hospital/settings.py` 文件中的 DATABASES 配置。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 初始化测试数据（推荐）

```bash
python manage.py init_data
```

该命令会自动创建以下测试账号和数据：

**登录账号：**
- 超级管理员: admin / admin123
- 医生: user1 / 123456 (内科医生)
- 前台: user2 / 123456
- 管理员: user3 / 123456

**基础数据：**
- 4个科室（内科、外科、皮肤科、牙科）
- 4位医生
- 3位主人信息
- 3只宠物档案
- 4种常用药品

### 5. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

## 访问地址

- **管理后台**: http://localhost:8000/admin/
- **API接口**: http://localhost:8000/api/

## API接口列表

### 公共接口

| 接口路径 | 方法 | 说明 |
|---------|------|------|
| `/api/user-info/` | GET | 获取当前登录用户信息 |

### 分页参数

所有列表接口支持以下分页参数：
- `page`: 页码，默认为1
- `page_size`: 每页条数，默认10条，最大100条

分页响应格式：
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/visits/?page=2",
    "previous": null,
    "results": [...]
}
```

### 接口详情

| 接口路径 | 方法 | 筛选参数 | 说明 |
|---------|------|---------|------|
| `/api/departments/` | GET/POST | - | 科室列表/新增科室 |
| `/api/staff/` | GET/POST | `name`, `role` | 员工列表/新增员工（管理员） |
| `/api/doctors/` | GET/POST | `name`, `department_id` | 医生列表/新增医生 |
| `/api/owners/` | GET/POST | `name`, `phone` | 主人列表/新增主人 |
| `/api/pets/` | GET/POST | `name`, `owner_name`, `species`, `gender` | 宠物列表/宠物建档 |
| `/api/medicines/` | GET/POST | `name`, `category`, `low_stock` | 药品列表/新增药品 |
| `/api/visits/` | GET/POST | `pet_name`, `owner_name`, `status`, `doctor_id`, `department_id`, `visit_no`, `date_from`, `date_to` | 就诊列表/挂号就诊 |
| `/api/visits/{id}/start_treatment/` | POST | - | 开始诊疗（医生） |
| `/api/visits/{id}/complete/` | POST | - | 完成诊疗（医生），自动结算 |
| `/api/visits/{id}/cancel/` | POST | - | 取消就诊（前台/医生） |
| `/api/medical-records/` | GET/POST | `visit_no`, `pet_name`, `diagnosis` | 病历列表/填写病历（医生） |
| `/api/prescriptions/` | GET/POST | `medical_record_id`, `medicine_name` | 处方列表/开处方（医生） |
| `/api/charges/` | GET/POST | `charge_no`, `visit_no`, `status`, `payment_method` | 收费列表 |
| `/api/charges/{id}/pay/` | POST | - | 支付费用（前台/医生） |
| `/api/charges/{id}/refund/` | POST | - | 退款（管理员） |
| `/api/inventory-logs/` | GET | `medicine_name`, `operation` | 库存变更日志（医生/管理员） |

## 多条件筛选示例

### 1. 挂号就诊多条件筛选

```bash
# 按宠物名称筛选
GET /api/visits/?pet_name=豆豆

# 按主人姓名筛选
GET /api/visits/?owner_name=陈先生

# 按就诊状态筛选
GET /api/visits/?status=pending
GET /api/visits/?status=in_progress
GET /api/visits/?status=completed
GET /api/visits/?status=cancelled

# 按医生筛选
GET /api/visits/?doctor_id=1

# 按科室筛选
GET /api/visits/?department_id=1

# 按就诊单号模糊搜索
GET /api/visits/?visit_no=V2024

# 按日期范围筛选
GET /api/visits/?date_from=2024-01-01&date_to=2024-12-31

# 组合筛选：待诊状态 + 宠物名称包含"豆" + 主人是"陈先生"
GET /api/visits/?status=pending&pet_name=豆&owner_name=陈先生
```

### 2. 宠物档案筛选

```bash
# 按宠物名称筛选
GET /api/pets/?name=豆豆

# 按主人姓名筛选
GET /api/pets/?owner_name=陈先生

# 按品种筛选
GET /api/pets/?species=金毛犬

# 按性别筛选
GET /api/pets/?gender=male
```

### 3. 药品筛选

```bash
# 按药品名称筛选
GET /api/medicines/?name=阿莫西林

# 按分类筛选
GET /api/medicines/?category=antibiotic

# 查看低库存药品（库存<=10）
GET /api/medicines/?low_stock=1
```

### 4. 收费单筛选

```bash
# 按支付状态筛选
GET /api/charges/?status=unpaid
GET /api/charges/?status=paid
GET /api/charges/?status=refunded

# 按支付方式筛选
GET /api/charges/?payment_method=wechat
```

## 业务流程示例

### 完整就诊流程

```
1. 【前台】创建主人信息
   POST /api/owners/

2. 【前台】宠物建档
   POST /api/pets/

3. 【前台】挂号就诊（自动生成就诊单号，状态为"待诊"）
   POST /api/visits/

4. 【医生】开始诊疗
   POST /api/visits/{id}/start_treatment/
   状态从"待诊"变为"诊疗中"

5. 【医生】填写病历
   POST /api/medical-records/

6. 【医生】开处方（自动扣减库存，记录库存日志）
   POST /api/prescriptions/

7. 【医生】完成诊疗（自动生成结算单）
   POST /api/visits/{id}/complete/
   状态从"诊疗中"变为"已完成"
   自动计算挂号费 + 药品费 + 治疗费，生成Charge记录

8. 【前台】收费结算
   POST /api/charges/{id}/pay/
```

### 自动编号说明

- **就诊单号**: V + 日期(8位) + 序号(4位)，如 V202401150001
- **收费单号**: C + 日期(8位) + 序号(4位)，如 C202401150001

## 数据校验规则

### 必填字段校验

| 模块 | 必填字段 |
|-----|---------|
| 主人信息 | name, phone |
| 宠物档案 | name, species, gender, age, weight, owner |
| 挂号就诊 | pet, doctor, department, symptom, appointment_time |
| 药品管理 | name, category, specification, unit, price, stock, expiry_date |
| 病历记录 | visit, chief_complaint, physical_exam, diagnosis, treatment_plan |
| 处方明细 | medical_record, medicine, quantity, dosage |
| 收费结算 | visit |

### 数据合法性校验

| 字段 | 校验规则 |
|-----|---------|
| 宠物年龄 | 0-50岁 |
| 宠物体重 | 0-200kg |
| 药品价格 | >= 0 |
| 药品库存 | >= 0 |
| 各项费用 | >= 0 |
| 处方数量 | > 0 |

### 药品库存校验

- 开处方时自动校验药品库存是否充足
- 库存不足时返回错误信息：`药品库存不足，当前库存: X, 需要: Y`
- 开方成功后自动扣减对应库存
- 删除处方时自动回滚库存
- 所有库存变更都有日志记录（InventoryLog）

### 业务唯一性校验

- 一个就诊记录只能有一份病历
- 一个就诊记录只能有一份收费单

### 状态流转校验

| 操作 | 允许的前置状态 |
|-----|-------------|
| 开始诊疗 | 待诊 (pending) |
| 完成诊疗 | 诊疗中 (in_progress) |
| 取消就诊 | 待诊/诊疗中 |
| 支付 | 未支付 (unpaid) |
| 退款 | 已支付 (paid) |

## 自动结算功能

诊疗完成时（调用 `/api/visits/{id}/complete/`），系统会自动：

1. 计算处方药品总费用
2. 自动创建 Charge 结算单
3. 自动填充：挂号费 + 药品费 + 治疗费
4. 自动计算 total_amount 总金额
5. 状态为 unpaid（未支付）

## 项目结构

```
007/
├── manage.py                 # Django管理脚本
├── requirements.txt          # 依赖包列表
├── README.md                # 项目说明文档
├── pet_hospital/            # 项目主配置目录
│   ├── __init__.py
│   ├── settings.py          # 项目配置
│   ├── urls.py              # 主路由配置
│   ├── wsgi.py              # WSGI配置
│   └── asgi.py              # ASGI配置
└── hospital/                # 医院管理应用
    ├── __init__.py
    ├── admin.py             # 管理后台配置
    ├── apps.py              # 应用配置
    ├── models.py            # 数据模型
    ├── serializers.py       # 序列化器
    ├── views.py             # 视图集（含筛选、校验、分页、权限）
    ├── permissions.py       # 自定义权限类
    └── management/          # 自定义管理命令
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── init_data.py # 初始化测试数据脚本
```

## 数据模型说明

### Department (科室)
- 科室名称、描述

### Staff (员工)
- 关联用户、姓名、角色（前台/医生/管理员）、电话、头像、所属科室

### Doctor (医生)
- 关联员工、姓名、所属科室、职称、联系电话、头像

### Owner (主人)
- 姓名、电话、身份证号、住址

### Pet (宠物)
- 名称、品种、种类、性别、年龄、体重、主人、特征描述、照片

### Medicine (药品)
- 名称、分类、规格、单位、单价、库存、生产厂家、有效期

### Visit (挂号就诊)
- 就诊单号(自动生成)、就诊宠物、接诊医生、就诊科室、就诊状态、主诉症状、挂号费、治疗费、预约时间、完成时间

### MedicalRecord (病历记录)
- 关联就诊、主诉、体格检查、诊断结果、治疗方案、医生备注

### Prescription (处方明细)
- 所属病历、药品、数量、用法用量、使用说明

### Charge (收费结算)
- 收费单号(自动生成)、关联就诊、挂号费、药品费、治疗费、其他费用、总金额、支付状态、支付方式、支付时间

### InventoryLog (库存日志)
- 药品、操作类型（入库/出库/退库/调整）、数量、操作前库存、操作后库存、关联就诊、操作人、备注

## 注意事项

1. 确保MySQL服务已启动
2. 修改settings.py中的数据库配置以匹配您的环境
3. 生产环境部署时请修改SECRET_KEY并设置DEBUG=False
4. 建议使用虚拟环境进行依赖管理
5. 删除处方时会自动回滚药品库存，请谨慎操作
6. 所有库存变更都有日志记录，可通过 `/api/inventory-logs/` 查看
