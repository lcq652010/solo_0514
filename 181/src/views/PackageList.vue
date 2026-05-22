<template>
  <div class="page-container">
    <el-card class="card-box">
      <div slot="header" class="clearfix">
        <span>包裹管理</span>
      </div>
      
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-row :gutter="10">
            <el-col :span="5">
              <el-form-item label="快递单号">
                <el-input v-model="searchForm.trackingNo" placeholder="请输入" clearable style="width: 100%;"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="收件人">
                <el-input v-model="searchForm.receiverName" placeholder="请输入" clearable style="width: 100%;"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="快递公司">
                <el-select v-model="searchForm.expressCompany" placeholder="请选择" clearable style="width: 100%;">
                  <el-option label="顺丰速运" value="顺丰速运"></el-option>
                  <el-option label="圆通速递" value="圆通速递"></el-option>
                  <el-option label="中通快递" value="中通快递"></el-option>
                  <el-option label="韵达快递" value="韵达快递"></el-option>
                  <el-option label="申通快递" value="申通快递"></el-option>
                  <el-option label="邮政EMS" value="邮政EMS"></el-option>
                  <el-option label="京东物流" value="京东物流"></el-option>
                  <el-option label="其他" value="其他"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="物品类型">
                <el-select v-model="searchForm.goodsType" placeholder="请选择" clearable style="width: 100%;">
                  <el-option label="文件资料" value="文件资料"></el-option>
                  <el-option label="电子产品" value="电子产品"></el-option>
                  <el-option label="服装鞋帽" value="服装鞋帽"></el-option>
                  <el-option label="食品生鲜" value="食品生鲜"></el-option>
                  <el-option label="日常用品" value="日常用品"></el-option>
                  <el-option label="其他" value="其他"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item label="取件状态">
                <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 100%;">
                  <el-option label="待取件" value="待取件"></el-option>
                  <el-option label="已取件" value="已取件"></el-option>
                  <el-option label="已出库" value="已出库"></el-option>
                  <el-option label="已退回" value="已退回"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="10">
            <el-col :span="12">
              <el-form-item label="入库时间">
                <el-date-picker
                  v-model="searchForm.inboundDateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  style="width: 100%;">
                </el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :span="4">
              <el-form-item>
                <el-button type="primary" @click="handleSearch" icon="el-icon-search">查询</el-button>
                <el-button @click="handleReset" icon="el-icon-refresh">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
      
      <el-table :data="tableData" stripe style="width: 100%;" v-loading="loading">
        <el-table-column prop="trackingNo" label="快递单号" width="160" show-overflow-tooltip></el-table-column>
        <el-table-column prop="expressCompany" label="快递公司" width="100"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="90"></el-table-column>
        <el-table-column prop="receiverPhone" label="联系电话" width="120"></el-table-column>
        <el-table-column prop="pickupCode" label="取件码" width="90"></el-table-column>
        <el-table-column prop="location" label="存放位置" width="110"></el-table-column>
        <el-table-column prop="goodsType" label="物品类型" width="90"></el-table-column>
        <el-table-column prop="inboundTime" label="入库时间" width="170" show-overflow-tooltip></el-table-column>
        <el-table-column label="取件状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="warning" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>
    
    <el-dialog title="包裹详情" :visible.sync="dialogVisible" width="600px">
      <el-descriptions :column="1" border v-if="currentPackage">
        <el-descriptions-item label="快递单号">{{ currentPackage.trackingNo }}</el-descriptions-item>
        <el-descriptions-item label="快递公司">{{ currentPackage.expressCompany }}</el-descriptions-item>
        <el-descriptions-item label="收件人姓名">{{ currentPackage.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentPackage.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="取件码">{{ currentPackage.pickupCode }}</el-descriptions-item>
        <el-descriptions-item label="存放位置">{{ currentPackage.location }}</el-descriptions-item>
        <el-descriptions-item label="物品类型">{{ currentPackage.goodsType }}</el-descriptions-item>
        <el-descriptions-item label="入库时间">{{ currentPackage.inboundTime }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentPackage.status)">{{ currentPackage.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注">{{ currentPackage.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { packageStorage } from '@/utils/storage.js'
import { eventBus } from '@/utils/eventBus.js'

export default {
  name: 'PackageList',
  data() {
    return {
      loading: false,
      searchForm: {
        trackingNo: '',
        receiverName: '',
        phone: '',
        expressCompany: '',
        goodsType: '',
        status: '',
        inboundDateRange: []
      },
      tableData: [],
      allData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      currentPackage: null
    }
  },
  methods: {
    getStatusType(status) {
      const statusMap = {
        '待取件': 'warning',
        '已取件': 'success',
        '已出库': 'info',
        '已退回': 'danger'
      }
      return statusMap[status] || 'info'
    },
    handleSearch() {
      this.loading = true
      this.pagination.currentPage = 1
      setTimeout(() => {
        this.loadData()
        this.loading = false
      }, 300)
    },
    handleReset() {
      this.searchForm = {
        trackingNo: '',
        receiverName: '',
        phone: '',
        expressCompany: '',
        goodsType: '',
        status: '',
        inboundDateRange: []
      }
      this.pagination.currentPage = 1
      this.handleSearch()
    },
    handleView(row) {
      this.currentPackage = row
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.$message.info('编辑功能开发中')
    },
    handleDelete(row) {
      this.$confirm('确认删除该包裹记录？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        packageStorage.deletePackage(row.trackingNo)
        this.pagination.currentPage = 1
        this.loadData()
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
      this.applyFilter()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.applyFilter()
    },
    loadData() {
      this.allData = packageStorage.getAllPackages().map(pkg => ({
        ...pkg,
        receiverPhone: pkg.receiverPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
      }))
      
      this.applyFilter()
    },
    applyFilter() {
      let filteredData = [...this.allData]
      
      if (this.searchForm.trackingNo) {
        filteredData = filteredData.filter(item => item.trackingNo.includes(this.searchForm.trackingNo))
      }
      
      if (this.searchForm.receiverName) {
        filteredData = filteredData.filter(item => item.receiverName.includes(this.searchForm.receiverName))
      }
      
      if (this.searchForm.expressCompany) {
        filteredData = filteredData.filter(item => item.expressCompany === this.searchForm.expressCompany)
      }
      
      if (this.searchForm.goodsType) {
        filteredData = filteredData.filter(item => item.goodsType === this.searchForm.goodsType)
      }
      
      if (this.searchForm.status) {
        filteredData = filteredData.filter(item => item.status === this.searchForm.status)
      }
      
      if (this.searchForm.inboundDateRange && this.searchForm.inboundDateRange.length === 2) {
        const startDate = new Date(this.searchForm.inboundDateRange[0])
        startDate.setHours(0, 0, 0, 0)
        const endDate = new Date(this.searchForm.inboundDateRange[1])
        endDate.setHours(23, 59, 59, 999)
        
        filteredData = filteredData.filter(item => {
          const inboundTime = new Date(item.inboundTime)
          return inboundTime >= startDate && inboundTime <= endDate
        })
      }
      
      this.pagination.total = filteredData.length
      this.updateTableData(filteredData)
    },
    updateTableData(filteredData) {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    }
  },
  mounted() {
    this.loadData()
    eventBus.$on('packageStatusUpdated', () => {
      this.loadData()
    })
  },
  beforeDestroy() {
    eventBus.$off('packageStatusUpdated')
  }
}
</script>

<style scoped>
.search-bar {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-pagination {
  padding: 0;
}
</style>
