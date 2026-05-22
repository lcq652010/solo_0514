<template>
  <el-dialog
    title="故障报修"
    :visible.sync="visible"
    width="550px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="repairForm"
      :model="repairForm"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="工单号">
        <el-input v-model="repairForm.orderNo" disabled />
      </el-form-item>
      <el-form-item label="选择设备" prop="deviceId">
        <el-select
          v-model="repairForm.deviceId"
          placeholder="请选择要报修的设备"
          style="width: 100%"
          filterable
          @change="handleDeviceChange"
        >
          <el-option
            v-for="device in availableDevices"
            :key="device.id"
            :label="`${device.deviceCode} - ${device.branchName} ${device.floor}`"
            :value="device.id"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="设备编号">
        <el-input v-model="repairForm.deviceCode" disabled />
      </el-form-item>
      <el-form-item label="分馆位置">
        <el-input v-model="repairForm.branchName" disabled />
      </el-form-item>
      <el-form-item label="部署楼层">
        <el-input v-model="repairForm.floor" disabled />
      </el-form-item>
      <el-form-item label="当前状态">
        <el-tag :type="currentStatusType" effect="light" size="small">
          {{ currentStatusText }}
        </el-tag>
      </el-form-item>
      <el-form-item label="问题描述" prop="problem">
        <el-input
          type="textarea"
          v-model="repairForm.problem"
          :rows="4"
          placeholder="请详细描述故障问题"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
      <el-form-item label="报修人" prop="reporter">
        <el-input v-model="repairForm.reporter" placeholder="请输入报修人姓名" />
      </el-form-item>
    </el-form>

    <div slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        提交报修
      </el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'RepairModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    device: {
      type: Object,
      default: () => ({})
    },
    devices: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      submitting: false,
      repairForm: {
        orderNo: '',
        deviceId: null,
        deviceCode: '',
        branchName: '',
        floor: '',
        problem: '',
        reporter: ''
      },
      rules: {
        deviceId: [
          { required: true, message: '请选择要报修的设备', trigger: 'change' }
        ],
        problem: [
          { required: true, message: '请描述故障问题', trigger: 'blur' },
          { min: 5, message: '问题描述不能少于5个字符', trigger: 'blur' },
          { max: 500, message: '问题描述不能超过500个字符', trigger: 'blur' }
        ],
        reporter: [
          { required: true, message: '请输入报修人姓名', trigger: 'blur' },
          { min: 2, message: '报修人姓名不能少于2个字符', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    availableDevices() {
      return this.devices.filter(d => d.status !== 'maintaining')
    },
    selectedDeviceInfo() {
      if (!this.repairForm.deviceId) return null
      return this.devices.find(d => d.id === this.repairForm.deviceId) || null
    },
    currentStatusType() {
      if (!this.selectedDeviceInfo) return 'info'
      const typeMap = {
        online: 'success',
        offline: 'info',
        fault: 'danger',
        maintaining: 'warning'
      }
      return typeMap[this.selectedDeviceInfo.status] || 'info'
    },
    currentStatusText() {
      if (!this.selectedDeviceInfo) return '未选择'
      const textMap = {
        online: '在线',
        offline: '离线',
        fault: '故障',
        maintaining: '维护中'
      }
      return textMap[this.selectedDeviceInfo.status] || '未知'
    }
  },
  watch: {
    visible(val) {
      if (val && this.device) {
        this.initForm()
      }
    },
    device: {
      immediate: true,
      handler(val) {
        if (val && this.visible) {
          this.initForm()
        }
      }
    }
  },
  methods: {
    generateOrderNo() {
      const now = new Date()
      const timestamp = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(now.getHours()).padStart(2, '0')}${String(now.getMinutes()).padStart(2, '0')}`
      const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0')
      return `GD${timestamp}${random}`
    },
    initForm() {
      const targetDevice = this.device && this.device.id ? this.device : null
      this.repairForm = {
        orderNo: this.generateOrderNo(),
        deviceId: targetDevice ? targetDevice.id : null,
        deviceCode: targetDevice ? targetDevice.deviceCode : '',
        branchName: targetDevice ? targetDevice.branchName : '',
        floor: targetDevice ? targetDevice.floor : '',
        problem: '',
        reporter: ''
      }
      this.$nextTick(() => {
        if (this.$refs.repairForm) {
          this.$refs.repairForm.clearValidate()
        }
      })
    },
    handleDeviceChange(deviceId) {
      const device = this.devices.find(d => d.id === deviceId)
      if (device) {
        this.repairForm.deviceCode = device.deviceCode
        this.repairForm.branchName = device.branchName
        this.repairForm.floor = device.floor
      } else {
        this.repairForm.deviceCode = ''
        this.repairForm.branchName = ''
        this.repairForm.floor = ''
      }
    },
    handleClose() {
      this.$emit('update:visible', false)
      if (this.$refs.repairForm) {
        this.$refs.repairForm.clearValidate()
      }
    },
    beforeSubmitValidate() {
      if (!this.repairForm.deviceId) {
        this.$message.warning('请选择要报修的设备')
        return false
      }
      const device = this.devices.find(d => d.id === this.repairForm.deviceId)
      if (!device) {
        this.$message.error('选择的设备不存在')
        return false
      }
      if (device.status === 'maintaining') {
        this.$message.warning('该设备正在维护中，无需重复报修')
        return false
      }
      if (!this.repairForm.problem || this.repairForm.problem.trim().length < 5) {
        this.$message.warning('请详细描述故障问题（至少5个字符）')
        return false
      }
      if (!this.repairForm.reporter || this.repairForm.reporter.trim().length < 2) {
        this.$message.warning('请输入报修人姓名（至少2个字符）')
        return false
      }
      return true
    },
    handleSubmit() {
      this.$refs.repairForm.validate((valid) => {
        if (valid && this.beforeSubmitValidate()) {
          this.submitting = true
          setTimeout(() => {
            this.$message.success('报修提交成功，工单号：' + this.repairForm.orderNo)
            this.$emit('submit', {
              ...this.repairForm,
              createTime: new Date().toLocaleString('zh-CN')
            })
            this.submitting = false
            this.handleClose()
          }, 500)
        }
      })
    }
  }
}
</script>

<style scoped lang="scss">
.dialog-footer {
  text-align: right;
}
</style>
