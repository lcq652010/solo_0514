<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <div class="logo">
          <h2>驾校管理系统</h2>
        </div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical-demo"
          router
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/class-type">
            <i class="el-icon-menu"></i>
            <span slot="title">班型选择</span>
          </el-menu-item>
          <el-menu-item index="/student-reg">
            <i class="el-icon-edit"></i>
            <span slot="title">学员报名</span>
          </el-menu-item>
          <el-menu-item index="/coach-list">
            <i class="el-icon-user"></i>
            <span slot="title">教练列表</span>
          </el-menu-item>
          <el-menu-item index="/reservation">
            <i class="el-icon-date"></i>
            <span slot="title">练车预约</span>
          </el-menu-item>
          <el-menu-item index="/reservation-list">
            <i class="el-icon-document"></i>
            <span slot="title">预约记录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>管理员</span>
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
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

#app {
  height: 100%;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #545c64;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
}

.el-header {
  background-color: #fff;
  color: #333;
  line-height: 60px;
  border-bottom: 1px solid #e6e6e6;
}

.el-aside {
  color: #333;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.card-wrapper {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
