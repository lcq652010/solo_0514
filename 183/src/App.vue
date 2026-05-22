<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="system-title">公积金自助查询打印终端运维管理系统</h1>
        </div>
      </el-header>
      <el-main>
        <DeviceList />
      </el-main>
    </el-container>
  </div>
</template>

<script>
import DeviceList from './components/DeviceList.vue'

export default {
  name: 'App',
  components: {
    DeviceList
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
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
  background-color: #f5f7fa;
}

.el-header {
  background-color: #409EFF;
  color: #fff;
  line-height: 60px;
  padding: 0 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
}

.system-title {
  font-size: 22px;
  font-weight: 500;
  color: #fff;
}

.el-main {
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  padding: 20px;
}
</style>
