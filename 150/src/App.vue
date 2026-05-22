<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <h1>医院自助病历打印终端运维管理系统</h1>
      </el-header>
      <el-main class="main-content">
        <DeviceManagement />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import DeviceManagement from './components/DeviceManagement.vue'

export default {
  name: 'App',
  components: {
    DeviceManagement
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
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

.header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  font-size: 24px;
  font-weight: 500;
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
}

.el-container {
  height: 100%;
}
</style>
