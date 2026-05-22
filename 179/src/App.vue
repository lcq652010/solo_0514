<template>
  <div id="app">
    <el-menu 
      :default-active="activeMenu" 
      mode="horizontal" 
      background-color="#409EFF" 
      text-color="#fff" 
      active-text-color="#ffd04b"
      router
    >
      <el-menu-item index="/order">
        <i class="el-icon-edit"></i>
        <span>客户下单</span>
      </el-menu-item>
      <el-menu-item index="/admin">
        <i class="el-icon-s-order"></i>
        <span>订单管理</span>
      </el-menu-item>
    </el-menu>

    <router-view />
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

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.el-menu {
  margin-bottom: 20px;
}
</style>
