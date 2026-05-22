<template>
  <div id="app">
    <el-container class="layout-container">
      <el-header class="header">
        <div class="logo">
          <i class="el-icon-monitor"></i>
          <span>社区服务自助办事终端运维管理系统</span>
        </div>
        <div class="user-info">
          <el-dropdown>
            <span class="el-dropdown-link">
              <i class="el-icon-user-solid"></i>
              管理员
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="sidebar">
          <el-menu
            :default-active="activeMenu"
            class="sidebar-menu"
            background-color="#001529"
            text-color="#b9c0cd"
            active-text-color="#ffffff"
            @select="handleMenuSelect"
          >
            <el-menu-item index="device">
              <i class="el-icon-s-platform"></i>
              <span slot="title">设备管理</span>
            </el-menu-item>
            <el-menu-item index="workorder">
              <i class="el-icon-document"></i>
              <span slot="title">工单管理</span>
            </el-menu-item>
            <el-menu-item index="statistics">
              <i class="el-icon-data-line"></i>
              <span slot="title">数据统计</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'App',
  data() {
    return {
      activeMenu: 'device'
    }
  },
  methods: {
    handleMenuSelect(index: string) {
      this.activeMenu = index
      this.$router.push(`/${index}`)
    }
  }
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.header {
  background: linear-gradient(90deg, #1890ff 0%, #096dd9 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.logo {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: 600;
}

.logo i {
  font-size: 28px;
  margin-right: 12px;
}

.user-info {
  font-size: 14px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #fff;
  display: flex;
  align-items: center;
}

.el-dropdown-link i {
  margin: 0 4px;
}

.sidebar {
  background: #001529;
  overflow: hidden;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  height: 56px;
  line-height: 56px;
}

.sidebar-menu .el-menu-item:hover {
  background: #1890ff !important;
  color: #fff !important;
}

.sidebar-menu .el-menu-item.is-active {
  background: #1890ff !important;
}

.main-content {
  background: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
