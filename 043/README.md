# 图书馆管理系统后端

基于 Python + Django + Django REST Framework + MySQL 实现的图书馆管理系统后端 API。

## 功能特性

- ✅ 图书录入与管理
- ✅ 读者办证与管理
- ✅ 借阅登记
- ✅ 归还处理
- ✅ 图书报失
- ✅ 逾期罚款自动计算
- ✅ 借阅状态管理（可借、已借出、已归还、已遗失）
- ✅ 自动生成借阅单号
- ✅ 数据统计接口

## 技术栈

- Python 3.8+
- Django 4.2
- Django REST Framework 3.15
- MySQL 5.7+ / 8.0+

## 快速开始

### 1. 环境准备

确保已安装：
- Python 3.8+
- MySQL 5.7+ 或 8.0+

### 2. 创建数据库

在 MySQL 中创建数据库：

```sql
CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. 配置环境变量

编辑 `.env` 文件，修改数据库连接信息：

```env
DB_NAME=library_db
DB_USER=root
DB_PASSWORD=你的数据库密码
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=你的密钥
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级管理员

```bash
python manage.py createsuperadmin
```

### 7. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

服务启动后访问：
- API 根地址：http://localhost:8000/api/
- Admin 后台：http://localhost:8000/admin/

## API 接口文档

### 图书管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/books/` | 获取图书列表 |
| POST | `/api/books/` | 新增图书 |
| GET | `/api/books/{id}/` | 获取图书详情 |
| PUT | `/api/books/{id}/` | 更新图书 |
| DELETE | `/api/books/{id}/` | 删除图书 |
| GET | `/api/books/statistics/` | 图书统计 |

查询参数（支持多条件组合筛选）：
| 参数 | 说明 | 示例 |
|------|------|------|
| `title` | 书名模糊搜索 | `Python` |
| `isbn` | ISBN 模糊搜索 | `9787` |
| `author` | 作者模糊搜索 | `张三` |
| `status` | 状态筛选 | `available` / `borrowed` / `lost` |
| `category` | 分类模糊搜索 | `计算机` |
| `min_copies` | 最小总册数 | `5` |
| `max_copies` | 最大总册数 | `100` |
| `start_date` | 录入起始日期 | `2024-01-01` |
| `end_date` | 录入结束日期 | `2024-12-31` |
| `page` | 页码 | `1` |
| `page_size` | 每页条数（默认10，最大100） | `20` |

### 读者管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/readers/` | 获取读者列表 |
| POST | `/api/readers/` | 新增读者（办证） |
| GET | `/api/readers/{id}/` | 获取读者详情 |
| PUT | `/api/readers/{id}/` | 更新读者 |
| DELETE | `/api/readers/{id}/` | 删除读者 |
| GET | `/api/readers/statistics/` | 读者统计 |
| GET | `/api/readers/{id}/borrow_history/` | 读者借阅历史 |

查询参数（支持多条件组合筛选）：
| 参数 | 说明 | 示例 |
|------|------|------|
| `name` | 姓名模糊搜索 | `张三` |
| `reader_no` | 读者证号模糊搜索 | `R2024` |
| `phone` | 电话模糊搜索 | `138` |
| `id_card` | 身份证号模糊搜索 | `110` |
| `reader_type` | 读者类型筛选 | `student` / `teacher` / `staff` / `other` |
| `is_active` | 是否有效 | `true` / `false` |
| `department` | 院系/部门模糊搜索 | `计算机` |
| `min_borrow_books` | 最小最大借阅册数 | `5` |
| `max_borrow_books` | 最大最大借阅册数 | `20` |
| `start_date` | 办证起始日期 | `2024-01-01` |
| `end_date` | 办证结束日期 | `2024-12-31` |
| `page` | 页码 | `1` |
| `page_size` | 每页条数 | `20` |

**读者借阅历史接口额外参数：**
| 参数 | 说明 | 示例 |
|------|------|------|
| `status` | 借阅状态筛选 | `borrowed` / `returned` / `lost` |
| `is_overdue` | 是否逾期 | `true` / `false` |

### 借阅管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/borrows/` | 获取借阅列表 |
| POST | `/api/borrows/` | 借阅登记 |
| GET | `/api/borrows/{id}/` | 获取借阅详情 |
| PUT | `/api/borrows/{id}/` | 更新借阅 |
| DELETE | `/api/borrows/{id}/` | 删除借阅 |
| POST | `/api/borrows/{id}/return_book/` | 归还图书 |
| POST | `/api/borrows/{id}/report_lost/` | 图书报失 |
| GET | `/api/borrows/statistics/` | 借阅统计 |
| GET | `/api/borrows/overdue_list/` | 逾期列表 |

