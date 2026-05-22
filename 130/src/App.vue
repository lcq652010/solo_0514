<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="title">物业报修管理系统</h1>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            @select="handleSelect"
            class="nav-menu"
          >
            <el-menu-item index="/apply">报修申请</el-menu-item>
            <el-menu-item index="/my-repairs">我的报修</el-menu-item>
            <el-menu-item index="/dispatch">维修派单</el-menu-item>
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
      return this.$route.path
    }
  },
  methods: {
    handleSelect(index) {
      this.$router.push(index)
    }
  }
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.el-header {
  background-color: #409EFF;
  color: #fff;
  padding: 0;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 100%;
}

.title {
  font-size: 20px;
  margin: 0 40px 0 20px;
  font-weight: 500;
}

.nav-menu {
  background-color: transparent;
  border: none;
  flex: 1;
}

.nav-menu .el-menu-item {
  color: #fff;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.2);
}

.el-main {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
}
</style>
