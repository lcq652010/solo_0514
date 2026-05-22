# 社团活动管理系统

基于 Vue2 + ElementUI 开发的社团活动管理前端页面。

## 功能模块

- **活动列表展示页**：展示所有活动，支持按状态和关键词搜索筛选
- **活动详情页**：展示活动详细信息，包含报名人数进度
- **在线报名表单页**：完整的报名表单，包含表单必填校验
- **活动签到页**：支持二维码签到和手动签到两种方式，展示签到列表
- **我的报名记录页**：查看个人报名记录，支持按状态筛选，可取消报名

## 技术栈

- Vue 2.x
- Vue Router 3.x
- Element UI 2.x
- Axios

## 项目结构

```
├── public/
│   └── index.html
├── src/
│   ├── views/           # 页面组件
│   │   ├── ActivityList.vue      # 活动列表
│   │   ├── ActivityDetail.vue    # 活动详情
│   │   ├── ActivityRegister.vue  # 报名表单
│   │   ├── ActivityCheckIn.vue   # 签到页面
│   │   └── MyRegistrations.vue   # 我的报名
│   ├── router/          # 路由配置
│   ├── mock/            # 模拟数据
│   ├── styles/          # 全局样式
│   ├── App.vue          # 根组件
│   └── main.js          # 入口文件
├── package.json
├── vue.config.js
└── babel.config.js
```

## 安装和运行

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run serve

# 构建生产版本
npm run build
```
