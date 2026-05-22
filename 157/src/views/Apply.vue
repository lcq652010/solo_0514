<template>
  <div class="page-container">
    <div class="page-header">
      <span class="page-title">用品申领</span>
    </div>
    
    <div class="form-container">
      <el-form :model="form" :rules="rules" ref="form" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="申请部门" prop="departmentId">
              <el-select v-model="form.departmentId" placeholder="请选择部门" style="width: 100%">
                <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="申请人" prop="applicant">
              <el-input v-model="form.applicant" placeholder="请输入申请人姓名"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="申领明细">
          <div style="margin-bottom: 10px;">
            <el-button type="primary" size="small" @click="addItem">
              <i class="el-icon-plus"></i> 添加用品
            </el-button>
          </div>
          <el-table :data="form.items" border>
            <el-table-column label="用品名称" min-width="150">
              <template slot-scope="scope">
                <el-select v-model="scope.row.supplyId" placeholder="请选择用品" style="width: 100%" @change="handleSupplyChange(scope.$index)">
                  <el-option v-for="supply in availableSupplies" :key="supply.id" :label="supply.name" :value="supply.id"></el-option>
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="规格" width="120">
              <template slot-scope="scope">
                <span>{{ getSupplySpec(scope.row.supplyId) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="单位" width="80" align="center">
              <template slot-scope="scope">
                <span>{{ getSupplyUnit(scope.row.supplyId) }}</span>
              </template>
            </el-table-column>
            <el-table-column label="库存数量" width="100" align="center">
              <template slot-scope="scope">
                <span :style="{ color: getSupplyStock(scope.row.supplyId) < 20 ? '#f56c6c' : '' }">
                  {{ getSupplyStock(scope.row.supplyId) }}
                </span>
              </template>
            </el-table-column>
            <el-table-column label="申领数量" width="150">
              <template slot-scope="scope">
                <el-input-number v-model="scope.row.quantity" :min="1" :max="Math.min(getSupplyStock(scope.row.supplyId), maxQuantityPerItem)" style="width: 100%"></el-input-number>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="100" align="center">
              <template slot-scope="scope">
                <el-button type="danger" size="mini" @click="removeItem(scope.$index)">
                  <i class="el-icon-delete"></i>
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
        
        <el-form-item label="备注" prop="remark">
          <el-input type="textarea" v-model="form.remark" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            <i class="el-icon-check"></i> 提交申请
          </el-button>
          <el-button @click="handleReset">
            <i class="el-icon-refresh"></i> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { supplies, departments } from '@/api/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'Apply',
  data() {
    return {
      departments: departments,
      availableSupplies: supplies.filter(s => s.status === 1),
      submitLoading: false,
      maxQuantityPerItem: 50,
      maxTotalQuantity: 100,
      form: {
        departmentId: '',
        applicant: '',
        items: [
          { supplyId: '', quantity: 1 }
        ],
        remark: ''
      },
      rules: {
        departmentId: [
          { required: true, message: '请选择申请部门', trigger: 'change' }
        ],
        applicant: [
          { required: true, message: '请输入申请人姓名', trigger: 'blur' },
          { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    EventBus.$on('stock-updated', () => {
      this.availableSupplies = supplies.filter(s => s.status === 1)
      this.$forceUpdate()
    })
  },
  beforeDestroy() {
    EventBus.$off('stock-updated')
  },
  methods: {
    getSupplySpec(supplyId) {
      const supply = supplies.find(s => s.id === supplyId)
      return supply ? supply.spec : '-'
    },
    getSupplyUnit(supplyId) {
      const supply = supplies.find(s => s.id === supplyId)
      return supply ? supply.unit : '-'
    },
    getSupplyStock(supplyId) {
      const supply = supplies.find(s => s.id === supplyId)
      return supply ? supply.stock : 0
    },
    handleSupplyChange(index) {
      const item = this.form.items[index]
      if (item.quantity > this.getSupplyStock(item.supplyId)) {
        item.quantity = this.getSupplyStock(item.supplyId)
      }
    },
    addItem() {
      this.form.items.push({ supplyId: '', quantity: 1 })
    },
    removeItem(index) {
      if (this.form.items.length <= 1) {
        this.$message.warning('至少需要至少保留一条明细')
        return
      }
      this.form.items.splice(index, 1)
    },
    handleSubmit() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          if (this.form.items.length === 0) {
            this.$message.warning('请添加申领明细')
            return
          }
          
          const hasEmptySupply = this.form.items.some(item => !item.supplyId)
          if (hasEmptySupply) {
            this.$message.warning('请选择所有用品')
            return
          }
          
          const insufficientStockItems = []
          this.form.items.forEach(item => {
            const stock = this.getSupplyStock(item.supplyId)
            if (item.quantity > stock) {
              const supply = supplies.find(s => s.id === item.supplyId)
              insufficientStockItems.push({
                name: supply ? supply.name : '未知用品',
                quantity: item.quantity,
                stock: stock
              })
            }
          })
          
          if (insufficientStockItems.length > 0) {
            const errorMsg = insufficientStockItems.map(item => 
              `${item.name}：申领${item.quantity}，库存${item.stock}`
            ).join('；')
            this.$message.error(`库存不足，无法提交！${errorMsg}`)
            return
          }
          
          const exceedLimitItems = []
          let totalQuantity = 0
          this.form.items.forEach(item => {
            totalQuantity += item.quantity
            if (item.quantity > this.maxQuantityPerItem) {
              const supply = supplies.find(s => s.id === item.supplyId)
              exceedLimitItems.push({
                name: supply ? supply.name : '未知用品',
                quantity: item.quantity
              })
            }
          })
          
          if (exceedLimitItems.length > 0) {
            const errorMsg = exceedLimitItems.map(item => 
              `${item.name}：申领${item.quantity}，上限${this.maxQuantityPerItem}`
            ).join('；')
            this.$message.error(`单品申领数量超上限！${errorMsg}`)
            return
          }
          
          if (totalQuantity > this.maxTotalQuantity) {
            this.$message.error(`单次申领总数量超上限！当前${totalQuantity}，上限${this.maxTotalQuantity}`)
            return
          }
          
          this.submitLoading = true
          
          setTimeout(() => {
            this.submitLoading = false
            this.$message.success('申领提交成功，等待审批')
            this.handleReset()
          }, 1000)
        }
      })
    },
    handleReset() {
      this.$refs.form.resetFields()
      this.form.items = [{ supplyId: '', quantity: 1 }]
    }
  }
}
</script>
