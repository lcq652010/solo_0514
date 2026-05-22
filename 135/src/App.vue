<template>
  <div id="app">
    <el-container>
      <el-header class="header">
        <h1>教育局自助学籍证明打印终端运维管理系统</h1>
      </el-header>
      <el-main>
        <DeviceList @report-fault="handleReportFault" />
      </el-main>
    </el-container>
    <FaultReportDialog
      :visible="dialogVisible"
      :device-list="deviceList"
      @close="dialogVisible = false"
      @submit="handleSubmitFault"
    />
  </div>
</template>

<script>
import DeviceList from './components/DeviceList.vue'
import FaultReportDialog from './components/FaultReportDialog.vue'
import { generateWorkOrderId } from './utils'

export default {
  name: 'App',
  components: {
    DeviceList,
    FaultReportDialog
  },
  data() {
    return {
      dialogVisible: false,
      deviceList: [],
      currentDevice: null
    }
  },
  methods: {
    handleReportFault(device) {
      this.currentDevice = device
      this.dialogVisible = true
    },
    handleSubmitFault(formData) {
      const workOrderId = generateWorkOrderId()
      this.$message.success(`故障上报成功！工单编号：${workOrderId}`)
      console.log('故障上报数据：', { ...formData, workOrderId })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 500;
}

.el-main {
  padding: 20px;
}
</style>
