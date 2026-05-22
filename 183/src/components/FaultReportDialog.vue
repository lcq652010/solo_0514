<template>
  <el-dialog
    title="故障上报"
    :visible.sync="dialogVisible"
    width="500px"
    :close-on-click-modal="false"
    @close="handleClose">
    <el-form :model="form" :rules="rules" ref="form" label-width="100px">
      <el-form-item label="工单编号">
        <el-input v-model="form.orderNo" disabled></el-input>
      </el-form-item>
      <el-form-item label="故障设备" prop="deviceCode">
        <el-select 
          v-model="form.deviceCode" 
          placeholder="请选择故障设备" 
          style="width: 100%" 
          filterable
          clearable
          no-data-text="暂无匹配设备">
          <el-option
            v-for="item in deviceList"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="故障类型" prop="faultType">
        <el-select v-model="form.faultType" placeholder="请选择故障类型" style="width: 100%">
          <el-option label="设备无法开机" value="power"></el-option>
          <el-option label="打印异常" value="print"></el-option>
          <el-option label="触摸屏无响应" value="touch"></el-option>
          <el-option label="网络连接异常" value="network"></el-option>
          <el-option label="软件运行异常" value="software"></el-option>
          <el-option label="硬件损坏" value="hardware"></el-option>
          <el-option label="其他故障" value="other"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="故障描述" prop="faultDescription">
        <el-input
          type="textarea"
          v-model="form.faultDescription"
          :rows="5"
          :maxlength="500"
          show-word-limit
          placeholder="请详细描述故障情况，便于维修人员快速定位问题">
        </el-input>
      </el-form-item>
      <el-form-item label="联系人" prop="contactPerson">
        <el-input v-model="form.contactPerson" placeholder="请填写联系人姓名" maxlength="20"></el-input>
      </el-form-item>
      <el-form-item label="联系电话" prop="contactPhone">
        <el-input v-model="form.contactPhone" placeholder="请填写联系电话" maxlength="11"></el-input>
      </el-form-item>
      <el-form-item label="上报时间">
        <el-input v-model="form.reportTime" disabled></el-input>
      </el-form-item>
    </el-form>
    <span slot="footer" class="dialog-footer">
      <el-button @click="dialogVisible = false">取 消</el-button>
      <el-button type="primary" @click="handleSubmit">提 交</el-button>
    </span>
  </el-dialog>
</template>

<script>
import moment from 'moment'

export default {
  name: 'FaultReportDialog',
  props: {
    deviceList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      dialogVisible: false,
      orderCounter: 1,
      form: {
        orderNo: '',
        deviceCode: '',
        faultType: '',
        faultDescription: '',
        contactPerson: '',
        contactPhone: '',
        reportTime: ''
      },
      rules: {
        deviceCode: [
          { required: true, message: '请选择故障设备', trigger: 'change' }
        ],
        faultType: [
          { required: true, message: '请选择故障类型', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请填写故障描述', trigger: 'blur' },
          { min: 10, message: '故障描述长度不能少于10个字符，请详细描述故障情况', trigger: 'blur' },
          { max: 500, message: '故障描述长度不能超过500个字符', trigger: 'blur' }
        ],
        contactPerson: [
          { required: true, message: '请填写联系人姓名', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请填写联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    open(deviceCode = '') {
      this.generateOrderNo()
      this.form.reportTime = moment().format('YYYY-MM-DD HH:mm:ss')
      this.form.deviceCode = deviceCode
      this.form.faultType = ''
      this.form.faultDescription = ''
      this.form.contactPerson = ''
      this.form.contactPhone = ''
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form.clearValidate()
      })
    },
    generateOrderNo() {
      const dateStr = moment().format('YYYYMMDDHHmmss')
      const randomStr = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
      this.form.orderNo = `GD${dateStr}${randomStr}`
    },
    handleClose() {
      this.$refs.form.resetFields()
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$confirm('确认提交该故障工单？提交后将通知维修人员处理。', '提交确认', {
            confirmButtonText: '确认提交',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(() => {
            const submitData = {
              ...this.form
            }
            this.$emit('submit', submitData)
            this.dialogVisible = false
            this.$message.success({
              message: '工单提交成功，维修人员将尽快处理',
              duration: 3000
            })
          }).catch(() => {
          })
        } else {
          this.$message.error('请检查并完善表单信息')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
