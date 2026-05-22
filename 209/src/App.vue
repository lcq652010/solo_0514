<template>
  <div id="app">
    <el-header class="header">
      <div class="logo">
        <i class="el-icon-coffee-cup"></i>
        <span>陶瓷茶盏定制系统</span>
      </div>
      <el-menu
        mode="horizontal"
        :default-active="$route.path"
        router
        class="nav-menu"
        background-color="#5D4037"
        text-color="#EFEBE9"
        active-text-color="#FFD54F"
      >
        <el-menu-item index="/order">
          <i class="el-icon-edit-outline"></i>
          <span>客户下单</span>
        </el-menu-item>
        <el-menu-item index="/admin">
          <i class="el-icon-setting"></i>
          <span>订单管理</span>
        </el-menu-item>
      </el-menu>
    </el-header>

    <main class="main-content">
      <router-view />
    </main>

    <el-footer class="footer">
      <p>&copy; 2024 陶瓷茶盏定制工坊 - 匠心独运，盏盏精品</p>
    </el-footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: linear-gradient(135deg, #5D4037 0%, #795548 100%);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.logo {
  display: flex;
  align-items: center;
  color: #EFEBE9;
  font-size: 20px;
  font-weight: bold;
}

.logo i {
  font-size: 28px;
  margin-right: 12px;
  color: #FFD54F;
}

.nav-menu {
  border-bottom: none;
  background: transparent;
}

.main-content {
  flex: 1;
  padding: 30px;
  background-color: #EFEBE9;
}

.footer {
  background-color: #3E2723;
  color: #BCAAA4;
  text-align: center;
  padding: 20px;
}

.footer p {
  margin: 0;
  font-size: 14px;
}
</style>
