<template>
  <div class="page-card">
    <div class="search-bar">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索书名/作者"
            clearable
            @clear="loadData"
          >
            <el-button slot="append" icon="el-icon-search" @click="loadData"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchStatus" placeholder="状态筛选" clearable style="width: 100%" @change="loadData">
            <el-option label="待审核" value="pending"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已拒绝" value="rejected"></el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>
    <el-table :data="tableData" border style="width: 100%" v-loading="loading">
      <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
      <el-table-column prop="bookName" label="书名" min-width="150"></el-table-column>
      <el-table-column prop="author" label="作者" width="120"></el-table-column>
      <el-table-column prop="sellerName" label="卖家" width="100"></el-table-column>
      <el-table-column prop="sellerPhone" label="卖家电话" width="120"></el-table-column>
      <el-table-column label="成色" width="100" align="center">
        <template slot-scope="scope">
          {{ getConditionLabel(scope.row.condition) }}
        </template>
      </el-table-column>
      <el-table-column prop="originalPrice" label="原价" width="100" align="center">
        <template slot-scope="scope">
          ¥{{ scope.row.originalPrice }}
        </template>
      </el-table-column>
      <el-table-column label="回收定价" width="120" align="center">
        <template slot-scope="scope">
          <el-input-number
            v-if="scope.row.status === 'pending'"
            v-model="scope.row.recyclePrice"
            :min="0"
            :precision="2"
            size="small"
          ></el-input-number>
          <span v-else>¥{{ scope.row.recyclePrice }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="申请时间" width="160"></el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" align="center" fixed="right">
        <template slot-scope="scope">
          <template v-if="scope.row.status === 'pending'">
            <el-button
              type="success"
              size="small"
              @click="approve(scope.row)"
            >通过</el-button>
            <el-button
              type="danger"
              size="small"
              @click="reject(scope.row)"
            >拒绝</el-button>
          </template>
          <template v-else>
            <el-button
              type="info"
              size="small"
              @click="viewDetail(scope.row)"
            >详情</el-button>
          </template>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        @current-change="handlePageChange"
      ></el-pagination>
    </div>

    <el-dialog title="拒绝原因" :visible.sync="rejectDialogVisible" width="500px">
      <el-form label-width="80px">
        <el-form-item label="拒绝原因">
          <el-input
            v-model="rejectReason"
            type="textarea"
            :rows="4"
            placeholder="请输入拒绝原因"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReject" :loading="submitLoading">确认</el-button>
      </div>
    </el-dialog>

    <el-dialog title="回收详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="书名">{{ currentRecord.bookName }}</el-descriptions-item>
        <el-descriptions-item label="作者">{{ currentRecord.author }}</el-descriptions-item>
        <el-descriptions-item label="卖家">{{ currentRecord.sellerName }}</el-descriptions-item>
        <el-descriptions-item label="卖家电话">{{ currentRecord.sellerPhone }}</el-descriptions-item>
        <el-descriptions-item label="成色">{{ getConditionLabel(currentRecord.condition) }}</el-descriptions-item>
        <el-descriptions-item label="原价">¥{{ currentRecord.originalPrice }}</el-descriptions-item>
        <el-descriptions-item label="回收价">¥{{ currentRecord.recyclePrice }}</el-descriptions-item>
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
import { getRecycleRecords, updateRecycleRecordStatus, initStorage } from '../utils/storage'

export default {
  name: 'Pricing',
  data() {
    return {
      loading: false,
      submitLoading: false,
      searchKeyword: '',
      searchStatus: '',
      page: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      statusMap: recycleStatusMap,
      conditions: bookConditions,
      rejectDialogVisible: false,
      detailDialogVisible: false,
      rejectReason: '',
      currentRecord: null,
      currentId: null
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
    loadData() {
      this.loading = true
      setTimeout(() => {
        let data = getRecycleRecords()
        if (this.searchKeyword) {
          data = data.filter(item => 
            item.bookName.includes(this.searchKeyword) || 
            item.author.includes(this.searchKeyword)
          )
        }
        if (this.searchStatus) {
          data = data.filter(item => item.status === this.searchStatus)
        }
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
    approve(row) {
      this.$confirm('确认通过该回收申请？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        updateRecycleRecordStatus(row.id, 'completed')
        this.$message.success('审核通过！')
        this.loadData()
      }).catch(() => {})
    },
    reject(row) {
      this.currentId = row.id
      this.rejectReason = ''
      this.rejectDialogVisible = true
    },
    confirmReject() {
      if (!this.rejectReason.trim()) {
        this.$message.warning('请输入拒绝原因')
        return
      }
      this.submitLoading = true
      setTimeout(() => {
        updateRecycleRecordStatus(this.currentId, 'rejected', this.rejectReason)
        this.$message.success('已拒绝申请')
        this.rejectDialogVisible = false
        this.submitLoading = false
        this.loadData()
      }, 300)
    },
    viewDetail(row) {
      this.currentRecord = row
      this.detailDialogVisible = true
    }
  }
}
</script>
