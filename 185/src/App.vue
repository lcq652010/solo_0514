<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee;">
      <el-header style="text-align: center; font-size: 24px; font-weight: bold; background: #4CAF50; color: white; line-height: 60px;">
        🍃 竹编茶笼定制系统
      </el-header>
      <el-container>
        <el-aside width="200px" style="background-color: #f5f7fa;">
          <el-menu router default-active="1" class="el-menu-vertical-demo">
            <el-menu-item index="1" route="/">
              <i class="el-icon-shopping-cart-2"></i>
              <span slot="title">定制下单</span>
            </el-menu-item>
            <el-menu-item index="2" route="/admin">
              <i class="el-icon-s-tools"></i>
              <span slot="title">生产管理</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: 'Microsoft YaHei', sans-serif;
}
#app {
  font-family: 'Microsoft YaHei', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
.el-header {
  background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%);
}
</style>
