<template>
  <el-dialog
    title="故障上报"
    :visible.sync="dialogVisible"
    width="600px"
    :close-on-click-modal="false"
    @close="handleClose"
  >
    <el-form
      ref="faultForm"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      class="fault-form"
    >
      <el-form-item label="工单编号">
        <el-input v-model="formData.workOrderNo" disabled></el-input>
      </el-form-item>

      <el-form-item label="故障设备" prop="selectedDevices" required>
        <div class="device-selector">
          <el-tag
            v-for="device in selectedDevices"
            :key="device.id"
            type="info"
            class="device-tag"
            closable
            @close="removeDevice(device)"
          >
            {{ device.deviceCode }} - {{ device.hallName }}
          </el-tag>
          <el-button
            type="primary"
            size="small"
            icon="el-icon-plus"
            @click="openDeviceSelect"
            class="add-device-btn"
          >
            选择设备
          </el-button>
        </div>
        <div v-if="selectedDevices.length === 0" class="error-tip">
          请至少选择一个故障设备
        </div>
      </el-form-item>

      <el-form-item label="故障类型" prop="faultType">
        <el-select v-model="formData.faultType" placeholder="请选择故障类型" style="width: 100%">
          <el-option label="硬件故障" value="hardware"></el-option>
          <el-option label="软件故障" value="software"></el-option>
          <el-option label="网络故障" value="network"></el-option>
          <el-option label="打印机故障" value="printer"></el-option>
          <el-option label="触摸屏故障" value="touchscreen"></el-option>
          <el-option label="其他故障" value="other"></el-option>
        </el-select>
      </el-form-item>

      <el-form-item label="故障详情" prop="faultDetail">
        <el-input
          v-model="formData.faultDetail"
          type="textarea"
          :rows="4"
          placeholder="请详细描述故障情况，以便运维人员快速定位问题"
          maxlength="500"
          show-word-limit
        ></el-input>
      </el-form-item>

      <el-form-item label="上报人">
        <el-input v-model="formData.reporter" placeholder="请输入上报人姓名"></el-input>
      </el-form-item>

      <el-form-item label="联系电话" prop="contactPhone">
        <el-input v-model="formData.contactPhone" placeholder="请输入联系电话"></el-input>
      </el-form-item>

      <el-form-item label="备注">
        <el-input
          v-model="formData.remark"
          type="textarea"
          :rows="2"
          placeholder="其他需要说明的信息"
        ></el-input>
      </el-form-item>
    </el-form>

    <div slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitting">
        提交工单
      </el-button>
    </div>

    <el-dialog
      title="选择故障设备"
      :visible.sync="deviceSelectVisible"
      width="800px"
      :close-on-click-modal="false"
    >
      <div class="device-search-bar">
        <el-input
          v-model="deviceSearchKeyword"
          placeholder="搜索设备编号、营业厅或安装点位"
          clearable
          class="search-input"
        >
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-select v-model="statusFilter" placeholder="按状态筛选" clearable class="status-filter">
          <el-option label="全部" value=""></el-option>
          <el-option label="正常运行" value="normal"></el-option>
          <el-option label="故障" value="fault"></el-option>
          <el-option label="离线" value="offline"></el-option>
          <el-option label="维护中" value="maintenance"></el-option>
        </el-select>
      </div>
      <div class="selected-count">
        已选择 <span class="count">{{ tempSelectedDevices.length }}</span> 台设备
      </div>
      <el-table
        ref="deviceTable"
        :data="filteredDeviceList"
        border
        height="350"
        @selection-change="handleDeviceSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="deviceCode" label="设备编号" width="130" align="center"></el-table-column>
        <el-table-column prop="hallName" label="供电营业厅" min-width="140" align="center"></el-table-column>
        <el-table-column prop="installLocation" label="安装点位" min-width="140" align="center"></el-table-column>
        <el-table-column prop="status" label="设备状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="deviceSelectVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmDeviceSelect" :disabled="tempSelectedDevices.length === 0">
          确定选择 ({{ tempSelectedDevices.length }})
        </el-button>
      </div>
    </el-dialog>
  </el-dialog>
</template>

