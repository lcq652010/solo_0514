<template>
  <div id="app">
    <el-menu 
      :default-active="activeRoute" 
      mode="horizontal" 
      background-color="#303133"
      text-color="#fff"
      active-text-color="#409EFF"
      router>
      <el-menu-item index="/">
        <i class="el-icon-shopping-cart-2"></i>
        <span>我要定制</span>
      </el-menu-item>
      <el-menu-item index="/admin">
        <i class="el-icon-s-tools"></i>
        <span>管理后台</span>
      </el-menu-item>
    </el-menu>
    
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeRoute() {
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
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}

#app {
  min-height: 100vh;
}

.el-menu {
  margin-bottom: 0 !important;
}
</style>
