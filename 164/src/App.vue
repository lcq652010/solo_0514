<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h2 class="logo">琉璃工坊</h2>
          <el-menu mode="horizontal" :default-active="activeMenu" router class="nav-menu">
            <el-menu-item index="/">客户下单</el-menu-item>
            <el-menu-item index="/admin">订单管理</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view></router-view>
      </el-main>
      <el-footer>
        <p>© 2024 琉璃吊坠定制系统 - 匠心打造，独一无二</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  line-height: 60px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}
.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}
.logo {
  color: white;
  font-size: 24px;
  margin: 0;
}
.nav-menu {
  background: transparent;
  border: none;
}
.nav-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.9);
}
.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}
.el-main {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
}
.el-footer {
  text-align: center;
  color: #666;
  padding: 20px;
  font-size: 14px;
}
</style>
