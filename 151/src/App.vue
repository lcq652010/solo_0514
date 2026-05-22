<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee;">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246);">
        <div class="logo">
          <h3>健身房管理</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b">
          <el-menu-item index="/trainers">
            <i class="el-icon-s-custom"></i>
            <span slot="title">私教列表</span>
          </el-menu-item>
          <el-menu-item index="/booking">
            <i class="el-icon-edit-outline"></i>
            <span slot="title">私教预约</span>
          </el-menu-item>
          <el-menu-item index="/classes">
            <i class="el-icon-date"></i>
            <span slot="title">团课展示</span>
          </el-menu-item>
          <el-menu-item index="/my-bookings">
            <i class="el-icon-document"></i>
            <span slot="title">我的预约</span>
          </el-menu-item>
          <el-menu-item index="/course-hours">
            <i class="el-icon-s-order"></i>
            <span slot="title">课时管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px;">
          <span>欢迎使用健身房管理系统</span>
        </el-header>
        <el-main>
          <router-view></router-view>
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #409EFF;
  color: #fff;
}

.el-header {
  background-color: #fff;
  color: #333;
  line-height: 60px;
  padding-right: 20px;
  border-bottom: 1px solid #e6e6e6;
}

.el-aside {
  overflow: hidden;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: 500;
  margin-bottom: 20px;
  color: #303133;
}
</style>
