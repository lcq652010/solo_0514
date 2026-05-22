# 驾校管理系统后端

基于 Python + Django + Django REST Framework + MySQL 实现的驾校管理系统后端。

## 功能特性

### 1. 学员管理
- 学员报名注册
- 自动生成学员学号（格式：YYYYMMDDXXXX，如：202401150001）
- 学员信息维护
- 学员状态管理（报名中、学习中、已毕业、已退学）

### 2. 档案管理
- 学员档案建档
- 自动生成档案编号
- 身份证照片、体检报告等材料上传
- 档案完整性验证

### 3. 教练管理
- 教练信息维护
- 自动生成教练编号
- 教练状态管理

### 4. 车辆管理
- 车辆信息维护
- 车辆状态管理
- 教练与车辆绑定

### 5. 教练排班
- 排班计划制定
- 按日期查询排班
- 排班容量管理

### 6. 练车预约
- 学员预约练车
- **预约状态管理**：待培训、培训中、已完成、已取消
- 预约取消自动释放名额
- 按学员/状态查询预约

### 7. 考试登记
- 考试报名登记
- 考试结果录入
- 考试成绩管理

### 8. 费用缴纳
- 各种费用类型管理
- 支付状态跟踪
- 支付方式记录

## 技术栈

- **后端框架**: Django 4.2
- **API框架**: Django REST Framework
- **数据库**: MySQL
- **跨域支持**: django-cors-headers

## 安装部署

### 前置要求

1. Python 3.8+
2. MySQL 5.7+ 或 MySQL 8.0+
3. pip 包管理工具

### 快速开始

#### 1. 数据库准备

首先在MySQL中创建数据库：

```sql
CREATE DATABASE driving_school DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

修改 `driving_school/settings.py` 中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'driving_school',      # 数据库名
        'USER': 'root',                # 数据库用户名
        'PASSWORD': 'root',            # 数据库密码
        'HOST': 'localhost',           # 数据库地址
        'PORT': '3306',                # 数据库端口
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

#### 2. 一键启动（Windows）

双击运行 `start.bat` 脚本，自动完成：
- 安装依赖包
- 生成数据库迁移
- 执行数据库迁移
- 创建超级管理员

#### 3. 手动启动

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 生成数据库迁移：
```bash
python manage.py makemigrations
```

3. 执行数据库迁移：
```bash
python manage.py migrate
```

4. 创建超级管理员：
```bash
python manage.py createsuperuser
```

5. 启动开发服务器：
```bash
python manage.py runserver
```

### 访问地址

- 管理后台: http://127.0.0.1:8000/admin/
- API接口: http://127.0.0.1:8000/api/

## 权限系统说明

### 三级角色权限
| 角色 | 权限范围 |
|------|----------|
| **前台** | 学员管理、预约管理、排班管理、缴费管理 |
| **教练** | 查看自己的排班、学员签到、完成培训、查看课时记录 |
| **管理员** | 所有功能、用户管理、教练管理、系统配置 |

### 认证方式
- Session Authentication
- Basic Authentication
- 登录后访问所有接口

## API接口说明

### 分页参数
所有列表接口支持分页参数：
- `page`: 页码（默认1）
- `page_size`: 每页条数（默认10，最大100）

响应格式：
```json
{
    "count": 100,
    "next": "http://...?page=2",
    "previous": null,
    "results": [...]
}
```

### 用户相关
- `GET /api/current-user/` - 获取当前登录用户信息及角色
- `GET /api/user-profiles/` - 用户配置列表（管理员）
- `POST /api/user-profiles/` - 创建用户配置（管理员）

### 学员管理（多条件筛选）
- `GET /api/students/` - 获取学员列表（支持多条件筛选）
  - 筛选参数：`name`, `student_id`, `status`, `license_type`, `phone`, `start_date`, `end_date`
  - 支持模糊搜索：姓名、学号、手机号
- `POST /api/students/` - 新增学员（前台/管理员，含自动校验）
- `GET /api/students/{id}/` - 获取学员详情
- `PUT /api/students/{id}/` - 更新学员信息（前台/管理员）

### 教练管理（权限控制）
- `GET /api/coaches/` - 获取教练列表（支持多条件筛选）
  - 筛选参数：`name`, `coach_id`, `status`, `teach_type`
- `POST /api/coaches/` - 新增教练（仅管理员）
- `GET /api/coaches/active/` - 获取在职教练列表

### 排班管理（教练数据隔离）
- `GET /api/schedules/` - 获取排班列表（支持多条件筛选）
  - 筛选参数：`coach_name`, `coach_id`, `vehicle_plate`, `date`, `start_date`, `end_date`, `has_available=true`
  - **教练角色**：自动只显示自己的排班
- `POST /api/schedules/` - 新增排班（前台/管理员）
  - 自动校验：时段冲突、车辆冲突

### 练车预约（核心功能）
- `GET /api/reservations/` - 获取预约列表（学员+教练+状态多条件组合筛选）
  - 筛选参数：`student_name`, `student_id`, `coach_name`, `coach_id`, `status`(支持多选如: `待培训,培训中`), `subject`, `start_date`, `end_date`
  - **教练角色**：自动只显示自己学员的预约
  - 示例：`/api/reservations/?student_name=张&coach_name=李&status=待培训,培训中`
- `POST /api/reservations/` - 新增预约（前台/管理员）
  - 自动校验：学员时段冲突、预约是否已满
- `POST /api/reservations/{id}/sign_in/` - **学员签到（仅教练）**
  - 自动更新状态为：培训中
  - 记录实际开始时间
- `POST /api/reservations/{id}/complete_training/` - **完成培训（仅教练）**
  - ✅ **自动记课时**：计算培训时长并写入课时记录
  - ✅ **自动归档**：创建/更新培训档案，累计已完成课时
  - 可填写培训内容和教练点评
- `POST /api/reservations/{id}/cancel/` - 取消预约

### 课时记录管理
- `GET /api/training-hours/` - 获取课时记录列表（多条件筛选）
  - 筛选参数：`student_name`, `student_id`, `coach_name`, `subject`, `start_date`, `end_date`
  - **教练角色**：自动只显示自己的教学记录
- `POST /api/training-hours/` - 手动添加课时记录

### 培训档案管理
- `GET /api/training-archives/` - 获取培训档案列表
  - 筛选参数：`student_name`, `student_id`, `subject`, `status`
  - 额外字段：`remaining_hours` 剩余课时
- `POST /api/training-archives/{id}/mark_complete/` - 标记培训完成
- `POST /api/training-archives/{id}/archive/` - 正式归档

### 学员档案管理
- `GET /api/archives/` - 获取档案列表（支持多条件筛选）
  - 筛选参数：`student_name`, `is_complete=true/false`, `start_date`, `end_date`
- `POST /api/archives/` - 新建档案
- `GET /api/archives/by_student/?student_id=202401150001` - 按学员查询
- `POST /api/archives/{id}/mark_complete/` - 标记档案完整

### 考试登记
- `GET /api/exams/` - 获取考试列表（支持多条件筛选）
  - 筛选参数：`student_name`, `exam_type`, `status`, `start_date`, `end_date`
- `POST /api/exams/` - 新增考试登记（含重复报名校验）
- `GET /api/exams/by_student/?student_id=202401150001` - 按学员查询
- `POST /api/exams/{id}/update_result/` - 更新考试结果

### 费用缴纳
- `GET /api/payments/` - 获取缴费列表（支持多条件筛选）
  - 筛选参数：`student_name`, `payment_type`, `payment_method`, `status`, `start_date`, `end_date`
- `POST /api/payments/` - 新增缴费（含金额校验）
- `GET /api/payments/by_student/?student_id=202401150001` - 按学员查询
- `POST /api/payments/{id}/confirm_payment/` - 确认支付

### 车辆管理
- `GET /api/vehicles/` - 获取车辆列表
- `POST /api/vehicles/` - 新增车辆
- `GET /api/vehicles/available/` - 获取可用车辆

## 预约状态流转

```
待培训
   ↓ (调用 start_training)
