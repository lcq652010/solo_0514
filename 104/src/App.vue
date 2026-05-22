<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="logo">
          <i class="el-icon-box"></i>
          <span>传统锡制茶叶罐定制系统</span>
        </div>
        <el-menu
          mode="horizontal"
          :default-active="$route.path"
          class="nav-menu"
          router
        >
          <el-menu-item index="/">客户下单</el-menu-item>
          <el-menu-item index="/admin">订单管理</el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
      <el-footer class="footer">
        <p>© 2024 传统锡制工艺品 - 匠心独运，品质传承</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.header {
  background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  color: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.logo {
  display: flex;
  align-items: center;
  font-size: 22px;
  font-weight: bold;
}

.logo i {
  font-size: 28px;
  margin-right: 12px;
  color: #d4af37;
}

.nav-menu {
  background: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: #fff;
  font-size: 16px;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background: rgba(212, 175, 55, 0.3);
  color: #d4af37;
}

.main-content {
  padding: 30px;
  min-height: calc(100vh - 120px);
}

.footer {
  background: #2c3e50;
  color: #fff;
  text-align: center;
  line-height: 60px;
  font-size: 14px;
}
</style>
