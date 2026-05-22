<template>
  <div class="page-container">
    <el-card class="card-box">
      <div slot="header" class="clearfix">
        <span>会员管理</span>
        <el-button style="float: right; padding: 3px 0" type="primary" @click="handleAdd">
          <i class="el-icon-plus"></i> 新增会员
        </el-button>
      </div>
      
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="会员卡号">
            <el-input v-model="searchForm.memberNo" placeholder="请输入" clearable style="width: 150px;"></el-input>
          </el-form-item>
          <el-form-item label="姓名">
            <el-input v-model="searchForm.name" placeholder="请输入" clearable style="width: 120px;"></el-input>
          </el-form-item>
          <el-form-item label="手机号">
            <el-input v-model="searchForm.phone" placeholder="请输入" clearable style="width: 150px;"></el-input>
          </el-form-item>
          <el-form-item label="会员等级">
            <el-select v-model="searchForm.level" placeholder="请选择" clearable style="width: 120px;">
              <el-option label="普通会员" value="普通会员"></el-option>
              <el-option label="银卡会员" value="银卡会员"></el-option>
              <el-option label="金卡会员" value="金卡会员"></el-option>
              <el-option label="钻石会员" value="钻石会员"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择" clearable style="width: 120px;">
              <el-option label="正常" value="正常"></el-option>
              <el-option label="冻结" value="冻结"></el-option>
              <el-option label="已注销" value="已注销"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <el-table :data="tableData" stripe style="width: 100%;" v-loading="loading">
        <el-table-column prop="memberNo" label="会员卡号" width="140"></el-table-column>
        <el-table-column prop="name" label="姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="手机号" width="130"></el-table-column>
        <el-table-column label="会员等级" width="110">
          <template slot-scope="scope">
            <el-tag :type="getLevelType(scope.row.level)" size="small">{{ scope.row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="points" label="积分" width="100"></el-table-column>
        <el-table-column prop="balance" label="余额(元)" width="110"></el-table-column>
        <el-table-column prop="totalPackages" label="累计包裹" width="100"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '正常' ? 'success' : 'danger'" size="small">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="registerTime" label="注册时间" width="160"></el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="warning" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
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
    
    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="600px">
      <el-form :model="memberForm" :rules="rules" ref="memberForm" label-width="100px">
        <el-form-item label="会员卡号" v-if="isView">
          <span>{{ memberForm.memberNo }}</span>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="memberForm.name" :disabled="isView" placeholder="请输入姓名"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="memberForm.phone" :disabled="isView" placeholder="请输入手机号"></el-input>
        </el-form-item>
        <el-form-item label="会员等级" prop="level">
          <el-select v-model="memberForm.level" :disabled="isView" placeholder="请选择会员等级" style="width: 100%;">
            <el-option label="普通会员" value="普通会员"></el-option>
            <el-option label="银卡会员" value="银卡会员"></el-option>
            <el-option label="金卡会员" value="金卡会员"></el-option>
            <el-option label="钻石会员" value="钻石会员"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="积分" prop="points" v-if="!isAdd">
          <el-input-number v-model="memberForm.points" :disabled="isView" :min="0" style="width: 100%;"></el-input-number>
        </el-form-item>
        <el-form-item label="余额(元)" prop="balance" v-if="!isAdd">
          <el-input-number v-model="memberForm.balance" :disabled="isView" :min="0" :precision="2" style="width: 100%;"></el-input-number>
        </el-form-item>
        <el-form-item label="状态" prop="status" v-if="!isAdd">
          <el-select v-model="memberForm.status" :disabled="isView" placeholder="请选择状态" style="width: 100%;">
            <el-option label="正常" value="正常"></el-option>
            <el-option label="冻结" value="冻结"></el-option>
            <el-option label="已注销" value="已注销"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="memberForm.remark" :disabled="isView" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" v-if="!isView">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'MemberManage',
  data() {
    const validatePhone = (rule, value, callback) => {
      const reg = /^1[3-9]\d{9}$/
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!reg.test(value)) {
        callback(new Error('请输入正确的手机号码格式'))
      } else {
        callback()
      }
    }
    return {
      loading: false,
      searchForm: {
        memberNo: '',
        name: '',
        phone: '',
        level: '',
        status: ''
      },
      tableData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '',
      isView: false,
      isAdd: false,
      memberForm: {
        memberNo: '',
        name: '',
        phone: '',
        level: '',
        points: 0,
        balance: 0,
        status: '正常',
        remark: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        level: [
          { required: true, message: '请选择会员等级', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    getLevelType(level) {
      const levelMap = {
        '普通会员': 'info',
        '银卡会员': 'warning',
        '金卡会员': 'success',
        '钻石会员': 'danger'
      }
      return levelMap[level] || 'info'
    },
    handleSearch() {
      this.loading = true
      setTimeout(() => {
        this.loadData()
        this.loading = false
      }, 500)
    },
    handleReset() {
      this.searchForm = {
        memberNo: '',
        name: '',
        phone: '',
        level: '',
        status: ''
      }
      this.handleSearch()
    },
    handleAdd() {
      this.dialogTitle = '新增会员'
      this.isView = false
      this.isAdd = true
      this.memberForm = {
        memberNo: '',
        name: '',
        phone: '',
        level: '普通会员',
        points: 0,
        balance: 0,
        status: '正常',
        remark: ''
      }
      this.dialogVisible = true
    },
    handleView(row) {
      this.dialogTitle = '会员详情'
      this.isView = true
      this.isAdd = false
      this.memberForm = { ...row }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.dialogTitle = '编辑会员'
      this.isView = false
      this.isAdd = false
      this.memberForm = { ...row }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm('确认删除该会员？删除后数据不可恢复！', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.tableData.findIndex(item => item.memberNo === row.memberNo)
        if (index > -1) {
          this.tableData.splice(index, 1)
          this.pagination.total--
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.memberForm.validate((valid) => {
        if (valid) {
          if (this.isAdd) {
            const newMember = {
              ...this.memberForm,
              memberNo: 'VIP' + Date.now().toString().slice(-6),
              totalPackages: 0,
              registerTime: new Date().toLocaleString()
            }
            this.tableData.unshift(newMember)
            this.pagination.total++
            this.$message.success('新增会员成功')
          } else {
            const index = this.tableData.findIndex(item => item.memberNo === this.memberForm.memberNo)
            if (index > -1) {
              this.tableData[index] = { ...this.memberForm }
            }
            this.$message.success('编辑会员成功')
          }
          this.dialogVisible = false
        } else {
          this.$message.error('请检查表单信息是否填写正确')
          return false
        }
      })
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadData()
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
      this.loadData()
    },
    loadData() {
      const allData = []
      const levels = ['普通会员', '银卡会员', '金卡会员', '钻石会员']
      const statuses = ['正常', '正常', '正常', '冻结']
      const names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十',
                     '郑十一', '王十二', '冯十三', '陈十四', '褚十五', '卫十六',
                     '蒋十七', '沈十八', '韩十九', '杨二十']
      
      for (let i = 1; i <= 42; i++) {
        allData.push({
          memberNo: 'VIP' + (100000 + i).toString(),
          name: names[i % names.length] + i,
          phone: '138' + (10000000 + i).toString().slice(-8),
          level: levels[Math.floor(Math.random() * levels.length)],
          points: Math.floor(Math.random() * 5000),
          balance: (Math.random() * 500).toFixed(2),
          totalPackages: Math.floor(Math.random() * 100),
          status: statuses[Math.floor(Math.random() * statuses.length)],
          registerTime: '2023-' + (Math.floor(Math.random() * 12) + 1).toString().padStart(2, '0') + '-' +
                        (Math.floor(Math.random() * 28) + 1).toString().padStart(2, '0') + ' ' +
                        Math.floor(Math.random() * 24).toString().padStart(2, '0') + ':' +
                        Math.floor(Math.random() * 60).toString().padStart(2, '0') + ':' +
                        Math.floor(Math.random() * 60).toString().padStart(2, '0'),
          remark: ''
        })
      }
      
      let filteredData = allData.filter(item => {
        if (this.searchForm.memberNo && !item.memberNo.includes(this.searchForm.memberNo)) return false
        if (this.searchForm.name && !item.name.includes(this.searchForm.name)) return false
        if (this.searchForm.phone && !item.phone.includes(this.searchForm.phone)) return false
        if (this.searchForm.level && item.level !== this.searchForm.level) return false
        if (this.searchForm.status && item.status !== this.searchForm.status) return false
        return true
      })
      
      this.pagination.total = filteredData.length
      
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      this.tableData = filteredData.slice(start, end)
    }
  },
  mounted() {
    this.loadData()
  }
}
</script>

<style scoped>
.search-bar {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 15px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.el-pagination {
  padding: 0;
}
</style>
