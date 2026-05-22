# 企业考勤管理系统后端

基于 Python + Django + MySQL 实现的企业考勤管理系统后端，支持按部门、日期、考勤状态筛选，自动识别异常考勤，加班时长与打卡时长比对，完善的分页与数据格式化处理。支持月度考勤自动汇总、请假审批流程自动流转、加班时长折算调休、Excel数据归档导出。

## 功能特性

### 核心功能
- **员工管理**：部门、员工信息 CRUD、搜索、筛选
- **考勤打卡**：员工签到签退，自动判断迟到早退，计算工作时长
- **请假管理**：请假申请提交、审批流程（批准/拒绝/转审），自动扣除假期余额
- **加班管理**：加班登记、审批流程，自动比对打卡时长，支持折算调休
- **考勤统计**：月度考勤统计自动生成，支持按部门筛选
- **薪资核算**：根据考勤数据自动计算薪资（加班费、扣款等）
- **数据导出**：考勤记录、薪资报表、考勤统计 Excel 导出
- **自动编号**：所有业务单据自动生成唯一编号

### 新增优化功能（V2.0）
- **多维度筛选**：支持按部门、日期范围、考勤状态、异常标识等筛选
- **异常考勤识别**：自动识别迟到、早退、缺卡、工时不足等多种异常，提供异常统计
- **加班时长比对**：自动计算实际打卡加班时长与申报时长的差异，标记异常
- **月度汇总**：按部门自动生成月度考勤汇总报告，支持确认和归档
- **调休管理**：加班自动折算调休，支持不同类型加班的不同折算比例
- **假期余额**：自动管理年假、病假、事假、调休的余额和使用记录
- **审批日志**：完整记录所有审批操作，支持审批流程转审
- **数据归档**：支持按月份、部门归档考勤数据，永久保存可下载
- **分页与排序**：所有列表接口支持分页、多字段排序、关键字搜索
- **数据格式化**：日期、时间统一格式化显示，计算字段自动展示

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.14
- django-filter 23.5
- MySQL
- pandas + openpyxl (Excel 导出)

## 安装部署

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 MySQL 数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE attendance_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `attendance_system/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'attendance_db',
        'USER': 'root',           # 你的 MySQL 用户名
        'PASSWORD': '123456',     # 你的 MySQL 密码
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 5. 初始化测试数据（可选）

```bash
python init_data.py
```

### 6. 启动服务

```bash
python manage.py runserver
```

访问地址：http://127.0.0.1:8000/

## API 接口文档

### 基础路径

所有 API 接口前缀：`/api/`

### 分页参数

所有列表接口支持分页：
- `page`: 页码（默认 1）
- `page_size`: 每页数量（默认 20，可在 settings 配置）
- `ordering`: 排序字段（如 `ordering=-attendance_date` 降序）
- `search`: 关键字搜索

### 部门管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/departments/` | 获取部门列表 |
| POST | `/api/departments/` | 创建部门 |
| GET | `/api/departments/{id}/` | 获取部门详情 |
| PUT | `/api/departments/{id}/` | 更新部门 |
| DELETE | `/api/departments/{id}/` | 删除部门 |

### 员工管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/employees/` | 获取员工列表 |
| POST | `/api/employees/` | 创建员工 |
| GET | `/api/employees/{id}/` | 获取员工详情 |
| PUT | `/api/employees/{id}/` | 更新员工 |
| DELETE | `/api/employees/{id}/` | 删除员工 |

**筛选参数**：
- `department`: 部门 ID
- `is_active`: 是否在职 (true/false)
- `gender`: 性别
- `search`: 搜索关键词（姓名、工号、电话、邮箱）

