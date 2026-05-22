<template>
  <div id="app">
    <el-header class="header">
      <div class="container">
        <div class="logo" @click="$router.push('/')">
          <i class="el-icon-film"></i>
          <span>星光影院</span>
        </div>
        <el-menu mode="horizontal" :default-active="$route.path" class="nav-menu" router>
          <el-menu-item index="/">电影列表</el-menu-item>
          <el-menu-item index="/orders">我的订单</el-menu-item>
          <el-menu-item index="/refund">退票改签</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <main class="main-content">
      <div class="container">
        <router-view />
      </div>
    </main>
    <el-footer class="footer">
      <div class="container">
        <p>© 2024 星光影院 版权所有</p>
      </div>
    </el-footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  height: 60px;
  line-height: 60px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  float: left;
  color: white;
  font-size: 22px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
}

.logo i {
  font-size: 26px;
}

.nav-menu {
  float: right;
  background: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: white;
  border-bottom: 2px solid transparent;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border-bottom: 2px solid white;
}

.main-content {
  flex: 1;
  background: #f5f7fa;
  padding: 20px 0;
}

.footer {
  background: #303133;
  color: #909399;
  text-align: center;
  padding: 20px 0;
  height: auto;
}

.footer p {
  margin: 0;
}
</style>
