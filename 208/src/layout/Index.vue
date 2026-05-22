<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <i class="el-icon-s-goods"></i>
        <span>农产品批发管理</span>
      </div>
      <el-menu
        :default-active="$route.path"
        class="sidebar-menu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item
          v-for="item in menuItems"
          :key="item.path"
          :index="item.path"
        >
          <i :class="item.icon"></i>
          <span slot="title">{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="header">
        <div class="header-left">
          <span class="current-page">{{ currentPageTitle }}</span>
        </div>
        <div class="header-right">
          <el-dropdown>
            <span class="user-info">
              <i class="el-icon-user-solid"></i>
              管理员
              <i class="el-icon-arrow-down"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'Layout',
  computed: {
    menuItems() {
      return this.$router.options.routes[0].children.map(route => ({
        path: '/' + route.path,
        title: route.meta.title,
        icon: route.meta.icon
      }))
    },
    currentPageTitle() {
      return this.$route.meta.title || ''
    }
  }
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100%;
}

.sidebar {
  background-color: #304156;
  height: 100%;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 1001;
  overflow-y: auto;

  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    background-color: #2b2f3a;

    i {
      margin-right: 8px;
      font-size: 20px;
    }
  }

  .sidebar-menu {
    border-right: none;
  }
}

.el-container {
  margin-left: 220px;
}

.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  height: 60px;

  .header-left {
    .current-page {
      font-size: 16px;
      font-weight: 500;
      color: #303133;
    }
  }

  .header-right {
    .user-info {
      cursor: pointer;
      color: #606266;
      display: flex;
      align-items: center;

      i {
        margin: 0 4px;
      }
    }
  }
}

.main-content {
  padding: 0;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style>
