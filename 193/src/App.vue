<template>
  <div id="app">
    <el-container>
      <el-aside width="200px">
        <div class="logo">
          <i class="el-icon-truck"></i>
          <span>物流管理系统</span>
        </div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF">
          <el-menu-item index="/order-form">
            <i class="el-icon-edit-outline"></i>
            <span slot="title">货单下单</span>
          </el-menu-item>
          <el-menu-item index="/vehicle-list">
            <i class="el-icon-truck"></i>
            <span slot="title">车辆管理</span>
          </el-menu-item>
          <el-menu-item index="/dispatch">
            <i class="el-icon-s-order"></i>
            <span slot="title">调度分配</span>
          </el-menu-item>
          <el-menu-item index="/order-list">
            <i class="el-icon-document"></i>
            <span slot="title">运单记录</span>
          </el-menu-item>
          <el-menu-item index="/tracking">
            <i class="el-icon-location"></i>
            <span slot="title">在途状态</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <div class="header-content">
            <span class="page-title">{{ pageTitle }}</span>
            <div class="header-right">
              <el-dropdown>
                <span class="el-dropdown-link">
                  <i class="el-icon-user-solid"></i>
                  管理员
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
        <el-main>
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
        '/order-form': '货单下单',
        '/vehicle-list': '车辆管理',
        '/dispatch': '调度分配',
        '/order-list': '运单记录',
        '/tracking': '在途状态'
      }
      return titleMap[this.$route.path] || '物流管理系统'
    }
  }
}
</script>

<style>
#app {
  height: 100vh;
}
.el-container {
  height: 100%;
}
.el-aside {
  background-color: #304156;
  height: 100%;
  overflow: hidden;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  background-color: #2b3a4a;
}
.logo i {
  margin-right: 8px;
  font-size: 20px;
}
.el-menu-vertical {
  border-right: none;
}
.el-header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
  display: flex;
  align-items: center;
}
.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.page-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}
.header-right {
  display: flex;
  align-items: center;
}
.el-dropdown-link {
  cursor: pointer;
  color: #606266;
  display: flex;
  align-items: center;
}
.el-dropdown-link i {
  margin: 0 5px;
}
.el-main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
