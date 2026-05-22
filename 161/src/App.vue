<template>
  <div id="app">
    <el-header class="header">
      <div class="header-content">
        <h1 class="title">篆刻印章定制系统</h1>
        <el-menu mode="horizontal" :router="true" class="nav-menu">
          <el-menu-item index="/">客户下单</el-menu-item>
          <el-menu-item index="/admin">管理员订单</el-menu-item>
        </el-menu>
      </div>
    </el-header>
    <main class="main-content">
      <router-view />
    </main>
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
  background: #f5f5f5;
}
</style>
