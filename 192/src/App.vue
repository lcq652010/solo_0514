<template>
  <div id="app">
    <device-list></device-list>
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
#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  min-height: 100vh;
  padding: 20px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>
