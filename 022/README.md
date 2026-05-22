# 线上课程平台后端

基于 Python + Django + MySQL 实现的在线课程学习平台后端。

## 功能特性

- ✅ **用户认证**：JWT 登录注册、用户信息管理
- ✅ **课程管理**：课程上架、章节管理、视频管理
- ✅ **订单系统**：自动生成订单号、支付、退款、取消
- ✅ **学习进度**：视频观看记录、学习进度追踪
- ✅ **课程状态**：未开始、学习中、已完结、已退款
- ✅ **多条件筛选**：支持课程名称、学员姓名、学习状态等组合筛选
- ✅ **防重复购买**：防止重复购买已购课程、防止重复创建待支付订单
- ✅ **必填字段校验**：所有关键字段均有非空校验
- ✅ **金额合法性校验**：防止负数金额异常
- ✅ **分页支持**：所有列表接口支持分页查询
- ✅ **统一响应格式**：code、message、data 标准响应结构

## 技术栈

- **后端框架**: Django 4.2 + Django REST Framework
- **数据库**: MySQL
- **认证方式**: JWT (SimpleJWT)
- **筛选过滤**: django-filter
- **跨域处理**: django-cors-headers

## 快速开始

### 方式一：一键启动（推荐 Windows）

直接双击运行 `start.bat` 脚本即可完成全部配置并启动。

### 方式二：手动启动

#### 1. 环境要求

- Python 3.8+
- MySQL 5.7+

#### 2. 数据库配置

在 `course_platform/settings.py` 中修改数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'course_platform',      # 数据库名
        'USER': 'root',                  # 数据库用户名
        'PASSWORD': '',                  # 数据库密码
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

**注意**：请先在 MySQL 中创建 `course_platform` 数据库。

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

#### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 5. 初始化演示数据

```bash
python init_db.py
```

#### 6. 创建管理员（可选）

```bash
python manage.py createsuperuser
```

#### 7. 启动服务

```bash
python manage.py runserver
```

服务启动后访问：http://127.0.0.1:8000/

## 测试账号

初始化脚本会自动创建以下测试账号：

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 讲师 | teacher | teacher123 |
| 学生 | student | student123 |

## API 接口文档

### 认证接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/auth/register/` | 用户注册 | 公开 |
| POST | `/api/auth/login/` | 用户登录 | 公开 |
| POST | `/api/auth/refresh/` | 刷新 Token | 公开 |
| GET | `/api/auth/user/` | 获取当前用户信息 | 认证 |

### 课程接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/courses/` | 课程列表 | 公开 |
| GET | `/api/courses/{id}/` | 课程详情 | 公开 |
| POST | `/api/courses/` | 创建课程 | 认证 |
| PUT | `/api/courses/{id}/` | 更新课程 | 认证 |
| DELETE | `/api/courses/{id}/` | 删除课程 | 认证 |
| POST | `/api/courses/{id}/publish/` | 上架课程 | 认证 |
| GET | `/api/courses/{id}/chapters_with_progress/` | 带进度的章节列表 | 认证 |

### 章节与视频接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/chapters/` | 章节列表 | 认证 |
| POST | `/api/chapters/` | 创建章节 | 认证 |
| GET | `/api/videos/` | 视频列表 | 认证 |
| POST | `/api/videos/` | 创建视频 | 认证 |

### 订单接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/orders/` | 我的订单列表 | 认证 |
| POST | `/api/orders/` | 创建订单 | 认证 |
| POST | `/api/orders/{id}/pay/` | 支付订单 | 认证 |
| POST | `/api/orders/{id}/refund/` | 申请退款 | 认证 |
| POST | `/api/orders/{id}/cancel/` | 取消订单 | 认证 |

### 报名与进度接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/enrollments/` | 我的报名记录 | 认证 |
| POST | `/api/progress/update_progress/` | 更新学习进度 | 认证 |
| GET | `/api/dashboard/stats/` | 学习统计数据 | 认证 |

### 分页与筛选参数

#### 通用分页参数
| 参数 | 类型 | 说明 |
|------|------|------|
| page | int | 页码，默认 1 |
| page_size | int | 每页条数，默认 10，最大 100 |
| ordering | string | 排序字段，多个用逗号分隔，如 `-created_at` 表示倒序 |

