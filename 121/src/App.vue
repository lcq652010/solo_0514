<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-aside width="200px" style="background-color: #2f4050">
        <div class="logo">物流管理系统</div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#2f4050"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/order">
            <i class="el-icon-edit"></i>
            <span>包裹下单</span>
          </el-menu-item>
          <el-menu-item index="/pickup">
            <i class="el-icon-box"></i>
            <span>揽收任务</span>
          </el-menu-item>
          <el-menu-item index="/tracking">
            <i class="el-icon-location"></i>
            <span>派件跟踪</span>
          </el-menu-item>
          <el-menu-item index="/sign">
            <i class="el-icon-check"></i>
            <span>签收确认</span>
          </el-menu-item>
          <el-menu-item index="/query">
            <i class="el-icon-search"></i>
            <span>包裹查询</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <span>欢迎使用物流管理系统</span>
        </el-header>
        <el-main style="background-color: #f0f2f5">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background-color: #1f2d3d;
}

.el-header {
  background-color: #fff;
  line-height: 60px;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}

.el-main {
  padding: 20px;
}

.page-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 20px;
  color: #303133;
}
</style>
