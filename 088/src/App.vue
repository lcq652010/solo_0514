<template>
  <div id="app">
    <el-container class="layout-container">
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <h3>🏋️ 健身房管理</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="sidebar-menu"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/trainers">
            <i class="el-icon-user"></i>
            <span slot="title">私教列表</span>
          </el-menu-item>
          <el-menu-item index="/booking">
            <i class="el-icon-edit"></i>
            <span slot="title">会员约课</span>
          </el-menu-item>
          <el-menu-item index="/my-bookings">
            <i class="el-icon-document"></i>
            <span slot="title">我的约课</span>
          </el-menu-item>
          <el-menu-item index="/verify">
            <i class="el-icon-check"></i>
            <span slot="title">课时核销</span>
          </el-menu-item>
          <el-menu-item index="/schedule">
            <i class="el-icon-date"></i>
            <span slot="title">教练排班</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-title">{{ pageTitle }}</div>
          <div class="header-user">
            <el-dropdown>
              <span class="el-dropdown-link">
                <i class="el-icon-user-solid"></i> 管理员
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
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
  name: 'App',
  computed: {
    pageTitle() {
      const titleMap = {
        '/trainers': '私教列表',
        '/booking': '会员约课',
        '/my-bookings': '我的约课记录',
        '/verify': '课时核销',
        '/schedule': '教练排班表'
      }
      return titleMap[this.$route.path] || '健身房管理系统'
    }
  }
}
</script>

<style>
#app {
  height: 100vh;
}
</style>
