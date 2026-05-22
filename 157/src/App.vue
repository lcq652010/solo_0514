<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <h3>办公用品管理</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
        >
          <el-menu-item index="/categories">
            <i class="el-icon-s-grid"></i>
            <span slot="title">用品分类</span>
          </el-menu-item>
          <el-menu-item index="/apply">
            <i class="el-icon-edit-outline"></i>
            <span slot="title">用品申领</span>
          </el-menu-item>
          <el-menu-item index="/records">
            <i class="el-icon-document"></i>
            <span slot="title">申领记录</span>
          </el-menu-item>
          <el-menu-item index="/inventory">
            <i class="el-icon-s-goods"></i>
            <span slot="title">库存管理</span>
          </el-menu-item>
          <el-menu-item index="/stock-in">
            <i class="el-icon-download"></i>
            <span slot="title">入库登记</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <span class="system-title">办公用品管理系统</span>
        </el-header>
        <el-main class="main-content">
          <router-view></router-view>
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
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>
