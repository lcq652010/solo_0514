# 医疗器械租赁平台后端

基于 Django + Django REST Framework + MySQL 实现的医疗器械租赁管理系统后端。

## 功能特性

### 核心功能
- ✅ 设备建档管理（含使用科室字段）
- ✅ 机构信息管理
- ✅ 租赁申请与审批流程
- ✅ 租期设置与管理
- ✅ 自动生成租赁单号（格式：RE + 年月日 + 4位序号）
- ✅ 定期校准登记
- ✅ 设备归还验收
- ✅ 费用结算管理
- ✅ 数据统计仪表板

### 新增功能
- ✅ **多条件筛选**：支持按设备类型、使用科室、租赁状态、校准状态筛选
- ✅ **校准有效期校验**：自动计算校准剩余天数，分级提醒
- ✅ **租期倒计时提醒**：租赁到期提醒，支持逾期状态标记
- ✅ **设备状态联动更新**：租赁、校准、维修流程中设备状态自动联动更新
- ✅ **续租功能**：租期自动顺延，不重叠
- ✅ **设备利用率统计**：自动统计设备30天利用率、总租赁天数、总收入
- ✅ **损耗记录管理**：归还时自动生成损耗记录，关联设备和租赁
- ✅ **维修流程管理**：损耗记录关联维修，支持维修流程管理
- ✅ **精准租金核算**：按实际使用天数核算，支持逾期加价
- ✅ **费用明细拆分**：租金费用、逾期费用、损坏赔偿、其他费用分别统计

---

## 环境要求

- Python 3.8+
- MySQL 5.7+ / 8.0+

## 快速开始

### 1. 数据库准备

首先在 MySQL 中创建数据库：

```sql
CREATE DATABASE medical_rental CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. 配置环境变量

编辑 `.env` 文件，修改数据库连接信息：

```env
DB_NAME=medical_rental
DB_USER=root
DB_PASSWORD=你的密码
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key-here
DEBUG=True
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

服务启动后访问：
- API 根地址：http://localhost:8000/api/
- 管理后台：http://localhost:8000/admin/

---

## API 接口列表

### 机构管理 (`/api/institutions/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/institutions/` | 机构列表（支持筛选：is_active） |
| POST | `/api/institutions/` | 创建机构 |
| GET | `/api/institutions/{id}/` | 机构详情 |
| PUT | `/api/institutions/{id}/` | 修改机构 |
| DELETE | `/api/institutions/{id}/` | 删除机构 |

### 设备管理 (`/api/devices/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/devices/` | 设备列表（支持多条件筛选） |
| POST | `/api/devices/` | 创建设备 |
| GET | `/api/devices/{id}/` | 设备详情 |
| PUT | `/api/devices/{id}/` | 修改设备 |
| DELETE | `/api/devices/{id}/` | 删除设备 |
| GET | `/api/devices/filters/` | 获取筛选项 |
| GET | `/api/devices/utilization_stats/` | 获取设备利用率统计 |
| GET | `/api/devices/calibration_alerts/` | 校准提醒统计 |
| POST | `/api/devices/{id}/start_rental/` | 开始租赁 |
| POST | `/api/devices/{id}/end_rental/` | 结束租赁 |
| POST | `/api/devices/{id}/start_calibration/` | 开始校准 |
| POST | `/api/devices/{id}/complete_calibration/` | 完成校准 |
| POST | `/api/devices/{id}/start_maintenance/` | 开始维修 |
| POST | `/api/devices/{id}/complete_maintenance/` | 完成维修 |
| POST | `/api/devices/{id}/retire/` | 设备报废 |

**设备筛选参数**：
- `device_type`: 设备类型
- `use_department`: 使用科室
- `status`: 设备状态
- `calibration_status`: 校准状态 (normal/warning/urgent/expired)

**设备状态值**：
- `available`: 可租赁
- `rented`: 已租赁
- `calibrating`: 校准中
- `maintenance`: 维修中
- `retired`: 已报废

**使用科室选项**：
- `emergency`: 急诊科
- `icu`: ICU
- `operating`: 手术室
- `internal`: 内科
- `surgical`: 外科
- `pediatric`: 儿科
- `obstetrics`: 妇产科
- `radiology`: 放射科
- `cardiology`: 心内科
- `neurology`: 神经科
- `other`: 其他科室

