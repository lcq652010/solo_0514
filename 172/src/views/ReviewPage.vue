<template>
  <div class="page-container">
    <div class="page-title">资格审核管理</div>
    
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="申请人姓名">
          <el-input v-model="searchForm.applicantName" placeholder="请输入姓名" clearable></el-input>
        </el-form-item>
        <el-form-item label="审核状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="待审核" :value="1"></el-option>
            <el-option label="审核通过" :value="2"></el-option>
            <el-option label="审核不通过" :value="3"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-table :data="paginatedRecords" border style="width: 100%;">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="applicantName" label="申请人" width="100" align="center"></el-table-column>
      <el-table-column prop="idCard" label="身份证号" width="180" align="center">
        <template slot-scope="scope">
          {{ maskIdCard(scope.row.idCard) }}
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
      <el-table-column prop="subjectName" label="报考科目" min-width="180"></el-table-column>
      <el-table-column prop="applyTime" label="申请时间" width="160" align="center"></el-table-column>
      <el-table-column prop="status" label="审核状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="applyStatusTagType[scope.row.status]" size="small">
            {{ applyStatusMap[scope.row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="250" align="center">
        <template slot-scope="scope">
          <el-button type="info" size="small" @click="viewDetail(scope.row)">
            详情
          </el-button>
          <el-button
            v-if="scope.row.status === 1"
            type="success"
            size="small"
            @click="approve(scope.row)"
          >
            通过
          </el-button>
          <el-button
            v-if="scope.row.status === 1"
            type="danger"
            size="small"
            @click="reject(scope.row)"
          >
            驳回
          </el-button>
          <el-button
            v-if="scope.row.status === 2 && scope.row.ticketNo"
            type="primary"
            size="small"
            icon="el-icon-tickets"
            @click="viewTicket(scope.row)"
          >
            准考证
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
      layout="total, prev, pager, next, jumper"
      @current-change="handlePageChange"
    ></el-pagination>

    <el-dialog
      title="报名详情"
      :visible.sync="detailDialogVisible"
      width="600px"
    >
      <div v-if="currentRecord">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="申请人姓名">{{ currentRecord.applicantName }}</el-descriptions-item>
          <el-descriptions-item label="身份证号">{{ currentRecord.idCard }}</el-descriptions-item>
          <el-descriptions-item label="手机号码">{{ currentRecord.phone }}</el-descriptions-item>
          <el-descriptions-item label="电子邮箱">{{ currentRecord.email }}</el-descriptions-item>
          <el-descriptions-item label="报考科目" :span="2">{{ currentRecord.subjectName }}</el-descriptions-item>
          <el-descriptions-item label="科目代码">{{ currentRecord.subjectCode }}</el-descriptions-item>
          <el-descriptions-item label="考试时间">{{ currentRecord.examDate }} {{ currentRecord.examTime }}</el-descriptions-item>
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
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="驳回申请"
      :visible.sync="rejectDialogVisible"
      width="500px"
    >
      <el-form :model="rejectForm" label-width="100px">
        <el-form-item label="驳回原因">
          <el-input
            v-model="rejectForm.reason"
            type="textarea"
            :rows="4"
            placeholder="请输入驳回原因"
            maxlength="200"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rejectDialogVisible = false">取消</el-button>
        <el-button type="danger" @click="confirmReject" :loading="rejectLoading">确认驳回</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { applicationRecords, applyStatusMap, applyStatusTagType, ticketList } from '@/mock/data.js'

export default {
  name: 'ReviewPage',
  data() {
    return {
      records: applicationRecords,
      ticketList,
      applyStatusMap,
      applyStatusTagType,
      searchForm: {
        applicantName: '',
        status: ''
      },
      detailDialogVisible: false,
      rejectDialogVisible: false,
      currentRecord: null,
      rejectForm: {
        reason: ''
      },
      rejectLoading: false,
      pageSize: 10,
      currentPage: 1
    }
  },
  computed: {
    filteredRecords() {
      let result = this.records
      
      if (this.searchForm.applicantName) {
        const keyword = this.searchForm.applicantName.toLowerCase()
        result = result.filter(item => 
          item.applicantName.toLowerCase().includes(keyword)
        )
      }
      
      if (this.searchForm.status) {
        result = result.filter(item => item.status === this.searchForm.status)
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
    maskIdCard(idCard) {
      if (!idCard) return ''
      return idCard.substring(0, 6) + '********' + idCard.substring(14)
    },
    handleSearch() {
      this.currentPage = 1
    },
    handlePageChange() {
    },
    resetSearch() {
      this.searchForm = {
        applicantName: '',
        status: ''
      }
      this.currentPage = 1
    },
    viewDetail(row) {
      this.currentRecord = row
      this.detailDialogVisible = true
    },
    generateTicketNo(recordId) {
      const now = new Date()
      const year = now.getFullYear()
      return `${year}${String(recordId).padStart(6, '0')}${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`
    },
    approve(row) {
      this.$confirm('确认审核通过该报名申请？系统将自动生成准考证。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = 2
        row.reviewTime = this.getCurrentTime()
        row.reviewer = '当前管理员'
        
        if (!row.ticketNo) {
          row.ticketNo = this.generateTicketNo(row.id)
          row.roomNo = '第' + String(Math.floor(Math.random() * 30) + 1).padStart(2, '0') + '考场'
          row.seatNo = String(Math.floor(Math.random() * 30) + 1).padStart(2, '0') + '号'
          row.examSite = '第一考点'
          row.examAddress = '北京市海淀区中关村大街1号'
          
          this.ticketList.push({
            id: row.id,
            ticketNo: row.ticketNo,
            applicantName: row.applicantName,
            idCard: row.idCard,
            subjectId: row.subjectId,
            subjectName: row.subjectName,
            subjectCode: row.subjectCode,
            examDate: row.examDate,
            examTime: row.examTime,
            roomNo: row.roomNo,
            seatNo: row.seatNo,
            examSite: row.examSite,
            examAddress: row.examAddress,
            createTime: this.getCurrentTime()
          })
        }
        
        this.$message.success('审核通过，准考证已自动生成')
      }).catch(() => {})
    },
    reject(row) {
      this.currentRecord = row
      this.rejectForm.reason = ''
      this.rejectDialogVisible = true
    },
    confirmReject() {
      if (!this.rejectForm.reason.trim()) {
        this.$message.warning('请输入驳回原因')
        return
      }
      
      this.rejectLoading = true
      
      setTimeout(() => {
        this.currentRecord.status = 3
        this.currentRecord.reviewTime = this.getCurrentTime()
        this.currentRecord.reviewer = '当前管理员'
        this.currentRecord.rejectReason = this.rejectForm.reason
        
        this.rejectLoading = false
        this.rejectDialogVisible = false
        this.$message.success('已驳回申请')
      }, 800)
    },
    getCurrentTime() {
      const now = new Date()
      const year = now.getFullYear()
      const month = String(now.getMonth() + 1).padStart(2, '0')
      const day = String(now.getDate()).padStart(2, '0')
      const hours = String(now.getHours()).padStart(2, '0')
      const minutes = String(now.getMinutes()).padStart(2, '0')
      const seconds = String(now.getSeconds()).padStart(2, '0')
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    },
    viewTicket(row) {
      this.$router.push({
        path: '/ticket',
        query: { idCard: row.idCard, name: row.applicantName, autoQuery: 'true' }
      })
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
