# 传统漆雕墨盒定制系统

基于 Vue2 + ElementUI 实现的传统漆雕墨盒定制前端页面。

## 功能特性

### 客户下单页面
- 胎体材质选择：紫铜、黄铜、木胎、脱胎
- 墨盒边长、盒高输入
- 雕漆层数选择：10层、15层、20层、30层、50层
- 纹饰图案选择：云龙纹、花卉纹、山水纹、花鸟纹、福寿纹、龙凤纹
- 表单验证与提交

### 管理员订单页面
- 订单列表展示
- 生产工序进度管理：制胎 → 刮灰 → 髹漆 → 雕刻 → 推光 → 装配 → 完工
- 工序进度可视化（步骤条）
- 订单删除功能

## 项目结构

```
├── public/
│   └── index.html          # HTML 模板
├── src/
│   ├── components/
│   │   ├── OrderForm.vue   # 客户下单组件
│   │   └── AdminPanel.vue  # 管理员订单组件
│   ├── router/
│   │   └── index.js        # 路由配置
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── package.json            # 依赖配置
└── webpack.config.js       # Webpack 配置
```

## 运行方式

### 1. 安装依赖
```bash
npm install
```

### 2. 启动开发服务器
```bash
npm run dev
```

### 3. 访问页面
- 客户下单页：http://localhost:8080/
- 管理员订单页：http://localhost:8080/admin

## 技术栈

- Vue 2.6.x
- Vue Router 3.x
- Element UI 2.x
- Webpack 5.x

## 数据存储

订单数据使用浏览器 localStorage 存储，便于演示。
