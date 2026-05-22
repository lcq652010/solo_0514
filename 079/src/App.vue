<template>
  <div id="app">
    <el-container class="layout-container">
      <el-header class="layout-header">
        <div class="header-content">
          <h1 class="system-title">会员管理系统</h1>
          <div class="header-nav">
            <el-menu
              :default-active="activeMenu"
              mode="horizontal"
              router
              background-color="#409EFF"
              text-color="#fff"
              active-text-color="#ffd04b"
            >
              <el-menu-item index="/members">会员列表</el-menu-item>
              <el-menu-item index="/transactions">交易流水</el-menu-item>
            </el-menu>
          </div>
        </div>
      </el-header>
      <el-main class="layout-main">
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
      const path = this.$route.path
      if (path.startsWith('/members') || path.startsWith('/member')) {
        return '/members'
      }
      if (path.startsWith('/transactions')) {
        return '/transactions'
      }
      return path
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background-color: #f5f7fa;
}
</style>
