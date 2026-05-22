<template>
  <div class="report-query">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="记录编号">
          <el-input v-model="searchForm.recordId" placeholder="请输入记录编号" style="width: 180px"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="searchForm.name" placeholder="请输入姓名" style="width: 150px"></el-input>
        </el-form-item>
        <el-form-item label="手机号码">
          <el-input v-model="searchForm.phone" placeholder="请输入手机号" style="width: 180px"></el-input>
        </el-form-item>
        <el-form-item label="身份证号">
          <el-input v-model="searchForm.idCard" placeholder="请输入身份证号" style="width: 220px"></el-input>
        </el-form-item>
        <el-form-item label="报告类型">
          <el-select v-model="searchForm.reportType" placeholder="请选择" style="width: 150px">
            <el-option label="全部" value=""></el-option>
            <el-option label="主报告" value="main"></el-option>
            <el-option label="检验报告" value="lab"></el-option>
            <el-option label="影像报告" value="image"></el-option>
            <el-option label="其他" value="other"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上传时间">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 280px"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table :data="tableData" border style="width: 100%" v-loading="loading" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="id" label="报告ID" width="80" align="center"></el-table-column>
        <el-table-column prop="recordId" label="记录编号" width="120" align="center"></el-table-column>
        <el-table-column prop="name" label="姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="手机号码" width="130" align="center"></el-table-column>
        <el-table-column prop="packageName" label="体检套餐" min-width="180"></el-table-column>
        <el-table-column prop="reportName" label="报告名称" min-width="180"></el-table-column>
        <el-table-column prop="reportType" label="报告类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getReportTypeColor(scope.row.reportType)" size="small">
              {{ getReportTypeName(scope.row.reportType) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="fileName" label="文件名" min-width="180" show-overflow-tooltip></el-table-column>
        <el-table-column prop="uploadTime" label="上传时间" width="160" align="center"></el-table-column>
        <el-table-column prop="uploader" label="上传人" width="100" align="center"></el-table-column>
        <el-table-column label="操作" width="260" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="openVerifyDialog(scope.row, 'view')">
              查看详情
            </el-button>
            <el-button type="success" size="mini" @click="openVerifyDialog(scope.row, 'download')">
              下载
            </el-button>
            <el-button type="danger" size="mini" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 20px">
        <el-button type="danger" @click="handleBatchDelete" :disabled="selectedRows.length === 0">
          批量删除 ({{ selectedRows.length }})
        </el-button>
      </div>

      <el-pagination
        class="pagination"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.size"
        layout="total, sizes, prev, pager, next, jumper"
        :total="pagination.total"
      ></el-pagination>
    </el-card>

    <el-dialog
      title="身份验证"
      :visible.sync="verifyVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="verifyForm" :rules="verifyRules" ref="verifyFormRef" label-width="100px">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="verifyForm.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="手机号码" prop="phone">
          <el-input v-model="verifyForm.inputPhone" placeholder="请输入手机号码"></el-input>
        </el-form-item>
        <el-form-item label="身份证号" prop="idCard">
          <el-input v-model="verifyForm.inputIdCard" placeholder="请输入身份证号"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="verifyVisible = false">取消</el-button>
        <el-button type="primary" @click="handleVerify">验证并{{ currentAction === 'view' ? '查看' : '下载' }}</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="报告详情"
      :visible.sync="detailVisible"
      width="800px"
    >
      <el-descriptions :column="2" border v-if="currentReport">
        <el-descriptions-item label="报告ID">{{ currentReport.id }}</el-descriptions-item>
        <el-descriptions-item label="记录编号">{{ currentReport.recordId }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentReport.name }}</el-descriptions-item>
        <el-descriptions-item label="手机号码">{{ currentReport.phone }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentReport.idCard }}</el-descriptions-item>
        <el-descriptions-item label="体检套餐">{{ currentReport.packageName }}</el-descriptions-item>
        <el-descriptions-item label="报告类型">
          <el-tag :type="getReportTypeColor(currentReport.reportType)" size="small">
            {{ getReportTypeName(currentReport.reportType) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="报告名称">{{ currentReport.reportName }}</el-descriptions-item>
        <el-descriptions-item label="文件名称">{{ currentReport.fileName }}</el-descriptions-item>
        <el-descriptions-item label="上传时间">{{ currentReport.uploadTime }}</el-descriptions-item>
        <el-descriptions-item label="上传人">{{ currentReport.uploader }}</el-descriptions-item>
        <el-descriptions-item label="报告摘要" :span="2">{{ currentReport.summary || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleDownload(currentReport)">下载报告</el-button>
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ReportQuery',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码格式'))
      } else {
        callback()
      }
    }

    const validateIdCard = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入身份证号'))
      } else if (!/^\d{17}[\dXx]$/.test(value)) {
        callback(new Error('请输入正确的身份证号格式'))
      } else {
        callback()
      }
    }

    return {
      searchForm: {
        recordId: '',
        name: '',
        phone: '',
        idCard: '',
        reportType: '',
        dateRange: []
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      tableData: [],
      selectedRows: [],
      loading: false,
      detailVisible: false,
      currentReport: null,
      verifyVisible: false,
      verifyForm: {
        name: '',
        inputPhone: '',
        inputIdCard: ''
      },
      verifyRules: {
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        idCard: [
          { validator: validateIdCard, trigger: 'blur' }
        ]
      },
      currentAction: '',
      pendingReport: null
    }
  },
  created() {
    this.loadReports()
  },
  methods: {
    loadReports() {
      this.loading = true
      
      const mockData = [
        {
          id: 1,
          recordId: 'REC001',
          name: '张三',
          phone: '13800138001',
          idCard: '110101199001011234',
          packageName: '入职基础体检套餐',
          reportName: '入职体检主报告',
          reportType: 'main',
          fileName: 'REC001_入职体检主报告.pdf',
          uploadTime: '2024-01-18 10:30:00',
          uploader: '管理员',
          summary: '各项指标正常，身体健康。建议保持良好的生活习惯，定期体检。'
        },
        {
          id: 2,
          recordId: 'REC001',
          name: '张三',
          phone: '13800138001',
          idCard: '110101199001011234',
          packageName: '入职基础体检套餐',
          reportName: '入职体检检验报告',
          reportType: 'lab',
          fileName: 'REC001_入职体检检验报告.pdf',
          uploadTime: '2024-01-18 10:35:00',
          uploader: '管理员',
          summary: '血常规、尿常规、肝功能等检验项目结果均在正常范围内。'
        },
        {
          id: 3,
          recordId: 'REC002',
          name: '李四',
          phone: '13800138002',
          idCard: '310101199202025678',
          packageName: '青年常规体检套餐',
          reportName: '青年常规体检主报告',
          reportType: 'main',
          fileName: 'REC002_青年常规体检主报告.pdf',
          uploadTime: '2024-01-22 09:15:00',
          uploader: '管理员',
          summary: '整体健康状况良好，血压略偏高，建议注意饮食和运动。'
        },
        {
          id: 4,
          recordId: 'REC002',
          name: '李四',
          phone: '13800138002',
          idCard: '310101199202025678',
          packageName: '青年常规体检套餐',
          reportName: '腹部B超报告',
          reportType: 'image',
          fileName: 'REC002_腹部B超报告.pdf',
          uploadTime: '2024-01-22 09:20:00',
          uploader: '管理员',
          summary: '肝、胆、胰、脾、肾未见明显异常。'
        },
        {
          id: 5,
          recordId: 'REC005',
          name: '王五',
          phone: '13800138005',
          idCard: '440101198505059012',
          packageName: '中年全面体检套餐',
          reportName: '中年全面体检主报告',
          reportType: 'main',
          fileName: 'REC005_中年全面体检主报告.pdf',
          uploadTime: '2024-01-12 14:00:00',
          uploader: '管理员',
          summary: '血脂偏高，建议低脂饮食，适当增加有氧运动。'
        }
      ]

      let filtered = mockData

      if (this.searchForm.recordId) {
        filtered = filtered.filter(item => item.recordId.includes(this.searchForm.recordId))
      }

      if (this.searchForm.name) {
        filtered = filtered.filter(item => item.name.includes(this.searchForm.name))
      }

      if (this.searchForm.phone) {
        filtered = filtered.filter(item => item.phone.includes(this.searchForm.phone))
      }

      if (this.searchForm.idCard) {
        filtered = filtered.filter(item => item.idCard.includes(this.searchForm.idCard))
      }

      if (this.searchForm.reportType) {
        filtered = filtered.filter(item => item.reportType === this.searchForm.reportType)
      }

      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const startDate = this.searchForm.dateRange[0].getTime()
        const endDate = this.searchForm.dateRange[1].getTime()
        filtered = filtered.filter(item => {
          const itemDate = new Date(item.uploadTime).getTime()
          return itemDate >= startDate && itemDate <= endDate
        })
      }

      this.pagination.total = filtered.length

      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      
      setTimeout(() => {
        this.tableData = filtered.slice(start, end)
        this.loading = false
        this.selectedRows = []
      }, 500)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadReports()
    },
    handleReset() {
      this.searchForm = {
        recordId: '',
        name: '',
        phone: '',
        idCard: '',
        reportType: '',
        dateRange: []
      }
      this.pagination.page = 1
      this.loadReports()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.loadReports()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadReports()
    },
    handleSelectionChange(val) {
      this.selectedRows = val
    },
    openVerifyDialog(row, action) {
      this.pendingReport = row
      this.currentAction = action
      this.verifyForm.name = row.name
      this.verifyForm.inputPhone = ''
      this.verifyForm.inputIdCard = ''
      this.verifyVisible = true
      this.$nextTick(() => {
        this.$refs.verifyFormRef.clearValidate()
      })
    },
    handleVerify() {
      this.$refs.verifyFormRef.validate((valid) => {
        if (valid) {
          if (this.verifyForm.inputPhone === this.pendingReport.phone &&
              this.verifyForm.inputIdCard === this.pendingReport.idCard) {
            this.verifyVisible = false
            if (this.currentAction === 'view') {
              this.currentReport = this.pendingReport
              this.detailVisible = true
            } else if (this.currentAction === 'download') {
              this.handleDownload(this.pendingReport)
            }
            this.$message.success('身份验证通过')
          } else {
            this.$message.error('手机号码或身份证号不正确，请重新输入')
          }
        }
      })
    },
    handleView(row) {
      this.currentReport = row
      this.detailVisible = true
    },
    handleDownload(row) {
      this.$message.success(`正在下载: ${row.fileName}`)
    },
    handleDelete(row) {
      this.$confirm('确定要删除该报告吗？此操作不可恢复！', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.tableData.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.tableData.splice(index, 1)
          this.pagination.total--
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleBatchDelete() {
      this.$confirm(`确定要删除选中的 ${this.selectedRows.length} 份报告吗？此操作不可恢复！`, '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const ids = this.selectedRows.map(item => item.id)
        this.tableData = this.tableData.filter(item => !ids.includes(item.id))
        this.pagination.total -= ids.length
        this.selectedRows = []
        this.$message.success('批量删除成功')
      }).catch(() => {})
    },
    getReportTypeName(type) {
      const map = {
        main: '主报告',
        lab: '检验报告',
        image: '影像报告',
        other: '其他'
      }
      return map[type] || type
    },
    getReportTypeColor(type) {
      const map = {
        main: 'primary',
        lab: 'success',
        image: 'warning',
        other: 'info'
      }
      return map[type] || ''
    }
  }
}
</script>

<style scoped>
.report-query {
  padding: 0;
}

.search-card {
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>
