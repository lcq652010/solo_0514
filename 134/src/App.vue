<template>
  <div id="app">
    <el-menu :default-active="activeMenu" mode="horizontal" background-color="#60463b" text-color="#fff" active-text-color="#ffd04b" router>
      <div class="nav-container">
        <div class="logo">
          <i class="el-icon-collection"></i>
          <span>传统砚台定制系统</span>
        </div>
        <div class="nav-items">
          <el-menu-item index="/order">
            <i class="el-icon-edit"></i>
            <span>客户下单</span>
          </el-menu-item>
          <el-menu-item index="/admin">
            <i class="el-icon-s-order"></i>
            <span>订单管理</span>
          </el-menu-item>
        </div>
      </div>
    </el-menu>

    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path;
    }
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  background-color: #f5f5f5;
}

#app {
  min-height: 100vh;
}

.el-menu {
  border-bottom: none !important;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
}

.logo i {
  margin-right: 8px;
  font-size: 22px;
}

.nav-items {
  display: flex;
}
</style>
