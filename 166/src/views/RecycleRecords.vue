<template>
  <div class="page-card">
    <div class="search-bar">
      <el-row :gutter="20">
        <el-col :span="5">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索书名/作者/卖家"
            clearable
            @clear="loadData"
          >
            <el-button slot="append" icon="el-icon-search" @click="loadData"></el-button>
          </el-input>
        </el-col>
        <el-col :span="3">
          <el-select v-model="searchStatus" placeholder="状态筛选" clearable style="width: 100%" @change="loadData">
            <el-option label="待审核" value="pending"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已拒绝" value="rejected"></el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="searchDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 100%"
            clearable
            @change="loadData"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          ></el-date-picker>
        </el-col>
        <el-col :span="3">
          <el-button type="primary" @click="resetSearch" style="width: 100%">重置筛选</el-button>
        </el-col>
      </el-row>
    </div>
    <el-table :data="tableData" border style="width: 100%" v-loading="loading">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="bookName" label="书名" min-width="150"></el-table-column>
      <el-table-column prop="author" label="作者" width="120"></el-table-column>
      <el-table-column prop="sellerName" label="卖家" width="100"></el-table-column>
      <el-table-column prop="sellerPhone" label="卖家电话" width="120"></el-table-column>
      <el-table-column label="成色" width="100" align="center">
        <template slot-scope="scope">
          {{ getConditionLabel(scope.row.condition) }}
        </template>
      </el-table-column>
      <el-table-column prop="originalPrice" label="原价" width="90" align="center">
        <template slot-scope="scope">
          ¥{{ scope.row.originalPrice }}
        </template>
      </el-table-column>
      <el-table-column prop="recyclePrice" label="回收价" width="100" align="center">
        <template slot-scope="scope">
          <span style="color: #67c23a; font-weight: bold">¥{{ scope.row.recyclePrice }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="申请时间" width="160"></el-table-column>
      <el-table-column prop="completeTime" label="完成时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.completeTime || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="small"
            @click="viewDetail(scope.row)"
          >详情</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        :current-page="page"
        :page-sizes="[5, 10, 20, 50]"
        :page-size="pageSize"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="handlePageChange"
        @size-change="handleSizeChange"
      ></el-pagination>
    </div>

    <el-dialog title="回收记录详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="书名">{{ currentRecord.bookName }}</el-descriptions-item>
        <el-descriptions-item label="作者">{{ currentRecord.author }}</el-descriptions-item>
        <el-descriptions-item label="卖家姓名">{{ currentRecord.sellerName }}</el-descriptions-item>
        <el-descriptions-item label="卖家电话">{{ currentRecord.sellerPhone }}</el-descriptions-item>
        <el-descriptions-item label="成色">{{ getConditionLabel(currentRecord.condition) }}</el-descriptions-item>
        <el-descriptions-item label="原价">¥{{ currentRecord.originalPrice }}</el-descriptions-item>
        <el-descriptions-item label="回收价">
          <span style="color: #67c23a; font-weight: bold">¥{{ currentRecord.recyclePrice }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusMap[currentRecord.status].type">
            {{ statusMap[currentRecord.status].label }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="申请时间" :span="2">{{ currentRecord.createTime }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.completeTime" label="完成时间" :span="2">{{ currentRecord.completeTime }}</el-descriptions-item>
        <el-descriptions-item v-if="currentRecord.rejectReason" label="拒绝原因" :span="2">{{ currentRecord.rejectReason }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { bookConditions, recycleStatusMap } from '../utils/mockData'
import { getRecycleRecords, initStorage } from '../utils/storage'

export default {
  name: 'RecycleRecords',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      searchStatus: '',
      searchDateRange: [],
      page: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      conditions: bookConditions,
      statusMap: recycleStatusMap,
      detailDialogVisible: false,
      currentRecord: null
    }
  },
  mounted() {
    initStorage()
    this.loadData()
  },
  methods: {
    getConditionLabel(value) {
      const cond = this.conditions.find(c => c.value === value)
      return cond ? cond.label : value
    },
    filterByDateRange(dateStr, dateRange) {
      if (!dateRange || dateRange.length !== 2) return true
      const [startDate, endDate] = dateRange
      const itemDate = dateStr.split(' ')[0]
      return itemDate >= startDate && itemDate <= endDate
    },
    loadData() {
      this.loading = true
      setTimeout(() => {
        let data = getRecycleRecords()
        if (this.searchKeyword) {
          data = data.filter(item => 
            item.bookName.includes(this.searchKeyword) || 
            item.author.includes(this.searchKeyword) ||
            item.sellerName.includes(this.searchKeyword)
          )
        }
        if (this.searchStatus) {
          data = data.filter(item => item.status === this.searchStatus)
        }
        data = data.filter(item => this.filterByDateRange(item.createTime, this.searchDateRange))
        this.total = data.length
        const start = (this.page - 1) * this.pageSize
        this.tableData = data.slice(start, start + this.pageSize)
        this.loading = false
      }, 300)
    },
    handlePageChange(page) {
      this.page = page
      this.loadData()
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.page = 1
      this.loadData()
    },
    resetSearch() {
      this.searchKeyword = ''
      this.searchStatus = ''
      this.searchDateRange = []
      this.page = 1
      this.loadData()
    },
    viewDetail(row) {
      this.currentRecord = row
      this.detailDialogVisible = true
    }
  }
}
</script>