<script>
export default {
  name: 'FaultReportDialog',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    selectedDevices: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      dialogVisible: false,
      submitting: false,
      deviceSelectVisible: false,
      deviceSearchKeyword: '',
      statusFilter: '',
      tempSelectedDevices: [],
      allDeviceList: [],
      formData: {
        workOrderNo: '',
        faultType: '',
        faultDetail: '',
        reporter: '',
        contactPhone: '',
        remark: ''
      },
      formRules: {
        faultType: [
          { required: true, message: '请选择故障类型', trigger: 'change' }
        ],
        faultDetail: [
          { required: true, message: '请输入故障详情', trigger: 'blur' },
          { min: 10, message: '故障详情至少10个字符', trigger: 'blur' }
        ],
        reporter: [
          { required: true, message: '请输入上报人姓名', trigger: 'blur' }
        ],
        contactPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          {
            pattern: /^1[3-9]\d{9}$|^0\d{2,3}-?\d{7,8}$/,
            message: '请输入正确的手机号码或固定电话',
            trigger: 'blur'
          }
        ]
      }
    }
  },
  watch: {
    visible: {
      handler(val) {
        this.dialogVisible = val
        if (val) {
          this.initForm()
        }
      },
      immediate: true
    },
    dialogVisible(val) {
      this.$emit('update:visible', val)
    }
  },
  computed: {
    filteredDeviceList() {
      let list = [...this.allDeviceList]
      
      if (this.deviceSearchKeyword) {
        const keyword = this.deviceSearchKeyword.toLowerCase().trim()
        list = list.filter(item =>
          item.deviceCode.toLowerCase().includes(keyword) ||
          item.hallName.includes(keyword) ||
          item.installLocation.includes(keyword)
        )
      }
      
      if (this.statusFilter) {
        list = list.filter(item => item.status === this.statusFilter)
      }
      
      return list
    }
  },
  methods: {
    initForm() {
      this.generateWorkOrderNo()
      this.initDeviceList()
      this.formData = {
        workOrderNo: this.formData.workOrderNo,
        faultType: '',
        faultDetail: '',
        reporter: '',
        contactPhone: '',
        remark: ''
      }
      this.$nextTick(() => {
        if (this.$refs.faultForm) {
          this.$refs.faultForm.clearValidate()
        }
      })
    },
    generateWorkOrderNo() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0')
      this.formData.workOrderNo = `WO${year}${month}${day}${hours}${minutes}${seconds}${random}`
    },
    initDeviceList() {
      const halls = [
        '朝阳供电营业厅', '海淀供电营业厅', '东城供电营业厅',
        '西城供电营业厅', '丰台供电营业厅', '石景山供电营业厅',
        '通州供电营业厅', '顺义供电营业厅', '昌平供电营业厅',
        '大兴供电营业厅'
      ]
      const locations = [
        '一楼大厅入口处', '二楼服务区左侧', '营业厅正门右侧',
        '自助服务区A区', '自助服务区B区', '缴费窗口旁',
        '客户休息区旁', '营业厅后门入口', '停车场入口处',
        '营业厅中心区域'
      ]
      const statuses = ['normal', 'normal', 'normal', 'fault', 'offline', 'maintenance']
      const moduleStatuses = ['normal', 'normal', 'normal', 'normal', 'warning', 'error']

      this.allDeviceList = []
      for (let i = 1; i <= 86; i++) {
        this.allDeviceList.push({
          id: i,
          deviceCode: `PWR-${String(i).padStart(5, '0')}`,
          hallName: halls[Math.floor(Math.random() * halls.length)],
          installLocation: locations[Math.floor(Math.random() * locations.length)],
          status: statuses[Math.floor(Math.random() * statuses.length)],
          cardReader: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          printer: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
          network: moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)]
        })
      }
    },
    getStatusTagType(status) {
      const typeMap = {
        normal: 'success',
        fault: 'danger',
        offline: 'info',
        maintenance: 'warning'
      }
      return typeMap[status] || 'info'
    },
    getStatusText(status) {
      const textMap = {
        normal: '正常运行',
        fault: '故障',
        offline: '离线',
        maintenance: '维护中'
      }
      return textMap[status] || '未知'
    },
    openDeviceSelect() {
      this.deviceSearchKeyword = ''
      this.statusFilter = ''
      this.tempSelectedDevices = [...this.selectedDevices]
      this.deviceSelectVisible = true
      this.$nextTick(() => {
        if (this.$refs.deviceTable) {
          this.$refs.deviceTable.clearSelection()
          this.tempSelectedDevices.forEach(device => {
            const row = this.allDeviceList.find(d => d.id === device.id)
            if (row) {
              this.$refs.deviceTable.toggleRowSelection(row, true)
            }
          })
        }
      })
    },
    handleDeviceSelectionChange(selection) {
      this.tempSelectedDevices = selection
    },
    confirmDeviceSelect() {
      this.$emit('update:selectedDevices', this.tempSelectedDevices)
      this.deviceSelectVisible = false
    },
    removeDevice(device) {
      const newDevices = this.selectedDevices.filter(d => d.id !== device.id)
      this.$emit('update:selectedDevices', newDevices)
    },
    handleSubmit() {
      if (this.selectedDevices.length === 0) {
        this.$message.warning('请至少选择一个故障设备')
        return
      }
      
      this.$refs.faultForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const submitData = {
              ...this.formData,
              devices: this.selectedDevices,
              reportTime: new Date().toISOString()
            }
            this.$emit('submit', submitData)
            this.submitting = false
          }, 800)
        } else {
          this.$message.error('请完善表单必填项')
        }
      })
    },
    handleClose() {
      this.dialogVisible = false
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.fault-form .device-selector {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  min-height: 32px;
}
.fault-form .device-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}
.fault-form .add-device-btn {
  margin-bottom: 8px;
}
.fault-form .error-tip {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
}
.fault-form >>> .el-textarea__inner {
  resize: none;
}
.device-search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 15px;
}
.device-search-bar .search-input {
  flex: 1;
}
.device-search-bar .status-filter {
  width: 150px;
}
.selected-count {
  margin-bottom: 10px;
  font-size: 14px;
  color: #606266;
}
.selected-count .count {
  color: #409eff;
  font-weight: bold;
}
.dialog-footer {
  text-align: right;
}
</style>
