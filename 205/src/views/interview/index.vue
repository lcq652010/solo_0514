<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">面试安排</h2>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增面试</el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="候选人">
          <el-input v-model="searchForm.candidateName" placeholder="请输入候选人姓名" clearable></el-input>
        </el-form-item>
        <el-form-item label="面试岗位">
          <el-input v-model="searchForm.jobName" placeholder="请输入岗位名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="面试官">
          <el-select v-model="searchForm.interviewer" placeholder="请选择面试官" clearable style="width: 180px;">
            <el-option v-for="item in interviewerOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 150px;">
            <el-option label="未开始" value="未开始"></el-option>
            <el-option label="进行中" value="进行中"></el-option>
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="已取消" value="已取消"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试日期">
          <el-date-picker
            v-model="searchForm.date"
            type="date"
            placeholder="选择日期"
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
        <el-table-column prop="candidateName" label="候选人" width="100" align="center"></el-table-column>
        <el-table-column prop="jobName" label="面试岗位" min-width="150"></el-table-column>
        <el-table-column prop="type" label="面试类型" width="100" align="center"></el-table-column>
        <el-table-column prop="interviewer" label="面试官" width="130" align="center"></el-table-column>
        <el-table-column prop="time" label="面试时间" width="160" align="center"></el-table-column>
        <el-table-column prop="location" label="面试地点" width="100" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="面试结果" width="100" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.result" :type="getResultType(scope.row.result)">
              {{ scope.row.result }}
            </el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="text" icon="el-icon-view" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="text" icon="el-icon-edit" @click="handleEdit(scope.row)" :disabled="scope.row.status === '已完成'">编辑</el-button>
            <el-button size="mini" type="text" icon="el-icon-check" @click="handleResult(scope.row)" v-if="scope.row.status === '未开始' || scope.row.status === '进行中'">录入结果</el-button>
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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px" @close="handleDialogClose">
      <el-form :model="interviewForm" :rules="interviewRules" ref="interviewForm" label-width="100px">
        <el-form-item label="候选人" prop="candidateName">
          <el-select v-model="interviewForm.candidateName" placeholder="请选择候选人" filterable style="width: 100%;">
            <el-option
              v-for="item in candidateOptions"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试岗位" prop="jobName">
          <el-select v-model="interviewForm.jobName" placeholder="请选择岗位" filterable style="width: 100%;">
            <el-option
              v-for="item in jobOptions"
              :key="item.id"
              :label="item.name"
              :value="item.name">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试类型" prop="type">
          <el-select v-model="interviewForm.type" placeholder="请选择面试类型" style="width: 100%;">
            <el-option v-for="item in interviewTypeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试官" prop="interviewer">
          <el-select v-model="interviewForm.interviewer" placeholder="请选择面试官" style="width: 100%;" @change="handleInterviewerChange">
            <el-option v-for="item in interviewerOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="面试时间" prop="time">
          <el-date-picker
            v-model="interviewForm.time"
            type="datetime"
            placeholder="选择面试时间"
            style="width: 100%;"
            :disabled-date="disabledDate"
            :disabled-hours="disabledHours"
            :disabled-minutes="disabledMinutes"
            format="yyyy-MM-dd HH:mm"
            value-format="yyyy-MM-dd HH:mm">
          </el-date-picker>
          <div v-if="busyTimes.length > 0" class="busy-tip">
            <i class="el-icon-warning" style="color: #E6A23C;"></i>
            <span style="color: #E6A23C; margin-left: 5px;">该面试官已有安排：{{ busyTimes.join('、') }}</span>
          </div>
        </el-form-item>
        <el-form-item label="面试地点" prop="location">
          <el-input v-model="interviewForm.location" placeholder="请输入面试地点"></el-input>
        </el-form-item>
        <el-form-item label="面试状态" prop="status">
          <el-radio-group v-model="interviewForm.status">
            <el-radio label="未开始">未开始</el-radio>
            <el-radio label="进行中">进行中</el-radio>
            <el-radio label="已完成">已完成</el-radio>
            <el-radio label="已取消">已取消</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="interviewForm.remark" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </span>
    </el-dialog>

    <el-dialog title="面试详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="候选人">{{ interviewDetail.candidateName }}</el-descriptions-item>
        <el-descriptions-item label="面试岗位">{{ interviewDetail.jobName }}</el-descriptions-item>
        <el-descriptions-item label="面试类型">{{ interviewDetail.type }}</el-descriptions-item>
        <el-descriptions-item label="面试官">{{ interviewDetail.interviewer }}</el-descriptions-item>
        <el-descriptions-item label="面试时间">{{ interviewDetail.time }}</el-descriptions-item>
        <el-descriptions-item label="面试地点">{{ interviewDetail.location }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(interviewDetail.status)">{{ interviewDetail.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="面试结果">
          <el-tag v-if="interviewDetail.result" :type="getResultType(interviewDetail.result)">
            {{ interviewDetail.result }}
          </el-tag>
          <span v-else>-</span>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ interviewDetail.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog title="录入面试结果" :visible.sync="resultVisible" width="500px">
      <el-form :model="resultForm" :rules="resultRules" ref="resultForm" label-width="100px">
        <el-form-item label="面试结果" prop="result">
          <el-radio-group v-model="resultForm.result">
            <el-radio label="通过">通过</el-radio>
            <el-radio label="不通过">不通过</el-radio>
            <el-radio label="待定">待定</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="评价" prop="comment">
          <el-input type="textarea" v-model="resultForm.comment" :rows="4" placeholder="请输入面试评价"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resultVisible = false">取消</el-button>
        <el-button type="primary" @click="handleResultSubmit">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { interviewerOptions, interviewTypeOptions, applicationList, jobList } from '@/mock/data.js'
import { store } from '@/store/index.js'

export default {
  name: 'Interview',
  data() {
    return {
      searchForm: {
        candidateName: '',
        jobName: '',
        interviewer: '',
        status: '',
        date: ''
      },
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogType: 'add',
      dialogTitle: '新增面试',
      detailVisible: false,
      interviewDetail: {},
      resultVisible: false,
      currentInterview: null,
      resultForm: {
        result: '',
        comment: ''
      },
      resultRules: {
        result: [{ required: true, message: '请选择面试结果', trigger: 'change' }],
        comment: [{ required: true, message: '请输入面试评价', trigger: 'blur' }]
      },
      interviewForm: {
        id: null,
        candidateName: '',
        jobName: '',
        type: '',
        interviewer: '',
        time: '',
        location: '',
        status: '未开始',
        remark: ''
      },
      interviewRules: {
        candidateName: [{ required: true, message: '请选择候选人', trigger: 'change' }],
        jobName: [{ required: true, message: '请选择面试岗位', trigger: 'change' }],
        type: [{ required: true, message: '请选择面试类型', trigger: 'change' }],
        interviewer: [{ required: true, message: '请选择面试官', trigger: 'change' }],
        time: [{ required: true, message: '请选择面试时间', trigger: 'change' }],
        location: [{ required: true, message: '请输入面试地点', trigger: 'blur' }],
        status: [{ required: true, message: '请选择面试状态', trigger: 'change' }]
      },
      interviewerOptions,
      interviewTypeOptions,
      candidateOptions: applicationList,
      jobOptions: jobList.filter(item => item.status === '招聘中'),
      busyTimes: []
    }
  },
  computed: {
    list() {
      return store.interviews
    },
    filteredList() {
      return this.list.filter(item => {
        const matchName = !this.searchForm.candidateName || item.candidateName.includes(this.searchForm.candidateName)
        const matchJob = !this.searchForm.jobName || item.jobName.includes(this.searchForm.jobName)
        const matchInterviewer = !this.searchForm.interviewer || item.interviewer === this.searchForm.interviewer
        const matchStatus = !this.searchForm.status || item.status === this.searchForm.status
        let matchDate = true
        if (this.searchForm.date) {
          const searchDate = this.searchForm.date.toISOString().split('T')[0]
          matchDate = item.time.includes(searchDate)
        }
        return matchName && matchJob && matchInterviewer && matchStatus && matchDate
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
        '未开始': 'info',
        '进行中': 'warning',
        '已完成': 'success',
        '已取消': 'danger'
      }
      return typeMap[status] || 'info'
    },
    getResultType(result) {
      const typeMap = {
        '通过': 'success',
        '不通过': 'danger',
        '待定': 'warning'
      }
      return typeMap[result] || 'info'
    },
    handleInterviewerChange() {
      if (this.interviewForm.interviewer) {
        this.busyTimes = store.getInterviewerBusyTimes(this.interviewForm.interviewer, this.interviewForm.id)
      } else {
        this.busyTimes = []
      }
    },
    disabledDate(time) {
      return time.getTime() < Date.now() - 8.64e7
    },
    disabledHours() {
      if (!this.interviewForm.interviewer) return []
      return []
    },
    disabledMinutes(hour) {
      if (!this.interviewForm.interviewer) return []
      const busyTimes = store.getInterviewerBusyTimes(this.interviewForm.interviewer, this.interviewForm.id)
      const disabled = []
      busyTimes.forEach(timeStr => {
        const [datePart, timePart] = timeStr.split(' ')
        const [h, m] = timePart.split(':').map(Number)
        if (this.interviewForm.time) {
          const selectedDate = new Date(this.interviewForm.time).toISOString().split('T')[0]
          if (datePart === selectedDate && h === hour) {
            for (let i = m; i < m + 60 && i < 60; i++) {
              if (!disabled.includes(i)) {
                disabled.push(i)
              }
            }
          }
        }
      })
      return disabled
    },
    checkTimeConflict() {
      const { interviewer, time, id } = this.interviewForm
      if (!interviewer || !time) return null
      
      const interviewDuration = 60
      const newStartTime = new Date(time).getTime()
      const newEndTime = newStartTime + interviewDuration * 60 * 1000
      
      for (const item of this.list) {
        if (item.id === id || item.status === '已取消' || item.status === '已完成') continue
        if (item.interviewer !== interviewer) continue
        
        const existStartTime = new Date(item.time).getTime()
        const existEndTime = existStartTime + interviewDuration * 60 * 1000
        
        if ((newStartTime >= existStartTime && newStartTime < existEndTime) ||
            (newEndTime > existStartTime && newEndTime <= existEndTime) ||
            (newStartTime <= existStartTime && newEndTime >= existEndTime)) {
          return item
        }
      }
      return null
    },
    handleSearch() {
      this.currentPage = 1
    },
    handleReset() {
      this.searchForm = { candidateName: '', jobName: '', interviewer: '', status: '', date: '' }
      this.currentPage = 1
    },
    handleAdd() {
      this.dialogType = 'add'
      this.dialogTitle = '新增面试'
      this.resetForm()
      this.busyTimes = []
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogType = 'edit'
      this.dialogTitle = '编辑面试'
      this.interviewForm = { ...row }
      this.handleInterviewerChange()
      this.dialogVisible = true
    },
    handleView(row) {
      this.interviewDetail = { ...row }
      this.detailVisible = true
    },
    handleResult(row) {
      this.currentInterview = row
      this.resultForm = { result: '', comment: '' }
      this.resultVisible = true
    },
    handleResultSubmit() {
      this.$refs.resultForm.validate((valid) => {
        if (valid) {
          store.updateInterviewResult(this.currentInterview.id, this.resultForm.result)
          this.$message.success('面试结果已提交，状态已同步更新')
          this.resultVisible = false
        }
      })
    },
    handleDelete(row) {
      this.$confirm(`确定要删除"${row.candidateName}"的面试安排吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        store.deleteInterview(row.id)
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.interviewForm.validate((valid) => {
        if (valid) {
          const conflict = this.checkTimeConflict()
          if (conflict) {
            this.$message.error(`面试官"${conflict.interviewer}"在 ${conflict.time} 已有面试安排（${conflict.candidateName} - ${conflict.type}），请选择其他时间！`)
            return
          }
          
          if (this.dialogType === 'add') {
            const newId = Math.max(...this.list.map(item => item.id), 0) + 1
            store.addInterview({ ...this.interviewForm, id: newId })
            this.$message.success('新增成功')
          } else {
            store.updateInterview(this.interviewForm.id, { ...this.interviewForm })
            this.$message.success('编辑成功')
          }
          this.dialogVisible = false
        }
      })
    },
    handleDialogClose() {
      this.resetForm()
      this.busyTimes = []
    },
    resetForm() {
      this.interviewForm = {
        id: null,
        candidateName: '',
        jobName: '',
        type: '',
        interviewer: '',
        time: '',
        location: '',
        status: '未开始',
        remark: ''
      }
      this.$nextTick(() => {
        if (this.$refs.interviewForm) {
          this.$refs.interviewForm.clearValidate()
        }
      })
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

.busy-tip {
  margin-top: 8px;
  font-size: 12px;
}
</style>