查询参数（支持多条件组合筛选）：
| 参数 | 说明 | 示例 |
|------|------|------|
| `book_title` | 书名模糊搜索 | `Python` |
| `book_isbn` | ISBN 模糊搜索 | `9787` |
| `reader_name` | 读者姓名模糊搜索 | `张三` |
| `reader_no` | 读者证号模糊搜索 | `R2024` |
| `status` | 借阅状态筛选 | `borrowed` / `returned` / `lost` |
| `borrow_no` | 借阅单号模糊搜索 | `B2024` |
| `operator` | 操作员模糊搜索 | `管理员` |
| `is_overdue` | 是否逾期筛选 | `true` / `false` |
| `min_fine` | 最小罚款金额 | `0.5` |
| `max_fine` | 最大罚款金额 | `100` |
| `borrow_start_date` | 借阅起始日期 | `2024-01-01` |
| `borrow_end_date` | 借阅结束日期 | `2024-12-31` |
| `due_start_date` | 应还起始日期 | `2024-01-01` |
| `due_end_date` | 应还结束日期 | `2024-12-31` |
| `page` | 页码 | `1` |
| `page_size` | 每页条数 | `20` |

**借阅管理新增接口：**

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/borrows/batch_calculate_fines/` | 批量计算所有借阅中图书的逾期罚款 |
| GET | `/api/borrows/{id}/fine_detail/` | 获取借阅记录的罚款详情 |
| POST | `/api/borrows/{id}/pay_fine/` | 缴纳罚款 |

## 分页说明

所有列表接口均支持分页，分页参数：
- `page`: 页码，默认第1页
- `page_size`: 每页记录数，默认10条，最大100条

分页响应格式：
```json
{
    "count": 100,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [...]
}
```

## 借阅状态说明

| 状态码 | 说明 |
|--------|------|
| available | 可借 |
| borrowed | 已借出 |
| returned | 已归还 |
| lost | 已遗失 |

## 编号规则

- **读者证号**: R + 日期(YYYYMMDD) + 序号(4位)，如：R202405160001
- **借阅单号**: B + 日期时间(YYYYMMDDHHMMSS) + 随机数(6位)，如：B20240516123045123456

## 逾期罚款计算

### 核心功能

1. **自动计算**
   - 默认罚款标准：0.5元/天
   - 逾期天数 = 实际归还日期 - 应还日期（或当前日期）
   - 罚款金额 = 逾期天数 × 每日罚款
   - 归还时自动计算并记录罚款

2. **动态更新**
   - 查询借阅列表时自动计算最新罚款
   - 支持实时查询罚款详情
   - 支持批量更新所有逾期罚款

3. **罚款管理**
   - 支持手动设置每日罚款标准
   - 支持罚款缴纳状态追踪
   - 统计总罚款、已缴罚款、未缴罚款

### API 接口说明

#### 1. 归还图书（自动计算罚款）
```bash
POST /api/borrows/{id}/return_book/
Content-Type: application/json

{
    "operator": "管理员",
    "remarks": "图书完好",
    "fine_per_day": 0.5
}
```

#### 2. 批量计算所有逾期罚款
```bash
POST /api/borrows/batch_calculate_fines/
Content-Type: application/json

