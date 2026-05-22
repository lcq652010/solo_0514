<template>
  <div id="app">
    <div class="header">
      <h1>政务大厅自助征信查询终端运维管理系统</h1>
    </div>
    <div class="main-content">
      <DeviceList @open-report="handleOpenReport"></DeviceList>
    </div>
    <FaultReport 
      :visible.sync="reportVisible" 
      :selected-device="selectedDevice"
      @submit-success="handleSubmitSuccess">
    </FaultReport>
  </div>
</template>

<script>
import DeviceList from './components/DeviceList.vue'
import FaultReport from './components/FaultReport.vue'

export default {
  name: 'App',
  components: {
    DeviceList,
    FaultReport
  },
  data() {
    return {
      reportVisible: false,
      selectedDevice: null
    }
  },
  methods: {
    handleOpenReport(device) {
      this.selectedDevice = device || null
      this.reportVisible = true
    },
    handleSubmitSuccess(orderData) {
      console.log('工单提交成功:', orderData)
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
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  padding: 20px 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #fff;
  font-size: 24px;
  font-weight: 500;
  text-align: center;
}

.main-content {
  padding: 30px 40px;
  max-width: 1400px;
  margin: 0 auto;
}
</style>
