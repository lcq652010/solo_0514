<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <h3>保养预约系统</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/packages">
            <i class="el-icon-goods"></i>
            <span slot="title">保养套餐</span>
          </el-menu-item>
          <el-menu-item index="/appointment">
            <i class="el-icon-edit"></i>
            <span slot="title">在线预约</span>
          </el-menu-item>
          <el-menu-item index="/schedule">
            <i class="el-icon-date"></i>
            <span slot="title">技师排班</span>
          </el-menu-item>
          <el-menu-item index="/records">
            <i class="el-icon-document"></i>
            <span slot="title">预约记录</span>
          </el-menu-item>
          <el-menu-item index="/customers">
            <i class="el-icon-user"></i>
            <span slot="title">客户档案</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-title">保养预约管理系统</div>
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
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
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
