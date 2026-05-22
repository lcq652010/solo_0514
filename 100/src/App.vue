<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-header style="background: #409eff; padding: 0;">
        <div class="header-content">
          <h2 class="logo">🚗 4S店保养预约系统</h2>
          <el-menu
            mode="horizontal"
            :default-active="$route.path"
            router
            background-color="#409eff"
            text-color="#fff"
            active-text-color="#ffd04b"
            class="nav-menu"
          >
            <el-menu-item index="/packages">保养套餐</el-menu-item>
            <el-menu-item index="/reserve">在线预约</el-menu-item>
            <el-menu-item index="/records">我的预约</el-menu-item>
            <el-menu-item index="/progress">施工进度</el-menu-item>
            <el-menu-item index="/evaluate">服务评价</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main style="padding: 0; overflow-y: auto;">
        <router-view></router-view>
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
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}

.logo {
  color: #fff;
  font-size: 20px;
  margin-right: 40px;
  white-space: nowrap;
}

.nav-menu {
  flex: 1;
  border: none;
}
</style>
