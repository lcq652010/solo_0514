<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>传统木雕瑞兽镇纸定制系统</h1>
          <el-menu mode="horizontal" :router="true" class="nav-menu">
            <el-menu-item index="/order">客户下单</el-menu-item>
            <el-menu-item index="/admin">管理员订单</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.el-header {
  background: linear-gradient(90deg, #8B4513 0%, #A0522D 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  font-size: 22px;
  font-weight: 500;
}

.nav-menu {
  background: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: white;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.el-main {
  padding: 30px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}
</style>
