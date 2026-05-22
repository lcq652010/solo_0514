<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">录用管理</h2>
      <el-button type="primary" icon="el-icon-plus" @click="handleAdd">发放Offer</el-button>
    </div>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="候选人">
          <el-input v-model="searchForm.candidateName" placeholder="请输入姓名" clearable></el-input>
        </el-form-item>
        <el-form-item label="岗位">
          <el-input v-model="searchForm.jobName" placeholder="请输入岗位名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 150px;">
            <el-option label="待确认" value="待确认"></el-option>
            <el-option label="已接受" value="已接受"></el-option>
            <el-option label="已拒绝" value="已拒绝"></el-option>
            <el-option label="已入职" value="已入职"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="发放日期">
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
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="filteredList" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="60" align="center"></el-table-column>
        <el-table-column prop="candidateName" label="候选人" width="100" align="center"></el-table-column>
        <el-table-column prop="jobName" label="录用岗位" min-width="150"></el-table-column>
        <el-table-column prop="salary" label="薪资" width="100" align="center"></el-table-column>
        <el-table-column prop="offerTime" label="Offer发放时间" width="140" align="center"></el-table-column>
        <el-table-column prop="entryTime" label="预计入职时间" width="140" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="text" icon="el-icon-view" @click="handleView(scope.row)">详情</el-button>
            <el-button size="mini" type="text" icon="el-icon-edit" @click="handleEdit(scope.row)" v-if="scope.row.status === '待确认'">编辑</el-button>
            <el-button size="mini" type="text" icon="el-icon-message" @click="handleSend(scope.row)" v-if="scope.row.status === '待确认'">重新发送</el-button>
            <el-button size="mini" type="text" icon="el-icon-check" @click="handleEntry(scope.row)" v-if="scope.row.status === '已接受'">确认入职</el-button>
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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="650px" @close="handleDialogClose">
      <el-form :model="offerForm" :rules="offerRules" ref="offerForm" label-width="120px">
        <el-divider content-position="left">基本信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="候选人" prop="candidateName">
              <el-select v-model="offerForm.candidateName" placeholder="请选择候选人" filterable style="width: 100%;">
                <el-option
                  v-for="item in candidateOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.name">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="录用岗位" prop="jobName">
              <el-select v-model="offerForm.jobName" placeholder="请选择岗位" filterable style="width: 100%;">
                <el-option
                  v-for="item in jobOptions"
                  :key="item.id"
                  :label="item.name"
                  :value="item.name">
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="薪资" prop="salary">
              <el-input v-model="offerForm.salary" placeholder="如：20k"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="试用期" prop="probation">
              <el-select v-model="offerForm.probation" placeholder="请选择试用期" style="width: 100%;">
                <el-option label="1个月" value="1个月"></el-option>
                <el-option label="2个月" value="2个月"></el-option>
                <el-option label="3个月" value="3个月"></el-option>
                <el-option label="6个月" value="6个月"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="Offer发放时间" prop="offerTime">
              <el-date-picker
                v-model="offerForm.offerTime"
                type="date"
                placeholder="选择发放日期"
                style="width: 100%;">
              </el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计入职时间" prop="entryTime">
              <el-date-picker
                v-model="offerForm.entryTime"
                type="date"
                placeholder="选择入职日期"
                style="width: 100%;">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="工作地点" prop="location">
              <el-input v-model="offerForm.location" placeholder="请输入工作地点"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="合同期限" prop="contractPeriod">
              <el-select v-model="offerForm.contractPeriod" placeholder="请选择合同期限" style="width: 100%;">
                <el-option label="1年" value="1年"></el-option>
                <el-option label="2年" value="2年"></el-option>
                <el-option label="3年" value="3年"></el-option>
                <el-option label="5年" value="5年"></el-option>
                <el-option label="无固定期限" value="无固定期限"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider content-position="left">福利待遇</el-divider>
        <el-form-item label="福利说明" prop="benefits">
          <el-input type="textarea" v-model="offerForm.benefits" :rows="4" placeholder="请描述福利待遇，如五险一金、年终奖、带薪年假等"></el-input>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="offerForm.remark" :rows="3" placeholder="请输入其他备注信息"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确认发放</el-button>
      </span>
    </el-dialog>

    <el-dialog title="Offer详情" :visible.sync="detailVisible" width="650px">
      <el-descriptions :column="2" border v-if="offerDetail">
        <el-descriptions-item label="候选人">{{ offerDetail.candidateName }}</el-descriptions-item>
        <el-descriptions-item label="录用岗位">{{ offerDetail.jobName }}</el-descriptions-item>
        <el-descriptions-item label="薪资">{{ offerDetail.salary }}</el-descriptions-item>
        <el-descriptions-item label="试用期">{{ offerDetail.probation || '3个月' }}</el-descriptions-item>
        <el-descriptions-item label="Offer发放时间">{{ offerDetail.offerTime }}</el-descriptions-item>
        <el-descriptions-item label="预计入职时间">{{ offerDetail.entryTime }}</el-descriptions-item>
        <el-descriptions-item label="工作地点">{{ offerDetail.location || '公司指定' }}</el-descriptions-item>
        <el-descriptions-item label="合同期限">{{ offerDetail.contractPeriod || '3年' }}</el-descriptions-item>
        <el-descriptions-item label="状态" :span="2">
          <el-tag :type="getStatusType(offerDetail.status)">{{ offerDetail.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="福利待遇" :span="2">{{ offerDetail.benefits || '五险一金、年终奖、带薪年假' }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ offerDetail.remark || '-' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { offerList, applicationList, jobList } from '@/mock/data.js'

export default {
  name: 'Offer',
  data() {
    return {
      list: [...offerList],
      searchForm: {
        candidateName: '',
        jobName: '',
        status: '',
        dateRange: []
      },
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogType: 'add',
      dialogTitle: '发放Offer',
      detailVisible: false,
      offerDetail: {},
      offerForm: {
        id: null,
        candidateName: '',
        jobName: '',
        salary: '',
        probation: '3个月',
        offerTime: '',
        entryTime: '',
        location: '',
        contractPeriod: '3年',
        benefits: '五险一金、年终奖、带薪年假、节日福利',
        remark: '',
        status: '待确认'
      },
      offerRules: {
        candidateName: [{ required: true, message: '请选择候选人', trigger: 'change' }],
        jobName: [{ required: true, message: '请选择录用岗位', trigger: 'change' }],
        salary: [{ required: true, message: '请输入薪资', trigger: 'blur' }],
        probation: [{ required: true, message: '请选择试用期', trigger: 'change' }],
        offerTime: [{ required: true, message: '请选择Offer发放时间', trigger: 'change' }],
        entryTime: [{ required: true, message: '请选择预计入职时间', trigger: 'change' }]
      },
      candidateOptions: applicationList.filter(item => item.status === '待录用' || item.status === '面试中'),
      jobOptions: jobList.filter(item => item.status === '招聘中')
    }
  },
  computed: {
    filteredList() {
      return this.list.filter(item => {
        const matchName = !this.searchForm.candidateName || item.candidateName.includes(this.searchForm.candidateName)
        const matchJob = !this.searchForm.jobName || item.jobName.includes(this.searchForm.jobName)
        const matchStatus = !this.searchForm.status || item.status === this.searchForm.status
        let matchDate = true
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          const startTime = this.searchForm.dateRange[0].toISOString().split('T')[0]
          const endTime = this.searchForm.dateRange[1].toISOString().split('T')[0]
          matchDate = item.offerTime >= startTime && item.offerTime <= endTime
        }
        return matchName && matchJob && matchStatus && matchDate
      })
    }
  },
  methods: {
    getStatusType(status) {
      const typeMap = {
        '待确认': 'warning',
        '已接受': 'primary',
        '已拒绝': 'danger',
        '已入职': 'success'
      }
      return typeMap[status] || 'info'
    },
    handleSearch() {
      this.currentPage = 1
    },
    handleReset() {
      this.searchForm = { candidateName: '', jobName: '', status: '', dateRange: [] }
      this.currentPage = 1
    },
    handleAdd() {
      this.dialogType = 'add'
      this.dialogTitle = '发放Offer'
      this.resetForm()
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogType = 'edit'
      this.dialogTitle = '编辑Offer'
      this.offerForm = { ...row }
      this.dialogVisible = true
    },
    handleView(row) {
      this.offerDetail = { ...row }
      this.detailVisible = true
    },
    handleSend(row) {
      this.$confirm(`确定要重新发送Offer给"${row.candidateName}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'info'
      }).then(() => {
        this.$message.success('Offer已重新发送')
      }).catch(() => {})
    },
    handleEntry(row) {
      this.$confirm(`确认"${row.candidateName}"已入职吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        const index = this.list.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.list[index].status = '已入职'
        }
        this.$message.success('已确认入职')
      }).catch(() => {})
    },
    handleDelete(row) {
      this.$confirm(`确定要删除"${row.candidateName}"的Offer记录吗？`, '提示', {
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
    handleSubmit() {
      this.$refs.offerForm.validate((valid) => {
        if (valid) {
          if (this.dialogType === 'add') {
            const newId = Math.max(...this.list.map(item => item.id)) + 1
            this.list.push({ ...this.offerForm, id: newId })
            this.$message.success('Offer发放成功')
          } else {
            const index = this.list.findIndex(item => item.id === this.offerForm.id)
            if (index > -1) {
              this.list.splice(index, 1, { ...this.offerForm })
            }
            this.$message.success('Offer更新成功')
          }
          this.dialogVisible = false
        }
      })
    },
    handleDialogClose() {
      this.resetForm()
    },
    resetForm() {
      this.offerForm = {
        id: null,
        candidateName: '',
        jobName: '',
        salary: '',
        probation: '3个月',
        offerTime: '',
        entryTime: '',
        location: '',
        contractPeriod: '3年',
        benefits: '五险一金、年终奖、带薪年假、节日福利',
        remark: '',
        status: '待确认'
      }
      this.$nextTick(() => {
        if (this.$refs.offerForm) {
          this.$refs.offerForm.clearValidate()
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
</style>