培训中
   ↓ (调用 complete_training)
已完成

待培训/培训中
   ↓ (调用 cancel)
已取消
```

## 自动编号规则

- **学员学号**: `YYYYMMDD + 4位序号`（如：202401150001）
- **教练编号**: `JL + YYYYMM + 4位序号`（如：JL2024010001）
- **档案编号**: `DA + YYYYMMDD + 4位序号`（如：DA202401150001）

## 项目结构

```
driving_school/
├── driving_school/          # 项目配置目录
│   ├── __init__.py
│   ├── settings.py         # 项目设置
│   ├── urls.py            # 主路由
│   ├── wsgi.py
│   └── asgi.py
├── management/             # 管理应用
│   ├── migrations/         # 数据库迁移
│   ├── __init__.py
│   ├── admin.py           # 管理后台配置
│   ├── apps.py            # 应用配置
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── urls.py            # API路由
│   └── views.py           # 视图函数
├── manage.py              # Django管理脚本
├── requirements.txt       # 依赖包列表
├── init_db.sql           # 数据库初始化脚本
├── start.bat             # Windows启动脚本
└── README.md             # 说明文档
```

## 常见问题

### 1. MySQL连接失败
- 检查MySQL服务是否启动
- 确认用户名密码是否正确
- 确认数据库已创建

### 2. 迁移失败
- 删除 `management/migrations/` 目录下的文件（除了 `__init__.py`）
- 重新执行 `makemigrations` 和 `migrate`

### 3. 运行时缺少mysqlclient
- Windows: 可能需要安装对应版本的whl文件
- Linux: 可能需要先安装 `libmysqlclient-dev` 包

## 开发说明

如需添加新功能，请遵循以下步骤：
1. 在 `models.py` 中定义数据模型
2. 在 `serializers.py` 中创建序列化器
3. 在 `views.py` 中实现视图逻辑
4. 在 `urls.py` 中配置路由
5. 在 `admin.py` 中注册到管理后台
