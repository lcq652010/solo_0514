<template>
  <div class="app-container">
    <div class="header">
      <h1>档案馆自助查阅打印终端运维管理系统</h1>
    </div>

    <div class="content">
      <div class="toolbar">
        <div class="search-group">
          <input
            type="text"
            v-model="searchDeviceId"
            @input="handleSearch"
            placeholder="设备编号"
            class="search-input"
          />
          <input
            type="text"
            v-model="searchArea"
            @input="handleSearch"
            placeholder="馆区/服务中心名称"
            class="search-input"
          />
          <select v-model="searchStatus" @change="handleSearch" class="search-input">
            <option value="">全部状态</option>
            <option value="normal">正常</option>
            <option value="fault">故障</option>
            <option value="offline">离线</option>
            <option value="maintenance">维护中</option>
          </select>
          <button @click="handleReset" class="btn btn-reset">重置</button>
        </div>
        <button @click="openReportModal" class="btn btn-primary">故障上报</button>
      </div>

      <div class="table-container" :class="{ 'table-loading': isLoading }">
        <div v-if="isLoading" class="loading-overlay">
          <div class="loading-spinner"></div>
          <span>加载中...</span>
        </div>
        <table class="device-table">
          <thead>
            <tr>
              <th>设备编号</th>
              <th>档案馆区</th>
              <th>放置位置</th>
              <th>设备状态</th>
              <th>身份证读卡</th>
              <th>档案打印</th>
              <th>权限校验</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="device in paginatedDevices" 
              :key="device.id"
              :class="getRowClass(device.status)"
            >
              <td>{{ device.deviceId }}</td>
              <td>{{ device.area }}</td>
              <td>{{ device.location }}</td>
              <td>
                <span :class="getStatusClass(device.status)">
                  {{ getStatusText(device.status) }}
                </span>
              </td>
              <td>
                <span :class="getModuleStatusClass(device.modules.idCard)">
                  {{ getModuleStatusText(device.modules.idCard) }}
                </span>
              </td>
              <td>
                <span :class="getModuleStatusClass(device.modules.print)">
                  {{ getModuleStatusText(device.modules.print) }}
                </span>
              </td>
              <td>
                <span :class="getModuleStatusClass(device.modules.permission)">
                  {{ getModuleStatusText(device.modules.permission) }}
                </span>
              </td>
              <td>
                <button @click="openReportModal(device)" class="btn btn-small btn-report">
                  上报故障
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination" v-if="totalPages > 1">
        <button
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1 || isLoading"
          class="page-btn"
        >
          上一页
        </button>
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="changePage(page)"
          :class="{ active: currentPage === page }"
          class="page-btn"
          :disabled="isLoading"
        >
          {{ page }}
        </button>
        <button
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages || isLoading"
          class="page-btn"
        >
          下一页
        </button>
        <span class="page-info">
          共 {{ total }} 条，第 {{ currentPage }} / {{ totalPages }} 页
        </span>
      </div>
    </div>

    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>故障上报</h3>
          <button @click="closeModal" class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>工单编号</label>
            <input type="text" v-model="reportForm.orderId" disabled class="form-input disabled" />
          </div>
          <div class="form-group">
            <label>选择设备 <span class="required">*</span></label>
            <select 
              v-model="reportForm.deviceId" 
              class="form-input"
              :class="{ 'form-input-error': formErrors.deviceId }"
            >
              <option value="">请选择设备</option>
              <option v-for="device in deviceList" :key="device.id" :value="device.deviceId">
                {{ device.deviceId }} - {{ device.area }} - {{ device.location }}
              </option>
            </select>
            <div v-if="formErrors.deviceId" class="error-message">{{ formErrors.deviceId }}</div>
          </div>
          <div class="form-group">
            <label>故障描述 <span class="required">*</span></label>
            <textarea
              v-model="reportForm.description"
              placeholder="请详细描述故障情况..."
              class="form-textarea"
              :class="{ 'form-input-error': formErrors.description }"
              rows="5"
            ></textarea>
            <div v-if="formErrors.description" class="error-message">{{ formErrors.description }}</div>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="btn btn-cancel">取消</button>
          <button @click="submitReport" class="btn btn-submit" :disabled="isSubmitting || !reportForm.deviceId">
            <span v-if="isSubmitting">提交中...</span>
            <span v-else>提交</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="showToast" class="toast" :class="toastType">
      {{ toastMessage }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchDeviceId: '',
      searchArea: '',
      searchStatus: '',
      currentPage: 1,
      pageSize: 10,
      showModal: false,
      showToast: false,
      toastMessage: '',
      toastType: 'success',
      isLoading: false,
      isSubmitting: false,
      formErrors: {
        deviceId: '',
        description: ''
      },
      reportForm: {
        orderId: '',
        deviceId: '',
        description: ''
      },
      deviceList: [
        { id: 1, deviceId: 'DA-2024-001', area: '第一档案馆区', location: '一楼大厅入口处', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 2, deviceId: 'DA-2024-002', area: '第一档案馆区', location: '二楼阅览室', status: 'fault', modules: { idCard: 'fault', print: 'normal', permission: 'normal' } },
        { id: 3, deviceId: 'DA-2024-003', area: '第二档案馆区', location: '一楼服务台旁', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 4, deviceId: 'DA-2024-004', area: '第二档案馆区', location: '三楼查阅室', status: 'offline', modules: { idCard: 'offline', print: 'offline', permission: 'offline' } },
        { id: 5, deviceId: 'DA-2024-005', area: '第三档案馆区', location: '二楼大厅', status: 'maintenance', modules: { idCard: 'maintenance', print: 'maintenance', permission: 'maintenance' } },
        { id: 6, deviceId: 'DA-2024-006', area: '第三档案馆区', location: '四楼档案库', status: 'normal', modules: { idCard: 'normal', print: 'fault', permission: 'normal' } },
        { id: 7, deviceId: 'DA-2024-007', area: '第一档案馆区', location: '地下一层库房', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 8, deviceId: 'DA-2024-008', area: '第二档案馆区', location: '五楼会议室', status: 'fault', modules: { idCard: 'normal', print: 'fault', permission: 'normal' } },
        { id: 9, deviceId: 'DA-2024-009', area: '第三档案馆区', location: '一楼展厅', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 10, deviceId: 'DA-2024-010', area: '第一档案馆区', location: '二楼休息区', status: 'offline', modules: { idCard: 'offline', print: 'offline', permission: 'offline' } },
        { id: 11, deviceId: 'DA-2024-011', area: '第二档案馆区', location: '六楼办公室', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 12, deviceId: 'DA-2024-012', area: '第三档案馆区', location: '七楼多功能厅', status: 'maintenance', modules: { idCard: 'maintenance', print: 'maintenance', permission: 'maintenance' } },
        { id: 13, deviceId: 'DA-2024-013', area: '第一档案馆区', location: '八楼培训室', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 14, deviceId: 'DA-2024-014', area: '第二档案馆区', location: '九楼机房', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'fault' } },
        { id: 15, deviceId: 'DA-2024-015', area: '第三档案馆区', location: '十楼档案室', status: 'fault', modules: { idCard: 'fault', print: 'fault', permission: 'normal' } },
        { id: 16, deviceId: 'DA-2024-016', area: '第一档案馆区', location: '东门入口', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 17, deviceId: 'DA-2024-017', area: '第二档案馆区', location: '西门服务点', status: 'offline', modules: { idCard: 'offline', print: 'offline', permission: 'offline' } },
        { id: 18, deviceId: 'DA-2024-018', area: '第三档案馆区', location: '北门接待处', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 19, deviceId: 'DA-2024-019', area: '第一档案馆区', location: '南门值班室', status: 'normal', modules: { idCard: 'normal', print: 'normal', permission: 'normal' } },
        { id: 20, deviceId: 'DA-2024-020', area: '第二档案馆区', location: '中心广场', status: 'maintenance', modules: { idCard: 'maintenance', print: 'maintenance', permission: 'maintenance' } }
      ],
      displayDevices: []
    }
  },
  computed: {
    filteredDevices() {
      return this.deviceList.filter(device => {
        const matchDeviceId = device.deviceId.toLowerCase().includes(this.searchDeviceId.toLowerCase())
        const matchArea = device.area.toLowerCase().includes(this.searchArea.toLowerCase())
        const matchStatus = this.searchStatus === '' || device.status === this.searchStatus
        return matchDeviceId && matchArea && matchStatus
      })
    },
    total() {
      return this.filteredDevices.length
    },
    totalPages() {
      return Math.ceil(this.total / this.pageSize)
    },
    paginatedDevices() {
      return this.displayDevices
    },
    visiblePages() {
      const pages = []
      const maxVisible = 5
      let start = Math.max(1, this.currentPage - Math.floor(maxVisible / 2))
      const end = Math.min(this.totalPages, start + maxVisible - 1)
      
      if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1)
      }
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      return pages
    }
  },
  watch: {
    currentPage: {
      handler() {
        this.loadPageData()
      }
    },
    filteredDevices: {
      handler() {
        this.loadPageData()
      },
      deep: true
    }
  },
  mounted() {
    this.loadPageData()
  },
  methods: {
    getStatusClass(status) {
      const statusMap = {
        normal: 'status-normal',
        fault: 'status-fault',
        offline: 'status-offline',
        maintenance: 'status-maintenance'
      }
      return `status ${statusMap[status] || ''}`
    },
    getStatusText(status) {
      const statusMap = {
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintenance: '维护中'
      }
      return statusMap[status] || status
    },
    getModuleStatusClass(status) {
      const statusMap = {
        normal: 'module-status module-normal',
        fault: 'module-status module-fault',
        offline: 'module-status module-offline',
        maintenance: 'module-status module-maintenance'
      }
      return statusMap[status] || 'module-status module-normal'
    },
    getModuleStatusText(status) {
      const statusMap = {
        normal: '正常',
        fault: '故障',
        offline: '离线',
        maintenance: '维护'
      }
      return statusMap[status] || status
    },
    getRowClass(status) {
      if (status === 'fault') {
        return 'row-fault-highlight'
      }
      if (status === 'offline') {
        return 'row-offline-highlight'
      }
      return ''
    },
    loadPageData() {
      this.isLoading = true
      setTimeout(() => {
        const start = (this.currentPage - 1) * this.pageSize
        const end = start + this.pageSize
        this.displayDevices = this.filteredDevices.slice(start, end)
        this.isLoading = false
      }, 300)
    },
    handleSearch() {
      this.currentPage = 1
    },
    handleReset() {
      this.searchDeviceId = ''
      this.searchArea = ''
      this.searchStatus = ''
      this.currentPage = 1
    },
    changePage(page) {
      if (page >= 1 && page <= this.totalPages && !this.isLoading) {
        this.currentPage = page
      }
    },
    generateOrderId() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const random = Math.floor(Math.random() * 10000).toString().padStart(4, '0')
      return `GD${year}${month}${day}${random}`
    },
    openReportModal(device = null) {
      this.formErrors = {
        deviceId: '',
        description: ''
      }
      this.reportForm = {
        orderId: this.generateOrderId(),
        deviceId: device ? device.deviceId : '',
        description: ''
      }
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
      this.formErrors = {
        deviceId: '',
        description: ''
      }
    },
    validateForm() {
      let isValid = true
      this.formErrors = {
        deviceId: '',
        description: ''
      }
      
      if (!this.reportForm.deviceId) {
        this.formErrors.deviceId = '请选择设备'
        isValid = false
      }
      
      if (!this.reportForm.description.trim()) {
        this.formErrors.description = '请填写故障描述'
        isValid = false
      } else if (this.reportForm.description.trim().length < 5) {
        this.formErrors.description = '故障描述至少5个字符'
        isValid = false
      }
      
      return isValid
    },
    submitReport() {
      if (!this.validateForm()) {
        this.showToastMessage('请完善表单信息', 'error')
        return
      }
      
      this.isSubmitting = true
      setTimeout(() => {
        console.log('提交故障上报:', this.reportForm)
        this.showToastMessage('故障上报成功！', 'success')
        this.isSubmitting = false
        this.closeModal()
      }, 1000)
    },
    showToastMessage(message, type = 'success') {
      this.toastMessage = message
      this.toastType = type
      this.showToast = true
      setTimeout(() => {
        this.showToast = false
      }, 3000)
    }
  }
}
</script>
