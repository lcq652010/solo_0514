<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">
        <div class="logo">
          <i class="el-icon-coffee-cup"></i>
          <span>奶茶门店点单系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          router
          class="nav-menu"
        >
          <el-menu-item index="/menu">商品点单</el-menu-item>
          <el-menu-item index="/orders">订单列表</el-menu-item>
          <el-menu-item index="/production">制作状态</el-menu-item>
          <el-menu-item index="/statistics">营业统计</el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="app-main">
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

<style lang="scss">
#app {
  height: 100vh;
  .app-header {
    background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
    display: flex;
    align-items: center;
    padding: 0 20px;
    color: #fff;
    .logo {
      display: flex;
      align-items: center;
      font-size: 20px;
      font-weight: bold;
      margin-right: 40px;
      i {
        margin-right: 10px;
        font-size: 24px;
      }
    }
    .nav-menu {
      background: transparent;
      border: none;
      .el-menu-item {
        color: rgba(255, 255, 255, 0.9);
        &.is-active {
          background: rgba(255, 255, 255, 0.2);
          color: #fff;
        }
        &:hover {
          background: rgba(255, 255, 255, 0.15);
          color: #fff;
        }
      }
    }
  }
  .app-main {
    background: #f5f7fa;
    padding: 20px;
    overflow-y: auto;
  }
}
</style>
