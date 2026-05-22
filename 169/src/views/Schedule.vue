<template>
  <div class="page-container">
    <div class="page-title">技师排班管理</div>
    
    <div class="search-bar">
      <el-date-picker
        v-model="selectedWeek"
        type="week"
        format="yyyy 年第 WW 周"
        placeholder="选择周次"
        style="width: 220px; margin-right: 10px"
        @change="handleWeekChange"
      ></el-date-picker>
      <el-select v-model="selectedTechnician" placeholder="选择技师" style="width: 150px; margin-right: 10px" clearable>
        <el-option label="全部技师" value=""></el-option>
        <el-option
          v-for="tech in technicianList"
          :key="tech.id"
          :label="tech.name"
          :value="tech.id"
        ></el-option>
      </el-select>
      <el-button type="primary" @click="loadSchedule">查询</el-button>
      <el-button style="margin-left: 10px" @click="showAddDialog">添加排班</el-button>
    </div>

    <div class="table-container">
      <el-table :data="scheduleData" border style="width: 100%">
        <el-table-column prop="technicianName" label="技师姓名" width="120" align="center"></el-table-column>
        <el-table-column prop="level" label="级别" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getLevelTagType(scope.row.level)" size="small">{{ scope.row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date" label="日期" width="120" align="center"></el-table-column>
        <el-table-column prop="timeSlot" label="时段" width="150" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)" size="small">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="120" align="center"></el-table-column>
        <el-table-column prop="plateNumber" label="车牌号" width="120" align="center"></el-table-column>
        <el-table-column prop="packageName" label="保养项目" min-width="150"></el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="warning" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="pagination-container">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form
        ref="scheduleForm"
        :model="scheduleForm"
        :rules="scheduleRules"
        label-width="100px"
      >
        <el-form-item label="技师" prop="technicianId">
          <el-select v-model="scheduleForm.technicianId" placeholder="请选择技师" style="width: 100%">
            <el-option
              v-for="tech in technicianList"
              :key="tech.id"
              :label="tech.name + ' - ' + tech.level"
              :value="tech.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期" prop="date">
          <el-date-picker
            v-model="scheduleForm.date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="时段" prop="timeSlot">
          <el-select v-model="scheduleForm.timeSlot" placeholder="请选择时段" style="width: 100%">
            <el-option
              v-for="slot in timeSlots"
              :key="slot.value"
              :label="slot.label"
              :value="slot.value"
              :disabled="slot.disabled"
            >
              <span>{{ slot.label }}</span>
              <span v-if="slot.disabled" style="color: #f56c6c; margin-left: 10px; font-size: 12px;">(已有排班)</span>
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="scheduleForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="空闲" value="空闲"></el-option>
            <el-option label="已预约" value="已预约"></el-option>
            <el-option label="休息" value="休息"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="scheduleForm.status === '已预约'" label="客户信息" prop="customerName">
          <el-input v-model="scheduleForm.customerName" placeholder="请输入客户姓名"></el-input>
        </el-form-item>
        <el-form-item v-if="scheduleForm.status === '已预约'" label="车牌号" prop="plateNumber">
          <el-input v-model="scheduleForm.plateNumber" placeholder="请输入车牌号"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Schedule',
  data() {
    return {
      selectedWeek: '',
      selectedTechnician: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      scheduleData: [],
      allScheduleData: [],
      technicianList: [],
      dialogVisible: false,
      dialogTitle: '添加排班',
      isEdit: false,
      editingId: null,
      scheduleForm: {
        technicianId: '',
        date: '',
        timeSlot: '',
        status: '空闲',
        customerName: '',
        plateNumber: ''
      },
      scheduleRules: {
        technicianId: [
          { required: true, message: '请选择技师', trigger: 'change' }
        ],
        date: [
          { required: true, message: '请选择日期', trigger: 'change' }
        ],
        timeSlot: [
          { required: true, message: '请选择时段', trigger: 'change' }
        ],
        status: [
          { required: true, message: '请选择状态', trigger: 'change' }
        ]
      },
      timeSlots: [
        { label: '09:00 - 10:00', value: '09:00 - 10:00', disabled: false },
        { label: '10:00 - 11:00', value: '10:00 - 11:00', disabled: false },
        { label: '11:00 - 12:00', value: '11:00 - 12:00', disabled: false },
        { label: '14:00 - 15:00', value: '14:00 - 15:00', disabled: false },
        { label: '15:00 - 16:00', value: '15:00 - 16:00', disabled: false },
        { label: '16:00 - 17:00', value: '16:00 - 17:00', disabled: false }
      ]
    }
  },
  watch: {
    'scheduleForm.technicianId': function() {
      this.updateTimeSlotsAvailability()
    },
    'scheduleForm.date': function() {
      this.updateTimeSlotsAvailability()
    }
  },
  created() {
    this.loadTechnicianList()
    this.loadSchedule()
  },
  methods: {
    getLevelTagType(level) {
      const typeMap = {
        '高级技师': 'danger',
        '中级技师': 'warning',
        '初级技师': 'success'
      }
      return typeMap[level] || 'info'
    },
    getStatusTagType(status) {
      const typeMap = {
        '空闲': 'success',
        '已预约': 'warning',
        '休息': 'info'
      }
      return typeMap[status] || 'info'
    },
    loadTechnicianList() {
      this.technicianList = [
        { id: 1, name: '张师傅', level: '高级技师' },
        { id: 2, name: '李师傅', level: '高级技师' },
        { id: 3, name: '王师傅', level: '中级技师' },
        { id: 4, name: '赵师傅', level: '中级技师' },
        { id: 5, name: '刘师傅', level: '初级技师' }
      ]
    },
    updateTimeSlotsAvailability() {
      if (!this.scheduleForm.technicianId || !this.scheduleForm.date) {
        this.timeSlots.forEach(slot => slot.disabled = false)
        return
      }

      const selectedDate = this.formatDate(this.scheduleForm.date)
      
      this.timeSlots.forEach(slot => {
        const hasConflict = this.allScheduleData.some(schedule => 
          schedule.technicianId === this.scheduleForm.technicianId &&
          schedule.date === selectedDate &&
          schedule.timeSlot === slot.value &&
          (!this.isEdit || schedule.id !== this.editingId)
        )
        slot.disabled = hasConflict
      })

      if (this.scheduleForm.timeSlot) {
        const currentSlot = this.timeSlots.find(slot => slot.value === this.scheduleForm.timeSlot)
        if (currentSlot && currentSlot.disabled) {
          this.$message.warning('该时段已有排班，请选择其他时段')
          this.scheduleForm.timeSlot = ''
        }
      }
    },
    loadSchedule() {
      const mockData = [
        { id: 1, technicianId: 1, technicianName: '张师傅', level: '高级技师', date: '2024-01-15', timeSlot: '09:00 - 10:00', status: '已预约', customerName: '陈先生', plateNumber: '京A12345', packageName: '基础保养套餐' },
        { id: 2, technicianId: 1, technicianName: '张师傅', level: '高级技师', date: '2024-01-15', timeSlot: '10:00 - 11:00', status: '空闲', customerName: '', plateNumber: '', packageName: '' },
        { id: 3, technicianId: 1, technicianName: '张师傅', level: '高级技师', date: '2024-01-15', timeSlot: '14:00 - 15:00', status: '已预约', customerName: '林女士', plateNumber: '京B67890', packageName: '深度保养套餐A' },
        { id: 4, technicianId: 2, technicianName: '李师傅', level: '高级技师', date: '2024-01-15', timeSlot: '09:00 - 10:00', status: '休息', customerName: '', plateNumber: '', packageName: '' },
        { id: 5, technicianId: 2, technicianName: '李师傅', level: '高级技师', date: '2024-01-15', timeSlot: '10:00 - 11:00', status: '已预约', customerName: '吴先生', plateNumber: '京C11111', packageName: '豪华保养套餐' },
        { id: 6, technicianId: 3, technicianName: '王师傅', level: '中级技师', date: '2024-01-15', timeSlot: '09:00 - 10:00', status: '空闲', customerName: '', plateNumber: '', packageName: '' },
        { id: 7, technicianId: 3, technicianName: '王师傅', level: '中级技师', date: '2024-01-15', timeSlot: '14:00 - 15:00', status: '已预约', customerName: '郑女士', plateNumber: '京D22222', packageName: '常规保养套餐' },
        { id: 8, technicianId: 4, technicianName: '赵师傅', level: '中级技师', date: '2024-01-16', timeSlot: '09:00 - 10:00', status: '空闲', customerName: '', plateNumber: '', packageName: '' },
        { id: 9, technicianId: 5, technicianName: '刘师傅', level: '初级技师', date: '2024-01-16', timeSlot: '10:00 - 11:00', status: '已预约', customerName: '黄先生', plateNumber: '京E33333', packageName: '基础保养套餐' },
        { id: 10, technicianId: 5, technicianName: '刘师傅', level: '初级技师', date: '2024-01-16', timeSlot: '14:00 - 15:00', status: '空闲', customerName: '', plateNumber: '', packageName: '' }
      ]

      this.allScheduleData = mockData
      let filteredData = [...mockData]

      if (this.selectedTechnician) {
        filteredData = filteredData.filter(item => 
          item.technicianId === this.selectedTechnician
        )
      }

      this.total = filteredData.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.scheduleData = filteredData.slice(start, end)
    },
    handleWeekChange() {
      this.loadSchedule()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadSchedule()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadSchedule()
    },
    showAddDialog() {
      this.isEdit = false
      this.editingId = null
      this.dialogTitle = '添加排班'
      this.timeSlots.forEach(slot => slot.disabled = false)
      this.scheduleForm = {
        technicianId: '',
        date: '',
        timeSlot: '',
        status: '空闲',
        customerName: '',
        plateNumber: ''
      }
      this.dialogVisible = true
    },
    handleView(row) {
      this.$alert(`
        技师：${row.technicianName}
        级别：${row.level}
        日期：${row.date}
        时段：${row.timeSlot}
        状态：${row.status}
        客户：${row.customerName || '-'}
        车牌：${row.plateNumber || '-'}
        项目：${row.packageName || '-'}
      `, '排班详情', {
        confirmButtonText: '确定'
      })
    },
    handleEdit(row) {
      this.isEdit = true
      this.editingId = row.id
      this.dialogTitle = '编辑排班'
      this.timeSlots.forEach(slot => slot.disabled = false)
      this.scheduleForm = {
        id: row.id,
        technicianId: row.technicianId,
        date: row.date,
        timeSlot: row.timeSlot,
        status: row.status,
        customerName: row.customerName,
        plateNumber: row.plateNumber
      }
      this.dialogVisible = true
      this.$nextTick(() => {
        this.updateTimeSlotsAvailability()
      })
    },
    handleDelete(row) {
      this.$confirm(`确定要删除 ${row.technicianName} 在 ${row.date} ${row.timeSlot} 的排班吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('删除成功！')
        this.loadSchedule()
      }).catch(() => {})
    },
    checkScheduleConflict() {
      if (!this.scheduleForm.technicianId || !this.scheduleForm.date || !this.scheduleForm.timeSlot) {
        return false
      }

      const formattedDate = this.formatDate(this.scheduleForm.date)
      
      const hasConflict = this.allScheduleData.some(schedule => 
        schedule.technicianId === this.scheduleForm.technicianId &&
        schedule.date === formattedDate &&
        schedule.timeSlot === this.scheduleForm.timeSlot &&
        (!this.isEdit || schedule.id !== this.editingId)
      )

      if (hasConflict) {
        const tech = this.technicianList.find(t => t.id === this.scheduleForm.technicianId)
        this.$message.error(`排班冲突！${tech ? tech.name : '技师'}在${formattedDate} ${this.scheduleForm.timeSlot}已有安排`)
        return true
      }

      return false
    },
    formatDate(date) {
      if (typeof date === 'string') return date
      if (!date) return ''
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleSave() {
      this.$refs.scheduleForm.validate((valid) => {
        if (valid) {
          if (this.checkScheduleConflict()) {
            return false
          }
          this.dialogVisible = false
          this.$message.success(this.isEdit ? '编辑成功！' : '添加成功！')
          this.loadSchedule()
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleDialogClose() {
      this.$refs.scheduleForm.resetFields()
    }
  }
}
</script>

<style scoped>
</style>
