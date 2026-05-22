<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="title">传统玉雕平安扣定制系统</h1>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            router
            class="nav-menu"
          >
            <el-menu-item index="/order">客户下单</el-menu-item>
            <el-menu-item index="/admin">管理员后台</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <keep-alive>
          <router-view />
        </keep-alive>
      </el-main>
      <el-footer>
        <p>© 2024 传统玉雕平安扣定制系统 - 匠心传承，精工细作</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
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

html, body, #app {
  height: 100%;
  font-family: "Microsoft YaHei", sans-serif;
}

.el-container {
  height: 100%;
}

.el-header {
  background: linear-gradient(135deg, #8B4513 0%, #D2691E 100%);
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

.title {
  font-size: 24px;
  font-weight: bold;
  letter-spacing: 2px;
}

.nav-menu {
  background: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: white;
  font-size: 16px;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.el-main {
  background: #f5f5f5;
  padding: 30px;
}

.el-footer {
  background: #333;
  color: #999;
  text-align: center;
  line-height: 60px;
  font-size: 14px;
}
</style>
