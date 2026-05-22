<template>
  <div id="app">
    <DeviceManagement />
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

body {
  font-family: 'Microsoft YaHei', sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
  padding: 20px;
}
</style>
