<template>
  <div class="member-info">
    <div class="page-title">会员信息管理</div>
    <div class="card-wrapper">
      <el-row :gutter="20" style="margin-bottom: 20px;">
        <el-col :span="6">
          <el-input v-model="searchKey" placeholder="请输入会员姓名或手机号搜索">
            <i slot="prefix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-select v-model="searchLevel" placeholder="会员等级" clearable style="width: 100%;">
            <el-option label="普通会员" value="普通会员"></el-option>
            <el-option label="银卡会员" value="银卡会员"></el-option>
            <el-option label="金卡会员" value="金卡会员"></el-option>
            <el-option label="钻石会员" value="钻石会员"></el-option>
          </el-select>
        </el-col>
        <el-col :span="12" style="text-align: right;">
          <el-button type="primary" @click="handleAdd">
            <i class="el-icon-plus"></i> 添加会员
          </el-button>
          <el-button @click="handleRefresh">
            <i class="el-icon-refresh"></i> 刷新
          </el-button>
          <el-button @click="handleExport">
            <i class="el-icon-download"></i> 导出数据
          </el-button>
        </el-col>
      </el-row>

      <el-table :data="filteredMemberList" border stripe style="width: 100%;">
        <el-table-column prop="cardNo" label="会员卡号" width="140"></el-table-column>
        <el-table-column prop="name" label="会员姓名" width="120"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130"></el-table-column>
        <el-table-column prop="petName" label="宠物名称" width="120"></el-table-column>
        <el-table-column prop="petType" label="宠物类型" width="100"></el-table-column>
        <el-table-column prop="level" label="会员等级" width="120">
          <template slot-scope="scope">
            <el-tag :type="getLevelType(scope.row.level)">{{ scope.row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="balance" label="账户余额" width="120">
          <template slot-scope="scope">
            <span style="color: #67C23A; font-weight: bold;">¥{{ scope.row.balance }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="points" label="积分" width="100"></el-table-column>
        <el-table-column prop="registerDate" label="注册日期" width="160"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '正常' ? 'success' : 'danger'">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button size="small" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="small" type="success" @click="handleRecharge(scope.row)">充值</el-button>
            <el-button size="small" type="danger" @click="handleDelete(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        style="margin-top: 20px; text-align: right;"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredMemberList.length"
      ></el-pagination>
    </div>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="600px"
    >
      <el-form :model="formData" :rules="rules" ref="formData" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="会员姓名" prop="name">
              <el-input v-model="formData.name"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="formData.phone"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="宠物名称" prop="petName">
              <el-input v-model="formData.petName"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宠物类型" prop="petType">
              <el-select v-model="formData.petType" style="width: 100%;">
                <el-option label="小型犬" value="小型犬"></el-option>
                <el-option label="中型犬" value="中型犬"></el-option>
                <el-option label="大型犬" value="大型犬"></el-option>
                <el-option label="猫咪" value="猫咪"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="会员等级" prop="level">
              <el-select v-model="formData.level" style="width: 100%;">
                <el-option label="普通会员" value="普通会员"></el-option>
                <el-option label="银卡会员" value="银卡会员"></el-option>
                <el-option label="金卡会员" value="金卡会员"></el-option>
                <el-option label="钻石会员" value="钻石会员"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户余额" prop="balance">
              <el-input-number v-model="formData.balance" :min="0" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="会员状态" prop="status">
          <el-radio-group v-model="formData.status">
            <el-radio label="正常">正常</el-radio>
            <el-radio label="冻结">冻结</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="formData.remark" :rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="会员充值"
      :visible.sync="rechargeDialogVisible"
      width="500px"
    >
      <el-form :model="rechargeForm" label-width="100px">
        <el-form-item label="会员姓名">
          <span>{{ currentMember.name }}</span>
        </el-form-item>
        <el-form-item label="当前余额">
          <span style="color: #67C23A; font-weight: bold;">¥{{ currentMember.balance }}</span>
        </el-form-item>
        <el-form-item label="充值金额" prop="amount">
          <el-input-number v-model="rechargeForm.amount" :min="0" :step="50" style="width: 100%;"></el-input-number>
        </el-form-item>
        <el-form-item label="赠送积分">
          <el-input-number v-model="rechargeForm.points" :min="0" style="width: 100%;"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rechargeDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleRechargeSubmit">确认充值</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'MemberInfo',
  data() {
    const validatePhone = (rule, value, callback) => {
      const phoneReg = /^1[3-9]\d{9}$/
      if (!value) {
        callback(new Error('请输入联系电话'))
      } else if (!phoneReg.test(value)) {
        callback(new Error('请输入正确的手机号码'))
      } else {
        callback()
      }
    }

    return {
      searchKey: '',
      searchLevel: '',
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      dialogTitle: '添加会员',
      editIndex: -1,
      rechargeDialogVisible: false,
      currentMember: {},
      rechargeForm: {
        amount: 0,
        points: 0
      },
      formData: {
        cardNo: '',
        name: '',
        phone: '',
        petName: '',
        petType: '',
        level: '普通会员',
        balance: 0,
        points: 0,
        status: '正常',
        remark: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入会员姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        petName: [
          { required: true, message: '请输入宠物名称', trigger: 'blur' }
        ],
        petType: [
          { required: true, message: '请选择宠物类型', trigger: 'change' }
        ]
      },
      memberList: []
    }
  },
  created() {
    this.loadMemberList()
    window.addEventListener('storage', this.handleStorageChange)
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.handleStorageChange)
  },
  methods: {
    loadMemberList() {
      const defaultMembers = [
        {
          cardNo: 'VIP20240001',
          name: '张三',
          phone: '13800138001',
          petName: '豆豆',
          petType: '小型犬',
          level: '金卡会员',
          balance: 1580,
          points: 3200,
          registerDate: '2024-01-15',
          status: '正常',
          remark: '老客户，服务周到'
        },
        {
          cardNo: 'VIP20240002',
          name: '李四',
          phone: '13800138002',
          petName: '咪咪',
          petType: '猫咪',
          level: '银卡会员',
          balance: 680,
          points: 1500,
          registerDate: '2024-02-20',
          status: '正常',
          remark: ''
        },
        {
          cardNo: 'VIP20240003',
          name: '王五',
          phone: '13800138003',
          petName: '旺财',
          petType: '中型犬',
          level: '钻石会员',
          balance: 3200,
          points: 8500,
          registerDate: '2023-11-08',
          status: '正常',
          remark: 'VIP客户，优先服务'
        },
        {
          cardNo: 'VIP20240004',
          name: '赵六',
          phone: '13800138004',
          petName: '毛球',
          petType: '大型犬',
          level: '普通会员',
          balance: 200,
          points: 300,
          registerDate: '2024-03-10',
          status: '正常',
          remark: ''
        },
        {
          cardNo: 'VIP20240005',
          name: '孙七',
          phone: '13800138005',
          petName: '小白',
          petType: '小型犬',
          level: '银卡会员',
          balance: 850,
          points: 1800,
          registerDate: '2024-01-25',
          status: '冻结',
          remark: '长期未消费'
        }
      ]
      const stored = localStorage.getItem('memberList')
      if (stored) {
        this.memberList = JSON.parse(stored)
      } else {
        this.memberList = defaultMembers
        this.saveMemberList(defaultMembers)
      }
    },
    handleStorageChange(e) {
      if (e.key === 'memberList') {
        this.loadMemberList()
      }
    },
    saveMemberList(list) {
      localStorage.setItem('memberList', JSON.stringify(list))
    },
    handleRefresh() {
      this.loadMemberList()
      this.$message.success('数据已刷新')
    }
  },
  computed: {
    filteredMemberList() {
      let list = this.memberList
      if (this.searchKey) {
        list = list.filter(item => 
          item.name.includes(this.searchKey) || 
          item.phone.includes(this.searchKey)
        )
      }
      if (this.searchLevel) {
        list = list.filter(item => item.level === this.searchLevel)
      }
      return list
    }
  },
  methods: {
    getLevelType(level) {
      const typeMap = {
        '普通会员': 'info',
        '银卡会员': '',
        '金卡会员': 'warning',
        '钻石会员': 'danger'
      }
      return typeMap[level] || ''
    },
    handleAdd() {
      this.dialogTitle = '添加会员'
      this.editIndex = -1
      this.formData = {
        cardNo: 'VIP' + Date.now().toString().slice(-8),
        name: '',
        phone: '',
        petName: '',
        petType: '',
        level: '普通会员',
        balance: 0,
        points: 0,
        status: '正常',
        remark: ''
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑会员'
      this.editIndex = this.memberList.indexOf(row)
      this.formData = { ...row }
      this.dialogVisible = true
    },
    handleDelete(index) {
      this.$confirm('确定要删除该会员吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.memberList.splice(index, 1)
        this.saveMemberList(this.memberList)
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleRecharge(row) {
      this.currentMember = row
      this.rechargeForm = { amount: 0, points: 0 }
      this.rechargeDialogVisible = true
    },
    handleRechargeSubmit() {
      if (this.rechargeForm.amount <= 0) {
        this.$message.error('请输入充值金额')
        return
      }
      const index = this.memberList.findIndex(m => m.cardNo === this.currentMember.cardNo)
      if (index > -1) {
        this.memberList[index].balance = Math.round((this.memberList[index].balance + this.rechargeForm.amount) * 100) / 100
        this.memberList[index].points += this.rechargeForm.points
        this.saveMemberList(this.memberList)
        this.$message.success('充值成功')
        this.rechargeDialogVisible = false
      }
    },
    handleSubmit() {
      this.$refs.formData.validate((valid) => {
        if (valid) {
          this.formData.registerDate = new Date().toLocaleDateString()
          if (this.editIndex === -1) {
            this.memberList.unshift({ ...this.formData })
            this.$message.success('添加成功')
          } else {
            this.memberList[this.editIndex] = { ...this.formData }
            this.$message.success('修改成功')
          }
          this.saveMemberList(this.memberList)
          this.dialogVisible = false
        }
      })
    },
    handleExport() {
      this.$message.success('数据导出成功')
    },
    handleSizeChange(size) {
      this.pageSize = size
    },
    handleCurrentChange(page) {
      this.currentPage = page
    }
  }
}
</script>

<style scoped>
</style>
