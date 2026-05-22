<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="header-left">
        <i class="el-icon-s-platform logo-icon"></i>
        <span class="system-title">人才服务自助证明打印终端运维管理系统</span>
      </div>
      <div class="header-right">
        <span class="user-info">
          <i class="el-icon-user-solid"></i>
          <span>管理员</span>
        </span>
      </div>
    </el-header>
    <el-container>
      <el-aside width="220px" class="sidebar">
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          background-color="#001529"
          text-color="#fff"
          active-text-color="#1890ff"
          @select="handleMenuSelect"
        >
          <el-menu-item index="/">
            <i class="el-icon-monitor"></i>
            <span slot="title">设备管理</span>
          </el-menu-item>
          <el-menu-item index="/workorder">
            <i class="el-icon-document"></i>
            <span slot="title">工单管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeMenu: '/'
    }
  },
  watch: {
    $route(to) {
      this.activeMenu = to.path
    }
  },
  methods: {
    handleMenuSelect(index) {
      this.$router.push(index)
    }
  }
}
</script>

<style lang="scss" scoped>
.header {
  background: linear-gradient(90deg, #001529, #003a8c);
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;

    .logo-icon {
      font-size: 28px;
      color: #1890ff;
    }

    .system-title {
      font-size: 18px;
      font-weight: 600;
      letter-spacing: 1px;
    }
  }

  .header-right {
    .user-info {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      opacity: 0.9;
    }
  }
}

.sidebar {
  background-color: #001529;
  height: calc(100vh - 64px);

  .sidebar-menu {
    height: 100%;
    border-right: none;

    ::v-deep .el-menu-item {
      height: 56px;
      line-height: 56px;
      font-size: 15px;

      &:hover {
        background-color: rgba(24, 144, 255, 0.1);
      }

      i {
        font-size: 18px;
        margin-right: 10px;
      }
    }

    ::v-deep .el-menu-item.is-active {
      background-color: rgba(24, 144, 255, 0.2);
      border-left: 4px solid #1890ff;
    }
  }
}
</style>
