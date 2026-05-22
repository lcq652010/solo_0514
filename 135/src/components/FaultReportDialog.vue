<template>
  <el-dialog
    title="故障上报"
    :visible.sync="dialogVisible"
    width="500px"
    @close="handleClose"
  >
    <el-form ref="form" :model="form" :rules="rules" label-width="100px">
      <el-form-item label="选择设备" prop="deviceId">
        <el-select
          v-model="form.deviceId"
          placeholder="请选择设备"
          style="width: 100%;"
          filterable
        >
          <el-option
            v-for="device in deviceOptions"
            :key="device.id"
            :label="`${device.deviceCode} - ${device.servicePoint}`"
            :value="device.id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="设备编号" prop="deviceCode">
        <el-input
          v-model="form.deviceCode"
          placeholder="设备编号自动显示"
          disabled
        ></el-input>
      </el-form-item>
      <el-form-item label="政务服务点" prop="servicePoint">
        <el-input
          v-model="form.servicePoint"
          placeholder="服务点自动显示"
          disabled
        ></el-input>
      </el-form-item>
      <el-form-item label="故障描述" prop="faultDescription">
        <el-input
          type="textarea"
          v-model="form.faultDescription"
          placeholder="请详细描述故障情况..."
          :rows="4"
          maxlength="500"
          show-word-limit
        ></el-input>
      </el-form-item>
      <el-form-item label="上报人" prop="reporter">
        <el-input
          v-model="form.reporter"
          placeholder="请输入上报人姓名"
        ></el-input>
      </el-form-item>
      <el-form-item label="联系电话" prop="contactPhone">
        <el-input
          v-model="form.contactPhone"
          placeholder="请输入联系电话"
        ></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">提 交</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { mockDeviceList } from '../mockData'

export default {
  name: 'FaultReportDialog',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    deviceList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      submitting: false,
      form: {
        deviceId: '',
        deviceCode: '',
        servicePoint: '',
        faultDescription: '',
        reporter: '',
        contactPhone: ''
      },
      rules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请输入故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述不能少于5个字', trigger: 'blur' }
        ],
        reporter: [
          { required: true, message: '请输入上报人姓名', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    dialogVisible: {
      get() {
        return this.visible
      },
      set(val) {
        this.$emit('close')
      }
    },
    deviceOptions() {
      return mockDeviceList.filter(item => item.status !== '正常')
    }
  },
  watch: {
    'form.deviceId'(newVal) {
      if (newVal) {
        const device = mockDeviceList.find(item => item.id === newVal)
        if (device) {
          this.form.deviceCode = device.deviceCode
          this.form.servicePoint = device.servicePoint
        }
      } else {
        this.form.deviceCode = ''
        this.form.servicePoint = ''
      }
    }
  },
  methods: {
    handleClose() {
      this.$refs.form.resetFields()
      this.$emit('close')
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.submitting = false
            this.$emit('submit', { ...this.form })
            this.handleClose()
          }, 1000)
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
