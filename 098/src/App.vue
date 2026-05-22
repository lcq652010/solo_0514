<template>
  <div id="app">
    <el-container>
      <el-header style="background: #fff; border-bottom: 1px solid #e6e6e6; padding: 0;">
        <div class="header-content">
          <div class="logo">
            <i class="el-icon-document"></i>
            <span>传统石质印章定制系统</span>
          </div>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            router
            class="nav-menu"
          >
            <el-menu-item index="/">客户下单</el-menu-item>
            <el-menu-item index="/admin">管理员订单管理</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main style="background: #f5f7fa; min-height: calc(100vh - 60px);">
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
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-right: 40px;
}

.logo i {
  font-size: 24px;
  margin-right: 8px;
  color: #409EFF;
}

.nav-menu {
  flex: 1;
  border-bottom: none;
}
</style>
