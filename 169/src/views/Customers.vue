<template>
  <div class="page-container">
    <div class="page-title">客户档案管理</div>
    
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索客户姓名/电话/车牌号"
        style="width: 300px; margin-right: 10px"
        clearable
      ></el-input>
      <el-select v-model="selectedLevel" placeholder="客户等级" style="width: 150px; margin-right: 10px" clearable>
        <el-option label="全部等级" value=""></el-option>
        <el-option label="普通客户" value="普通客户"></el-option>
        <el-option label="VIP客户" value="VIP客户"></el-option>
        <el-option label="SVIP客户" value="SVIP客户"></el-option>
      </el-select>
      <el-button type="primary" @click="loadCustomers">搜索</el-button>
      <el-button type="success" style="margin-left: 10px" @click="showAddDialog">新增客户</el-button>
    </div>

    <div class="table-container">
      <el-table :data="customerList" border style="width: 100%">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="customerNo" label="客户编号" width="130" align="center"></el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column prop="gender" label="性别" width="70" align="center"></el-table-column>
        <el-table-column prop="plateNumber" label="车牌号" width="110" align="center"></el-table-column>
        <el-table-column prop="carBrand" label="车辆品牌" width="100" align="center"></el-table-column>
        <el-table-column prop="carModel" label="车型" width="130" align="center"></el-table-column>
        <el-table-column prop="level" label="客户等级" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getLevelTagType(scope.row.level)" size="small">{{ scope.row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="totalOrders" label="预约次数" width="90" align="center"></el-table-column>
        <el-table-column prop="totalAmount" label="累计消费" width="100" align="center">
          <template slot-scope="scope">
            ¥{{ scope.row.totalAmount }}
          </template>
        </el-table-column>
        <el-table-column prop="lastServiceTime" label="最后服务时间" width="160" align="center"></el-table-column>
        <el-table-column prop="registerTime" label="注册时间" width="160" align="center"></el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">详情</el-button>
            <el-button size="mini" type="warning" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="pagination-container">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="650px" @close="handleDialogClose">
      <el-form
        ref="customerForm"
        :model="customerForm"
        :rules="customerRules"
        label-width="100px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="customerForm.customerName" placeholder="请输入客户姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="customerForm.phone" placeholder="请输入联系电话" maxlength="11"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="customerForm.gender">
                <el-radio label="男">男</el-radio>
                <el-radio label="女">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="客户等级" prop="level">
              <el-select v-model="customerForm.level" placeholder="请选择客户等级" style="width: 100%">
                <el-option label="普通客户" value="普通客户"></el-option>
                <el-option label="VIP客户" value="VIP客户"></el-option>
                <el-option label="SVIP客户" value="SVIP客户"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-divider content-position="left">车辆信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="车牌号" prop="plateNumber">
              <el-input v-model="customerForm.plateNumber" placeholder="请输入车牌号"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="车辆品牌" prop="carBrand">
              <el-select v-model="customerForm.carBrand" placeholder="请选择车辆品牌" style="width: 100%">
                <el-option label="奥迪" value="奥迪"></el-option>
                <el-option label="宝马" value="宝马"></el-option>
                <el-option label="奔驰" value="奔驰"></el-option>
                <el-option label="大众" value="大众"></el-option>
                <el-option label="丰田" value="丰田"></el-option>
                <el-option label="本田" value="本田"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="车型" prop="carModel">
              <el-input v-model="customerForm.carModel" placeholder="请输入车型"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注" prop="remark">
              <el-input
                v-model="customerForm.remark"
                type="textarea"
                :rows="3"
                placeholder="请输入备注信息"
              ></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </div>
    </el-dialog>

    <el-dialog title="客户详情" :visible.sync="detailDialogVisible" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="客户编号">{{ currentDetail.customerNo }}</el-descriptions-item>
        <el-descriptions-item label="客户等级">
          <el-tag :type="getLevelTagType(currentDetail.level)" size="small">{{ currentDetail.level }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentDetail.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentDetail.phone }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ currentDetail.gender }}</el-descriptions-item>
        <el-descriptions-item label="车牌号">{{ currentDetail.plateNumber }}</el-descriptions-item>
        <el-descriptions-item label="车辆品牌">{{ currentDetail.carBrand }}</el-descriptions-item>
        <el-descriptions-item label="车型">{{ currentDetail.carModel }}</el-descriptions-item>
        <el-descriptions-item label="预约次数">{{ currentDetail.totalOrders }} 次</el-descriptions-item>
        <el-descriptions-item label="累计消费">¥{{ currentDetail.totalAmount }}</el-descriptions-item>
        <el-descriptions-item label="最后服务时间" :span="2">{{ currentDetail.lastServiceTime }}</el-descriptions-item>
        <el-descriptions-item label="注册时间" :span="2">{{ currentDetail.registerTime }}</el-descriptions-item>
        <el-descriptions-item label="备注信息" :span="2">{{ currentDetail.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Customers',
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
      selectedLevel: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      customerList: [],
      dialogVisible: false,
      dialogTitle: '新增客户',
      detailDialogVisible: false,
      isEdit: false,
      currentDetail: {},
      customerForm: {
        customerName: '',
        phone: '',
        gender: '男',
        level: '普通客户',
        plateNumber: '',
        carBrand: '',
        carModel: '',
        remark: ''
      },
      customerRules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        plateNumber: [
          { required: true, message: '请输入车牌号', trigger: 'blur' }
        ],
        carBrand: [
          { required: true, message: '请选择车辆品牌', trigger: 'change' }
        ],
        carModel: [
          { required: true, message: '请输入车型', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.loadCustomers()
  },
  methods: {
    getLevelTagType(level) {
      const typeMap = {
        '普通客户': 'info',
        'VIP客户': 'warning',
        'SVIP客户': 'danger'
      }
      return typeMap[level] || 'info'
    },
    loadCustomers() {
      const mockData = [
        { id: 1, customerNo: 'KH20240001', customerName: '陈先生', phone: '13800138001', gender: '男', plateNumber: '京A12345', carBrand: '奥迪', carModel: 'A6L', level: 'VIP客户', totalOrders: 12, totalAmount: 8600, lastServiceTime: '2024-01-15 11:30:00', registerTime: '2023-06-15 09:30:00', remark: '老客户，服务态度要好' },
        { id: 2, customerNo: 'KH20240002', customerName: '林女士', phone: '13800138002', gender: '女', plateNumber: '京B67890', carBrand: '宝马', carModel: '5系', level: '普通客户', totalOrders: 5, totalAmount: 3500, lastServiceTime: '2024-01-14 16:00:00', registerTime: '2023-09-20 14:20:00', remark: '' },
        { id: 3, customerNo: 'KH20240003', customerName: '吴先生', phone: '13800138003', gender: '男', plateNumber: '京C11111', carBrand: '奔驰', carModel: 'E级', level: 'SVIP客户', totalOrders: 25, totalAmount: 28000, lastServiceTime: '2024-01-13 10:00:00', registerTime: '2023-03-10 11:00:00', remark: '重要客户，需专人接待' },
        { id: 4, customerNo: 'KH20240004', customerName: '郑女士', phone: '13800138004', gender: '女', plateNumber: '京D22222', carBrand: '大众', carModel: '迈腾', level: '普通客户', totalOrders: 3, totalAmount: 1800, lastServiceTime: '2024-01-12 15:30:00', registerTime: '2023-11-05 09:00:00', remark: '' },
        { id: 5, customerNo: 'KH20240005', customerName: '黄先生', phone: '13800138005', gender: '男', plateNumber: '京E33333', carBrand: '丰田', carModel: '凯美瑞', level: 'VIP客户', totalOrders: 8, totalAmount: 6200, lastServiceTime: '2024-01-11 14:00:00', registerTime: '2023-07-18 16:30:00', remark: '' },
        { id: 6, customerNo: 'KH20240006', customerName: '张先生', phone: '13800138006', gender: '男', plateNumber: '京F44444', carBrand: '本田', carModel: '雅阁', level: '普通客户', totalOrders: 2, totalAmount: 1200, lastServiceTime: '2024-01-10 11:00:00', registerTime: '2023-12-01 10:00:00', remark: '' },
        { id: 7, customerNo: 'KH20240007', customerName: '李女士', phone: '13800138007', gender: '女', plateNumber: '京G55555', carBrand: '奥迪', carModel: 'Q5', level: 'VIP客户', totalOrders: 10, totalAmount: 12000, lastServiceTime: '2024-01-09 15:00:00', registerTime: '2023-05-20 09:30:00', remark: '对机油品质要求高' },
        { id: 8, customerNo: 'KH20240008', customerName: '王先生', phone: '13800138008', gender: '男', plateNumber: '京H66666', carBrand: '宝马', carModel: 'X3', level: '普通客户', totalOrders: 4, totalAmount: 3200, lastServiceTime: '2024-01-08 10:30:00', registerTime: '2023-10-12 14:00:00', remark: '' },
        { id: 9, customerNo: 'KH20240009', customerName: '赵先生', phone: '13800138009', gender: '男', plateNumber: '京I77777', carBrand: '奔驰', carModel: 'GLC', level: 'SVIP客户', totalOrders: 18, totalAmount: 22000, lastServiceTime: '2024-01-07 16:00:00', registerTime: '2023-04-08 11:30:00', remark: '高端客户' },
        { id: 10, customerNo: 'KH20240010', customerName: '刘女士', phone: '13800138010', gender: '女', plateNumber: '京J88888', carBrand: '大众', carModel: '途观', level: '普通客户', totalOrders: 6, totalAmount: 4200, lastServiceTime: '2024-01-06 14:30:00', registerTime: '2023-08-25 09:00:00', remark: '' }
      ]

      let filteredData = mockData

      if (this.searchKeyword) {
        filteredData = filteredData.filter(item => 
          item.customerName.includes(this.searchKeyword) || 
          item.phone.includes(this.searchKeyword) || 
          item.plateNumber.includes(this.searchKeyword)
        )
      }

      if (this.selectedLevel) {
        filteredData = filteredData.filter(item => 
          item.level === this.selectedLevel
        )
      }

      this.total = filteredData.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.customerList = filteredData.slice(start, end)
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadCustomers()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadCustomers()
    },
    showAddDialog() {
      this.isEdit = false
      this.dialogTitle = '新增客户'
      this.customerForm = {
        customerName: '',
        phone: '',
        gender: '男',
        level: '普通客户',
        plateNumber: '',
        carBrand: '',
        carModel: '',
        remark: ''
      }
      this.dialogVisible = true
    },
    handleView(row) {
      this.currentDetail = row
      this.detailDialogVisible = true
    },
    handleEdit(row) {
      this.isEdit = true
      this.dialogTitle = '编辑客户'
      this.customerForm = {
        id: row.id,
        customerName: row.customerName,
        phone: row.phone,
        gender: row.gender,
        level: row.level,
        plateNumber: row.plateNumber,
        carBrand: row.carBrand,
        carModel: row.carModel,
        remark: row.remark
      }
      this.dialogVisible = true
    },
    handleDelete(row) {
      this.$confirm(`确定要删除客户 ${row.customerName} 的档案吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('删除成功！')
        this.loadCustomers()
      }).catch(() => {})
    },
    handleSave() {
      this.$refs.customerForm.validate((valid) => {
        if (valid) {
          this.dialogVisible = false
          this.$message.success(this.isEdit ? '编辑成功！' : '新增成功！')
          this.loadCustomers()
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleDialogClose() {
      this.$refs.customerForm.resetFields()
    }
  }
}
</script>

<style scoped>
</style>
