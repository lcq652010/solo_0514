<template>
  <div class="page-container">
    <div class="page-header">
      <span class="page-title">申领记录</span>
    </div>
    
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="申请单号">
          <el-input v-model="searchForm.applyNo" placeholder="请输入申请单号" clearable></el-input>
        </el-form-item>
        <el-form-item label="申请部门">
          <el-select v-model="searchForm.departmentId" placeholder="请选择部门" clearable>
            <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="用品类型">
          <el-select v-model="searchForm.categoryId" placeholder="请选择用品类型" clearable>
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="yyyy-MM-dd"
            style="width: 240px">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="审批状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待审批" :value="0"></el-option>
            <el-option label="已通过" :value="1"></el-option>
            <el-option label="已拒绝" :value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i class="el-icon-search"></i> 搜索
          </el-button>
          <el-button @click="handleReset">
            <i class="el-icon-refresh"></i> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="applyNo" label="申请单号" width="150" align="center"></el-table-column>
        <el-table-column prop="departmentName" label="申请部门" width="120" align="center"></el-table-column>
        <el-table-column prop="applicant" label="申请人" width="100" align="center"></el-table-column>
        <el-table-column label="申领明细" min-width="250">
          <template slot-scope="scope">
            <div v-for="(item, index) in scope.row.items" :key="index" style="margin-bottom: 5px;">
              <span>{{ item.supplyName }} × {{ item.quantity }}{{ item.unit }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="statusMap[scope.row.status].type" size="small">
              {{ statusMap[scope.row.status].label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="applyTime" label="申请时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="handleApprove(scope.row)" v-if="scope.row.status === 0">
              <i class="el-icon-check"></i> 通过
            </el-button>
            <el-button size="mini" type="danger" @click="handleReject(scope.row)" v-if="scope.row.status === 0">
              <i class="el-icon-close"></i> 拒绝
            </el-button>
            <el-button size="mini" type="primary" @click="handleDetail(scope.row)">
              <i class="el-icon-view"></i> 详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>

    <el-dialog title="申领详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="申请单号">{{ currentRecord.applyNo }}</el-descriptions-item>
        <el-descriptions-item label="申请部门">{{ currentRecord.departmentName }}</el-descriptions-item>
        <el-descriptions-item label="申请人">{{ currentRecord.applicant }}</el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ currentRecord.applyTime }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusMap[currentRecord.status].type" size="small">
            {{ statusMap[currentRecord.status].label }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申领明细" :span="2">
          <el-table :data="currentRecord.items" border size="small">
            <el-table-column prop="supplyName" label="用品名称"></el-table-column>
            <el-table-column prop="quantity" label="数量" width="100" align="center"></el-table-column>
            <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
          </el-table>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRecord.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { applyRecords, departments, categories, supplies, statusMap } from '@/api/mockData'

export default {
  name: 'Records',
  data() {
    return {
      departments: departments,
      categories: categories,
      statusMap: statusMap,
      searchForm: {
        applyNo: '',
        departmentId: null,
        categoryId: null,
        dateRange: [],
        status: null
      },
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      detailDialogVisible: false,
      currentRecord: null,
      dataList: []
    }
  },
  created() {
    this.dataList = [...applyRecords]
    this.loadData()
  },
  methods: {
    loadData() {
      let filtered = [...this.dataList]
      
      if (this.searchForm.applyNo) {
        filtered = filtered.filter(item => item.applyNo.includes(this.searchForm.applyNo))
      }
      
      if (this.searchForm.departmentId) {
        filtered = filtered.filter(item => item.departmentId === this.searchForm.departmentId)
      }
      
      if (this.searchForm.categoryId) {
        filtered = filtered.filter(item => {
          return item.items.some(applyItem => {
            const supply = supplies.find(s => s.id === applyItem.supplyId)
            return supply && supply.categoryId === this.searchForm.categoryId
          })
        })
      }
      
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const [startDate, endDate] = this.searchForm.dateRange
        filtered = filtered.filter(item => {
          const itemDate = item.applyTime.split(' ')[0]
          return itemDate >= startDate && itemDate <= endDate
        })
      }
      
      if (this.searchForm.status !== null && this.searchForm.status !== '') {
        filtered = filtered.filter(item => item.status === this.searchForm.status)
      }
      
      this.total = filtered.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.tableData = filtered.slice(start, end)
    },
    handleSearch() {
      this.currentPage = 1
      this.loadData()
    },
    handleReset() {
      this.searchForm = {
        applyNo: '',
        departmentId: null,
        categoryId: null,
        dateRange: [],
        status: null
      }
      this.currentPage = 1
      this.loadData()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadData()
    },
    handlePageChange(val) {
      this.currentPage = val
      this.loadData()
    },
    handleApprove(row) {
      this.$confirm('确定要通过该申请吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.dataList.findIndex(item => item.id === row.id)
        if (index !== -1) {
          this.dataList[index].status = 1
          this.loadData()
          this.$message.success('审批通过')
        }
      }).catch(() => {})
    },
    handleReject(row) {
      this.$confirm('确定要拒绝该申请吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.dataList.findIndex(item => item.id === row.id)
        if (index !== -1) {
          this.dataList[index].status = 2
          this.loadData()
          this.$message.success('已拒绝')
        }
      }).catch(() => {})
    },
    handleDetail(row) {
      this.currentRecord = row
      this.detailDialogVisible = true
    }
  }
}
</script>