### 考勤记录

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/attendance-records/` | 获取考勤记录列表 |
| POST | `/api/attendance-records/` | 创建考勤记录 |
| POST | `/api/attendance-records/check_in/` | 员工签到 |
| POST | `/api/attendance-records/check_out/` | 员工签退 |
| GET | `/api/attendance-records/today_records/` | 获取今日考勤 |
| GET | `/api/attendance-records/exception_summary/` | 异常考勤统计 |

**筛选参数**：
- `department`: 部门 ID
- `employee`: 员工 ID
- `start_date`: 开始日期 (YYYY-MM-DD)
- `end_date`: 结束日期 (YYYY-MM-DD)
- `status`: 考勤状态 (normal/late/early_leave/absent)
- `is_exception`: 是否异常 (true/false)
- `search`: 搜索关键词

**签到示例**：
```json
POST /api/attendance-records/check_in/
{
    "employee_id": 1
}
```

**返回字段说明**：
- `late_minutes`: 迟到分钟数
- `early_leave_minutes`: 早退分钟数
- `is_exception`: 是否异常考勤
- `exception_type`: 异常类型（missing_checkin 缺签到、missing_checkout 缺签退、late 迟到、early_leave 早退、work_hours_abnormal 工时异常、multi_exception 多异常）
- `exception_desc`: 异常描述

### 请假申请

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/leave-requests/` | 获取请假列表 |
| POST | `/api/leave-requests/` | 提交请假申请 |
| POST | `/api/leave-requests/{id}/approve/` | 批准请假 |
| POST | `/api/leave-requests/{id}/reject/` | 拒绝请假 |
| POST | `/api/leave-requests/{id}/transfer/` | 转审请假 |
| GET | `/api/leave-requests/pending/` | 获取待审批请假 |
| GET | `/api/leave-requests/approval_history/` | 获取审批历史 |

**筛选参数**：
- `department`: 部门 ID
- `employee`: 员工 ID
- `start_date`: 开始日期
- `end_date`: 结束日期
- `leave_type`: 请假类型（annual 年假、sick 病假、personal 事假、marriage 婚假、maternity 产假、other 其他）
- `status`: 状态（pending 待审批、approved 已批准、rejected 已拒绝）
- `search`: 搜索关键词

**审批示例**：
```json
POST /api/leave-requests/1/approve/
{
    "approver": "张三",
    "remark": "同意请假"
}
```

**转审示例**：
```json
POST /api/leave-requests/1/transfer/
{
    "operator": "张三",
    "next_approver": "李四",
    "remark": "请李经理审批"
}
```

### 加班登记

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/overtimes/` | 获取加班列表 |
| POST | `/api/overtimes/` | 提交加班登记 |
| POST | `/api/overtimes/{id}/approve/` | 批准加班（支持自动折算调休） |
| POST | `/api/overtimes/{id}/reject/` | 拒绝加班 |
| GET | `/api/overtimes/pending/` | 获取待审批加班 |
| GET | `/api/overtimes/discrepancy_summary/` | 加班差异统计 |

**筛选参数**：
- `department`: 部门 ID
- `employee`: 员工 ID
- `start_date`: 开始日期
- `end_date`: 结束日期
- `overtime_type`: 加班类型（weekday 工作日、weekend 周末、holiday 节假日）
- `status`: 状态
- `has_discrepancy`: 是否有差异 (true/false)
- `search`: 搜索关键词

**批准加班示例**：
```json
POST /api/overtimes/1/approve/
{
    "approver": "张三",
    "remark": "同意加班",
    "convert_to_cl": true
}
```

**差异类型说明**：
- `less`: 实际打卡时长不足申报时长
- `more`: 实际打卡时长超出申报时长
- `no_record`: 无打卡记录
- `none`: 无差异

**返回字段说明**：
- `hours`: 申报加班时长
- `actual_hours`: 实际打卡加班时长
- `hours_discrepancy`: 时长差异（申报-实际）
- `discrepancy_type`: 差异类型
- `has_discrepancy`: 是否存在差异

### 调休管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/compensatory-leaves/` | 获取调休列表 |
| GET | `/api/compensatory-leaves/employee_summary/` | 获取员工调休汇总 |

**筛选参数**：
- `status`: 状态（pending 待生效、available 可使用、used 已使用、expired 已过期）
- `search`: 搜索关键词

**调休折算比例**：
- 工作日加班：1:1
- 周末加班：1:1.2
- 节假日加班：1:1.5

### 假期余额

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/leave-balances/` | 获取假期余额列表 |
| GET | `/api/leave-balances/employee_balance/` | 获取员工假期余额 |

**假期类型**：
- `annual_leave`: 年假（默认 10 天/年）
- `sick_leave`: 病假（默认 12 天/年）
- `personal_leave`: 事假（默认 6 天/年）
- `compensatory_leave`: 调休（按加班自动累计）

### 考勤统计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/attendance-statistics/` | 获取统计列表 |
| POST | `/api/attendance-statistics/generate_statistics/` | 生成月度考勤统计 |
| GET | `/api/attendance-statistics/by_month/` | 按月份查询 |

