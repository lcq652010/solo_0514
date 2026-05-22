<template>
  <div class="order-create-page">
    <div class="page-card">
      <div class="page-title">
        <i class="el-icon-edit"></i>
        订单下单
      </div>
      
      <el-form
        ref="orderForm"
        :model="orderForm"
        :rules="rules"
        label-width="120px"
      >
        <el-divider content-position="left">客户信息</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入客户姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="customerPhone">
              <el-input v-model="orderForm.customerPhone" placeholder="请输入联系电话" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="送货地址" prop="address">
          <el-input
            v-model="orderForm.address"
            type="textarea"
            :rows="2"
            placeholder="请输入详细送货地址"
          />
        </el-form-item>
        
        <el-divider content-position="left">商品明细</el-divider>
        
        <div style="margin-bottom: 15px;">
          <el-button type="primary" size="small" @click="showProductDialog">
            <i class="el-icon-plus"></i>
            添加商品
          </el-button>
        </div>
        
        <el-table :data="orderForm.items" border style="width: 100%">
          <el-table-column type="index" label="序号" width="60" align="center" />
          <el-table-column prop="productName" label="商品名称" min-width="180" />
          <el-table-column prop="spec" label="规格" width="120" align="center" />
          <el-table-column prop="unit" label="单位" width="80" align="center" />
          <el-table-column prop="price" label="单价（元）" width="120" align="center" />
          <el-table-column label="数量" width="150" align="center">
            <template slot-scope="scope">
              <el-input-number
                v-model="scope.row.quantity"
                :min="1"
                :max="Math.min(scope.row.stock, scope.row.maxOrder)"
                size="small"
                @change="calculateTotal"
              />
              <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                单次限购：{{ scope.row.maxOrder }} {{ scope.row.unit }}
              </div>
            </template>
          </el-table-column>
          <el-table-column label="小计（元）" width="150" align="center">
            <template slot-scope="scope">
              <span style="color: #f56c6c; font-weight: 600;">{{ (scope.row.price * scope.row.quantity).toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="center">
            <template slot-scope="scope">
              <el-button type="text" size="small" @click="removeItem(scope.$index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-divider content-position="left">订单汇总</el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="订单金额" prop="totalAmount">
              <span style="font-size: 24px; color: #f56c6c; font-weight: 600;">
                {{ orderForm.totalAmount.toFixed(2) }}
              </span>
              <span style="margin-left: 5px;">元</span>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="备注">
          <el-input
            v-model="orderForm.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息（选填）"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder">
            <i class="el-icon-check"></i>
            提交订单
          </el-button>
          <el-button size="large" @click="resetForm">
            <i class="el-icon-refresh-left"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <el-dialog title="选择商品" :visible.sync="productDialogVisible" width="700px">
      <el-input
        v-model="productSearchKeyword"
        placeholder="搜索商品名称"
        clearable
        style="margin-bottom: 15px;"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      
      <el-table :data="filteredProducts" border style="width: 100%" height="400">
        <el-table-column type="index" label="序号" width="60" align="center" />
        <el-table-column prop="name" label="商品名称" min-width="180" />
        <el-table-column prop="category" label="分类" width="100" align="center" />
        <el-table-column prop="spec" label="规格" width="120" align="center" />
        <el-table-column prop="price" label="单价" width="100" align="center" />
        <el-table-column prop="stock" label="库存" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.stock <= 0 ? 'danger' : 'success'" size="small">
              {{ scope.row.stock }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              :disabled="scope.row.stock <= 0 || isProductSelected(scope.row.id)"
              @click="addProduct(scope.row)"
            >
              添加
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script>
import { products, orders } from '@/mock/data'

export default {
  name: 'OrderCreate',
  data() {
    return {
      orderForm: {
        customerName: '',
        customerPhone: '',
        address: '',
        items: [],
        totalAmount: 0,
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        customerPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入送货地址', trigger: 'blur' },
          { min: 5, message: '请输入详细的送货地址', trigger: 'blur' }
        ]
      },
      productDialogVisible: false,
      productSearchKeyword: '',
      productsList: products
    }
  },
  computed: {
    filteredProducts() {
      if (!this.productSearchKeyword) {
        return this.productsList
      }
      return this.productsList.filter(item => 
        item.name.includes(this.productSearchKeyword)
      )
    }
  },
  created() {
    const productId = this.$route.query.productId
    if (productId) {
      const product = products.find(p => p.id === parseInt(productId))
      if (product) {
        this.addProduct(product)
      }
    }
  },
  methods: {
    showProductDialog() {
      this.productSearchKeyword = ''
      this.productDialogVisible = true
    },
    isProductSelected(productId) {
      return this.orderForm.items.some(item => item.productId === productId)
    },
    addProduct(product) {
      this.orderForm.items.push({
        productId: product.id,
        productName: product.name,
        spec: product.spec,
        unit: product.unit,
        price: product.price,
        stock: product.stock,
        maxOrder: product.maxOrder,
        quantity: 1
      })
      this.calculateTotal()
      this.productDialogVisible = false
    },
    removeItem(index) {
      this.orderForm.items.splice(index, 1)
      this.calculateTotal()
    },
    calculateTotal() {
      this.orderForm.totalAmount = this.orderForm.items.reduce((total, item) => {
        return total + item.price * item.quantity
      }, 0)
    },
    validateStock() {
      const insufficientItems = []
      const overLimitItems = []
      
      for (const item of this.orderForm.items) {
        const product = products.find(p => p.id === item.productId)
        if (product) {
          if (item.quantity > product.stock) {
            insufficientItems.push({
              name: item.productName,
              stock: product.stock,
              requested: item.quantity
            })
          }
          if (item.quantity > product.maxOrder) {
            overLimitItems.push({
              name: item.productName,
              maxOrder: product.maxOrder,
              requested: item.quantity
            })
          }
        }
      }
      
      return { insufficientItems, overLimitItems }
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          if (this.orderForm.items.length === 0) {
            this.$message.warning('请至少添加一种商品')
            return
          }
          
          const { insufficientItems, overLimitItems } = this.validateStock()
          if (insufficientItems.length > 0) {
            const errorMsg = insufficientItems.map(item => 
              `${item.name}（库存：${item.stock}，请求：${item.requested}）`
            ).join('、')
            this.$message.error('以下商品库存不足：' + errorMsg)
            return
          }
          
          if (overLimitItems.length > 0) {
            const errorMsg = overLimitItems.map(item => 
              `${item.name}（限购：${item.maxOrder}，请求：${item.requested}）`
            ).join('、')
            this.$message.error('以下商品超过单次下单数量上限：' + errorMsg)
            return
          }
          
          for (const item of this.orderForm.items) {
            const productIndex = products.findIndex(p => p.id === item.productId)
            if (productIndex !== -1) {
              products[productIndex].stock -= item.quantity
            }
          }
          
          const orderId = 'ORD' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + String(Math.floor(Math.random() * 1000)).padStart(3, '0')
          
          const newOrder = {
            id: orderId,
            customerName: this.orderForm.customerName,
            customerPhone: this.orderForm.customerPhone,
            address: this.orderForm.address,
            items: [...this.orderForm.items],
            totalAmount: this.orderForm.totalAmount,
            status: 'pending',
            isShipped: false,
            createTime: new Date().toLocaleString('zh-CN', { hour12: false }).replace(/\//g, '-'),
            remark: this.orderForm.remark
          }
          
          orders.unshift(newOrder)
          
          this.$message.success({
            message: '订单提交成功！订单号：' + orderId,
            duration: 3000
          })
          
          setTimeout(() => {
            this.$router.push('/orders')
          }, 1500)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.items = []
      this.orderForm.totalAmount = 0
    }
  }
}
</script>

<style lang="less" scoped>
.order-create-page {
  .el-divider {
    /deep/ .el-divider__text {
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }
  }
}
</style>
