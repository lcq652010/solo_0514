<template>
  <div id="app">
    <el-menu :default-active="activeIndex" mode="horizontal" background-color="#8B4513" text-color="#fff" active-text-color="#ffd04b" router>
      <div class="nav-container">
        <div class="logo">
          <span>景泰蓝定制</span>
        </div>
        <div class="nav-items">
          <el-menu-item index="/">
            <i class="el-icon-edit-outline"></i>
            <span>客户下单</span>
          </el-menu-item>
          <el-menu-item index="/admin">
            <i class="el-icon-s-order"></i>
            <span>订单管理</span>
          </el-menu-item>
        </div>
      </div>
    </el-menu>
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeIndex: '/'
    }
  },
  watch: {
    $route(to) {
      this.activeIndex = to.path;
    }
  },
  mounted() {
    this.activeIndex = this.$route.path;
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.el-menu {
  border-bottom: none;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  color: #fff;
  font-size: 20px;
  font-weight: 600;
  padding: 0 20px;
}

.nav-items {
  display: flex;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px 0;
}

.el-menu-item {
  border-bottom: none !important;
}

.el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}
</style>
