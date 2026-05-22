<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">采购下单</h2>
    </div>

    <div class="form-card">
      <el-form :model="purchaseForm" :rules="rules" ref="purchaseForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="供应商" prop="supplierId">
              <el-select 
                v-model="purchaseForm.supplierId" 
                placeholder="请选择供应商" 
                style="width: 100%"
                filterable
                @change="handleSupplierChange">
                <el-option
                  v-for="item in activeSuppliers"
                  :key="item.id"
                  :label="item.name"
                  :value="item.id">
                  <span>{{ item.name }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ item.contact }} - {{ item.phone }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="采购日期" prop="purchaseDate">
              <el-date-picker
                v-model="purchaseForm.purchaseDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="采购明细" prop="items">
          <div class="items-table">
            <el-table :data="purchaseForm.items" border style="width: 100%">
              <el-table-column prop="productName" label="农产品名称" min-width="160">
                <template slot-scope="scope">
                  <el-select 
                    v-model="scope.row.productId" 
                    placeholder="请选择" 
                    style="width: 100%"
                    filterable
                    :disabled="!purchaseForm.supplierId"
                    @change="(val) => handleProductChange(val, scope.$index)">
                    <el-option
                      v-for="item in availableProducts"
                      :key="item.productId"
                      :label="item.productName + ' (可供应: ' + item.availableQuantity + item.unit + ')'"
                      :value="item.productId">
                    </el-option>
                  </el-select>
                </template>
              </el-table-column>
              <el-table-column prop="unit" label="单位" width="80" align="center">
                <template slot-scope="scope">
                  {{ scope.row.unit }}
                </template>
              </el-table-column>
              <el-table-column prop="availableQuantity" label="可供应量" width="100" align="center">
                <template slot-scope="scope">
                  <span v-if="scope.row.availableQuantity !== undefined" style="color: #67c23a">
                    {{ scope.row.availableQuantity }}
                  </span>
                  <span v-else style="color: #909399">-</span>
                </template>
              </el-table-column>
              <el-table-column prop="price" label="单价(元)" width="140" align="center">
                <template slot-scope="scope">
                  <el-input-number 
                    v-model="scope.row.price" 
                    :min="0.01" 
                    :precision="2" 
                    style="width: 100%"
                    @change="calculateAmount(scope.$index)">
                  </el-input-number>
                </template>
              </el-table-column>
              <el-table-column prop="quantity" label="采购数量" width="140" align="center">
                <template slot-scope="scope">
                  <el-input-number 
                    v-model="scope.row.quantity" 
                    :min="1" 
                    :max="scope.row.availableQuantity || 99999"
                    style="width: 100%"
                    @change="calculateAmount(scope.$index)">
                  </el-input-number>
                </template>
              </el-table-column>
              <el-table-column prop="amount" label="金额(元)" width="140" align="center">
                <template slot-scope="scope">
                  {{ scope.row.amount | formatCurrency }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="100" align="center">
                <template slot-scope="scope">
                  <el-button 
                    type="danger" 
                    icon="el-icon-delete" 
                    circle 
                    size="mini"
                    @click="removeItem(scope.$index)"
                    :disabled="purchaseForm.items.length <= 1">
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="add-item-btn">
              <el-button type="primary" icon="el-icon-plus" @click="addItem">添加农产品</el-button>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="合计金额">
          <span class="total-amount">{{ totalAmount | formatCurrency }}</span>
        </el-form-item>

        <el-form-item label="备注">
          <el-input 
            v-model="purchaseForm.remark" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入备注信息">
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="handleSubmit" :loading="submitting" :disabled="hasStockShortage || submitting">提交采购单</el-button>
          <el-button size="large" @click="handleReset">重置</el-button>
          <el-tooltip v-if="hasStockShortage" content="存在可供应量不足的商品，请检查采购数量" placement="right">
            <i class="el-icon-warning" style="color: #e6a23c; margin-left: 10px;"></i>
          </el-tooltip>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { products, suppliers, orders } from '../mock/data.js'

export default {
  name: 'Purchase',
  data() {
    return {
      products,
      suppliers,
      submitting: false,
      purchaseForm: {
        supplierId: null,
        supplierName: '',
        purchaseDate: '',
        items: [
          { productId: null, productName: '', unit: '', availableQuantity: undefined, price: 0, quantity: 1, amount: 0 }
        ],
        remark: ''
      },
      rules: {
        supplierId: [{ required: true, message: '请选择供应商', trigger: 'change' }],
        purchaseDate: [{ required: true, message: '请选择采购日期', trigger: 'change' }]
      }
    }
  },
  computed: {
    activeSuppliers() {
      return this.suppliers.filter(item => item.status === 1)
    },
    currentSupplier() {
      return this.suppliers.find(item => item.id === this.purchaseForm.supplierId)
    },
    availableProducts() {
      if (!this.currentSupplier || !this.currentSupplier.products) return []
      return this.currentSupplier.products.map(sp => {
        const product = this.products.find(p => p.id === sp.productId)
        return {
          productId: sp.productId,
          productName: sp.productName,
          availableQuantity: sp.availableQuantity,
          unit: product ? product.unit : '',
          price: product ? product.price : 0
        }
      })
    },
    totalAmount() {
      return this.purchaseForm.items.reduce((sum, item) => sum + (item.amount || 0), 0)
    },
    hasStockShortage() {
      return this.purchaseForm.items.some(item => {
        return item.productId && 
               item.availableQuantity !== undefined && 
               (item.quantity > item.availableQuantity || item.availableQuantity <= 0)
      })
    }
  },
  methods: {
    handleSupplierChange(val) {
      const supplier = this.suppliers.find(item => item.id === val)
      if (supplier) {
        this.purchaseForm.supplierName = supplier.name
        this.purchaseForm.items.forEach((item, index) => {
          if (item.productId) {
            const supplierProduct = supplier.products.find(p => p.productId === item.productId)
            if (supplierProduct) {
              item.availableQuantity = supplierProduct.availableQuantity
              if (item.quantity > supplierProduct.availableQuantity) {
                item.quantity = supplierProduct.availableQuantity
                this.calculateAmount(index)
              }
            } else {
              item.productId = null
              item.productName = ''
              item.unit = ''
              item.availableQuantity = undefined
              item.quantity = 1
              item.price = 0
              item.amount = 0
            }
          }
        })
      }
    },
    handleProductChange(val, index) {
      const supplierProduct = this.availableProducts.find(item => item.productId === val)
      if (supplierProduct) {
        this.purchaseForm.items[index].productName = supplierProduct.productName
        this.purchaseForm.items[index].unit = supplierProduct.unit
        this.purchaseForm.items[index].price = supplierProduct.price
        this.purchaseForm.items[index].availableQuantity = supplierProduct.availableQuantity
        if (this.purchaseForm.items[index].quantity > supplierProduct.availableQuantity) {
          this.purchaseForm.items[index].quantity = supplierProduct.availableQuantity
        }
        this.calculateAmount(index)
      }
    },
    calculateAmount(index) {
      const item = this.purchaseForm.items[index]
      item.amount = Number((item.price * item.quantity).toFixed(2))
    },
    addItem() {
      this.purchaseForm.items.push({
        productId: null,
        productName: '',
        unit: '',
        availableQuantity: undefined,
        price: 0,
        quantity: 1,
        amount: 0
      })
    },
    removeItem(index) {
      this.purchaseForm.items.splice(index, 1)
    },
    validateItems() {
      for (let i = 0; i < this.purchaseForm.items.length; i++) {
        const item = this.purchaseForm.items[i]
        if (!item.productId) {
          this.$message.error(`第${i + 1}行请选择农产品`)
          return false
        }
        if (!item.price || item.price <= 0) {
          this.$message.error(`第${i + 1}行采购价格必须为正数`)
          return false
        }
        if (!item.quantity || item.quantity <= 0) {
          this.$message.error(`第${i + 1}行采购数量必须大于0`)
          return false
        }
        if (item.availableQuantity !== undefined && item.quantity > item.availableQuantity) {
          this.$message.error(`第${i + 1}行采购数量(${item.quantity})超过供应商可供应量(${item.availableQuantity})`)
          return false
        }
      }
      return true
    },
    handleSubmit() {
      this.$refs.purchaseForm.validate((valid) => {
        if (valid && this.validateItems()) {
          this.submitting = true
          
          setTimeout(() => {
            const orderNo = 'PO' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + 
              String(orders.length + 1).padStart(4, '0')
            
            const newOrder = {
              id: orderNo,
              supplierId: this.purchaseForm.supplierId,
              supplierName: this.purchaseForm.supplierName,
              totalAmount: this.totalAmount,
              status: 'pending',
              createTime: new Date().toLocaleString(),
              items: this.purchaseForm.items.map(item => ({
                productId: item.productId,
                productName: item.productName,
                quantity: item.quantity,
                unit: item.unit,
                price: item.price,
                amount: item.amount
              }))
            }
            
            orders.unshift(newOrder)
            
            const supplier = this.suppliers.find(s => s.id === this.purchaseForm.supplierId)
            if (supplier && supplier.products) {
              this.purchaseForm.items.forEach(item => {
                const sp = supplier.products.find(p => p.productId === item.productId)
                if (sp) {
                  sp.availableQuantity = Math.max(0, sp.availableQuantity - item.quantity)
                }
              })
            }
            
            this.$message.success('采购单提交成功，订单号：' + orderNo)
            this.submitting = false
            
            const lastSupplierId = this.purchaseForm.supplierId
            this.handleReset()
            this.$nextTick(() => {
              if (lastSupplierId) {
                this.purchaseForm.supplierId = lastSupplierId
                this.handleSupplierChange(lastSupplierId)
              }
            })
          }, 500)
        }
      })
    },
    handleReset() {
      this.$refs.purchaseForm.clearValidate()
      this.purchaseForm = {
        supplierId: null,
        supplierName: '',
        purchaseDate: '',
        items: [
          { productId: null, productName: '', unit: '', availableQuantity: undefined, price: 0, quantity: 1, amount: 0 }
        ],
        remark: ''
      }
    }
  }
}
</script>

<style scoped lang="scss">
.items-table {
  width: 100%;
  
  .add-item-btn {
    margin-top: 12px;
    text-align: left;
  }
}

.total-amount {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}
</style>
