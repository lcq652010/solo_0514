# 燃气自助缴费打印终端运维管理系统

基于 Vue2 + Element UI 实现的前端管理系统。

## 功能特性

- ✅ 设备列表分页展示（支持每页5/10/20/50条）
- ✅ 显示设备编号、服务网点、安装位置、设备运行状态
- ✅ 故障上报弹窗，可选择设备并录入故障描述
- ✅ 按设备编号、网点名称进行检索
- ✅ 不同设备状态使用不同颜色区分（在线-绿色、离线-灰色、故障-红色）
- ✅ 工单自动生成编号（格式：GD + 年月日 + 4位随机数）

## 项目结构

```
.
├── index.html              # 入口 HTML
├── package.json            # 项目配置
├── vite.config.js          # Vite 配置
└── src/
    ├── main.js            # 入口 JS
    ├── App.vue            # 根组件
    └── components/
        └── DeviceManagement.vue  # 设备管理主组件
```

## 安装运行

### 方法1：使用 npm（推荐）

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 访问 http://localhost:3000
```

### 方法2：使用 CDN 版本

如果遇到 npm 安装问题，可以使用 CDN 版本直接在浏览器运行：

```bash
# 直接在浏览器打开 index-cdn.html 即可
```

## 技术栈

- Vue 2.7.14
- Element UI 2.15.13
- Vite 4.5.0