**筛选参数**：
- `department`: 部门 ID
- `employee`: 员工 ID
- `year`: 年份
- `month`: 月份
- `search`: 搜索关键词

### 月度汇总

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/monthly-summaries/` | 获取月度汇总列表 |
| POST | `/api/monthly-summaries/generate_summaries/` | 按部门生成月度汇总 |
| POST | `/api/monthly-summaries/{id}/confirm/` | 确认月度汇总 |

**返回字段说明**：
- `total_employees`: 员工总数
- `avg_attendance_rate`: 平均出勤率
- `total_late_times`: 总迟到次数
- `total_early_leave_times`: 总早退次数
- `total_absent_days`: 总旷工天数
- `total_leave_days`: 总请假天数
- `total_overtime_hours`: 总加班时长
- `exception_count`: 异常考勤人数
- `status`: 状态（draft 草稿、confirmed 已确认、archived 已归档）

### 薪资核算

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/salary-calculations/` | 获取薪资列表 |
| POST | `/api/salary-calculations/calculate_salary/` | 计算月度薪资 |
| GET | `/api/salary-calculations/by_month/` | 按月份查询 |

**筛选参数**：
- `department`: 部门 ID
- `employee`: 员工 ID
- `year`: 年份
- `month`: 月份
- `search`: 搜索关键词

### 审批日志

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/approval-logs/` | 获取审批日志列表 |

**筛选参数**：
- `related_type`: 关联类型（leave 请假、overtime 加班）
- `search`: 搜索关键词

### 数据导出

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/exports/attendance_records/` | 导出考勤记录 |
| GET | `/api/exports/salary_report/` | 导出薪资报表 |
| GET | `/api/exports/attendance_statistics/` | 导出考勤统计 |
| POST | `/api/exports/archive_attendance/` | 归档考勤数据 |
| GET | `/api/exports/archives/` | 获取归档记录列表 |
| GET | `/api/exports/{id}/download_archive/` | 下载归档文件 |

**导出参数**：
- 考勤记录：`start_date`, `end_date`, `department_id`, `employee_id`, `is_exception`
- 薪资报表/考勤统计：`year`, `month`, `department_id`

**归档示例**：
```json
POST /api/exports/archive_attendance/
{
    "year": 2024,
    "month": 1,
    "department_id": 1,
    "archived_by": "管理员",
    "remark": "2024年1月技术部考勤归档"
}
```

## 调休折算规则

| 加班类型 | 折算比例 | 说明 |
|---------|---------|------|
| 工作日加班 | 1:1.0 | 1小时加班 = 1小时调休 |
| 周末加班 | 1:1.2 | 1小时加班 = 1.2小时调休 |
| 节假日加班 | 1:1.5 | 1小时加班 = 1.5小时调休 |

## 考勤规则

- 工作时间：09:00 - 18:00
- 迟到：签到时间 > 09:00（计算迟到分钟数）
- 早退：签退时间 < 18:00（计算早退分钟数）
- 旷工：当日无签到记录
- 工时异常：实际工作时长不足 4 小时

## 薪资计算规则

- 日薪 = 基本工资 / 21.75
- 时薪 = 日薪 / 8
- 加班费 = 加班时长 × 时薪 × 1.5
- 请假扣款 = 请假天数 × 日薪
- 迟到扣款 = 迟到次数 × 50元
- 旷工扣款 = 旷工天数 × 日薪 × 2
- 实发工资 = 基本工资 + 加班费 + 奖金 - 请假扣款 - 迟到扣款 - 旷工扣款

## 项目结构

```
attendance_system/
├── attendance_app/
│   ├── models.py           # 数据模型（含异常识别、加班比对逻辑）
│   ├── serializers.py      # 序列化器（含数据格式化、计算字段）
│   ├── views.py            # 视图/API接口（含筛选、分页、统计功能）
│   ├── filters.py          # 筛选器（多维度筛选支持）
│   ├── urls.py             # 路由配置
│   ├── admin.py            # 管理后台配置
│   └── apps.py             # 应用配置
├── attendance_system/
│   ├── settings.py         # 项目设置（DRF 配置、分页、日期格式化）
│   ├── urls.py             # 主路由
│   └── wsgi.py             # WSGI配置
├── manage.py               # Django 管理脚本
├── init_data.py            # 初始化数据脚本
├── requirements.txt        # 依赖包列表
└── README.md               # 项目说明
```
