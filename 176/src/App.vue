<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>锡制茶叶罐定制系统</h1>
          <el-menu 
            :default-active="activeMenu" 
            mode="horizontal" 
            @select="handleMenuSelect"
            class="nav-menu"
          >
            <el-menu-item index="order">客户下单</el-menu-item>
            <el-menu-item index="admin">订单管理</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      activeMenu: 'order'
    }
  },
  created() {
    this.activeMenu = this.$route.name || 'order'
  },
  methods: {
    handleMenuSelect(index) {
      this.activeMenu = index
      if (index === 'order') {
        this.$router.push('/')
      } else if (index === 'admin') {
        this.$router.push('/admin')
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  min-height: 100vh;
  background: #f5f7fa;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.header-content h1 {
  font-size: 24px;
  font-weight: 600;
}

.nav-menu {
  background: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: rgba(255, 255, 255, 0.9);
  border-bottom: 2px solid transparent;
}

.nav-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border-bottom: 2px solid white;
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  width: 100%;
}
</style>
