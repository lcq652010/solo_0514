<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <h1 class="title">社团活动管理系统</h1>
          <el-menu mode="horizontal" :default-active="$route.path" router class="nav-menu">
            <el-menu-item index="/">活动列表</el-menu-item>
            <el-menu-item index="/my-registrations">我的报名</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
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
  font-family: "Microsoft YaHei", sans-serif;
  min-height: 100vh;
}

.header {
  background-color: #409EFF;
  padding: 0;
  height: 60px !important;
  line-height: 60px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.title {
  color: white;
  font-size: 20px;
  margin: 0;
}

.nav-menu {
  background-color: transparent;
  border: none;
}

.nav-menu .el-menu-item {
  color: white;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  min-height: calc(100vh - 60px);
}
</style>
