<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <h1>燃气营业厅自助缴费打印终端运维管理系统</h1>
      </el-header>
      <el-main>
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, #app {
  height: 100%;
  font-family: 'Microsoft YaHei', sans-serif;
}

.el-header.header {
  background-color: #409EFF;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 40px;
}

.el-header.header h1 {
  font-size: 24px;
  font-weight: 500;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
</style>
