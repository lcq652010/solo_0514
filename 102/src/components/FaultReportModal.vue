<template>
  <el-dialog 
    title="故障上报" 
    :visible.sync="visible" 
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form :model="form" :rules="rules" ref="form" label-width="100px">
      <el-form-item label="选择设备" prop="deviceId">
        <el-select 
          v-model="form.deviceId" 
          placeholder="请选择故障设备" 
          style="width: 100%;"
          filterable
        >
          <el-option
            v-for="device in deviceList"
            :key="device.id"
            :label="`${device.deviceCode} - ${device.branchName}`"
            :value="device.id"
          >
            <span style="float: left;">{{ device.deviceCode }}</span>
            <span style="float: right; color: #8492a6; font-size: 13px;">{{ device.branchName }}</span>
          </el-option>
        </el-select>
      </el-form-item>
      
      <el-form-item label="设备编号" v-if="selectedDevice">
        <el-input :value="selectedDevice.deviceCode" disabled />
      </el-form-item>
      
      <el-form-item label="所属网点" v-if="selectedDevice">
        <el-input :value="selectedDevice.branchName" disabled />
      </el-form-item>
      
      <el-form-item label="放置区域" v-if="selectedDevice">
        <el-input :value="selectedDevice.area" disabled />
      </el-form-item>
      
      <el-form-item label="故障说明" prop="description">
        <el-input
          type="textarea"
          v-model="form.description"
          placeholder="请详细描述故障情况，如：设备无法启动、触摸屏失灵、打印异常等"
          :rows="4"
          maxlength="500"
          show-word-limit
        />
      </el-form-item>
      
      <el-form-item label="联系人">
        <el-input v-model="form.contact" placeholder="请输入联系人姓名" />
      </el-form-item>
      
      <el-form-item label="联系电话">
        <el-input v-model="form.phone" placeholder="请输入联系电话" />
      </el-form-item>
    </el-form>
    
    <div slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="loading">提交工单</el-button>
    </div>
  </el-dialog>
</template>

<script>
export default {
  name: 'FaultReportModal',
  props: {
    deviceList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      visible: false,
      loading: false,
      form: {
        deviceId: null,
        description: '',
        contact: '',
        phone: ''
      },
      rules: {
        deviceId: [
          { required: true, message: '请选择故障设备', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请填写故障说明', trigger: 'blur' },
          { min: 5, message: '故障说明至少5个字符', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    selectedDevice() {
      if (!this.form.deviceId) return null
      return this.deviceList.find(d => d.id === this.form.deviceId)
    }
  },
  methods: {
    open(device = null) {
      this.resetForm()
      if (device) {
        this.form.deviceId = device.id
      }
      this.visible = true
    },
    handleClose() {
      this.visible = false
      this.resetForm()
    },
    resetForm() {
      this.form = {
        deviceId: null,
        description: '',
        contact: '',
        phone: ''
      }
      if (this.$refs.form) {
        this.$refs.form.resetFields()
      }
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.loading = true
          
          setTimeout(() => {
            this.loading = false
            this.$emit('submit', {
              deviceId: this.form.deviceId,
              description: this.form.description,
              contact: this.form.contact,
              phone: this.form.phone
            })
            this.handleClose()
          }, 800)
        }
      })
    }
  }
}
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
