<template>
  <el-dialog
    title="故障上报"
    :visible.sync="dialogVisible"
    width="640px"
    :close-on-click-modal="false"
    @closed="handleClosed"
    custom-class="fault-report-modal"
    :before-close="handleBeforeClose"
  >
    <el-alert
      v-if="selectedDeviceInfo.device"
      :title="`设备状态：${selectedDeviceInfo.device.statusText}`"
      :type="selectedDeviceInfo.device.status === 'running' ? 'success' : 'warning'"
      show-icon
      :closable="false"
      style="margin-bottom: 20px"
    >
      <span v-if="selectedDeviceInfo.device.status === 'fault'" style="color: #ff4d4f">
        该设备已标记为故障状态，提交后将更新故障信息
      </span>
      <span v-else>
        确认上报该设备的故障信息
      </span>
    </el-alert>

    <el-form
      ref="faultForm"
      :model="formData"
      :rules="formRules"
      label-width="100px"
      class="fault-form"
    >
      <el-form-item label="选择设备" prop="deviceCode" required>
        <el-select
          v-model="formData.deviceCode"
          placeholder="请选择故障设备"
          style="width: 100%"
          filterable
          :loading="loading"
          clearable
          size="default"
          popper-class="device-select-popper"
          @change="handleDeviceChange"
        >
          <el-option-group
            v-for="group in deviceGroups"
            :key="group.community"
            :label="group.community"
          >
            <el-option
              v-for="device in group.devices"
              :key="device.deviceCode"
              :label="`${device.deviceCode} - ${device.location}`"
              :value="device.deviceCode"
            >
              <div class="device-option">
                <span class="device-option-code">{{ device.deviceCode }}</span>
                <span class="device-option-status">
                  <el-tag :type="getStatusType(device.status)" size="mini">
                    {{ device.statusText }}
                  </el-tag>
                </span>
                <span class="device-option-location">{{ device.location }}</span>
              </div>
            </el-option>
          </el-option-group>
        </el-select>
        <div v-if="deviceError" class="error-tip">
          <i class="el-icon-error"></i>
          {{ deviceError }}
        </div>
      </el-form-item>

      <el-form-item label="所属社区" prop="community">
        <el-input
          v-model="selectedDeviceInfo.community"
          placeholder="选择设备后自动填充"
          disabled
          prefix-icon="el-icon-place"
        ></el-input>
      </el-form-item>

      <el-form-item label="安放点位" prop="location">
        <el-input
          v-model="selectedDeviceInfo.location"
          placeholder="选择设备后自动填充"
          disabled
          prefix-icon="el-icon-location-outline"
        ></el-input>
      </el-form-item>

      <el-form-item label="安装日期">
        <el-input
          v-model="selectedDeviceInfo.installDate"
          placeholder="选择设备后自动填充"
          disabled
          prefix-icon="el-icon-date"
        ></el-input>
      </el-form-item>

      <el-form-item label="故障说明" prop="faultDescription">
        <el-input
          type="textarea"
          v-model="formData.faultDescription"
          :rows="5"
          placeholder="请详细描述故障情况，如：触摸屏无响应、打印机卡纸等"
          maxlength="500"
          show-word-limit
        ></el-input>
      </el-form-item>

      <el-form-item label="紧急程度" prop="urgency">
        <el-radio-group v-model="formData.urgency">
          <el-radio label="low" border>
            <i class="el-icon-info" style="color: #52c41a; margin-right: 4px"></i>
            一般
          </el-radio>
          <el-radio label="medium" border>
            <i class="el-icon-warning" style="color: #fa8c16; margin-right: 4px"></i>
            紧急
          </el-radio>
          <el-radio label="high" border>
            <i class="el-icon-circle-close" style="color: #ff4d4f; margin-right: 4px"></i>
            非常紧急
          </el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="上报人" prop="reporter">
        <el-input
          v-model="formData.reporter"
          placeholder="请输入上报人姓名（可选）"
          maxlength="20"
          prefix-icon="el-icon-user"
        ></el-input>
      </el-form-item>

      <el-form-item label="联系电话" prop="reporterPhone">
        <el-input
          v-model="formData.reporterPhone"
          placeholder="请输入联系电话（可选）"
          maxlength="11"
          prefix-icon="el-icon-phone"
        ></el-input>
      </el-form-item>
    </el-form>

    <div slot="footer" class="dialog-footer">
      <el-button @click="handleCancel">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        <i class="el-icon-check" style="margin-right: 4px"></i>
        提交工单
      </el-button>
    </div>
  </el-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import type { Device } from '@/mock/data'