### 租赁管理 (`/api/rentals/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/rentals/` | 租赁列表（支持多条件筛选） |
| POST | `/api/rentals/` | 创建租赁申请 |
| GET | `/api/rentals/{id}/` | 租赁详情 |
| PUT | `/api/rentals/{id}/` | 修改租赁 |
| DELETE | `/api/rentals/{id}/` | 删除租赁 |
| GET | `/api/rentals/rental_alerts/` | 租期提醒统计 |
| POST | `/api/rentals/{id}/renew/` | 续租 |
| POST | `/api/rentals/{id}/approve/` | 审批通过 |
| POST | `/api/rentals/{id}/start_rental/` | 开始租赁 |
| POST | `/api/rentals/{id}/return_device/` | 归还设备 |
| POST | `/api/rentals/{id}/cancel/` | 取消租赁 |

**租赁筛选参数**：
- `status`: 租赁状态
- `institution`: 机构ID
- `device`: 设备ID
- `countdown_status`: 租期状态 (normal/warning/urgent/overdue)
- `start_date_from`: 开始日期起
- `start_date_to`: 开始日期止
- `end_date_from`: 结束日期起
- `end_date_to`: 结束日期止

**租赁状态值**：
- `pending`: 待审批
- `approved`: 已批准
- `active`: 租赁中
- `returned`: 已归还
- `completed`: 已完成
- `renewed`: 已续租
- `cancelled`: 已取消

**续租接口参数**：
```json
{
  "renewal_days": 30,
  "new_daily_fee": 150.00
}
```
- `renewal_days`: 续租天数（必填）
- `new_daily_fee`: 新的日租金（可选，默认沿用原有日租金）

### 损耗记录 (`/api/damage-records/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/damage-records/` | 损耗记录列表 |
| POST | `/api/damage-records/` | 创建损耗记录 |
| GET | `/api/damage-records/{id}/` | 损耗记录详情 |
| PUT | `/api/damage-records/{id}/` | 修改损耗记录 |
| DELETE | `/api/damage-records/{id}/` | 删除损耗记录 |

**损坏类型**：
- `appearance`: 外观损坏
- `function`: 功能故障
- `accessory`: 配件丢失
- `other`: 其他

**损坏程度**：
- `minor`: 轻微
- `moderate`: 中等
- `severe`: 严重

### 维修记录 (`/api/maintenance-records/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/maintenance-records/` | 维修记录列表 |
| POST | `/api/maintenance-records/` | 创建维修记录 |
| GET | `/api/maintenance-records/{id}/` | 维修记录详情 |
| PUT | `/api/maintenance-records/{id}/` | 修改维修记录 |
| DELETE | `/api/maintenance-records/{id}/` | 删除维修记录 |
| POST | `/api/maintenance-records/{id}/start_maintenance/` | 开始维修 |
| POST | `/api/maintenance-records/{id}/complete_maintenance/` | 完成维修 |

**维修类型**：
- `damage`: 损坏维修
- `preventive`: 预防性维护
- `calibration_failure`: 校准未通过维修
- `other`: 其他

**维修状态**：
- `pending`: 待维修
- `in_progress`: 维修中
- `completed`: 已完成
- `cancelled`: 已取消

### 校准管理 (`/api/calibrations/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/calibrations/` | 校准列表 |
| POST | `/api/calibrations/` | 创建校准记录 |
| GET | `/api/calibrations/{id}/` | 校准详情 |
| PUT | `/api/calibrations/{id}/` | 修改校准 |
| DELETE | `/api/calibrations/{id}/` | 删除校准 |
| POST | `/api/calibrations/{id}/start_calibration/` | 开始校准 |
| POST | `/api/calibrations/{id}/complete_calibration/` | 完成校准 |
| POST | `/api/calibrations/{id}/fail_calibration/` | 校准未通过 |

### 归还验收 (`/api/return-acceptances/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/return-acceptances/` | 验收列表 |
| POST | `/api/return-acceptances/` | 创建验收（自动创建结算单） |
| GET | `/api/return-acceptances/{id}/` | 验收详情 |
| PUT | `/api/return-acceptances/{id}/` | 修改验收 |
| DELETE | `/api/return-acceptances/{id}/` | 删除验收 |
| POST | `/api/return-acceptances/{id}/create_damage_record/` | 创建损耗记录 |
| POST | `/api/return-acceptances/{id}/create_maintenance_record/` | 创建维修记录 |

