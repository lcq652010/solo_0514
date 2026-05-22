<template>
  <div class="device-list">
    <div class="page-header">
      <div class="page-title">设备管理</div>
      <div class="page-desc">管理和监控所有自助证明打印终端设备的运行状态</div>
    </div>

    <div class="card-container">
      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="输入设备编号、机构名称或摆放区域智能搜索"
          clearable
          style="width: 320px"
          prefix-icon="el-icon-search"
          @keyup.enter.native="handleSearch"
        >
          <el-button
            slot="append"
            icon="el-icon-search"
            type="primary"
            @click="handleSearch"
          >搜索</el-button>
        </el-input>
        <el-select
          v-model="searchForm.status"
          placeholder="运行状态"
          clearable
          style="width: 140px"
          @change="handleSearch"
        >
          <el-option label="在线" value="online" />
          <el-option label="离线" value="offline" />
          <el-option label="故障" value="fault" />
        </el-select>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        <el-button
          type="danger"
          icon="el-icon-warning"
          style="margin-left: auto"
          @click="openFaultReport"
        >
          故障提报
        </el-button>
      </div>

      <div class="table-wrapper">
        <el-table
          :data="tableData"
          border
          stripe
          style="width: 100%"
          v-loading="loading"
          :row-class-name="tableRowClassName"
          highlight-current-row
        >
          <el-table-column
            prop="deviceNo"
            label="设备编号"
            width="140"
            align="center"
          />
          <el-table-column
            prop="organization"
            label="人才服务中心"
            min-width="180"
            show-overflow-tooltip
          />
          <el-table-column
            prop="location"
            label="摆放区域"
            width="140"
            align="center"
          />
          <el-table-column
            prop="status"
            label="运行状态"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" effect="light">
                <span class="status-tag">
                  <span :class="['status-dot', scope.row.status]"></span>
                  {{ getStatusText(scope.row.status) }}
                </span>
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="身份核验"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.identityVerifyStatus)" size="small" effect="plain">
                {{ getModuleStatusText(scope.row.identityVerifyStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="证明打印"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.printStatus)" size="small" effect="plain">
                {{ getModuleStatusText(scope.row.printStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            label="联网查询"
            width="110"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag :type="getModuleStatusType(scope.row.networkQueryStatus)" size="small" effect="plain">
                {{ getModuleStatusText(scope.row.networkQueryStatus) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column
            prop="lastOnlineTime"
            label="最后在线时间"
            width="170"
            align="center"
          >
            <template slot-scope="scope">
              {{ formatDate(scope.row.lastOnlineTime) }}
            </template>
          </el-table-column>
          <el-table-column
            label="操作"
            width="100"
            align="center"
            fixed="right"
          >
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                icon="el-icon-warning"
                @click="openFaultReport(scope.row)"
              >
                故障提报
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size.sync="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
          background
        />
      </div>
    </div>

    <el-dialog
      title="故障提报"
      :visible.sync="dialogVisible"
      width="560px"
      :close-on-click-modal="false"
      @close="handleDialogClose"
    >
      <el-form
        ref="faultForm"
        :model="faultForm"
        :rules="faultRules"
        label-width="100px"
      >
        <el-form-item label="工单编号">
          <el-input v-model="faultForm.workOrderNo" disabled />
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select
            v-model="faultForm.deviceId"
            placeholder="请选择故障设备（支持搜索）"
            filterable
            clearable
            style="width: 100%"
            @change="handleDeviceChange"
            size="medium"
          >
            <el-option
              v-for="device in allDevices"
              :key="device.id"
              :label="`${device.deviceNo} | ${device.organization} | ${device.location}`"
              :value="device.id"
            >
              <span style="float: left;">{{ device.deviceNo }}</span>
              <span style="float: right; color: #8492a6; font-size: 12px;">
                <el-tag :type="getStatusType(device.status)" size="mini" effect="plain">
                  {{ getStatusText(device.status) }}
                </el-tag>
              </span>
              <div style="clear: both; font-size: 12px; color: #606266; margin-top: 4px;">
                {{ device.organization }} - {{ device.location }}
              </div>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="设备编号" v-if="selectedDevice">
          <el-input v-model="selectedDevice.deviceNo" disabled />
        </el-form-item>
        <el-form-item label="所属机构" v-if="selectedDevice">
          <el-input v-model="selectedDevice.organization" disabled />
        </el-form-item>
        <el-form-item label="摆放区域" v-if="selectedDevice">
          <el-input v-model="selectedDevice.location" disabled />
        </el-form-item>
        <el-form-item label="问题详情" prop="problemDesc">
          <el-input
            v-model="faultForm.problemDesc"
            type="textarea"
            :rows="4"
            placeholder="请详细描述故障现象（至少10个字）"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleSubmit">
          提交工单
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import devices from '@/mock/device.js'
import workOrders from '@/mock/workOrder.js'
import {
  generateWorkOrderNo,
  formatDate,
  getStatusText,
  getStatusType,
  getModuleStatusText,
  getModuleStatusType
} from '@/utils/index.js'

export default {
  name: 'DeviceList',
  data() {
    return {
      loading: false,
      searchForm: {
        keyword: '',
        status: ''
      },
      allDevices: [],
      filteredDevices: [],
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      submitting: false,
      faultForm: {
        workOrderNo: '',
        deviceId: '',
        problemDesc: ''
      },
      faultRules: {
        deviceId: [
          { required: true, message: '请选择故障设备', trigger: 'change' }
        ],
        problemDesc: [
          { required: true, message: '请填写问题详情', trigger: 'blur' },
          { min: 10, message: '问题描述至少10个字', trigger: 'blur' }
        ]
      },
      selectedDevice: null,
      workOrderList: []
    }
  },
  watch: {
    'pagination.currentPage': function() {
      this.loadTableData()
    },
    'pagination.pageSize': function() {
      this.pagination.currentPage = 1
      this.loadTableData()
    }
  },
  created() {
    this.allDevices = [...devices]
    this.workOrderList = [...workOrders]
    this.filteredDevices = [...this.allDevices]
    this.pagination.total = this.filteredDevices.length
    this.loadTableData()
  },
  methods: {
    formatDate,
    getStatusText,
    getStatusType,
    getModuleStatusText,
    getModuleStatusType,
    tableRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row'
      } else if (row.status === 'offline') {
        return 'offline-row'
      }
      return ''
    },
    loadTableData() {
      const { currentPage, pageSize } = this.pagination
      const start = (currentPage - 1) * pageSize
      const end = start + pageSize
      this.tableData = this.filteredDevices.slice(start, end)
    },
    handleSearch() {
      this.loading = true
      setTimeout(() => {
        const { keyword, status } = this.searchForm
        this.filteredDevices = this.allDevices.filter(item => {
          let matchKeyword = true
          let matchStatus = true
          
          if (keyword) {
            const lowerKeyword = keyword.toLowerCase()
            const matchDeviceNo = item.deviceNo.toLowerCase().includes(lowerKeyword)
            const matchOrg = item.organization.toLowerCase().includes(lowerKeyword)
            const matchLocation = item.location.toLowerCase().includes(lowerKeyword)
            const matchStatusText = this.getStatusText(item.status).includes(keyword)
            matchKeyword = matchDeviceNo || matchOrg || matchLocation || matchStatusText
          }
          
          if (status) {
            matchStatus = item.status === status
          }
          
          return matchKeyword && matchStatus
        })
        this.pagination.total = this.filteredDevices.length
        this.pagination.currentPage = 1
        this.loadTableData()
        this.loading = false
      }, 200)
    },
    handleReset() {
      this.searchForm = {
        keyword: '',
        status: ''
      }
      this.handleSearch()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    openFaultReport(device) {
      this.faultForm.workOrderNo = generateWorkOrderNo()
      this.faultForm.problemDesc = ''
      this.selectedDevice = null

      if (device) {
        this.faultForm.deviceId = device.id
        this.selectedDevice = { ...device }
      } else {
        this.faultForm.deviceId = ''
      }

      this.dialogVisible = true
      this.$nextTick(() => {
        if (this.$refs.faultForm) {
          this.$refs.faultForm.clearValidate()
        }
      })
    },
    handleDeviceChange(deviceId) {
      this.selectedDevice = this.allDevices.find(d => d.id === deviceId) || null
    },
    handleDialogClose() {
      this.selectedDevice = null
    },
    handleSubmit() {
      if (!this.faultForm.deviceId) {
        this.$message.warning('请先选择故障设备')
        return
      }
      
      this.$refs.faultForm.validate(valid => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const newWorkOrder = {
              id: `WO${String(this.workOrderList.length + 1).padStart(3, '0')}`,
              workOrderNo: this.faultForm.workOrderNo,
              deviceId: this.selectedDevice.id,
              deviceNo: this.selectedDevice.deviceNo,
              organization: this.selectedDevice.organization,
              problemDesc: this.faultForm.problemDesc,
              status: 'pending',
              createTime: new Date().toISOString(),
              updateTime: new Date().toISOString()
            }
            this.workOrderList.unshift(newWorkOrder)
            
            const deviceIndex = this.allDevices.findIndex(d => d.id === this.selectedDevice.id)
            if (deviceIndex !== -1) {
              this.allDevices[deviceIndex].status = 'fault'
              this.allDevices[deviceIndex].identityVerifyStatus = 'error'
              this.allDevices[deviceIndex].printStatus = 'error'
              this.allDevices[deviceIndex].networkQueryStatus = 'error'
              this.handleSearch()
            }
            
            this.$message.success('工单提交成功！设备状态已更新')
            this.dialogVisible = false
            this.submitting = false
          }, 800)
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.device-list {
  ::v-deep .el-input__prefix {
    color: #8c8c8c;
  }

  ::v-deep .el-table th {
    background-color: #fafafa;
    color: #262626;
    font-weight: 600;
  }

  ::v-deep .el-table__row:hover > td {
    background-color: #f5faff;
  }

  ::v-deep .el-table .fault-row {
    background-color: #fff1f0 !important;

    &:hover > td {
      background-color: #ffccc7 !important;
    }

    td {
      background-color: #fff1f0 !important;
    }
  }

  ::v-deep .el-table .offline-row {
    background-color: #fff7e6 !important;

    &:hover > td {
      background-color: #ffd591 !important;
    }

    td {
      background-color: #fff7e6 !important;
    }
  }

  ::v-deep .el-tag {
    border: none;
    padding: 0 10px;
  }

  ::v-deep .el-select-dropdown__item {
    height: auto;
    padding: 8px 12px;
    line-height: 1.4;
  }
}
</style>