interface FormData {
  deviceCode: string
  faultDescription: string
  urgency: string
  reporter: string
  reporterPhone: string
}

interface DeviceGroup {
  community: string
  devices: Device[]
}

interface SelectedDeviceInfo {
  community: string
  location: string
  installDate: string
  device: Device | null
}

export default Vue.extend({
  name: 'FaultReportModal',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    selectedDevice: {
      type: Object as () => Device | null,
      default: null
    },
    deviceList: {
      type: Array as () => Device[],
      default: () => []
    }
  },
  data() {
    return {
      loading: false,
      submitting: false,
      deviceError: '',
      formData: {
        deviceCode: '',
        faultDescription: '',
        urgency: 'medium',
        reporter: '',
        reporterPhone: ''
      } as FormData,
      selectedDeviceInfo: {
        community: '',
        location: '',
        installDate: '',
        device: null
      } as SelectedDeviceInfo,
      formRules: {
        deviceCode: [
          { required: true, message: '请选择故障设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请填写故障说明', trigger: 'blur' },
          { min: 10, message: '故障说明至少10个字符', trigger: 'blur' },
          { max: 500, message: '故障说明不超过500个字符', trigger: 'blur' }
        ],
        urgency: [
          { required: true, message: '请选择紧急程度', trigger: 'change' }
        ],
        reporterPhone: [
          { validator: this.validatePhone, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    dialogVisible: {
      get(): boolean {
        return this.visible
      },
      set(val: boolean) {
        this.$emit('update:visible', val)
      }
    },
    deviceGroups(): DeviceGroup[] {
      const communityMap: Record<string, Device[]> = {}
      this.deviceList.forEach(device => {
        if (!communityMap[device.community]) {
          communityMap[device.community] = []
        }
        communityMap[device.community].push(device)
      })
      return Object.entries(communityMap)
        .map(([community, devices]) => ({
          community,
          devices
        }))
        .sort((a, b) => a.community.localeCompare(b.community))
    }
  },
  watch: {
    visible(val: boolean) {
      if (val) {
        this.resetForm()
        if (this.selectedDevice) {
          this.formData.deviceCode = this.selectedDevice.deviceCode
          this.updateDeviceInfo(this.selectedDevice.deviceCode)
        }
      }
    },
    'formData.deviceCode'(val: string) {
      this.deviceError = ''
      this.updateDeviceInfo(val)
    }
  },
  methods: {
    validatePhone(rule: any, value: string, callback: any) {
      if (value && !/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    },
    getStatusType(status: string): string {
      const typeMap: Record<string, string> = {
        running: 'success',
        fault: 'danger',
        offline: 'info',
        maintenance: 'warning'
      }
      return typeMap[status] || 'info'
    },
    updateDeviceInfo(deviceCode: string) {
      const device = this.deviceList.find(d => d.deviceCode === deviceCode)
      if (device) {
        this.selectedDeviceInfo.community = device.community
        this.selectedDeviceInfo.location = device.location
        this.selectedDeviceInfo.installDate = device.installDate
        this.selectedDeviceInfo.device = device
      } else {
        this.selectedDeviceInfo.community = ''
        this.selectedDeviceInfo.location = ''
        this.selectedDeviceInfo.installDate = ''
        this.selectedDeviceInfo.device = null
      }
    },
    handleDeviceChange(val: string) {
      this.deviceError = ''
      if (val) {
        const device = this.deviceList.find(d => d.deviceCode === val)
        if (device && device.status === 'fault') {
          this.$message.warning('该设备当前已处于故障状态')
        }
      }
    },
    resetForm() {
      this.formData = {
        deviceCode: '',
        faultDescription: '',
        urgency: 'medium',
        reporter: '',
        reporterPhone: ''
      }
      this.selectedDeviceInfo = {
        community: '',
        location: '',
        installDate: '',
        device: null
      }
      this.deviceError = ''
      this.$nextTick(() => {
        const form = this.$refs.faultForm as any
        if (form) {
          form.clearValidate()
        }
      })
    },
    handleBeforeClose(done: () => void) {
      if (this.submitting) {
        done()
        return
      }
      if (this.formData.deviceCode || this.formData.faultDescription) {
        this.$confirm('确定要关闭吗？已填写的信息将会丢失。', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          done()
        }).catch(() => {})
      } else {
        done()
      }
    },
    handleCancel() {
      this.handleBeforeClose(() => {
        this.dialogVisible = false
        this.$emit('close')
      })
    },
    validateDeviceSelection(): boolean {
      if (!this.formData.deviceCode) {
        this.deviceError = '请先选择要上报故障的设备'
        return false
      }
      const device = this.deviceList.find(d => d.deviceCode === this.formData.deviceCode)
      if (!device) {
        this.deviceError = '选择的设备不存在，请重新选择'
        return false
      }
      this.deviceError = ''
      return true
    },
    handleSubmit() {
      if (!this.validateDeviceSelection()) {
        this.$message.error(this.deviceError || '请选择故障设备')
        return
      }

      const form = this.$refs.faultForm as any
      form.validate((valid: boolean) => {
        if (!valid) {
          this.$message.error('请完善表单信息')
          return
        }

        if (this.formData.faultDescription.trim().length < 10) {
          this.$message.warning('故障说明至少需要10个字符')
          return
        }

        this.$confirm(`
          <div style="text-align: left;">
            <p><strong>设备编号：</strong>${this.formData.deviceCode}</p>
            <p><strong>所属社区：</strong>${this.selectedDeviceInfo.community}</p>
            <p><strong>安放点位：</strong>${this.selectedDeviceInfo.location}</p>
            <p><strong>紧急程度：</strong>${this.getUrgencyText(this.formData.urgency)}</p>
            <p><strong>故障说明：</strong>${this.formData.faultDescription}</p>
          </div>
        `, '确认提交工单', {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '确认提交',
          cancelButtonText: '返回修改',
          type: 'warning',
          width: '500px'
        }).then(() => {
          this.submitting = true
          setTimeout(() => {
            this.$emit('submit', this.formData.deviceCode, this.formData.faultDescription)
            this.submitting = false
            this.dialogVisible = false
          }, 800)
        }).catch(() => {})
      })
    },
    getUrgencyText(urgency: string): string {
      const map: Record<string, string> = {
        low: '一般',
        medium: '紧急',
        high: '非常紧急'
      }
      return map[urgency] || urgency
    },
    handleClosed() {
      this.resetForm()
    }
  }
})
</script>

<style scoped>
.fault-form {
  padding-right: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.device-option {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
}

.device-option-code {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #1890ff;
  min-width: 140px;
}

.device-option-status {
  flex-shrink: 0;
}

.device-option-location {
  color: #606266;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.error-tip {
  color: #ff4d4f;
  font-size: 12px;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

::v-deep .el-select {
  width: 100%;
}

::v-deep .el-select .el-input__inner {
  height: 40px;
  line-height: 40px;
}

::v-deep .el-select-dropdown__item {
  height: auto;
  padding: 8px 12px;
}

::v-deep .el-select-group__title {
  color: #1890ff;
  font-weight: 600;
  padding: 8px 12px;
}

::v-deep .el-radio-button__inner {
  padding: 8px 15px;
}

::v-deep .fault-report-modal .el-dialog__header {
  background: linear-gradient(90deg, #fff1f0 0%, #fff 100%);
  border-bottom: 1px solid #ffa39e;
  margin-bottom: 20px;
}

::v-deep .fault-report-modal .el-dialog__title {
  color: #ff4d4f;
  font-weight: 600;
}

::v-deep .fault-report-modal .el-dialog__headerbtn .el-dialog__close {
  color: #ff4d4f;
}

::v-deep .el-textarea__inner {
  resize: none;
}

::v-deep .el-input__icon {
  color: #c0c4cc;
}

::v-deep .el-form-item.is-error .el-select .el-input__inner {
  border-color: #ff4d4f;
}
</style>
