<template>
  <div class="device-table">
    <el-table
      :data="tableData"
      border
      stripe
      style="width: 100%"
      v-loading="loading"
      :row-class-name="getRowClassName"
    >
      <el-table-column
        prop="deviceCode"
        label="设备编号"
        width="150"
        align="center"
      />
      <el-table-column
        prop="branchName"
        label="分馆位置"
        align="center"
      />
      <el-table-column
        prop="floor"
        label="部署楼层"
        width="120"
        align="center"
      />
      <el-table-column
        prop="status"
        label="运行状态"
        width="120"
        align="center"
      >
        <template slot-scope="scope">
          <el-tag
            :type="getStatusType(scope.row.status)"
            effect="light"
            size="small"
          >
            {{ getStatusText(scope.row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="模块状态"
        align="center"
      >
        <el-table-column
          prop="modules.idRecognition"
          label="身份识别"
          width="110"
          align="center"
        >
          <template slot-scope="scope">
            <el-tooltip
              :content="getModuleStatusText(scope.row.modules?.idRecognition)"
              placement="top"
            >
              <i
                :class="getModuleStatusIcon(scope.row.modules?.idRecognition)"
                :style="{ color: getModuleStatusColor(scope.row.modules?.idRecognition), fontSize: '18px' }"
              ></i>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          prop="modules.ebookDownload"
          label="电子下载"
          width="110"
          align="center"
        >
          <template slot-scope="scope">
            <el-tooltip
              :content="getModuleStatusText(scope.row.modules?.ebookDownload)"
              placement="top"
            >
              <i
                :class="getModuleStatusIcon(scope.row.modules?.ebookDownload)"
                :style="{ color: getModuleStatusColor(scope.row.modules?.ebookDownload), fontSize: '18px' }"
              ></i>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          prop="modules.printOutput"
          label="打印输出"
          width="110"
          align="center"
        >
          <template slot-scope="scope">
            <el-tooltip
              :content="getModuleStatusText(scope.row.modules?.printOutput)"
              placement="top"
            >
              <i
                :class="getModuleStatusIcon(scope.row.modules?.printOutput)"
                :style="{ color: getModuleStatusColor(scope.row.modules?.printOutput), fontSize: '18px' }"
              ></i>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          prop="modules.networkComm"
          label="网络通信"
          width="110"
          align="center"
        >
          <template slot-scope="scope">
            <el-tooltip
              :content="getModuleStatusText(scope.row.modules?.networkComm)"
              placement="top"
            >
              <i
                :class="getModuleStatusIcon(scope.row.modules?.networkComm)"
                :style="{ color: getModuleStatusColor(scope.row.modules?.networkComm), fontSize: '18px' }"
              ></i>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table-column>
      <el-table-column
        prop="lastHeartbeat"
        label="最后心跳"
        width="180"
        align="center"
      />
      <el-table-column
        label="操作"
        width="120"
        align="center"
        fixed="right"
      >
        <template slot-scope="scope">
          <el-button
            type="danger"
            size="mini"
            icon="el-icon-warning"
            @click="handleRepair(scope.row)"
          >
            报修
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-wrapper">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 30, 50]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'DeviceTable',
  props: {
    data: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentPage: 1,
      pageSize: 10
    }
  },
  watch: {
    data: {
      immediate: true,
      handler(newVal, oldVal) {
        if (newVal && oldVal && newVal.length !== oldVal.length) {
          this.currentPage = 1
        }
      }
    },
    currentPage: {
      handler(newVal) {
        this.$emit('page-change', newVal, this.pageSize)
      }
    },
    pageSize: {
      handler(newVal) {
        this.currentPage = 1
        this.$emit('page-change', 1, newVal)
      }
    }
  },
  computed: {
    tableData() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.data.slice(start, end)
    },
    total() {
      return this.data.length
    }
  },
  methods: {
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'row-fault'
      } else if (row.status === 'offline') {
        return 'row-offline'
      }
      return ''
    },
    getStatusType(status) {
      const typeMap = {
        online: 'success',
        offline: 'info',
        fault: 'danger',
        maintaining: 'warning'
      }
      return typeMap[status] || 'info'
    },
    getStatusText(status) {
      const textMap = {
        online: '在线',
        offline: '离线',
        fault: '故障',
        maintaining: '维护中'
      }
      return textMap[status] || '未知'
    },
    getModuleStatusIcon(status) {
      const iconMap = {
        normal: 'el-icon-circle-check',
        warning: 'el-icon-question',
        error: 'el-icon-circle-close'
      }
      return iconMap[status] || 'el-icon-remove'
    },
    getModuleStatusColor(status) {
      const colorMap = {
        normal: '#67c23a',
        warning: '#e6a23c',
        error: '#f56c6c'
      }
      return colorMap[status] || '#909399'
    },
    getModuleStatusText(status) {
      const textMap = {
        normal: '正常',
        warning: '警告',
        error: '异常'
      }
      return textMap[status] || '未知'
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    handleRepair(row) {
      this.$emit('repair', row)
    }
  }
}
</script>

<style lang="scss">
.device-table {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  
  .pagination-wrapper {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
  
  ::v-deep .el-table .row-fault {
    background-color: #fff1f0 !important;
    
    &:hover > td {
      background-color: #fff1f0 !important;
    }
  }
  
  ::v-deep .el-table .row-offline {
    background-color: #f5f5f5 !important;
    
    &:hover > td {
      background-color: #f5f5f5 !important;
    }
  }
  
  ::v-deep .el-table--striped .el-table__body tr.row-fault td.el-table__cell {
    background-color: #fff1f0 !important;
  }
  
  ::v-deep .el-table--striped .el-table__body tr.row-offline td.el-table__cell {
    background-color: #f5f5f5 !important;
  }
}
</style>
