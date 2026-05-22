<template>
  <el-dialog
    title="故障上报"
    :visible.sync="dialogVisible"
    width="500px"
    @close="handleClose">
    <el-form :model="form" :rules="rules" ref="form" label-width="100px">
      <el-form-item label="工单编号">
        <el-input v-model="form.orderNo" disabled></el-input>
      </el-form-item>
      <el-form-item label="选择设备" prop="deviceId">
        <el-select v-model="form.deviceId" placeholder="请选择设备" style="width: 100%;">
          <el-option
            v-for="device in deviceList"
            :key="device.id"
            :label="`${device.deviceNo} - ${device.hallName}`"
            :value="device.id">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="故障描述" prop="description">
        <el-input
          type="textarea"
          v-model="form.description"
          :rows="4"
          placeholder="请详细描述故障情况">
        </el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="handleSubmit">提 交</el-button>
    </span>
  </el-dialog>
</template>

<script>
import { deviceList, generateOrderNo } from '../mock/data.js'

export default {
  name: 'FaultReport',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    selectedDevice: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      dialogVisible: false,
      deviceList: [],
      form: {
        orderNo: '',
        deviceId: '',
        description: ''
      },
      rules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请输入故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述不能少于5个字', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    visible(val) {
      this.dialogVisible = val
      if (val) {
        this.initForm()
      }
    },
    dialogVisible(val) {
      this.$emit('update:visible', val)
    }
  },
  created() {
    this.deviceList = [...deviceList]
  },
  methods: {
    initForm() {
      this.form.orderNo = generateOrderNo()
      this.form.description = ''
      if (this.selectedDevice) {
        this.form.deviceId = this.selectedDevice.id
      } else {
        this.form.deviceId = ''
      }
      if (this.$refs.form) {
        this.$refs.form.clearValidate()
      }
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const device = this.deviceList.find(d => d.id === this.form.deviceId)
          const orderData = {
            orderNo: this.form.orderNo,
            deviceId: this.form.deviceId,
            deviceNo: device.deviceNo,
            hallName: device.hallName,
            window: device.window,
            description: this.form.description,
            createTime: new Date().toLocaleString()
          }
          console.log('提交工单:', orderData)
          this.$message.success('故障上报成功！工单编号：' + this.form.orderNo)
          this.dialogVisible = false
          this.$emit('submit-success', orderData)
        } else {
          return false
        }
      })
    },
    handleClose() {
      this.$refs.form.resetFields()
    }
  }
}
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
