<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="title">传统陶瓷茶宠定制平台</h1>
          <el-menu mode="horizontal" :default-active="$route.path" class="nav-menu" router>
            <el-menu-item index="/">客户下单</el-menu-item>
            <el-menu-item index="/admin">管理员后台</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>
        <p>© 2024 传统陶瓷茶宠定制平台 - 传承匠心工艺</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  min-height: 100vh;
}
.el-header {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: white;
  padding: 0;
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
  margin: 0;
  font-weight: 600;
}
.nav-menu {
  background: transparent;
  border: none;
}
.nav-menu .el-menu-item {
  color: rgba(255,255,255,0.9);
}
.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background: rgba(255,255,255,0.2);
  color: white;
}
.el-main {
  background: #f5f0e8;
  padding: 30px;
}
.el-footer {
  background: #3d2914;
  color: rgba(255,255,255,0.7);
  text-align: center;
  line-height: 60px;
  font-size: 14px;
}
</style>