#### 课程列表筛选参数 (`/api/courses/`)
| 参数 | 类型 | 说明 |
|------|------|------|
| title | string | 课程名称模糊搜索 |
| instructor_name | string | 讲师姓名模糊搜索 |
| status | string | 课程状态：draft/published/offline |
| price_min | decimal | 最低价格 |
| price_max | decimal | 最高价格 |

**示例**：`/api/courses/?title=Python&status=published&price_min=0&ordering=-price`

#### 订单列表筛选参数 (`/api/orders/`)
| 参数 | 类型 | 说明 |
|------|------|------|
| course_name | string | 课程名称模糊搜索 |
| student_name | string | 学员姓名模糊搜索 |
| status | string | 订单状态：pending/paid/refunded/cancelled |
| order_no | string | 订单号模糊搜索 |
| price_min | decimal | 最小金额 |
| price_max | decimal | 最大金额 |
| order_date_start | datetime | 下单开始时间 |
| order_date_end | datetime | 下单结束时间 |

**示例**：`/api/orders/?status=paid&course_name=Python&ordering=-created_at`

#### 报名记录筛选参数 (`/api/enrollments/`)
| 参数 | 类型 | 说明 |
|------|------|------|
| course_name | string | 课程名称模糊搜索 |
| student_name | string | 学员姓名模糊搜索 |
| status | string | 学习状态：not_started/learning/completed/refunded |
| enrolled_date_start | date | 报名开始日期 |
| enrolled_date_end | date | 报名结束日期 |
| progress_min | float | 最小进度(%) |
| progress_max | float | 最大进度(%) |

**示例**：`/api/enrollments/?status=learning&course_name=Django&ordering=-progress`

## 数据库设计

### 核心表结构

1. **Course（课程表）**
   - 课程标题、描述、封面、价格、原价
   - 讲师关联、课程状态（草稿/已上架/已下架）
   - 学员数量、总时长等统计字段

2. **Chapter（章节表）**
   - 所属课程、章节标题、排序

3. **Video（视频表）**
   - 所属章节、视频标题、视频地址、时长、排序

4. **Order（订单表）**
   - 订单号（自动生成：ORD + 时间戳 + 6位随机字符）
   - 用户、课程、价格、订单状态、支付时间

5. **Enrollment（报名表）**
   - 用户、课程、关联订单
   - 学习状态：未开始/学习中/已完结/已退款
   - 学习进度（百分比）、最后观看时间

6. **LearningProgress（学习进度表）**
   - 报名记录、视频
   - 最后观看位置、是否完成、观看时长

## 订单号生成规则

订单号自动生成，格式为：
```
ORD + 时间戳(年月日时分秒) + 6位随机字符(大写字母+数字)
```

示例：`ORD20240516143025A3B7C9`

## 状态流转

### 订单状态
- pending（待支付）→ paid（已支付） → refunded（已退款）
- pending（待支付）→ cancelled（已取消）

### 报名状态
- not_started（未开始）
- learning（学习中）- 开始观看任意视频后自动切换
- completed（已完结）- 所有视频看完后自动切换
- refunded（已退款）- 订单退款后同步修改

## 项目结构

```
course_platform/
├── course_platform/          # 项目配置目录
│   ├── __init__.py
│   ├── settings.py          # Django 配置
│   ├── urls.py              # 主路由
│   └── wsgi.py
├── courses/                 # 课程应用
│   ├── __init__.py
│   ├── admin.py             # 后台管理配置
│   ├── apps.py              # 应用配置
│   ├── models.py            # 数据模型
│   ├── serializers.py       # 序列化器
│   ├── urls.py              # API 路由
│   └── views.py             # 视图函数
├── manage.py                # Django 管理脚本
├── requirements.txt         # 依赖包列表
├── init_db.py               # 初始化演示数据脚本
├── start.bat                # Windows 一键启动脚本
└── README.md                # 项目说明文档
```

## 后台管理

访问：http://127.0.0.1:8000/admin/

后台可以管理所有数据：
- 用户管理
- 课程、章节、视频管理
- 订单管理
- 报名记录
- 学习进度

## 常见问题

### 1. MySQL 连接失败

- 确认 MySQL 服务已启动
- 检查 `settings.py` 中的数据库配置是否正确
- 确认数据库 `course_platform` 是否已创建

### 2. 迁移失败

删除 `courses/migrations/` 目录下的文件（除 `__init__.py`），然后重新：
```bash
python manage.py makemigrations
python manage.py migrate
```

## 许可证

MIT License
