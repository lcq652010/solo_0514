<template>
  <div class="page-container">
    <div class="page-title">医师排班管理</div>
    
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>排班列表</span>
        <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog">
          新增排班
        </el-button>
      </div>
      
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="医师姓名">
          <el-input v-model="searchForm.doctorName" placeholder="请输入医师姓名"></el-input>
        </el-form-item>
        <el-form-item label="科室">
          <el-select v-model="searchForm.department" placeholder="请选择科室">
            <el-option label="全部" value=""></el-option>
            <el-option label="内科" value="内科"></el-option>
            <el-option label="外科" value="外科"></el-option>
            <el-option label="皮肤科" value="皮肤科"></el-option>
            <el-option label="眼科" value="眼科"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="tableData" border style="width: 100%">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="doctorName" label="医师姓名" width="120"></el-table-column>
        <el-table-column prop="department" label="科室" width="120"></el-table-column>
        <el-table-column prop="date" label="排班日期" width="150"></el-table-column>
        <el-table-column prop="timeSlot" label="时段" width="150"></el-table-column>
        <el-table-column prop="maxPatients" label="最大接诊数" width="120"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '正常' ? 'success' : 'danger'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
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
    
    <el-dialog
      title="新增排班"
      :visible.sync="dialogVisible"
      width="500px">
      <el-form :model="scheduleForm" :rules="rules" ref="scheduleForm" label-width="100px">
        <el-form-item label="医师姓名" prop="doctorName">
          <el-input v-model="scheduleForm.doctorName"></el-input>
        </el-form-item>
        <el-form-item label="科室" prop="department">
          <el-select v-model="scheduleForm.department" style="width: 100%">
            <el-option label="内科" value="内科"></el-option>
            <el-option label="外科" value="外科"></el-option>
            <el-option label="皮肤科" value="皮肤科"></el-option>
            <el-option label="眼科" value="眼科"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="排班日期" prop="date">
          <el-date-picker
            v-model="scheduleForm.date"
            type="date"
            placeholder="选择日期"
            style="width: 100%">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="时段" prop="timeSlot">
          <el-select v-model="scheduleForm.timeSlot" style="width: 100%">
            <el-option label="上午 08:00-12:00" value="上午 08:00-12:00"></el-option>
            <el-option label="下午 14:00-18:00" value="下午 14:00-18:00"></el-option>
            <el-option label="全天 08:00-18:00" value="全天 08:00-18:00"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="最大接诊数" prop="maxPatients">
          <el-input-number v-model="scheduleForm.maxPatients" :min="1" :max="50"></el-input-number>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="scheduleForm.status">
            <el-radio label="正常"></el-radio>
            <el-radio label="停诊"></el-radio>
          </el-radio-group>
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
  name: 'Schedule',
  data() {
    return {
      searchForm: {
        doctorName: '',
        department: ''
      },
      tableData: [
        { id: 1, doctorName: '张医生', department: '内科', date: '2024-01-15', timeSlot: '上午 08:00-12:00', maxPatients: 20, status: '正常' },
        { id: 2, doctorName: '李医生', department: '外科', date: '2024-01-15', timeSlot: '下午 14:00-18:00', maxPatients: 15, status: '正常' },
        { id: 3, doctorName: '王医生', department: '皮肤科', date: '2024-01-16', timeSlot: '全天 08:00-18:00', maxPatients: 25, status: '正常' },
        { id: 4, doctorName: '赵医生', department: '眼科', date: '2024-01-16', timeSlot: '上午 08:00-12:00', maxPatients: 18, status: '停诊' },
        { id: 5, doctorName: '刘医生', department: '内科', date: '2024-01-17', timeSlot: '下午 14:00-18:00', maxPatients: 22, status: '正常' }
      ],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 5
      },
      dialogVisible: false,
      isEdit: false,
      scheduleForm: {
        doctorName: '',
        department: '',
        date: '',
        timeSlot: '',
        maxPatients: 10,
        status: '正常'
      },
      rules: {
        doctorName: [
          { required: true, message: '请输入医师姓名', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择科室', trigger: 'change' }
        ],
        date: [
          { required: true, message: '请选择排班日期', trigger: 'change' }
        ],
        timeSlot: [
          { required: true, message: '请选择时段', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    showAddDialog() {
      this.isEdit = false
      this.dialogVisible = true
      this.resetForm()
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogVisible = true
      this.scheduleForm = { ...row }
    },
    handleDelete(row) {
      this.$confirm('此操作将永久删除该排班记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(() => {})
    },
    handleSearch() {
      this.$message.success('查询成功')
    },
    handleReset() {
      this.searchForm = {
        doctorName: '',
        department: ''
      }
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    formatDate(date) {
      if (!date) return ''
      if (typeof date === 'string') return date
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    checkTimeConflict(doctorName, date, timeSlot, excludeId = null) {
      const convertTimeSlot = (slot) => {
        if (slot.includes('全天')) {
          return ['08:00', '18:00']
        } else if (slot.includes('上午')) {
          return ['08:00', '12:00']
        } else if (slot.includes('下午')) {
          return ['14:00', '18:00']
        }
        const times = slot.match(/\d{2}:\d{2}/g)
        return times ? times : null
      }
      
      const [newStart, newEnd] = convertTimeSlot(timeSlot)
      const formattedDate = this.formatDate(date)
      
      return this.tableData.some(item => {
        if (excludeId && item.id === excludeId) return false
        if (item.doctorName !== doctorName || item.date !== formattedDate) return false
        
        const [existStart, existEnd] = convertTimeSlot(item.timeSlot)
        return !(newEnd <= existStart || newStart >= existEnd)
      })
    },
    handleSubmit() {
      this.$refs.scheduleForm.validate((valid) => {
        if (valid) {
          const editId = this.isEdit ? this.scheduleForm.id : null
          const hasConflict = this.checkTimeConflict(
            this.scheduleForm.doctorName,
            this.scheduleForm.date,
            this.scheduleForm.timeSlot,
            editId
          )
          
          if (hasConflict) {
            this.$message.error('该医师在此时段已有排班，存在时间冲突！')
            return
          }
          
          if (this.isEdit) {
            const index = this.tableData.findIndex(item => item.id === this.scheduleForm.id)
            if (index > -1) {
              this.tableData[index] = { 
                ...this.scheduleForm,
                date: this.formatDate(this.scheduleForm.date)
              }
            }
          } else {
            const newId = Math.max(...this.tableData.map(item => item.id)) + 1
            this.tableData.push({
              id: newId,
              ...this.scheduleForm,
              date: this.formatDate(this.scheduleForm.date)
            })
            this.pagination.total++
          }
          
          this.$message.success(this.isEdit ? '编辑成功' : '新增成功')
          this.dialogVisible = false
        }
      })
    },
    resetForm() {
      this.scheduleForm = {
        doctorName: '',
        department: '',
        date: '',
        timeSlot: '',
        maxPatients: 10,
        status: '正常'
      }
      this.$nextTick(() => {
        this.$refs.scheduleForm.clearValidate()
      })
    }
  }
}
</script>

<style scoped>
.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