### 费用结算 (`/api/settlements/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/settlements/` | 结算列表 |
| POST | `/api/settlements/` | 创建结算 |
| GET | `/api/settlements/{id}/` | 结算详情 |
| PUT | `/api/settlements/{id}/` | 修改结算 |
| DELETE | `/api/settlements/{id}/` | 删除结算 |
| POST | `/api/settlements/{id}/mark_paid/` | 标记已付款 |

### 仪表板统计 (`/api/dashboard/`)
| 方法 | 接口 | 说明 |
|------|------|------|
| GET | `/api/dashboard/` | 统计数据（设备、租赁、收入、提醒、维修等） |

---

## 业务流程说明

### 完整租赁流程

```
创建设备(available) → 创建租赁申请(pending) → 审批通过(approved)
→ 开始租赁(active + rented) → 归还验收(returned + available)
→ 费用结算(completed)
```

#### 详细步骤：
1. **创建机构信息** - 维护租赁机构基本信息
2. **创建设备档案** - 设备信息录入，选择设备类型和使用科室，默认状态：可租赁(available)
3. **创建租赁申请** - 选择机构、设备，设置租期，系统自动校验设备可用性（状态必须为可租赁且校准未过期），自动生成租赁单号
4. **审批租赁申请** - 管理员审批通过后，状态变为：已批准(approved)
5. **开始租赁** - 设备借出，联动更新设备状态为：已租赁(rented)，租赁状态变为：租赁中(active)
6. **设备续租** - 租赁中支持续租，新租期自动顺延不重叠，原租赁状态变为：已续租(renewed)
7. **归还验收** - 设备归还检查，记录损坏情况
   - 自动计算实际使用天数，包含逾期天数
   - 设备状态联动恢复为：可租赁(available)
   - 租赁状态变为：已归还(returned)
   - 自动创建费用结算单
8. **创建损耗记录** - 发现设备损坏时，记录损坏情况、程度、预估维修费用
9. **创建维修记录** - 关联损耗记录，进入维修流程
   - 开始维修：设备状态变为维修中(maintenance)
   - 完成维修：设备状态恢复为可租赁(available)，记录维修成本
10. **费用结算** - 确认付款后，租赁状态变为：已完成(completed)

### 续租流程

```
租赁中(active) → 申请续租 → 创建新租赁，租期自动顺延
→ 原租赁状态变为已续租(renewed) → 新租赁状态为已批准(approved)
```

**续租规则**：
- 只有租赁中(active)的租赁可以申请续租
- 新租期从原租期结束日次日开始
- 如果原租期已结束，从次日开始计算
- 支持重新设置日租金

### 校准流程

```
可租赁设备 → 创建校准记录 → 开始校准(calibrating)
→ 完成校准(available) / 未通过校准(maintenance)
```

1. **创建校准记录** - 登记设备校准计划
2. **开始校准** - 设备进入校准状态(calibrating)
3. **完成校准** - 校准通过，联动更新：
   - 设备状态恢复为：可租赁(available)
   - 自动更新设备的最后校准日期和下次校准日期
4. **校准未通过** - 设备需要维修，联动进入维修状态(maintenance)，自动创建维修记录

### 维修流程

```
可租赁设备 → 开始维修(maintenance) → 完成维修(available)
```

**触发维修的场景**：
1. 归还验收发现设备损坏，创建维修记录
2. 校准未通过，自动进入维修流程
3. 预防性维护，手动创建维修记录

**维修流程**：
1. 创建维修记录（可关联损耗记录）
2. 开始维修：设备状态变为维修中(maintenance)
3. 完成维修：记录零件费用、人工费用，设备状态恢复为可租赁(available)

### 租金精准核算

**计算公式**：
```
实际使用天数 = (实际归还日期 - 实际开始日期) + 1
逾期天数 = max(0, 实际归还日期 - 约定结束日期)
正常租赁天数 = 实际使用天数 - 逾期天数
正常租金 = 正常租赁天数 × 日租金
逾期租金 = 逾期天数 × 日租金 × 1.5
实际总租金 = 正常租金 + 逾期租金
```

