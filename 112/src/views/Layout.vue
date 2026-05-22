<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <i class="el-icon-office-building"></i>
        <span>政务服务中心</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/items" @click="goTo('/items')">
          <i class="el-icon-document"></i>
          <span>办事事项列表</span>
        </el-menu-item>
        <el-menu-item index="/appointment" @click="goTo('/appointment')">
          <i class="el-icon-edit-outline"></i>
          <span>在线预约</span>
        </el-menu-item>
        <el-menu-item index="/ticket" @click="goTo('/ticket')">
          <i class="el-icon-tickets"></i>
          <span>取号服务</span>
        </el-menu-item>
        <el-menu-item index="/calling" @click="goTo('/calling')">
          <i class="el-icon-microphone"></i>
          <span>叫号显示</span>
        </el-menu-item>
        <el-menu-item index="/records" @click="goTo('/records')">
          <i class="el-icon-notebook-2"></i>
          <span>办事记录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-title">
          <h2>{{ pageTitle }}</h2>
        </div>
        <div class="header-user">
          <el-dropdown>
            <span class="el-dropdown-link">
              <i class="el-icon-user-solid"></i>
              市民您好
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
</template>

<script>
export default {
  name: 'Layout',
  data() {
    return {
      pageTitle: '办事事项列表'
    }
  },
  computed: {
    activeMenu() {
      return this.$route.path
    }
  },
  watch: {
    '$route'(to) {
      this.updatePageTitle(to.path)
    }
  },
  created() {
    this.updatePageTitle(this.$route.path)
  },
  methods: {
    goTo(path) {
      this.$router.push(path)
    },
    updatePageTitle(path) {
      const titleMap = {
        '/items': '办事事项列表',
        '/appointment': '在线预约',
        '/ticket': '取号服务',
        '/calling': '叫号显示',
        '/records': '办事记录'
      }
      this.pageTitle = titleMap[path] || '政务服务中心'
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  overflow: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2b2f3a;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
}

.logo i {
  margin-right: 8px;
  font-size: 24px;
}

.sidebar-menu {
  border: none;
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-title h2 {
  color: #303133;
  font-size: 20px;
  font-weight: 500;
}

.header-user {
  color: #606266;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>
