<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-aside width="200px" style="background-color: #2e3b4e">
        <div class="logo">
          <h3>体检中心</h3>
        </div>
        <el-menu
          :default-active="activeMenu"
          router
          background-color="#2e3b4e"
          text-color="#fff"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/packages">
            <i class="el-icon-s-shop"></i>
            <span slot="title">体检套餐</span>
          </el-menu-item>
          <el-menu-item index="/appointment">
            <i class="el-icon-date"></i>
            <span slot="title">在线预约</span>
          </el-menu-item>
          <el-menu-item index="/records">
            <i class="el-icon-document"></i>
            <span slot="title">体检记录</span>
          </el-menu-item>
          <el-menu-item index="/report-upload">
            <i class="el-icon-upload2"></i>
            <span slot="title">报告上传</span>
          </el-menu-item>
          <el-menu-item index="/report-query">
            <i class="el-icon-search"></i>
            <span slot="title">报告查询</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="background-color: #fff; border-bottom: 1px solid #e6e6e6">
          <div class="header-content">
            <span class="system-title">健康体检管理系统</span>
            <div class="user-info">
              <el-dropdown>
                <span class="el-dropdown-link">
                  <i class="el-icon-user-solid"></i>
                  <span>张三</span>
                  <i class="el-icon-arrow-down el-icon--right"></i>
                </span>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
            </div>
          </div>
        </el-header>
        <el-main style="background-color: #f5f7fa">
          <router-view></router-view>
        </el-main>
      </el-container>
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
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
  background-color: #232f3e;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.system-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
}

.user-info {
  .el-dropdown-link {
    cursor: pointer;
    color: #606266;
    display: flex;
    align-items: center;
    gap: 8px;
  }
}

.el-aside {
  overflow: hidden;
}

.el-menu {
  border-right: none;
}
</style>