**费用组成**：
- `rental_fee`: 正常租赁费用（不含逾期）
- `overtime_fee`: 逾期费用（正常日租金的1.5倍）
- `damage_fee`: 损坏赔偿费用
- `other_fee`: 其他费用
- `total_amount`: 总金额 = 租赁费用 + 逾期费用 + 损坏赔偿 + 其他费用

---

## 校准有效期校验规则

系统自动计算设备校准剩余天数，并分为以下状态：

| 状态 | 剩余天数 | 说明 | 影响 |
|------|----------|------|------|
| `expired` | ≤ 0天 | 已过期 | ❌ 设备不可租赁 |
| `urgent` | 1-7天 | 紧急，即将过期 | ⚠️ 提醒，仍可租赁 |
| `warning` | 8-30天 | 提醒，需关注 | ⚠️ 提醒，仍可租赁 |
| `normal` | > 30天 | 正常，无需关注 | ✅ 正常租赁 |

**校验逻辑**：
- 设备可租赁的前提：设备状态为可租赁 **且** 校准未过期
- 校准过期的设备无法创建租赁申请
- 通过 `/api/devices/calibration_alerts/` 可获取各级别提醒数量

---

## 租期倒计时提醒规则

系统自动计算租赁剩余天数，并分为以下状态：

| 状态 | 剩余天数 | 说明 |
|------|----------|------|
| `overdue` | ≤ 0天 | 已逾期 |
| `urgent` | 1天 | 紧急，明天到期 |
| `warning` | 2-3天 | 提醒，3天内到期 |
| `normal` | > 3天 | 正常 |

**提醒接口**：
- 通过 `/api/rentals/rental_alerts/` 可获取各级别提醒数量
- 支持按 `countdown_status` 参数筛选对应状态的租赁记录

---

## 设备状态联动说明

系统支持完整的设备状态流转，确保数据一致性：

| 操作 | 设备状态变化 | 触发条件 |
|------|--------------|----------|
| 开始租赁 | available → rented | 租赁开始 |
| 归还设备 | rented → available | 租赁归还验收 |
| 开始校准 | available → calibrating | 创建校准任务 |
| 校准完成 | calibrating → available | 校准通过 |
| 校准未通过 | calibrating → maintenance | 校准不通过 |
| 开始维修 | available/rented → maintenance | 创建维修任务 |
| 维修完成 | maintenance → available | 维修完成 |
| 设备报废 | * → retired | 设备报废（租赁中不可报废） |

**重要说明**：
- 租赁中的设备不可直接报废
- 所有状态变更都有明确的业务校验规则
- 状态联动自动完成，无需手动干预

---

## 设备利用率统计

**计算公式**：
```
设备利用率 = (设备总租赁天数 / 统计周期天数) × 100%
```

**统计接口**：
- `/api/devices/utilization_stats/` - 获取所有设备的利用率统计
- 支持自定义统计天数（默认30天）
- 返回：设备利用率、总租赁天数、总收入

**返回字段**：
```json
{
  "days": 30,
  "avg_utilization": 68.5,
  "device_utilization": [
    {
      "device_id": 1,
      "device_name": "监护仪A",
      "device_type": "monitor",
      "utilization_rate": 85.0,
      "total_rental_days": 25,
      "total_revenue": 12500.00
    }
  ]
}
```

---

## 数据模型

### Institution（机构）
- 机构名称、联系人、联系电话、地址、营业执照号、是否激活

### Device（设备）
- 设备名称、设备类型、使用科室、型号、序列号、生产厂家
- 生产日期、采购日期、日租金、校准周期(天)
- 上次校准日期、下次校准日期、状态、设备描述
- 支持方法：`get_calibration_days_remaining()`, `get_calibration_status()`, `can_be_rented()`, `get_utilization_rate()`, `get_total_rental_days()`, `get_total_rental_revenue()`

