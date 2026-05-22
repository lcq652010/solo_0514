<template>
  <div class="records-page">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="业务类型">
          <el-select v-model="searchForm.type" placeholder="全部类型" clearable>
            <el-option label="综合业务" value="综合业务"></el-option>
            <el-option label="户政业务" value="户政业务"></el-option>
            <el-option label="社保业务" value="社保业务"></el-option>
            <el-option label="不动产" value="不动产"></el-option>
            <el-option label="市场监管" value="市场监管"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="办理状态">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable>
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="办理中" value="办理中"></el-option>
            <el-option label="待办理" value="待办理"></el-option>
            <el-option label="已取消" value="已取消"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期">
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
          <el-button type="success" icon="el-icon-download" @click="handleExport">导出</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <div class="stat-card total">
          <div class="stat-icon"><i class="el-icon-document"></i></div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.total }}</div>
            <div class="stat-label">总记录数</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card completed">
          <div class="stat-icon"><i class="el-icon-success"></i></div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.completed }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card processing">
          <div class="stat-icon"><i class="el-icon-loading"></i></div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.processing }}</div>
            <div class="stat-label">办理中</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card pending">
          <div class="stat-icon"><i class="el-icon-time"></i></div>
          <div class="stat-content">
            <div class="stat-number">{{ stats.pending }}</div>
            <div class="stat-label">待办理</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-card class="table-card">
      <div slot="header" class="card-header">
        <span>办事记录列表</span>
      </div>

      <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="ticketNumber" label="排队号" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="primary" size="small">{{ scope.row.ticketNumber }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="businessType" label="业务类型" width="120" align="center"></el-table-column>
        <el-table-column prop="applicant" label="申请人" width="120" align="center"></el-table-column>
        <el-table-column prop="idCard" label="身份证号" width="180" align="center"></el-table-column>
        <el-table-column prop="window" label="办理窗口" width="120" align="center"></el-table-column>
        <el-table-column prop="applyTime" label="申请时间" width="160" align="center"></el-table-column>
        <el-table-column prop="handleTime" label="办理时间" width="160" align="center">
          <template slot-scope="scope">
            {{ scope.row.handleTime || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" icon="el-icon-view" @click="handleView(scope.row)">
              详情
            </el-button>
            <el-button type="warning" size="mini" icon="el-icon-delete" @click="handleCancel(scope.row)" v-if="scope.row.status === '待办理'">
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog
      title="办事详情"
      :visible.sync="detailDialogVisible"
      width="600px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="排队号">{{ currentRecord.ticketNumber }}</el-descriptions-item>
        <el-descriptions-item label="业务类型">{{ currentRecord.businessType }}</el-descriptions-item>
        <el-descriptions-item label="申请人">{{ currentRecord.applicant }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentRecord.idCard }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRecord.phone }}</el-descriptions-item>
        <el-descriptions-item label="办理窗口">{{ currentRecord.window }}</el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ currentRecord.applyTime }}</el-descriptions-item>
        <el-descriptions-item label="办理时间">{{ currentRecord.handleTime || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentRecord.status)" size="small">
            {{ currentRecord.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="办理人员">{{ currentRecord.handler || '-' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRecord.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" v-if="currentRecord && currentRecord.status === '已完成'" @click="handlePrint">
          打印凭证
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Records',
  data() {
    return {
      searchForm: {
        type: '',
        status: '',
        dateRange: []
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      loading: false,
      stats: {
        total: 156,
        completed: 128,
        processing: 15,
        pending: 13
      },
      allData: [],
      tableData: [],
      detailDialogVisible: false,
      currentRecord: null
    }
  },
  computed: {
    filteredData() {
      let data = [...this.allData]
      
      if (this.searchForm.type) {
        data = data.filter(item => item.businessType === this.searchForm.type)
      }
      
      if (this.searchForm.status) {
        data = data.filter(item => item.status === this.searchForm.status)
      }
      
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const startDate = new Date(this.searchForm.dateRange[0]).setHours(0, 0, 0, 0)
        const endDate = new Date(this.searchForm.dateRange[1]).setHours(23, 59, 59, 999)
        data = data.filter(item => {
          const itemDate = new Date(item.applyTime).getTime()
          return itemDate >= startDate && itemDate <= endDate
        })
      }
      
      return data
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        this.allData = [
          { ticketNumber: 'A001', businessType: '综合业务', applicant: '张三', idCard: '110101199001011234', window: '1号窗口', applyTime: '2024-01-15 09:30:00', handleTime: '2024-01-15 09:45:00', status: '已完成', phone: '13800138001', handler: '李主任', remark: '材料齐全，办理顺利' },
          { ticketNumber: 'A002', businessType: '综合业务', applicant: '李四', idCard: '110101199002022345', window: '1号窗口', applyTime: '2024-01-15 10:00:00', handleTime: '2024-01-15 10:20:00', status: '已完成', phone: '13800138002', handler: '李主任', remark: '' },
          { ticketNumber: 'B015', businessType: '户政业务', applicant: '王五', idCard: '110101199003033456', window: '2号窗口', applyTime: '2024-01-15 10:30:00', handleTime: '', status: '办理中', phone: '13800138003', handler: '', remark: '' },
          { ticketNumber: 'C022', businessType: '社保业务', applicant: '赵六', idCard: '110101199004044567', window: '3号窗口', applyTime: '2024-01-15 11:00:00', handleTime: '', status: '待办理', phone: '13800138004', handler: '', remark: '' },
          { ticketNumber: 'D008', businessType: '不动产', applicant: '孙七', idCard: '110101199005055678', window: '4号窗口', applyTime: '2024-01-15 14:00:00', handleTime: '2024-01-15 14:40:00', status: '已完成', phone: '13800138005', handler: '王主任', remark: '不动产登记业务' },
          { ticketNumber: 'A005', businessType: '综合业务', applicant: '周八', idCard: '110101199006066789', window: '1号窗口', applyTime: '2024-01-15 14:30:00', handleTime: '', status: '待办理', phone: '13800138006', handler: '', remark: '' },
          { ticketNumber: 'B016', businessType: '户政业务', applicant: '吴九', idCard: '110101199007077890', window: '2号窗口', applyTime: '2024-01-15 15:00:00', handleTime: '2024-01-15 15:25:00', status: '已完成', phone: '13800138007', handler: '张主任', remark: '' },
          { ticketNumber: 'E003', businessType: '市场监管', applicant: '郑十', idCard: '110101199008088901', window: '5号窗口', applyTime: '2024-01-15 15:30:00', handleTime: '', status: '已取消', phone: '13800138008', handler: '', remark: '申请人主动取消' },
          { ticketNumber: 'F001', businessType: '出入境', applicant: '陈一', idCard: '110101199009099012', window: '6号窗口', applyTime: '2024-01-16 09:00:00', handleTime: '2024-01-16 09:30:00', status: '已完成', phone: '13800138009', handler: '刘主任', remark: '护照办理' },
          { ticketNumber: 'A006', businessType: '综合业务', applicant: '林二', idCard: '110101199010100123', window: '1号窗口', applyTime: '2024-01-16 10:00:00', handleTime: '', status: '待办理', phone: '13800138010', handler: '', remark: '' },
          { ticketNumber: 'C023', businessType: '社保业务', applicant: '黄三', idCard: '110101199011111234', window: '3号窗口', applyTime: '2024-01-16 11:00:00', handleTime: '2024-01-16 11:30:00', status: '已完成', phone: '13800138011', handler: '赵主任', remark: '' },
          { ticketNumber: 'B017', businessType: '户政业务', applicant: '杨四', idCard: '110101199012122345', window: '2号窗口', applyTime: '2024-01-17 09:30:00', handleTime: '', status: '办理中', phone: '13800138012', handler: '', remark: '' },
          { ticketNumber: 'D009', businessType: '不动产', applicant: '吴五', idCard: '110101199101013456', window: '4号窗口', applyTime: '2024-01-17 14:00:00', handleTime: '', status: '待办理', phone: '13800138013', handler: '', remark: '' },
          { ticketNumber: 'E004', businessType: '市场监管', applicant: '郑六', idCard: '110101199102024567', window: '5号窗口', applyTime: '2024-01-17 15:00:00', handleTime: '2024-01-17 15:45:00', status: '已完成', phone: '13800138014', handler: '孙主任', remark: '营业执照办理' },
          { ticketNumber: 'F002', businessType: '出入境', applicant: '王七', idCard: '110101199103035678', window: '6号窗口', applyTime: '2024-01-18 10:00:00', handleTime: '', status: '待办理', phone: '13800138015', handler: '', remark: '' }
        ]
        this.updatePagination()
        this.loading = false
      }, 500)
    },
    updatePagination() {
      this.pagination.total = this.filteredData.length
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = this.filteredData.slice(start, end)
      
      this.stats.total = this.allData.length
      this.stats.completed = this.allData.filter(item => item.status === '已完成').length
      this.stats.processing = this.allData.filter(item => item.status === '办理中').length
      this.stats.pending = this.allData.filter(item => item.status === '待办理').length
    },
    getStatusType(status) {
      const map = {
        '已完成': 'success',
        '办理中': 'warning',
        '待办理': 'info',
        '已取消': 'danger'
      }
      return map[status] || 'info'
    },
    handleSearch() {
      this.pagination.page = 1
      this.updatePagination()
      this.$message.success(`搜索完成，共找到 ${this.filteredData.length} 条记录`)
    },
    handleReset() {
      this.searchForm = { type: '', status: '', dateRange: [] }
      this.pagination.page = 1
      this.updatePagination()
      this.$message.info('筛选已重置')
    },
    handleExport() {
      this.$message.success('导出成功')
    },
    handleView(row) {
      this.currentRecord = row
      this.detailDialogVisible = true
    },
    handleCancel(row) {
      this.$confirm(`确定要取消 ${row.ticketNumber} 号的预约吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = '已取消'
        this.stats.pending--
        this.$message.success('取消成功')
      }).catch(() => {})
    },
    handlePrint() {
      this.$message.success('正在打印凭证...')
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.pagination.page = 1
      this.updatePagination()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.updatePagination()
    }
  }
}
</script>

<style scoped>
.records-page {
  height: 100%;
}

.search-card {
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  color: #fff;
}

.stat-card.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-card.completed {
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
}

.stat-card.processing {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-card.pending {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-icon {
  font-size: 48px;
  margin-right: 20px;
  opacity: 0.8;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.table-card {
  height: calc(100% - 280px);
  display: flex;
  flex-direction: column;
}

.card-header {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.el-table {
  flex: 1;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  padding: 20px 0 0;
}
</style>
