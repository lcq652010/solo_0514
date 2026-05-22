<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <h2>招聘管理系统</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="false"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF">
        <el-menu-item
          v-for="(item, index) in menuItems"
          :key="index"
          :index="item.path">
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
              <span>管理员</span>
              <i class="el-icon-arrow-down el-icon--right"></i>
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
  data() {
    return {
      menuItems: [
        { path: '/jobs', title: '岗位列表', icon: 'el-icon-suitcase' },
        { path: '/resume', title: '简历投递', icon: 'el-icon-document' },
        { path: '/interview', title: '面试安排', icon: 'el-icon-time' },
        { path: '/applications', title: '应聘记录', icon: 'el-icon-notebook-2' },
        { path: '/offer', title: '录用管理', icon: 'el-icon-medal-1' }
      ]
    }
  },
  computed: {
    activeMenu() {
      return this.$route.path
    },
    currentPageTitle() {
      const route = this.$route
      return route.meta ? route.meta.title : ''
    }
  }
}
</script>

<style lang="scss" scoped>
.layout-container {
  height: 100%;
}

.sidebar {
  background-color: #304156;
  height: 100%;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b2f3a;

  h2 {
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    margin: 0;
  }
}

.el-menu {
  border-right: none;
}

.header {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  height: 60px;
}

.header-left {
  .current-page {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
  }
}

.header-right {
  .user-info {
    cursor: pointer;
    color: #606266;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;

    &:hover {
      color: #409EFF;
    }
  }
}

.main-content {
  background-color: #f5f7fa;
  padding: 0;
  overflow-y: auto;
}
</style>
