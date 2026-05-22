<template>
  <div class="course-hours">
    <div class="page-title">会员课时管理</div>
    
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #409EFF;">
            <i class="el-icon-user"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ memberList.length }}</div>
            <div class="stat-label">会员总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #67C23A;">
            <i class="el-icon-time"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ totalRemaining }}</div>
            <div class="stat-label">剩余总课时</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #E6A23C;">
            <i class="el-icon-warning"></i>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ lowBalanceCount }}</div>
            <div class="stat-label">课时不足</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card>
      <div style="margin-bottom: 20px;">
        <el-button type="primary" @click="openAddDialog">新增会员</el-button>
        <el-input v-model="searchKeyword" placeholder="搜索会员姓名" style="width: 200px; margin-left: 10px;"></el-input>
      </div>

      <el-table :data="filteredMembers" border style="width: 100%">
        <el-table-column prop="id" label="会员编号" width="100" align="center"></el-table-column>
        <el-table-column prop="name" label="姓名" width="120" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" align="center"></el-table-column>
        <el-table-column prop="packageType" label="套餐类型" width="120" align="center">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.packageType }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="totalHours" label="总课时" width="100" align="center"></el-table-column>
        <el-table-column prop="usedHours" label="已用课时" width="100" align="center"></el-table-column>
        <el-table-column prop="remainingHours" label="剩余课时" width="100" align="center">
          <template slot-scope="scope">
            <span :class="{ 'low-balance': scope.row.remainingHours < 5 }">{{ scope.row.remainingHours }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="expireDate" label="有效期至" width="150" align="center">
          <template slot-scope="scope">
            <span :class="{ 'expired': isExpired(scope.row.expireDate) }">{{ scope.row.expireDate }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="rechargeHours(scope.row)">充值</el-button>
            <el-button type="success" size="small" @click="deductHours(scope.row)">消课</el-button>
            <el-button type="info" size="small" @click="viewRecords(scope.row)">记录</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="会员姓名" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone"></el-input>
        </el-form-item>
        <el-form-item label="套餐类型" prop="packageType">
          <el-select v-model="form.packageType" style="width: 100%;">
            <el-option label="月卡" value="月卡"></el-option>
            <el-option label="季卡" value="季卡"></el-option>
            <el-option label="年卡" value="年卡"></el-option>
            <el-option label="次卡" value="次卡"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="总课时" prop="totalHours">
          <el-input-number v-model="form.totalHours" :min="1" :max="200"></el-input-number>
        </el-form-item>
        <el-form-item label="有效期至" prop="expireDate">
          <el-date-picker v-model="form.expireDate" type="date" style="width: 100%;"></el-date-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="课时操作" :visible.sync="hourDialogVisible" width="400px">
      <el-form :model="hourForm" label-width="100px">
        <el-form-item :label="hourForm.type === 'recharge' ? '充值课时' : '消课时数'">
          <el-input-number v-model="hourForm.hours" :min="1" :max="100"></el-input-number>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="hourForm.remark" :rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="hourDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitHourForm">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="课时记录" :visible.sync="recordDialogVisible" width="600px">
      <el-table :data="currentMemberRecords" border>
        <el-table-column prop="time" label="时间" width="180"></el-table-column>
        <el-table-column prop="type" label="类型" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === '充值' ? 'success' : 'danger'" size="small">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="hours" label="数量" width="100"></el-table-column>
        <el-table-column prop="remark" label="备注"></el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CourseHours',
  data() {
    const validatePhone = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入联系电话'))
      } else if (!/^1[3-9]\d{9}$/.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }
    return {
      searchKeyword: '',
      memberList: [],
      dialogVisible: false,
      dialogTitle: '',
      dialogType: 'add',
      hourDialogVisible: false,
      recordDialogVisible: false,
      currentMember: null,
      currentMemberRecords: [],
      form: {
        name: '',
        phone: '',
        packageType: '',
        totalHours: 0,
        expireDate: ''
      },
      hourForm: {
        type: '',
        hours: 1,
        remark: ''
      },
      rules: {
        name: [{ required: true, message: '请输入会员姓名', trigger: 'blur' }],
        phone: [{ required: true, validator: validatePhone, trigger: 'blur' }],
        packageType: [{ required: true, message: '请选择套餐类型', trigger: 'change' }],
        totalHours: [{ required: true, message: '请输入总课时', trigger: 'blur' }],
        expireDate: [{ required: true, message: '请选择有效期', trigger: 'change' }]
      }
    }
  },
  computed: {
    totalRemaining() {
      return this.memberList.reduce((sum, m) => sum + m.remainingHours, 0)
    },
    lowBalanceCount() {
      return this.memberList.filter(m => m.remainingHours < 5).length
    },
    filteredMembers() {
      if (!this.searchKeyword) return this.memberList
      return this.memberList.filter(m => m.name.includes(this.searchKeyword))
    }
  },
  created() {
    this.loadMembers()
  },
  methods: {
    loadMembers() {
      const members = JSON.parse(localStorage.getItem('members') || '[]')
      if (members.length === 0) {
        const nextYear = new Date()
        nextYear.setFullYear(nextYear.getFullYear() + 1)
        this.memberList = [
          { id: 1001, name: '张三', phone: '13800138001', packageType: '年卡', totalHours: 100, usedHours: 35, remainingHours: 65, expireDate: nextYear.toLocaleDateString('zh-CN'), records: [] },
          { id: 1002, name: '李四', phone: '13800138002', packageType: '季卡', totalHours: 30, usedHours: 28, remainingHours: 2, expireDate: new Date().toLocaleDateString('zh-CN'), records: [] },
          { id: 1003, name: '王五', phone: '13800138003', packageType: '月卡', totalHours: 12, usedHours: 5, remainingHours: 7, expireDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toLocaleDateString('zh-CN'), records: [] }
        ]
      } else {
        this.memberList = members
      }
    },
    saveMembers() {
      localStorage.setItem('members', JSON.stringify(this.memberList))
    },
    isExpired(date) {
      return new Date(date) < new Date()
    },
    openAddDialog() {
      this.dialogType = 'add'
      this.dialogTitle = '新增会员'
      this.form = { name: '', phone: '', packageType: '', totalHours: 0, expireDate: '' }
      this.dialogVisible = true
    },
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.dialogType === 'add') {
            const newMember = {
              id: 1000 + this.memberList.length + 1,
              ...this.form,
              usedHours: 0,
              remainingHours: this.form.totalHours,
              expireDate: new Date(this.form.expireDate).toLocaleDateString('zh-CN'),
              records: []
            }
            this.memberList.push(newMember)
          }
          this.saveMembers()
          this.dialogVisible = false
          this.$message.success('操作成功')
        }
      })
    },
    rechargeHours(member) {
      this.currentMember = member
      this.hourForm = { type: 'recharge', hours: 10, remark: '' }
      this.hourDialogVisible = true
    },
    deductHours(member) {
      this.currentMember = member
      this.hourForm = { type: 'deduct', hours: 1, remark: '' }
      this.hourDialogVisible = true
    },
    submitHourForm() {
      const isRecharge = this.hourForm.type === 'recharge'
      const hours = this.hourForm.hours
      
      if (isRecharge) {
        this.currentMember.totalHours += hours
        this.currentMember.remainingHours += hours
      } else {
        if (this.currentMember.remainingHours < hours) {
          this.$message.error('剩余课时不足')
          return
        }
        this.currentMember.usedHours += hours
        this.currentMember.remainingHours -= hours
      }

      if (!this.currentMember.records) this.currentMember.records = []
      this.currentMember.records.unshift({
        time: new Date().toLocaleString(),
        type: isRecharge ? '充值' : '消课',
        hours: hours,
        remark: this.hourForm.remark
      })

      this.saveMembers()
      this.hourDialogVisible = false
      this.$message.success('操作成功')
    },
    viewRecords(member) {
      this.currentMemberRecords = member.records || []
      this.recordDialogVisible = true
    }
  }
}
</script>

<style scoped>
.course-hours {
  padding: 0;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: 500;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.low-balance {
  color: #f56c6c;
  font-weight: 500;
}

.expired {
  color: #909399;
  text-decoration: line-through;
}
</style>
