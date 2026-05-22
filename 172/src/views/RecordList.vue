<template>
  <div class="page-container">
    <div class="page-title">我的报名记录</div>
    
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="报考科目">
          <el-input v-model="searchForm.subjectName" placeholder="请输入科目名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="考试类型">
          <el-select v-model="searchForm.examType" placeholder="请选择" clearable>
            <el-option label="计算机类" value="computer"></el-option>
            <el-option label="英语类" value="english"></el-option>
            <el-option label="教师类" value="teacher"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="报名状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="待审核" :value="1"></el-option>
            <el-option label="审核通过" :value="2"></el-option>
            <el-option label="审核不通过" :value="3"></el-option>
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
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="paginatedRecords" border style="width: 100%;">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="subjectName" label="报考科目" min-width="180">
        <template slot-scope="scope">
          <div>
            <div style="font-weight: 500;">{{ scope.row.subjectName }}</div>
            <div style="font-size: 12px; color: #909399;">{{ scope.row.subjectCode }}</div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="examType" label="考试类型" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getExamTypeTagType(scope.row.examType)" size="small">
            {{ getExamTypeLabel(scope.row.examType) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="examDate" label="考试日期" width="120" align="center"></el-table-column>
      <el-table-column prop="examTime" label="考试时间" width="120" align="center"></el-table-column>
      <el-table-column prop="applyTime" label="申请时间" width="160" align="center"></el-table-column>
      <el-table-column prop="status" label="审核状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="applyStatusTagType[scope.row.status]" size="small">
            {{ applyStatusMap[scope.row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="reviewTime" label="审核时间" width="160" align="center">
        <template slot-scope="scope">
          {{ scope.row.reviewTime || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" align="center">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="viewDetail(scope.row)">
            查看详情
          </el-button>
          <el-button
            v-if="scope.row.status === 2"
            type="primary"
            size="small"
            @click="goToTicket(scope.row)"
          >
            查看准考证
          </el-button>
          <el-button
            v-if="scope.row.status === 1"
            type="danger"
            size="small"
            @click="cancelApply(scope.row)"
          >
            取消报名
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 20px; text-align: right;"
      background
      :page-size="pageSize"
      :total="filteredRecords.length"
      :current-page.sync="currentPage"
      layout="total, sizes, prev, pager, next, jumper"
      :page-sizes="[5, 10, 20, 50]"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
    ></el-pagination>

    <el-dialog
      title="报名详情"
      :visible.sync="detailDialogVisible"
      width="600px"
    >
      <div v-if="currentRecord">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="报考科目" :span="2">
            {{ currentRecord.subjectName }}（{{ currentRecord.subjectCode }}）
          </el-descriptions-item>
          <el-descriptions-item label="考试类型">
            <el-tag :type="getExamTypeTagType(currentRecord.examType)" size="small">
              {{ getExamTypeLabel(currentRecord.examType) }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="考试日期">{{ currentRecord.examDate }}</el-descriptions-item>
          <el-descriptions-item label="考试时间">{{ currentRecord.examTime }}</el-descriptions-item>
          <el-descriptions-item label="申请人姓名">{{ currentRecord.applicantName }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ currentRecord.idCard }}</el-descriptions-item>
          <el-descriptions-item label="手机号码">{{ currentRecord.phone }}</el-descriptions-item>
          <el-descriptions-item label="电子邮箱">{{ currentRecord.email }}</el-descriptions-item>
          <el-descriptions-item label="申请时间" :span="2">{{ currentRecord.applyTime }}</el-descriptions-item>
          <el-descriptions-item label="审核状态">
            <el-tag :type="applyStatusTagType[currentRecord.status]" size="small">
              {{ applyStatusMap[currentRecord.status] }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item v-if="currentRecord.reviewer" label="审核人">{{ currentRecord.reviewer }}</el-descriptions-item>
          <el-descriptions-item v-if="currentRecord.reviewTime" label="审核时间">{{ currentRecord.reviewTime }}</el-descriptions-item>
          <el-descriptions-item v-if="currentRecord.ticketNo" label="准考证号" :span="2">
            <span style="color: #409EFF; font-weight: bold;">{{ currentRecord.ticketNo }}</span>
          </el-descriptions-item>
          <el-descriptions-item v-if="currentRecord.rejectReason" label="驳回原因" :span="2">
            <span style="color: #f56c6c;">{{ currentRecord.rejectReason }}</span>
          </el-descriptions-item>
        </el-descriptions>
        
        <div v-if="currentRecord.status === 2" style="margin-top: 20px; text-align: center;">
          <el-alert
            title="您的报名已审核通过，请按时打印准考证参加考试"
            type="success"
            :closable="false"
            show-icon
          ></el-alert>
          <el-button
            type="primary"
            style="margin-top: 15px;"
            @click="goToTicket(currentRecord)"
          >
            立即查看准考证
          </el-button>
        </div>
        
        <div v-if="currentRecord.status === 3" style="margin-top: 20px;">
          <el-alert
            title="报名审核未通过，您可以修改信息后重新报名"
            type="error"
            :closable="false"
            show-icon
          ></el-alert>
          <div style="margin-top: 15px; text-align: center;">
            <el-button type="primary" @click="reApply">重新报名</el-button>
          </div>
        </div>
        
        <div v-if="currentRecord.status === 1" style="margin-top: 20px;">
          <el-alert
            title="您的报名正在审核中，请耐心等待"
            type="warning"
            :closable="false"
            show-icon
          ></el-alert>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { applicationRecords, applyStatusMap, applyStatusTagType, subjectList } from '@/mock/data.js'

export default {
  name: 'RecordList',
  data() {
    return {
      records: applicationRecords,
      subjectList,
      applyStatusMap,
      applyStatusTagType,
      searchForm: {
        subjectName: '',
        examType: '',
        status: '',
        dateRange: []
      },
      detailDialogVisible: false,
      currentRecord: null,
      pageSize: 10,
      currentPage: 1
    }
  },
  computed: {
    filteredRecords() {
      let result = this.records
      
      if (this.searchForm.subjectName) {
        const keyword = this.searchForm.subjectName.toLowerCase()
        result = result.filter(item => 
          item.subjectName.toLowerCase().includes(keyword) ||
          item.subjectCode.toLowerCase().includes(keyword)
        )
      }
      
      if (this.searchForm.examType) {
        const subjectIds = this.subjectList
          .filter(item => item.examType === this.searchForm.examType)
          .map(item => item.id)
        result = result.filter(item => subjectIds.includes(item.subjectId))
      }
      
      if (this.searchForm.status) {
        result = result.filter(item => item.status === this.searchForm.status)
      }
      
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const startDate = this.searchForm.dateRange[0]
        const endDate = this.searchForm.dateRange[1]
        result = result.filter(item => {
          const applyDate = item.applyTime.split(' ')[0]
          return applyDate >= startDate && applyDate <= endDate
        })
      }
      
      return result
    },
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredRecords.slice(start, end)
    }
  },
  methods: {
    getExamTypeTagType(type) {
      const typeMap = {
        'computer': 'primary',
        'english': 'success',
        'teacher': 'warning'
      }
      return typeMap[type] || 'info'
    },
    getExamTypeLabel(type) {
      const labelMap = {
        'computer': '计算机类',
        'english': '英语类',
        'teacher': '教师类'
      }
      return labelMap[type] || '其他'
    },
    handleSearch() {
      this.currentPage = 1
    },
    handlePageChange() {
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    resetSearch() {
      this.searchForm = {
        subjectName: '',
        examType: '',
        status: '',
        dateRange: []
      }
      this.currentPage = 1
    },
    viewDetail(row) {
      this.currentRecord = { ...row }
      const subject = this.subjectList.find(item => item.id === row.subjectId)
      if (subject) {
        this.currentRecord.examType = subject.examType
      }
      this.detailDialogVisible = true
    },
    goToTicket(row) {
      this.detailDialogVisible = false
      this.$router.push({
        path: '/ticket',
        query: { idCard: row.idCard, name: row.applicantName, autoQuery: 'true' }
      })
    },
    cancelApply(row) {
      this.$confirm('确认取消该报名申请？取消后将无法恢复。', '提示', {
        confirmButtonText: '确定取消',
        cancelButtonText: '再想想',
        type: 'warning'
      }).then(() => {
        const index = this.records.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.records.splice(index, 1)
        }
        this.$message.success('已取消报名')
      }).catch(() => {})
    },
    reApply() {
      this.detailDialogVisible = false
      this.$router.push('/apply')
    }
  }
}
</script>

<style scoped>
.search-bar {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}
</style>
