<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="logo">
          <i class="el-icon-location-outline"></i>
          <span>景区门票管理系统</span>
        </div>
        <el-menu
          mode="horizontal"
          :default-active="activeMenu"
          class="nav-menu"
          @select="handleSelect"
        >
          <el-menu-item index="tickets">
            <i class="el-icon-tickets"></i>
            门票类型
          </el-menu-item>
          <el-menu-item index="booking">
            <i class="el-icon-document"></i>
            在线预订
          </el-menu-item>
          <el-menu-item index="orders">
            <i class="el-icon-s-order"></i>
            订单列表
          </el-menu-item>
          <el-menu-item index="check">
            <i class="el-icon-check"></i>
            检票核销
          </el-menu-item>
          <el-menu-item index="user">
            <i class="el-icon-user"></i>
            个人中心
          </el-menu-item>
        </el-menu>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
      <el-footer class="footer">
        <span>© 2026 景区门票管理系统 版权所有</span>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path.split('/')[1] || 'tickets'
    }
  },
  methods: {
    handleSelect(index) {
      this.$router.push('/' + index)
    }
  }
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background-color: #409eff;
  color: #fff;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  padding: 0 20px;
  font-size: 20px;
  font-weight: bold;
}

.logo i {
  margin-right: 10px;
  font-size: 24px;
}

.nav-menu {
  background-color: transparent;
  border: none;
  flex: 1;
  justify-content: flex-end;
}

.nav-menu .el-menu-item {
  color: #fff;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.main {
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.footer {
  text-align: center;
  color: #909399;
  font-size: 14px;
  background-color: #fff;
  border-top: 1px solid #e4e7ed;
}
</style>
