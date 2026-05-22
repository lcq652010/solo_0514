<template>
  <div class="exam-records">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="套餐类型">
          <el-select v-model="searchForm.packageType" placeholder="请选择套餐类型" style="width: 150px">
            <el-option label="全部" value=""></el-option>
            <el-option label="入职体检" value="入职基础体检套餐"></el-option>
            <el-option label="常规体检" value="青年常规体检套餐"></el-option>
            <el-option label="高端体检" value="精英尊享体检套餐"></el-option>
            <el-option label="女性体检" value="女性专属体检套餐"></el-option>
            <el-option label="中年体检" value="中年全面体检套餐"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="体检日期">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="体检状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" style="width: 130px">
            <el-option label="全部" value=""></el-option>
            <el-option label="已预约" value="scheduled"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="报告已出" value="report_ready"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="记录编号" width="120" align="center"></el-table-column>
        <el-table-column prop="name" label="姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="packageName" label="体检套餐" min-width="180"></el-table-column>
        <el-table-column prop="examDate" label="体检日期" width="120" align="center"></el-table-column>
        <el-table-column prop="examTime" label="时段" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.examTime === 'morning' ? '上午' : '下午' }}
          </template>
        </el-table-column>
        <el-table-column prop="doctor" label="体检医生" width="120" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusName(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="260" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="mini"
              @click="openVerifyDialog(scope.row, 'view')"
            >
              查看详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'report_ready'"
              type="success"
              size="mini"
              @click="openVerifyDialog(scope.row, 'download')"
            >
              下载报告
            </el-button>
            <el-button
              v-if="scope.row.status === 'scheduled'"
              type="danger"
              size="mini"
              @click="handleCancel(scope.row)"
            >
              取消预约
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        class="pagination"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[10, 20, 50]"
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
      title="体检记录详情"
      :visible.sync="detailVisible"
      width="700px"
    >
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="记录编号">{{ currentRecord.id }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentRecord.name }}</el-descriptions-item>
        <el-descriptions-item label="体检套餐">{{ currentRecord.packageName }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentRecord.idCard }}</el-descriptions-item>
        <el-descriptions-item label="体检日期">{{ currentRecord.examDate }}</el-descriptions-item>
        <el-descriptions-item label="体检时段">{{ currentRecord.examTime === 'morning' ? '上午' : '下午' }}</el-descriptions-item>
        <el-descriptions-item label="体检医生">{{ currentRecord.doctor }}</el-descriptions-item>
        <el-descriptions-item label="体检状态">
          <el-tag :type="getStatusType(currentRecord.status)" size="small">
            {{ getStatusName(currentRecord.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRecord.phone }}</el-descriptions-item>
        <el-descriptions-item label="预约时间">{{ currentRecord.createTime }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentRecord.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ExamRecords',
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
        packageType: '',
        dateRange: [],
        status: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      tableData: [],
      allRecords: [],
      detailVisible: false,
      currentRecord: null,
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
      pendingRecord: null
    }
  },
  created() {
    this.loadRecords()
  },
  mounted() {
    if (this.$route.query.refresh === 'true') {
      this.loadRecords()
    }
  },
  watch: {
    '$route.query.refresh'(newVal) {
      if (newVal === 'true') {
        this.loadRecords()
      }
    }
  },
  methods: {
    loadRecords() {
      const mockData = [
        {
          id: 'REC001',
          name: '张三',
          packageName: '入职基础体检套餐',
          examDate: '2024-01-15',
          examTime: 'morning',
          doctor: '张医生',
          status: 'report_ready',
          phone: '13800138001',
          idCard: '110101199001011234',
          createTime: '2024-01-10 09:30:00',
          remark: ''
        },
        {
          id: 'REC002',
          name: '李四',
          packageName: '青年常规体检套餐',
          examDate: '2024-01-20',
          examTime: 'afternoon',
          doctor: '李医生',
          status: 'completed',
          phone: '13800138002',
          idCard: '310101199202025678',
          createTime: '2024-01-15 14:20:00',
          remark: '有青霉素过敏史'
        },
        {
          id: 'REC003',
          name: '王五',
          packageName: '精英尊享体检套餐',
          examDate: '2024-01-25',
          examTime: 'morning',
          doctor: '王医生',
          status: 'scheduled',
          phone: '13800138003',
          idCard: '440101198505059012',
          createTime: '2024-01-20 10:15:00',
          remark: ''
        },
        {
          id: 'REC004',
          name: '赵六',
          packageName: '女性专属体检套餐',
          examDate: '2024-01-05',
          examTime: 'morning',
          doctor: '陈医生',
          status: 'cancelled',
          phone: '13800138004',
          idCard: '510101199103033456',
          createTime: '2024-01-01 11:00:00',
          remark: '个人原因取消'
        },
        {
          id: 'REC005',
          name: '孙七',
          packageName: '中年全面体检套餐',
          examDate: '2024-01-08',
          examTime: 'afternoon',
          doctor: '刘医生',
          status: 'report_ready',
          phone: '13800138005',
          idCard: '330101197807078901',
          createTime: '2023-12-28 16:45:00',
          remark: ''
        },
        {
          id: 'REC006',
          name: '周八',
          packageName: '青年常规体检套餐',
          examDate: '2024-02-01',
          examTime: 'morning',
          doctor: '张医生',
          status: 'scheduled',
          phone: '13800138006',
          idCard: '320101199309091234',
          createTime: '2024-01-25 09:00:00',
          remark: ''
        },
        {
          id: 'REC007',
          name: '吴九',
          packageName: '精英尊享体检套餐',
          examDate: '2024-02-05',
          examTime: 'afternoon',
          doctor: '李医生',
          status: 'scheduled',
          phone: '13800138007',
          idCard: '120101198808085678',
          createTime: '2024-01-28 14:30:00',
          remark: '高端体检VIP'
        },
        {
          id: 'REC008',
          name: '郑十',
          packageName: '入职基础体检套餐',
          examDate: '2024-01-28',
          examTime: 'morning',
          doctor: '王医生',
          status: 'completed',
          phone: '13800138008',
          idCard: '420101199505059012',
          createTime: '2024-01-20 16:00:00',
          remark: ''
        }
      ]

      this.allRecords = mockData
      this.applyFilters()
    },
    applyFilters() {
      let filtered = [...this.allRecords]

      if (this.searchForm.packageType) {
        filtered = filtered.filter(item => item.packageName === this.searchForm.packageType)
      }

      if (this.searchForm.status) {
        filtered = filtered.filter(item => item.status === this.searchForm.status)
      }

      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        const startDate = this.searchForm.dateRange[0].getTime()
        const endDate = this.searchForm.dateRange[1].getTime()
        filtered = filtered.filter(item => {
          const itemDate = new Date(item.examDate).getTime()
          return itemDate >= startDate && itemDate <= endDate
        })
      }

      this.pagination.total = filtered.length

      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = filtered.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.applyFilters()
    },
    handleReset() {
      this.searchForm = {
        packageType: '',
        dateRange: [],
        status: ''
      }
      this.pagination.page = 1
      this.applyFilters()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.applyFilters()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.applyFilters()
    },
    openVerifyDialog(row, action) {
      this.pendingRecord = row
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
          if (this.verifyForm.inputPhone === this.pendingRecord.phone &&
              this.verifyForm.inputIdCard === this.pendingRecord.idCard) {
            this.verifyVisible = false
            if (this.currentAction === 'view') {
              this.currentRecord = this.pendingRecord
              this.detailVisible = true
            } else if (this.currentAction === 'download') {
              this.handleDownload(this.pendingRecord)
            }
            this.$message.success('身份验证通过')
          } else {
            this.$message.error('手机号码或身份证号不正确，请重新输入')
          }
        }
      })
    },
    handleView(row) {
      this.currentRecord = row
      this.detailVisible = true
    },
    handleDownload(row) {
      this.$message.success(`正在下载报告 ${row.id}...`)
    },
    handleCancel(row) {
      this.$confirm('确定要取消该预约吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = 'cancelled'
        this.$message.success('取消预约成功')
      }).catch(() => {})
    },
    getStatusType(status) {
      const map = {
        scheduled: 'warning',
        completed: 'info',
        report_ready: 'success',
        cancelled: 'danger'
      }
      return map[status] || ''
    },
    getStatusName(status) {
      const map = {
        scheduled: '已预约',
        completed: '已完成',
        report_ready: '报告已出',
        cancelled: '已取消'
      }
      return map[status] || status
    }
  }
}
</script>

<style scoped>
.exam-records {
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
