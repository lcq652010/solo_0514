<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="logo">
          <i class="el-icon-reading"></i>
          <span>线上课程管理系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          router
          class="nav-menu"
        >
          <el-menu-item index="/courses">课程列表</el-menu-item>
          <el-menu-item index="/enroll">学员报名</el-menu-item>
          <el-menu-item index="/progress">学习进度</el-menu-item>
          <el-menu-item index="/homework">作业提交</el-menu-item>
          <el-menu-item index="/my-courses">我的课程</el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="main-content">
        <router-view></router-view>
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

<style>
#app {
  height: 100vh;
}
</style>
