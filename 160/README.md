# 医院挂号管理系统

基于 Vue2 + ElementUI 开发的医院挂号管理前端系统。

## 功能模块

### 1. 科室列表
- 展示所有科室信息卡片
- 支持查看科室排班
- 支持直接跳转挂号

### 2. 医生排班
- 按科室、日期筛选排班
- 展示医生排班信息展示
- 剩余号源实时显示
- 支持直接挂号

### 3. 在线挂号
- 三步式挂号流程
- 选择科室、医生、日期、时段
- 填写患者信息
- 挂号成功展示

### 4. 挂号记录
- 多条件筛选查询
- 挂号记录列表展示
- 查看详情
- 取消挂号功能

### 5. 就诊签到
- 输入信息签到
- 二维码签到模拟
- 今日签到记录展示
- 签到成功弹窗

## 技术栈

- **框架: Vue 2.6.14
- **路由**: Vue Router 3.5.3
- **UI组件**: Element UI 2.15.13
- **构建工具**: Webpack 5.74.0

## 项目结构

```
hospital-registration/
├── public/
│   └── index.html
├── src/
│   ├── views/
│   │   ├── DepartmentList.vue    # 科室列表
│   │   ├── DoctorSchedule.vue    # 医生排班
│   │   ├── RegistrationForm.vue # 在线挂号
│   │   ├── RegistrationRecord.vue # 挂号记录
│   │   └── CheckIn.vue        # 就诊签到
│   ├── router/
│   │   └── index.js
│   ├── mock/
│   │   └── data.js
│   ├── App.vue
│   └── main.js
├── package.json
├── webpack.config.js
└── babel.config.json
```

## 安装和运行

### 安装依赖

```bash
npm install
```

### 开发模式运行

```bash
npm run dev
```

### 生产构建

```bash
npm run build
```

## 浏览器访问

开发模式启动后，访问：http://localhost:8080

## 功能说明

### 表单校验
- 必填项校验
- 身份证号格式校验
- 手机号格式校验
- 号源不足提示

### 数据交互
- 页面间参数传递
- 状态实时更新
- 操作成功/失败提示

### 样式风格
- 统一的卡片、表格样式
- 响应式布局
- ElementUI 主题配色

## 开发说明

本项目使用模拟数据，实际项目中可对接后端 API 接口。