### Rental（租赁记录）
- 租赁单号、租赁机构、租赁设备、原租赁记录（用于续租）
- 联系人、联系电话、租赁开始/结束日期、实际开始/结束日期
- 预计租赁天数、实际租赁天数、日租金、预计总金额、实际总金额
- 逾期天数、逾期费用、租赁状态、申请备注、审批备注
- 支持方法：`get_rental_days_remaining()`, `get_rental_countdown_status()`, `renew()`, `approve()`, `start()`, `return_device()`, `complete()`, `cancel()`, `calculate_actual_fee()`

### Calibration（校准记录）
- 设备、校准日期、校准人员、校准机构、证书号
- 校准状态、校准结果、下次校准日期、备注
- 支持方法：`start_calibration()`, `complete_calibration()`, `fail_calibration()`

### DamageRecord（损耗记录）
- 设备、租赁记录、检查人员、损坏类型、损坏程度
- 损坏描述、预估维修费用、损坏图片、是否需要维修
- 支持关联：`maintenance_record` - 关联的维修记录

### MaintenanceRecord（维修记录）
- 设备、关联损耗记录、维修类型、维修状态
- 报修人、报修日期、维修人员、开始维修日期、完成维修日期
- 维修内容、维修结果、零件费用、人工费用、总费用、备注
- 支持方法：`start_maintenance()`, `complete_maintenance()`

### ReturnAcceptance（归还验收）
- 租赁记录、归还日期、验收人员
- 外观检查、功能检查、配件检查、验收状态
- 发现问题、损坏赔偿费用、验收备注
- 关联损耗记录、关联维修记录
- 支持方法：`create_damage_record()`, `create_maintenance_record()`

### Settlement（费用结算）
- 租赁记录、验收记录、租赁天数、租赁费用
- 逾期天数、逾期费用、损坏赔偿、其他费用、其他费用说明、总金额
- 结算状态、付款方式、付款日期、发票号、备注

---

## 筛选与搜索

### 通用筛选
所有列表接口支持搜索（`search=关键词`）

### 设备专属筛选
- 设备类型：`device_type`
- 使用科室：`use_department`
- 设备状态：`status`
- 校准状态：`calibration_status` (normal/warning/urgent/expired)

### 租赁专属筛选
- 租赁状态：`status`
- 机构ID：`institution`
- 设备ID：`device`
- 租期状态：`countdown_status` (normal/warning/urgent/overdue)
- 租期范围：`start_date_from`, `start_date_to`, `end_date_from`, `end_date_to`

### 损耗记录筛选
- 损坏类型：`damage_type`
- 损坏程度：`damage_level`
- 是否需要维修：`needs_maintenance`
- 设备ID：`device`
- 租赁ID：`rental`

### 维修记录筛选
- 维修状态：`status`
- 维修类型：`maintenance_type`
- 设备ID：`device`

---

## 项目结构

```
medical_rental/
├── config/              # Django配置目录
│   ├── settings.py      # 主配置文件
│   ├── urls.py          # URL路由配置
│   └── wsgi.py          # WSGI入口
├── rental/              # 租赁应用
│   ├── migrations/      # 数据库迁移
│   ├── models.py        # 数据模型（含业务逻辑）
│   ├── serializers.py   # 序列化器
│   ├── views.py         # 视图集（含API接口）
│   └── admin.py         # 管理后台配置
├── manage.py            # Django管理脚本
├── requirements.txt     # 依赖包列表
├── .env                 # 环境变量配置
└── README.md            # 本文件
```

---

## 版本更新日志

### v2.0 (最新)
- ✅ 新增使用科室字段
- ✅ 实现多条件筛选功能
- ✅ 实现校准有效期校验
- ✅ 实现租期倒计时提醒
- ✅ 完善设备状态联动更新
- ✅ 实现续租功能，租期自动顺延不重叠
- ✅ 新增设备利用率自动统计
- ✅ 新增损耗记录管理模块
- ✅ 新增维修流程管理
- ✅ 租金按实际使用天数精准核算，支持逾期加价
- ✅ 费用明细拆分（租赁费用、逾期费用、损坏赔偿）
- ✅ 归还验收关联损耗记录和维修记录
- ✅ 更新仪表板统计，新增维修统计数据

### v1.0
- ✅ 基础设备管理
- ✅ 机构管理
- ✅ 租赁申请与审批
- ✅ 校准登记
- ✅ 归还验收
- ✅ 费用结算
- ✅ 数据统计仪表板
