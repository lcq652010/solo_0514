# 企业人事考勤薪资系统后端

基于 Python + Django + MySQL 开发的企业人事管理系统后端，提供完整的员工档案管理、考勤打卡、请假审批、加班登记、薪资核算功能。

## 功能特性

### 1. 员工档案管理
- 自动生成工号（格式：EMP + 年月日 + 4位随机数）
- 员工基本信息管理（姓名、性别、手机号、邮箱、身份证号等）
- 部门、职位关联
- 入职日期、状态管理
- 基本工资设置

### 2. 考勤打卡管理
- 签到/签退功能
- 考勤状态自动判断：正常、迟到、早退、旷工
- 工作时长自动计算
- 考勤记录查询

### 3. 请假审批管理
- 多种请假类型（病假、事假、年假、婚假、产假）
- 请假天数自动计算
- 审批流程（待审批、已通过、已拒绝）
- 审批人、审批备注

### 4. 加班登记管理
- 多种加班类型（工作日加班、周末加班、节假日加班）
- 加班时长自动计算
- 审批流程（待审批、已通过、已拒绝）

### 5. 月度薪资核算
- 基本工资、加班费自动核算
- 加班费计算（工作日1.5倍、周末2倍、节假日3倍）
- 扣款计算（迟到50元/次、旷工按日工资扣除、事假按日工资扣除）
- 实发工资自动计算
- 工资条自动生成

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.15
- MySQL 5.7+
- mysqlclient 2.2

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+
- MySQL 客户端库（Windows 可能需要安装 Visual C++ 编译环境）

### 2. 创建虚拟环境（可选）

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置数据库

1. 创建 MySQL 数据库：
```sql
CREATE DATABASE hrms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 修改 `.env` 文件中的数据库配置：
```env
DB_NAME=hrms_db
DB_USER=root
DB_PASSWORD=你的密码
DB_HOST=localhost
DB_PORT=3306
```

### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员

```bash
python manage.py createsuperuser
```

### 7. 启动服务

```bash
python manage.py runserver
```

访问：http://127.0.0.1:8000/

## API 接口文档

### 基础 URL 接口

#### 部门管理
- `GET /api/departments/` - 获取部门列表
- `POST /api/departments/` - 创建部门
- `GET /api/departments/{id}/` - 获取部门详情
- `PUT /api/departments/{id}/` - 更新部门
- `DELETE /api/departments/{id}/` - 删除部门

#### 职位管理
- `GET /api/positions/` - 获取职位列表
- `POST /api/positions/` - 创建职位
- `GET /api/positions/{id}/` - 获取职位详情
- `PUT /api/positions/{id}/` - 更新职位
- `DELETE /api/positions/{id}/` - 删除职位

#### 员工管理
- `GET /api/employees/` - 获取员工列表（支持筛选：department, status, keyword）
- `POST /api/employees/` - 创建员工（自动生成工号）
- `GET /api/employees/{id}/` - 获取员工详情
- `PUT /api/employees/{id}/` - 更新员工
- `DELETE /api/employees/{id}/` - 删除员工

#### 考勤管理
- `GET /api/attendances/` - 获取考勤列表（支持筛选：employee, date, start_date, end_date, status）
- `POST /api/attendances/` - 创建考勤
- `POST /api/attendances/check_in/` - 签到
- `POST /api/attendances/check_out/` - 签退
- `GET /api/attendances/{id}/` - 获取考勤详情
- `PUT /api/attendances/{id}/` - 更新考勤
- `DELETE /api/attendances/{id}/` - 删除考勤

#### 请假管理
- `GET /api/leaves/` - 获取请假列表（支持筛选：employee, status, leave_type）
- `POST /api/leaves/` - 申请请假
- `POST /api/leaves/{id}/approve/` - 审批通过
- `POST /api/leaves/{id}/reject/` - 审批拒绝
- `GET /api/leaves/{id}/` - 获取请假详情
- `PUT /api/leaves/{id}/` - 更新请假
- `DELETE /api/leaves/{id}/` - 删除请假

#### 加班管理
- `GET /api/overtimes/` - 获取加班列表（支持筛选：employee, status, overtime_type）
- `POST /api/overtimes/` - 申请加班
- `POST /api/overtimes/{id}/approve/` - 审批通过
- `POST /api/overtimes/{id}/reject/` - 审批拒绝
- `GET /api/overtimes/{id}/` - 获取加班详情
- `PUT /api/overtimes/{id}/` - 更新加班
- `DELETE /api/overtimes/{id}/` - 删除加班

#### 薪资管理
- `GET /api/salaries/` - 获取薪资列表（支持筛选：employee, year, month）
- `POST /api/salaries/` - 创建薪资
- `POST /api/salaries/batch_generate/` - 批量生成薪资（参数：year, month）
- `GET /api/salaries/{id}/` - 获取薪资详情
- `PUT /api/salaries/{id}/` - 更新薪资
- `DELETE /api/salaries/{id}/` - 删除薪资

#### 工资条管理
- `GET /api/payslips/` - 获取工资条列表（支持筛选：employee, issued, year, month）
- `POST /api/payslips/` - 创建工资条
- `POST /api/payslips/{id}/issue/` - 发放工资条
- `GET /api/payslips/{id}/` - 获取工资条详情
- `PUT /api/payslips/{id}/` - 更新工资条
- `DELETE /api/payslips/{id}/` - 删除工资条

#### 仪表盘统计
- `GET /api/dashboard/` - 获取仪表盘统计数据（员工总数、今日签到数、今日旷工数、待审批请假数、待审批加班数）

### 管理后台

访问：http://127.0.0.1:8000/admin/

使用创建的超级管理员账号登录，可进行后台管理所有数据。

## 考勤规则说明

- 标准工作时间：09:00 - 18:00
- 迟到：09:30 后签到
- 早退：17:30 前签退
- 旷工：迟到且早退，或全天未打卡

## 薪资计算规则

- 迟到扣款：50元/次
- 旷工扣款：日工资 × 旷工天数
- 事假扣款：日工资 × 事假天数
- 工作日加班费：时工资 × 1.5 × 加班小时数
- 周末加班费：时工资 × 2 × 加班小时数
- 节假日加班费：时工资 × 3 × 加班小时数
- 月计薪天数：21.75天

## 目录结构

```
.
├── hrms/              # 项目主目录
│   ├── __init__.py
│   ├── settings.py     # 项目配置
│   ├── urls.py         # 主路由
│   ├── wsgi.py       # WSGI配置
│   └── asgi.py       # ASGI配置
├── hr_system/           # 人事管理应用
│   ├── migrations/      # 数据库迁移文件
│   ├── __init__.py
│   ├── admin.py        # 管理后台配置
│   ├── apps.py         # 应用配置
│   ├── models.py       # 数据模型
│   ├── serializers.py  # 序列化器
│   ├── urls.py         # 路由配置
│   └── views.py        # 视图函数
├── manage.py             # Django管理脚本
├── requirements.txt      # 依赖包列表
├── .env                  # 环境变量配置
└── README.md             # 项目说明文档
```

## 注意事项

1. 确保 MySQL 服务已启动
2. 确保数据库字符集使用 utf8mb4
3. 生产环境请修改 SECRET_KEY 并设置 DEBUG=False
4. 生产环境请配置 CORS 白名单，不要使用 CORS_ALLOW_ALL_ORIGINS
5. 建议使用虚拟环境管理依赖

## 许可证

MIT License