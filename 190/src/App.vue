<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu
          :default-active="activeMenu"
          router
          class="el-menu-vertical-demo"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/schedule">
            <i class="el-icon-date"></i>
            <span>医师排班</span>
          </el-menu-item>
          <el-menu-item index="/appointment">
            <i class="el-icon-edit"></i>
            <span>就诊预约</span>
          </el-menu-item>
          <el-menu-item index="/medical-record">
            <i class="el-icon-document"></i>
            <span>病历录入</span>
          </el-menu-item>
          <el-menu-item index="/appointment-list">
            <i class="el-icon-s-order"></i>
            <span>预约记录</span>
          </el-menu-item>
          <el-menu-item index="/vaccine-reminder">
            <i class="el-icon-bell"></i>
            <span>疫苗提醒</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px; background: #fff; border-bottom: 1px solid #e6e6e6;">
          <div style="line-height: 60px; display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; font-size: 20px; color: #333;">宠物医院管理系统</h2>
            <span>管理员</span>
          </div>
        </el-header>
        <el-main style="background: #f5f7fa;">
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
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.el-menu-vertical-demo {
  height: 100%;
}

.page-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  min-height: calc(100vh - 120px);
}

.page-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}
</style>