{
    "fine_per_day": 0.5
}
```

响应示例：
```json
{
    "message": "批量计算逾期罚款完成",
    "updated_count": 5,
    "fine_per_day": 0.5
}
```

#### 3. 获取罚款详情
```bash
GET /api/borrows/{id}/fine_detail/
```

响应示例：
```json
{
    "borrow_no": "B20240516123456123456",
    "book_title": "Python编程：从入门到实践",
    "reader_name": "张三",
    "reader_no": "R202405160001",
    "borrow_date": "2024-05-01T12:00:00",
    "due_date": "2024-05-31T12:00:00",
    "return_date": null,
    "status": "borrowed",
    "status_display": "已借出",
    "is_overdue": true,
    "overdue_days": 15,
    "fine_amount": 7.5,
    "fine_paid": false,
    "fine_per_day": 0.5
}
```

#### 4. 缴纳罚款
```bash
POST /api/borrows/{id}/pay_fine/
```

响应示例：
```json
{
    "message": "罚款缴纳成功",
    "borrow_no": "B20240516123456123456",
    "fine_amount": 7.5
}
```

#### 5. 借阅统计（含罚款统计）
```bash
GET /api/borrows/statistics/
```

响应示例：
```json
{
    "total": 100,
    "borrowed": 45,
    "returned": 50,
    "lost": 5,
    "overdue_count": 8,
    "total_fine": 125.5,
    "unpaid_fine": 85.0,
    "paid_fine": 40.5
}
```

### 借阅响应新增字段
所有借阅相关接口新增以下字段：
- `is_overdue`: 是否逾期
- `overdue_days`: 逾期天数
- `current_fine`: 当前应缴罚款金额
- `fine_paid`: 罚款是否已缴纳

## 数据校验规则

### 图书字段校验
| 字段 | 校验规则 |
|------|----------|
| ISBN | 必填，长度10-20位 |
| 书名 | 必填，长度1-200字符 |
| 作者 | 必填，最少1个字符 |
| 出版社 | 必填 |
| 出版日期 | 必填，不能晚于当前日期 |
| 分类 | 必填 |
| 馆藏位置 | 必填 |
| 总册数 | 必填，1-10000之间 |
| 可借册数 | 必填，不能为负数，不能大于总册数 |

### 读者字段校验
| 字段 | 校验规则 |
|------|----------|
| 姓名 | 必填，长度2-50字符 |
| 性别 | 必填，可选值：male/female |
| 电话 | 必填，11位手机号格式 |
| 邮箱 | 可选，格式正确 |
| 身份证号 | 必填，18位，格式校验 |
| 读者类型 | 必填，可选值：student/teacher/staff/other |
| 最大借阅天数 | 必填，1-365天 |
| 最大借阅册数 | 必填，1-100本 |
| 有效期至 | 必填，不能早于当前日期 |

### 借阅业务规则
- ✅ 图书状态为"遗失"时不能借阅
- ✅ 读者证已失效时不能借阅
- ✅ 读者证已过期时不能借阅
- ✅ 已达到最大借阅数量时不能借阅
- ✅ 该读者已借阅此书且未归还时不能重复借阅
- ✅ 该读者有逾期图书未还时不能借阅新书
- ✅ 借阅中图书不能删除
- ✅ 有借阅中图书的读者不能删除

## 示例请求

### 1. 新增图书

```bash
POST /api/books/
Content-Type: application/json

{
    "isbn": "9787111544937",
    "title": "Python编程：从入门到实践",
    "author": "埃里克·马瑟斯",
    "publisher": "机械工业出版社",
    "publish_date": "2016-07-01",
    "category": "计算机",
    "location": "A区-1架-3层",
    "total_copies": 5,
    "available_copies": 5
}
```

### 2. 新增读者（办证）

```bash
POST /api/readers/
Content-Type: application/json

{
    "name": "张三",
    "gender": "male",
    "phone": "13800138000",
    "email": "zhangsan@example.com",
    "id_card": "110101199001011234",
    "reader_type": "student",
    "department": "计算机科学与技术学院",
    "max_borrow_days": 30,
    "max_borrow_books": 10
}
```

### 3. 借阅登记

```bash
POST /api/borrows/
Content-Type: application/json

{
    "book": 1,
    "reader": 1,
    "operator": "管理员",
    "remarks": ""
}
```

### 4. 归还图书

```bash
POST /api/borrows/1/return_book/
Content-Type: application/json

{
    "operator": "管理员",
    "remarks": "图书完好"
}
```

## 项目结构

```
library_management/
├── library/
│   ├── migrations/          # 数据库迁移文件
│   ├── __init__.py
│   ├── admin.py            # Admin 后台配置
│   ├── apps.py             # 应用配置
│   ├── models.py           # 数据模型
│   ├── serializers.py      # 序列化器
│   ├── tests.py            # 测试文件
│   ├── urls.py             # 路由配置
│   └── views.py            # 视图逻辑
├── library_management/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # 项目配置
│   ├── urls.py             # 主路由
│   └── wsgi.py
├── .env                    # 环境变量
├── manage.py               # Django 管理脚本
├── requirements.txt        # 依赖列表
└── README.md               # 项目文档
```

## 注意事项

1. 确保 MySQL 服务已启动
2. 数据库字符集建议使用 utf8mb4
3. 生产环境请修改 SECRET_KEY
4. 生产环境建议关闭 DEBUG 模式
5. 建议使用虚拟环境隔离依赖
