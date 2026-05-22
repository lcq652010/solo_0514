# 超市库存管理系统

基于 Vue2 + ElementUI 开发的超市库存管理前端系统

## 功能模块

- **商品入库**: 商品入库表单，支持选择商品、填写数量等
- **商品列表**: 商品信息列表展示，支持搜索筛选，分页
- **库存查询**: 库存统计，支持按状态、分类筛选，库存价值计算
- **库存预警**: 库存低于安全线预警，支持分级预警，快速入库
- **出入库记录**: 出入库操作历史记录，支持多条件筛选

## 技术栈

- Vue 2.6.14
- Vue Router 3.5.3
- Element UI 2.15.12
- Moment.js

## 安装运行

```bash
# 安装依赖
npm install

# 启动开发服务
npm run serve

# 打包构建
npm run build
```

## 项目结构

```
├── src/
│   ├── api/               # 模拟数据和API
│   ├── router/            # 路由配置
│   ├── styles/            # 公共样式
│   ├── views/             # 页面组件
│   ├── App.vue            # 根组件
│   └── main.js            # 入口文件
├── public/                # 静态资源
├── package.json
└── vue.config.js
```
