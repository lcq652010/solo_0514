<template>
  <div class="page-container">
    <div class="page-title">疫苗提醒</div>
    
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon warning">
              <i class="el-icon-bell"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.urgentCount }}</div>
              <div class="stat-label">紧急提醒(7天内)</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon info">
              <i class="el-icon-time"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.upcomingCount }}</div>
              <div class="stat-label">即将到期(30天内)</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon success">
              <i class="el-icon-check"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.completedCount }}</div>
              <div class="stat-label">已完成接种</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon danger">
              <i class="el-icon-warning"></i>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.overdueCount }}</div>
              <div class="stat-label">已过期</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>疫苗接种记录</span>
        <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog">
          新增接种记录
        </el-button>
      </div>
      
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="宠物名称">
          <el-input v-model="searchForm.petName" placeholder="请输入宠物名称"></el-input>
        </el-form-item>
        <el-form-item label="疫苗类型">
          <el-select v-model="searchForm.vaccineType" placeholder="请选择疫苗类型">
            <el-option label="全部" value=""></el-option>
            <el-option label="狂犬疫苗" value="狂犬疫苗"></el-option>
            <el-option label="六联疫苗" value="六联疫苗"></el-option>
            <el-option label="八联疫苗" value="八联疫苗"></el-option>
            <el-option label="猫三联" value="猫三联"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="提醒状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="全部" value=""></el-option>
            <el-option label="紧急提醒" value="紧急提醒"></el-option>
            <el-option label="即将到期" value="即将到期"></el-option>
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="已过期" value="已过期"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="petName" label="宠物名称" width="100"></el-table-column>
        <el-table-column prop="petType" label="宠物类型" width="80"></el-table-column>
        <el-table-column prop="breed" label="品种" width="100"></el-table-column>
        <el-table-column prop="ownerName" label="主人姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
        <el-table-column prop="vaccineType" label="疫苗类型" width="120"></el-table-column>
        <el-table-column prop="lastVaccineDate" label="上次接种日期" width="150"></el-table-column>
        <el-table-column prop="nextVaccineDate" label="下次接种日期" width="150"></el-table-column>
        <el-table-column prop="daysRemaining" label="剩余天数" width="100">
          <template slot-scope="scope">
            <span v-if="scope.row.daysRemaining <= 0" style="color: #f56c6c;">
              已过期{{ Math.abs(scope.row.daysRemaining) }}天
            </span>
            <span v-else-if="scope.row.daysRemaining <= 7" style="color: #e6a23c;">
              {{ scope.row.daysRemaining }}天
            </span>
            <span v-else style="color: #67c23a;">
              {{ scope.row.daysRemaining }}天
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" type="success" @click="handleComplete(scope.row)" :disabled="scope.row.status === '已完成'">
              完成接种
            </el-button>
            <el-button size="mini" type="primary" @click="handleSendReminder(scope.row)">
              发送提醒
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>
    
    <el-dialog title="新增接种记录" :visible.sync="dialogVisible" width="600px">
      <el-form :model="vaccineForm" :rules="rules" ref="vaccineForm" label-width="120px">
        <el-form-item label="宠物名称" prop="petName">
          <el-input v-model="vaccineForm.petName"></el-input>
        </el-form-item>
        <el-form-item label="宠物类型" prop="petType">
          <el-select v-model="vaccineForm.petType" style="width: 100%">
            <el-option label="狗" value="狗"></el-option>
            <el-option label="猫" value="猫"></el-option>
            <el-option label="鸟" value="鸟"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="品种" prop="breed">
          <el-input v-model="vaccineForm.breed"></el-input>
        </el-form-item>
        <el-form-item label="主人姓名" prop="ownerName">
          <el-input v-model="vaccineForm.ownerName"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="vaccineForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="疫苗类型" prop="vaccineType">
          <el-select v-model="vaccineForm.vaccineType" style="width: 100%">
            <el-option label="狂犬疫苗" value="狂犬疫苗"></el-option>
            <el-option label="六联疫苗" value="六联疫苗"></el-option>
            <el-option label="八联疫苗" value="八联疫苗"></el-option>
            <el-option label="猫三联" value="猫三联"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上次接种日期" prop="lastVaccineDate">
          <el-date-picker
            v-model="vaccineForm.lastVaccineDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="下次接种日期" prop="nextVaccineDate">
          <el-date-picker
            v-model="vaccineForm.nextVaccineDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input type="textarea" :rows="3" v-model="vaccineForm.remarks"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'VaccineReminder',
  data() {
    return {
      searchForm: {
        petName: '',
        vaccineType: '',
        status: ''
      },
      stats: {
        urgentCount: 2,
        upcomingCount: 1,
        completedCount: 3,
        overdueCount: 1
      },
      tableData: [
        {
          id: 1,
          petName: '豆豆',
          petType: '狗',
          breed: '金毛',
          ownerName: '张三',
          phone: '13800138000',
          vaccineType: '狂犬疫苗',
          lastVaccineDate: '2023-01-10',
          nextVaccineDate: '2024-01-10',
          daysRemaining: -5,
          status: '已过期',
          remarks: ''
        },
        {
          id: 2,
          petName: '咪咪',
          petType: '猫',
          breed: '英短',
          ownerName: '李四',
          phone: '13900139000',
          vaccineType: '猫三联',
          lastVaccineDate: '2023-07-15',
          nextVaccineDate: '2024-01-20',
          daysRemaining: 5,
          status: '紧急提醒',
          remarks: ''
        },
        {
          id: 3,
          petName: '旺财',
          petType: '狗',
          breed: '泰迪',
          ownerName: '王五',
          phone: '13700137000',
          vaccineType: '六联疫苗',
          lastVaccineDate: '2023-08-20',
          nextVaccineDate: '2024-02-20',
          daysRemaining: 35,
          status: '即将到期',
          remarks: ''
        },
        {
          id: 4,
          petName: '花花',
          petType: '猫',
          breed: '布偶',
          ownerName: '赵六',
          phone: '13600136000',
          vaccineType: '狂犬疫苗',
          lastVaccineDate: '2024-01-05',
          nextVaccineDate: '2025-01-05',
          daysRemaining: 355,
          status: '已完成',
          remarks: ''
        },
        {
          id: 5,
          petName: '小黑',
          petType: '狗',
          breed: '拉布拉多',
          ownerName: '孙七',
          phone: '13500135000',
          vaccineType: '八联疫苗',
          lastVaccineDate: '2023-12-25',
          nextVaccineDate: '2024-01-18',
          daysRemaining: 3,
          status: '紧急提醒',
          remarks: ''
        },
        {
          id: 6,
          petName: '小白',
          petType: '猫',
          breed: '橘猫',
          ownerName: '周八',
          phone: '13400134000',
          vaccineType: '猫三联',
          lastVaccineDate: '2024-01-02',
          nextVaccineDate: '2024-07-02',
          daysRemaining: 168,
          status: '已完成',
          remarks: ''
        },
        {
          id: 7,
          petName: '黄黄',
          petType: '狗',
          breed: '柯基',
          ownerName: '吴九',
          phone: '13300133000',
          vaccineType: '狂犬疫苗',
          lastVaccineDate: '2024-01-08',
          nextVaccineDate: '2025-01-08',
          daysRemaining: 358,
          status: '已完成',
          remarks: ''
        }
      ],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 7
      },
      dialogVisible: false,
      vaccineForm: {
        petName: '',
        petType: '',
        breed: '',
        ownerName: '',
        phone: '',
        vaccineType: '',
        lastVaccineDate: '',
        nextVaccineDate: '',
        remarks: ''
      },
      rules: {
        petName: [
          { required: true, message: '请输入宠物名称', trigger: 'blur' }
        ],
        petType: [
          { required: true, message: '请选择宠物类型', trigger: 'change' }
        ],
        ownerName: [
          { required: true, message: '请输入主人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' }
        ],
        vaccineType: [
          { required: true, message: '请选择疫苗类型', trigger: 'change' }
        ],
        lastVaccineDate: [
          { required: true, message: '请选择上次接种日期', trigger: 'change' }
        ],
        nextVaccineDate: [
          { required: true, message: '请选择下次接种日期', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    getStatusType(status) {
      const typeMap = {
        '紧急提醒': 'warning',
        '即将到期': '',
        '已完成': 'success',
        '已过期': 'danger'
      }
      return typeMap[status] || ''
    },
    handleSearch() {
      this.$message.success('查询完成')
    },
    handleReset() {
      this.searchForm = {
        petName: '',
        vaccineType: '',
        status: ''
      }
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    showAddDialog() {
      this.dialogVisible = true
      this.resetForm()
    },
    handleComplete(row) {
      this.$confirm('确认该疫苗已接种完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = '已完成'
        row.lastVaccineDate = row.nextVaccineDate
        this.$message.success('接种完成')
      }).catch(() => {})
    },
    handleSendReminder(row) {
      this.$confirm('确认给' + row.ownerName + '发送疫苗接种提醒短信吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('提醒短信已发送')
      }).catch(() => {})
    },
    handleDelete(row) {
      this.$confirm('确定要删除该记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.tableData.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.tableData.splice(index, 1)
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.vaccineForm.validate((valid) => {
        if (valid) {
          const newId = Math.max(...this.tableData.map(item => item.id)) + 1
          const today = new Date()
          const nextDate = new Date(this.vaccineForm.nextVaccineDate)
          const daysRemaining = Math.ceil((nextDate - today) / (1000 * 60 * 60 * 24))
          let status = '即将到期'
          if (daysRemaining <= 0) {
            status = '已过期'
          } else if (daysRemaining <= 7) {
            status = '紧急提醒'
          }
          this.tableData.unshift({
            id: newId,
            ...this.vaccineForm,
            daysRemaining: daysRemaining,
            status: status
          })
          this.$message.success('新增成功')
          this.dialogVisible = false
        }
      })
    },
    resetForm() {
      this.vaccineForm = {
        petName: '',
        petType: '',
        breed: '',
        ownerName: '',
        phone: '',
        vaccineType: '',
        lastVaccineDate: '',
        nextVaccineDate: '',
        remarks: ''
      }
      this.$nextTick(() => {
        this.$refs.vaccineForm.clearValidate()
      })
    }
  }
}
</script>

<style scoped>
.stat-card {
  height: 100px;
}
.stat-content {
  display: flex;
  align-items: center;
}
.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 15px;
}
.stat-icon.warning {
  background: #fdf6ec;
  color: #e6a23c;
}
.stat-icon.info {
  background: #ecf5ff;
  color: #409eff;
}
.stat-icon.success {
  background: #f0f9eb;
  color: #67c23a;
}
.stat-icon.danger {
  background: #fef0f0;
  color: #f56c6c;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}
.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
