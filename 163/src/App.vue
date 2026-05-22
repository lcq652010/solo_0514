<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="logo">社区团购平台</h1>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            router
            class="nav-menu"
          >
            <el-menu-item index="/">商品拼团</el-menu-item>
            <el-menu-item index="/order">下单参团</el-menu-item>
            <el-menu-item index="/leader">团长管理</el-menu-item>
            <el-menu-item index="/verify">提货核销</el-menu-item>
            <el-menu-item index="/progress">拼团进度</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <p>© 2024 社区团购平台 - 实惠就在身边</p>
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
#app {
  min-height: 100vh;
}
.el-header {
  background-color: #ff6b00;
  color: #fff;
  padding: 0;
}
.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}
.logo {
  font-size: 24px;
  margin: 0;
}
.nav-menu {
  background-color: transparent;
  border: none;
}
.nav-menu .el-menu-item {
  color: #fff;
}
.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
}
.el-main {
  background-color: #f5f5f5;
  padding: 20px;
}
.el-footer {
  background-color: #333;
  color: #999;
  text-align: center;
  line-height: 60px;
}
.el-footer p {
  margin: 0;
}
</style>