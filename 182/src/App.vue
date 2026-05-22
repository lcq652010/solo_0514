<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1>布艺香包定制系统</h1>
          <el-menu mode="horizontal" :default-active="activeMenu" @select="handleSelect">
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
  computed: {
    activeMenu() {
      return this.$route.path === '/admin' ? 'admin' : 'order'
    }
  },
  methods: {
    handleSelect(key) {
      this.$router.push(key === 'admin' ? '/admin' : '/order')
    }
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #333;
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
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.el-menu {
  background: transparent;
  border: none;
}

.el-menu-item {
  color: rgba(255, 255, 255, 0.9);
}

.el-menu-item:hover,
.el-menu-item.is-active {
  color: white;
  background: rgba(255, 255, 255, 0.2);
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 30px 20px;
}
</style>
