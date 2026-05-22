<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">应聘记录</h2>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="候选人">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" clearable style="width: 150px;"></el-input>
        </el-form-item>
        <el-form-item label="手机号码">
          <el-input v-model="searchForm.phone" placeholder="请输入手机号" clearable style="width: 150px;"></el-input>
        </el-form-item>
        <el-form-item label="应聘岗位">
          <el-select v-model="searchForm.jobName" placeholder="请选择岗位" clearable style="width: 180px;">
            <el-option v-for="item in jobOptions" :key="item.id" :label="item.name" :value="item.name"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="进度状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 150px;">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="申请日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="面试日期">
          <el-date-picker
            v-model="searchForm.interviewDate"
            type="date"
            placeholder="选择面试日期"
            clearable>
          </el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="paginatedList" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" align="center"></el-table-column>
        <el-table-column prop="name" label="候选人" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="手机号码" width="130" align="center"></el-table-column>
        <el-table-column prop="email" label="电子邮箱" min-width="180"></el-table-column>
        <el-table-column prop="jobName" label="应聘岗位" min-width="150"></el-table-column>
        <el-table-column label="简历" width="120" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="mini" icon="el-icon-download" @click="handleDownload(scope.row)">
              {{ scope.row.resume }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="applyTime" label="申请时间" width="120" align="center"></el-table-column>
        <el-table-column label="面试时间" width="160" align="center">
          <template slot-scope="scope">
            <span v-if="getInterviewInfo(scope.row).time">{{ getInterviewInfo(scope.row).time }}</span>
            <span v-else style="color: #909399;">-</span>
          </template>
        </el-table-column>
        <el-table-column label="面试官" width="120" align="center">
          <template slot-scope="scope">
            <span v-if="getInterviewInfo(scope.row).interviewer">{{ getInterviewInfo(scope.row).interviewer }}</span>
            <span v-else style="color: #909399;">-</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="110" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="text" icon="el-icon-view" @click="handleView(scope.row)">详情</el-button>
            <el-button size="mini" type="text" icon="el-icon-time" @click="handleSchedule(scope.row)" v-if="scope.row.status === '待面试' || scope.row.status === '面试中'">安排面试</el-button>
            <el-button size="mini" type="text" icon="el-icon-edit" @click="handleUpdateStatus(scope.row)">更新状态</el-button>
            <el-button size="mini" type="text" icon="el-icon-delete" style="color: #F56C6C" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredList.length">
      </el-pagination>
    </div>

    <el-dialog title="应聘详情" :visible.sync="detailVisible" width="750px">
      <el-descriptions :column="2" border v-if="currentApplication">
        <el-descriptions-item label="姓名">{{ currentApplication.name }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentApplication.phone }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentApplication.email }}</el-descriptions-item>
        <el-descriptions-item label="应聘岗位">{{ currentApplication.jobName }}</el-descriptions-item>
        <el-descriptions-item label="申请时间">{{ currentApplication.applyTime }}</el-descriptions-item>
        <el-descriptions-item label="简历">{{ currentApplication.resume }}</el-descriptions-item>
        <el-descriptions-item label="当前状态" :span="2">
          <el-tag :type="getStatusType(currentApplication.status)">{{ currentApplication.status }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
      
      <el-divider>面试记录</el-divider>
      <el-table v-if="interviewRecords.length > 0" :data="interviewRecords" size="small" border>
        <el-table-column prop="type" label="面试类型" width="100" align="center"></el-table-column>
        <el-table-column prop="interviewer" label="面试官" width="120" align="center"></el-table-column>
        <el-table-column prop="time" label="面试时间" width="160" align="center"></el-table-column>
        <el-table-column prop="location" label="面试地点" width="100" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="80" align="center">
          <template slot-scope="scope">
            <el-tag size="mini" :type="scope.row.status === '已完成' ? 'success' : 'info'">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="result" label="结果" width="80" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.result" size="mini" :type="scope.row.result === '通过' ? 'success' : scope.row.result === '不通过' ? 'danger' : 'warning'">
              {{ scope.row.result }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无面试记录"></el-empty>
      
      <el-divider>状态流转记录</el-divider>
      <el-timeline>
        <el-timeline-item
          v-for="(item, index) in statusHistory"
          :key="index"
          :timestamp="item.time"
          placement="top">
          <el-card shadow="never">
            <h4>{{ item.status }}</h4>
            <p>{{ item.remark || '状态已更新' }}</p>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-dialog>

    <el-dialog title="更新状态" :visible.sync="statusVisible" width="500px">
      <el-form :model="statusForm" :rules="statusRules" ref="statusForm" label-width="100px">
        <el-form-item label="当前状态">
          <el-tag :type="getStatusType(currentApplication ? currentApplication.status : '')">
            {{ currentApplication ? currentApplication.status : '' }}
          </el-tag>
        </el-form-item>
        <el-form-item label="更新为" prop="status">
          <el-select v-model="statusForm.status" placeholder="请选择新状态" style="width: 100%;">
            <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="statusForm.remark" :rows="3" placeholder="请输入状态变更备注"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="statusVisible = false">取消</el-button>
        <el-button type="primary" @click="handleStatusSubmit">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { jobList, statusOptions } from '@/mock/data.js'
import { store } from '@/store/index.js'

export default {
  name: 'Applications',
  data() {
    return {
      searchForm: {
        name: '',
        phone: '',
        jobName: '',
        status: '',
        dateRange: [],
        interviewDate: ''
      },
      currentPage: 1,
      pageSize: 10,
      detailVisible: false,
      statusVisible: false,
      currentApplication: null,
      statusForm: {
        status: '',
        remark: ''
      },
      statusRules: {
        status: [{ required: true, message: '请选择更新状态', trigger: 'change' }]
      },
      jobOptions: jobList,
      statusOptions,
      interviewRecords: [],
      statusHistory: []
    }
  },
  computed: {
    list() {
      return store.applications
    },
    interviews() {
      return store.interviews
    },
    filteredList() {
      return this.list.filter(item => {
        const matchName = !this.searchForm.name || item.name.includes(this.searchForm.name)
        const matchPhone = !this.searchForm.phone || item.phone.includes(this.searchForm.phone)
        const matchJob = !this.searchForm.jobName || item.jobName === this.searchForm.jobName
        const matchStatus = !this.searchForm.status || item.status === this.searchForm.status
        
        let matchDate = true
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          const startTime = this.searchForm.dateRange[0].toISOString().split('T')[0]
          const endTime = this.searchForm.dateRange[1].toISOString().split('T')[0]
          matchDate = item.applyTime >= startTime && item.applyTime <= endTime
        }
        
        let matchInterviewDate = true
        if (this.searchForm.interviewDate) {
          const searchDate = this.searchForm.interviewDate.toISOString().split('T')[0]
          const interviewInfo = this.getInterviewInfo(item)
          matchInterviewDate = interviewInfo.time && interviewInfo.time.includes(searchDate)
        }
        
        return matchName && matchPhone && matchJob && matchStatus && matchDate && matchInterviewDate
      })
    },
    paginatedList() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredList.slice(start, end)
    }
  },
  methods: {
    getStatusType(status) {
      const typeMap = {
        '待审核': 'info',
        '待面试': 'warning',
        '面试中': 'primary',
        '待录用': 'warning',
        '已录用': 'success',
        '已拒绝': 'danger'
      }
      return typeMap[status] || 'info'
    },
    getInterviewInfo(application) {
      const interview = this.interviews.find(item => 
        item.candidateName === application.name
      )
      return interview ? { time: interview.time, interviewer: interview.interviewer } : {}
    },
    handleSearch() {
      this.currentPage = 1
    },
    handleReset() {
      this.searchForm = { name: '', phone: '', jobName: '', status: '', dateRange: [], interviewDate: '' }
      this.currentPage = 1
    },
    handleView(row) {
      this.currentApplication = row
      this.interviewRecords = this.interviews.filter(item => item.candidateName === row.name)
      this.statusHistory = [
        { time: row.applyTime, status: '简历提交', remark: '候选人已提交简历申请' },
        { time: row.applyTime, status: '待审核', remark: '简历等待HR审核' },
        { time: row.applyTime, status: row.status, remark: '当前状态' }
      ]
      this.detailVisible = true
    },
    handleDownload(row) {
      this.$message.info(`正在下载简历：${row.resume}`)
    },
    handleSchedule(row) {
      this.$router.push({ path: '/interview', query: { candidate: row.name, job: row.jobName } })
    },
    handleUpdateStatus(row) {
      this.currentApplication = row
      this.statusForm = { status: '', remark: '' }
      this.statusVisible = true
    },
    handleStatusSubmit() {
      this.$refs.statusForm.validate((valid) => {
        if (valid) {
          store.updateApplicationStatus(this.currentApplication.id, this.statusForm.status)
          this.$message.success('状态更新成功')
          this.statusVisible = false
        }
      })
    },
    handleDelete(row) {
      this.$confirm(`确定要删除"${row.name}"的应聘记录吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.list.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.list.splice(index, 1)
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style lang="scss" scoped>
.search-form {
  margin-bottom: 0;
}
</style>
