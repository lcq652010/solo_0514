# 政务大厅自助征信查询终端运维管理系统

基于 Vue2 + Element UI 实现的前端管理系统。

## 功能特性

1. **设备列表展示** - 分页展示设备信息，包括：
   - 设备编号
   - 所属政务大厅
   - 摆放窗口
   - 设备状态（正常/故障/离线/维护中）

2. **设备状态颜色区分**：
   - 正常：绿色 (#67c23a)
   - 故障：红色 (#f56c6c)
   - 离线：灰色 (#909399)
   - 维护中：橙色 (#e6a23c)

3. **模糊搜索功能**：
   - 按设备编号搜索
   - 按政务大厅名称搜索

4. **故障上报弹窗**：
   - 选择故障设备
   - 填写故障描述
   - 表单验证

5. **工单自动编号**：
   - 格式：GD + 年月日 + 4位随机数
   - 示例：GD202605161234

## 项目结构

```
├── src/
│   ├── main.js              # 入口文件
│   ├── App.vue              # 主组件
│   ├── components/
│   │   ├── DeviceList.vue   # 设备列表组件
│   │   └── FaultReport.vue  # 故障上报组件
│   └── mock/
│       └── data.js          # 模拟数据
├── public/
│   └── index.html           # HTML模板
├── package.json
├── webpack.config.js
└── .babelrc
```

## 安装运行

```bash
# 安装依赖
npm install

# 启动开发服务器（端口8081）
npm run serve

# 生产构建
npm run build
```

## 技术栈

- Vue 2.7.14
- Element UI 2.15.13
- Webpack 5
