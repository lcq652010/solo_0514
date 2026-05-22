<template>
  <div id="app">
    <el-container class="app-container">
      <el-header class="app-header">
        <div class="header-title">
          <i class="el-icon-s-home"></i>
          <span>医院挂号管理系统</span>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="app-aside">
          <el-menu
            :default-active="activeMenu"
            class="sidebar-menu"
            router
            background-color="#304156"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
          >
            <el-menu-item index="/departments">
              <i class="el-icon-office-building"></i>
              <span>科室列表</span>
            </el-menu-item>
            <el-menu-item index="/schedule">
              <i class="el-icon-s-order"></i>
              <span>医生排班</span>
            </el-menu-item>
            <el-menu-item index="/register">
              <i class="el-icon-edit-outline"></i>
              <span>在线挂号</span>
            </el-menu-item>
            <el-menu-item index="/records">
              <i class="el-icon-document"></i>
              <span>挂号记录</span>
            </el-menu-item>
            <el-menu-item index="/checkin">
              <i class="el-icon-success"></i>
              <span>就诊签到</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="app-main">
          <router-view />
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

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

.app-container {
  height: 100%;
}

.app-header {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  color: #fff;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-title {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
}

.header-title i {
  margin-right: 10px;
  font-size: 24px;
}

.app-aside {
  background-color: #304156;
  box-shadow: 2px 0 6px rgba(0, 0, 0, 0.1);
}

.sidebar-menu {
  border: none;
}

.app-main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}

.page-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 2px solid #409EFF;
  display: flex;
  align-items: center;
}

.page-title i {
  margin-right: 10px;
  color: #409EFF;
}

.el-button + .el-button {
  margin-left: 10px;
}

.el-table {
  margin-top: 15px;
}

.el-pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
