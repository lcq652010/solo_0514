<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="layout-aside">
      <div class="logo">
        <i class="el-icon-s-custom"></i>
        <span>水电充值系统</span>
      </div>
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
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
      <el-header class="layout-header">
        <div class="header-left">
          <span class="breadcrumb-title">{{ currentPageTitle }}</span>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="el-dropdown-link user-info">
              <i class="el-icon-user"></i>
              <span>张三同学</span>
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="settings">设置</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="layout-main">
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
        { path: '/usage', title: '水电用量', icon: 'el-icon-data-line' },
        { path: '/recharge', title: '在线充值', icon: 'el-icon-wallet' },
        { path: '/records', title: '充值记录', icon: 'el-icon-document' },
        { path: '/reminder', title: '余额提醒', icon: 'el-icon-bell' },
        { path: '/binding', title: '宿舍绑定', icon: 'el-icon-house' }
      ]
    }
  },
  computed: {
    currentPageTitle() {
      const route = this.$route
      return route.meta && route.meta.title ? route.meta.title : ''
    }
  },
  methods: {
    handleCommand(command) {
      if (command === 'logout') {
        this.$confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message.success('已退出登录')
        }).catch(() => {})
      } else {
        this.$message.info(`点击了${command}`)
      }
    }
  }
}
</script>

<style scoped>
.layout-container {
  width: 100%;
  height: 100%;
}

.layout-aside {
  background-color: #304156;
  height: 100%;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo i {
  margin-right: 8px;
  font-size: 20px;
}

.el-menu-vertical-demo {
  border-right: none;
}

.layout-header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left .breadcrumb-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.header-right .user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  color: #606266;
}

.header-right .user-info i {
  margin: 0 5px;
}

.layout-main {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>
