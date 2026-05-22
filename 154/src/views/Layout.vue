<template>
  <div class="layout-container">
    <el-header class="layout-header">
      <div class="header-content">
        <div class="logo">
          <i class="el-icon-location-outline"></i>
          <span>景区门票预订系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          :router="true"
          class="header-menu"
          background-color="#409EFF"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <el-menu-item index="/tickets">
            <i class="el-icon-tickets"></i>
            <span>门票类型</span>
          </el-menu-item>
          <el-menu-item index="/booking">
            <i class="el-icon-edit-outline"></i>
            <span>在线预订</span>
          </el-menu-item>
          <el-menu-item index="/orders">
            <i class="el-icon-document"></i>
            <span>订单列表</span>
          </el-menu-item>
          <el-menu-item index="/check">
            <i class="el-icon-success"></i>
            <span>检票核销</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <i class="el-icon-data-line"></i>
            <span>客流统计</span>
          </el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <el-main class="layout-main">
      <router-view />
    </el-main>
    <el-footer class="layout-footer">
      <p>© 2024 景区门票预订系统 版权所有</p>
    </el-footer>
  </div>
</template>

<script>
export default {
  name: 'Layout',
  computed: {
    activeMenu() {
      const route = this.$route.path;
      if (route.startsWith('/booking')) return '/booking';
      return route;
    }
  }
};
</script>

<style scoped>
.layout-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.layout-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  color: #fff;
  font-size: 20px;
  font-weight: 600;
}

.logo i {
  font-size: 28px;
  margin-right: 10px;
}

.header-menu {
  border: none;
  background: transparent !important;
}

.header-menu /deep/ .el-menu-item {
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.header-menu /deep/ .el-menu-item:hover,
.header-menu /deep/ .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.15);
  border-bottom-color: #ffd04b;
}

.layout-main {
  flex: 1;
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.layout-footer {
  background: #303133;
  color: #909399;
  text-align: center;
  padding: 20px 0;
  font-size: 14px;
}

.layout-footer p {
  margin: 0;
}
</style>
