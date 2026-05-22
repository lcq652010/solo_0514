<template>
  <div id="app">
    <DeviceList />
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
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #f5f7fa;
  min-height: 100vh;
  padding: 20px;
}
</style>
