<template>
  <div class="order-form-container">
    <el-card class="order-card" shadow="hover">
      <div slot="header" class="card-header">
        <span>客户下单</span>
      </div>
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="木料种类" prop="woodType">
              <el-select v-model="orderForm.woodType" placeholder="请选择木料" style="width: 100%">
                <el-option
                  v-for="wood in woodTypes"
                  :key="wood.value"
                  :label="wood.label"
                  :value="wood.value">
                  <span style="float: left">{{ wood.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">¥{{ wood.price }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="瑞兽款式" prop="beastStyle">
              <el-select v-model="orderForm.beastStyle" placeholder="请选择款式" style="width: 100%">
                <el-option
                  v-for="style in beastStyles"
                  :key="style.value"
                  :label="style.label"
                  :value="style.value">
                  <span style="float: left">{{ style.label }}</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">{{ style.desc }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">尺寸规格（单位：厘米）</el-divider>

        <el-row :gutter="20">
              <el-col :span="8">
                <el-form-item label="长度" prop="length">
                  <el-input-number v-model="orderForm.length" :min="sizeRules.length.min" :max="sizeRules.length.max" :step="sizeRules.length.step" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="宽度" prop="width">
                  <el-input-number v-model="orderForm.width" :min="sizeRules.width.min" :max="sizeRules.width.max" :step="sizeRules.width.step" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
              <el-col :span="8">
                <el-form-item label="高度" prop="height">
                  <el-input-number v-model="orderForm.height" :min="sizeRules.height.min" :max="sizeRules.height.max" :step="sizeRules.height.step" style="width: 100%"></el-input-number>
                </el-form-item>
              </el-col>
            </el-row>

        <el-divider content-position="left">附加选项</el-divider>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="是否鎏金">
              <el-switch
                v-model="orderForm.isGilded"
                active-text="是"
                inactive-text="否">
              </el-switch>
              <span class="gilded-tip">鎏金工艺额外收取 ¥200 工本费</span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="客户备注" prop="remark">
              <el-input
                type="textarea"
                :rows="4"
                placeholder="请输入您的特殊要求或备注信息..."
                v-model="orderForm.remark">
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider></el-divider>

        <el-row :gutter="20">
          <el-col :span="12">
            <div class="price-summary">
              <p class="price-label">预估总价：</p>
              <p class="price-value">¥{{ totalPrice }}</p>
            </div>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <el-button type="primary" size="large" @click="submitOrder" style="width: 100%">提交订单</el-button>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import orderStore from '../store/orderStore'

export default {
  name: 'OrderForm',
  data() {
    const sizeRules = orderStore.sizeRules
    return {
      woodTypes: orderStore.woodTypes,
      beastStyles: orderStore.beastStyles,
      sizeRules: sizeRules,
      orderForm: {
        woodType: '',
        beastStyle: '',
        length: 15,
        width: 5,
        height: 3,
        isGilded: false,
        remark: ''
      },
      rules: {
        woodType: [
          { required: true, message: '请选择木料种类', trigger: 'change' }
        ],
        beastStyle: [
          { required: true, message: '请选择瑞兽款式', trigger: 'change' }
        ],
        length: [
          { required: true, message: '请输入长度', trigger: 'blur' },
          { type: 'number', min: sizeRules.length.min, max: sizeRules.length.max, message: `长度需在${sizeRules.length.min}-${sizeRules.length.max}厘米之间`, trigger: 'blur' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' },
          { type: 'number', min: sizeRules.width.min, max: sizeRules.width.max, message: `宽度需在${sizeRules.width.min}-${sizeRules.width.max}厘米之间`, trigger: 'blur' }
        ],
        height: [
          { required: true, message: '请输入高度', trigger: 'blur' },
          { type: 'number', min: sizeRules.height.min, max: sizeRules.height.max, message: `高度需在${sizeRules.height.min}-${sizeRules.height.max}厘米之间`, trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    totalPrice() {
      let basePrice = orderStore.getWoodPrice(this.orderForm.woodType)
      let gildedPrice = this.orderForm.isGilded ? 200 : 0
      return basePrice + gildedPrice
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const newOrder = orderStore.addOrder({ ...this.orderForm })
          this.$message({
            type: 'success',
            message: `订单提交成功！订单号：${newOrder.id}`
          })
          this.resetForm()
        } else {
          this.$message.error('请完善订单信息后再提交')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.orderForm.isGilded = false
    }
  }
}
</script>

<style scoped>
.order-form-container {
  max-width: 800px;
  margin: 0 auto;
}

.order-card {
  border-radius: 12px;
}

.card-header {
  font-size: 20px;
  font-weight: 600;
  color: #8B4513;
}

.gilded-tip {
  margin-left: 15px;
  color: #E6A23C;
  font-size: 14px;
}

.price-summary {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 10px 0;
}

.price-label {
  margin: 0;
  font-size: 16px;
  color: #606266;
}

.price-value {
  margin: 0 0 0 10px;
  font-size: 28px;
  font-weight: 600;
  color: #F56C6C;
}

.el-divider {
  margin: 20px 0;
}

.el-divider__text {
  color: #8B4513;
  font-weight: 500;
}
</style>
