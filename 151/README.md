# 健身房管理系统

基于 Vue 2 + Element UI 开发的健身房管理前端系统。

## 功能模块

1. **私教列表** - 查看所有私教信息，支持分页、查看详情、预约教练
2. **私教预约** - 表单提交预约，包含教练选择、时间选择等，带表单验证
3. **团课展示** - 卡片式展示团课信息，包含课程安排、价格等
4. **我的预约** - 查看预约记录，支持确认、取消预约操作
5. **课时管理** - 会员课时统计、充值、消课、记录查看等功能

## 项目结构

```
gym-management/
├── public/
│   └── index.html
├── src/
│   ├── views/
│   │   ├── TrainerList.vue    # 私教列表
│   │   ├── Booking.vue         # 私教预约
│   │   ├── Classes.vue         # 团课展示
│   │   ├── MyBookings.vue      # 我的预约
│   │   └── CourseHours.vue     # 课时管理
│   ├── router/
│   │   └── index.js
│   ├── App.vue
│   └── main.js
├── webpack.config.js
├── package.json
└── README.md
```

## 运行项目

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run serve
```

项目将在 http://localhost:8080 启动

### 3. 构建生产版本

```bash
npm run build
```

## 技术栈

- Vue 2.6.x
- Vue Router 3.5.x
- Element UI 2.15.x
- Webpack 5.x

## 功能说明

- **表单验证**：预约表单包含必填验证、手机号格式验证
- **数据持久化**：使用 localStorage 存储会员和预约数据
- **响应式布局**：适配不同屏幕尺寸
- **状态管理**：展示不同状态标签（待确认、已确认、已完成、已取消）
