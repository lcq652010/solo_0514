<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>漆木佛珠定制系统</h1>
          <el-menu
            :default-active="activeMenu" mode="horizontal" router>
            <el-menu-item index="/">客户下单</el-menu-item>
            <el-menu-item index="/admin">管理员订单管理</el-menu-item>
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
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.el-header {
  background: linear-gradient(90deg, #8B4513 0%, #A0522D 100%);
  color: white;
  padding: 0 !important;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-content h1 {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 2px;
}

.el-menu {
  background: transparent;
  border: none;
}

.el-menu-item {
  color: rgba(255, 255, 255, 0.9) !important;
}

.el-menu-item:hover {
  background: rgba(255, 255, 255, 0.2) !important;
}

.el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.3) !important;
  color: white !important;
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
}
</style>
