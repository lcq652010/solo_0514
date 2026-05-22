<template>
  <div class="page-container">
    <div class="page-header">
      <h2>商品入库</h2>
    </div>
    <div class="page-content">
      <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="form-container"
      >
        <el-form-item label="商品名称" prop="productId">
          <el-select
            v-model="form.productId"
            placeholder="请选择商品"
            style="width: 100%"
            filterable
            @change="handleProductChange"
          >
            <el-option
              v-for="item in productList"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            >
              <span style="float: left">{{ item.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 13px">
                当前库存: {{ item.stock }}{{ item.unit }}
              </span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="商品编码" prop="code">
          <el-input v-model="form.code" disabled placeholder="选择商品后自动填充" />
        </el-form-item>

        <el-form-item label="商品分类" prop="category">
          <el-input v-model="form.category" disabled placeholder="选择商品后自动填充" />
        </el-form-item>

        <el-form-item label="入库数量" prop="quantity">
          <el-input-number
            v-model="form.quantity"
            :min="1"
            :max="9999"
            style="width: 100%"
          />
        </el-form-item>

        <el-form-item label="当前库存" prop="currentStock">
          <el-input v-model="form.currentStock" disabled />
        </el-form-item>

        <el-form-item label="入库后库存" prop="afterStock">
          <el-input v-model="afterStock" disabled />
        </el-form-item>

        <el-form-item label="操作人" prop="operator">
          <el-input v-model="form.operator" placeholder="请输入操作人姓名" />
        </el-form-item>

        <el-form-item label="备注" prop="remark">
          <el-input
            v-model="form.remark"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="loading">
            确认入库
          </el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { api, mockProducts } from '../api/mockData'

export default {
  name: 'StockIn',
  data() {
    return {
      loading: false,
      productList: mockProducts,
      form: {
        productId: null,
        code: '',
        category: '',
        quantity: 1,
        currentStock: 0,
        operator: '',
        remark: ''
      },
      rules: {
        productId: [
          { required: true, message: '请选择商品', trigger: 'change' }
        ],
        quantity: [
          { required: true, message: '请输入入库数量', trigger: 'blur' },
          { type: 'number', min: 1, max: 9999, message: '入库数量必须在1-9999之间', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (!Number.isInteger(value)) {
                callback(new Error('入库数量必须为正整数'))
              } else if (value > 9999) {
                callback(new Error('入库数量上限为9999'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ],
        operator: [
          { required: true, message: '请输入操作人姓名', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    afterStock() {
      return this.form.currentStock + this.form.quantity
    }
  },
  methods: {
    handleProductChange(productId) {
      const product = this.productList.find(item => item.id === productId)
      if (product) {
        this.form.code = product.code
        this.form.category = product.category
        this.form.currentStock = product.stock
      }
    },
    submitForm() {
      this.$refs.form.validate(async (valid) => {
        if (valid) {
          this.loading = true
          try {
            const res = await api.addStockIn(this.form)
            if (res.code === 200) {
              this.$message.success(res.message)
              this.resetForm()
              const product = this.productList.find(item => item.id === this.form.productId)
              if (product) {
                product.stock += this.form.quantity
              }
            }
          } catch (error) {
            this.$message.error('入库失败，请重试')
          } finally {
            this.loading = false
          }
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
      this.form.productId = null
      this.form.code = ''
      this.form.category = ''
      this.form.quantity = 1
      this.form.currentStock = 0
      this.form.operator = ''
      this.form.remark = ''
    }
  }
}
</script>
