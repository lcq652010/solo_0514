<template>
  <div class="order-page">
    <el-card class="order-card">
      <div slot="header" class="card-header">
        <h2>定制您的专属锡制茶叶罐</h2>
        <p>匠心工艺，品质之选</p>
      </div>

      <el-form 
        ref="orderForm" 
        :model="orderForm" 
        :rules="formRules" 
        label-width="120px"
        class="order-form"
      >
        <el-divider content-position="left">
          <span class="divider-title">基本规格</span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="锡料纯度" prop="purity">
              <el-select v-model="orderForm.purity" placeholder="请选择锡料纯度" style="width: 100%">
                <el-option label="97% 纯锡" value="97%"></el-option>
                <el-option label="99% 高纯锡" value="99%"></el-option>
                <el-option label="99.9% 精锡" value="99.9%"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="罐身高度" prop="height">
              <el-input-number 
                v-model="orderForm.height" 
                :min="sizeRange.height.min" 
                :max="sizeRange.height.max" 
                :step="5"
                style="width: 100%"
              ></el-input-number>
              <span class="unit">mm</span>
              <div class="range-hint" :class="{'range-valid': isHeightValid, 'range-invalid': !isHeightValid}">
                <i class="el-icon-info"></i>
                工艺合理区间：{{ sizeRange.height.min }}-{{ sizeRange.height.max }}mm
                <span v-if="!isHeightValid" class="warning-text">（当前值超出合理范围！）</span>
              </div>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="口径尺寸" prop="diameter">
              <el-input-number 
                v-model="orderForm.diameter" 
                :min="sizeRange.diameter.min" 
                :max="sizeRange.diameter.max" 
                :step="5"
                style="width: 100%"
              ></el-input-number>
              <span class="unit">mm</span>
              <div class="range-hint" :class="{'range-valid': isDiameterValid, 'range-invalid': !isDiameterValid}">
                <i class="el-icon-info"></i>
                工艺合理区间：{{ sizeRange.diameter.min }}-{{ sizeRange.diameter.max }}mm
                <span v-if="!isDiameterValid" class="warning-text">（当前值超出合理范围！）</span>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20" v-if="showSizeRecommendation">
          <el-col :xs="24">
            <el-alert
              :title="sizeRecommendation.title"
              :type="sizeRecommendation.type"
              :description="sizeRecommendation.description"
              show-icon
              :closable="false"
            >
            </el-alert>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title">工艺配置</span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="纹饰风格" prop="pattern">
              <el-radio-group v-model="orderForm.pattern">
                <el-radio label="光面无纹">光面无纹</el-radio>
                <el-radio label="传统祥云">传统祥云</el-radio>
                <el-radio label="山水意境">山水意境</el-radio>
                <el-radio label="梅兰竹菊">梅兰竹菊</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="密封配置" prop="sealType">
              <el-radio-group v-model="orderForm.sealType">
                <el-radio label="标准硅胶圈">标准硅胶圈</el-radio>
                <el-radio label="双层密封圈">双层密封圈</el-radio>
                <el-radio label="真空密封盖">真空密封盖</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title">客户信息</span>
        </el-divider>

        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :xs="24" :sm="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注说明">
          <el-input 
            type="textarea" 
            :rows="3" 
            v-model="orderForm.remark"
            placeholder="如有特殊要求请在此说明..."
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
            提交定制订单
          </el-button>
          <el-button size="large" @click="resetForm">重置表单</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog
      title="订单提交成功"
      :visible.sync="successDialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <div class="success-content">
        <el-result icon="success" title="订单已提交" sub-title="我们将尽快为您安排生产">
          <template slot="extra">
            <div class="order-info">
              <p><strong>订单编号：</strong>{{ newOrder.id }}</p>
              <p><strong>提交时间：</strong>{{ newOrder.createTime }}</p>
              <p><strong>当前状态：</strong>{{ newOrder.status }}</p>
            </div>
          </template>
        </el-result>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="goToAdmin">查看订单管理</el-button>
        <el-button type="primary" @click="continueOrder">继续定制</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import orderStore from '@/store/orderStore'

export default {
  name: 'OrderPage',
  data() {
    return {
      submitting: false,
      successDialogVisible: false,
      newOrder: {},
      sizeRange: {
        height: {
          min: 70,
          max: 150,
          optimalMin: 80,
          optimalMax: 120
        },
        diameter: {
          min: 50,
          max: 120,
          optimalMin: 60,
          optimalMax: 90
        }
      },
      orderForm: {
        purity: '',
        height: 100,
        diameter: 80,
        pattern: '光面无纹',
        sealType: '标准硅胶圈',
        customerName: '',
        phone: '',
        remark: ''
      },
      formRules: {
        purity: [
          { required: true, message: '请选择锡料纯度', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入罐身高度', trigger: 'blur' },
          { type: 'number', min: 70, max: 150, message: '罐身高度必须在 70-150mm 之间', trigger: 'blur' }
        ],
        diameter: [
          { required: true, message: '请输入口径尺寸', trigger: 'blur' },
          { type: 'number', min: 50, max: 120, message: '口径尺寸必须在 50-120mm 之间', trigger: 'blur' }
        ],
        pattern: [
          { required: true, message: '请选择纹饰风格', trigger: 'change' }
        ],
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    isHeightValid() {
      return this.orderForm.height >= this.sizeRange.height.min && 
             this.orderForm.height <= this.sizeRange.height.max
    },
    isDiameterValid() {
      return this.orderForm.diameter >= this.sizeRange.diameter.min && 
             this.orderForm.diameter <= this.sizeRange.diameter.max
    },
    isHeightOptimal() {
      return this.orderForm.height >= this.sizeRange.height.optimalMin && 
             this.orderForm.height <= this.sizeRange.height.optimalMax
    },
    isDiameterOptimal() {
      return this.orderForm.diameter >= this.sizeRange.diameter.optimalMin && 
             this.orderForm.diameter <= this.sizeRange.diameter.optimalMax
    },
    showSizeRecommendation() {
      return !this.isHeightOptimal || !this.isDiameterOptimal
    },
    sizeRecommendation() {
      const messages = []
      if (!this.isHeightOptimal) {
        messages.push(`罐身高度推荐区间：${this.sizeRange.height.optimalMin}-${this.sizeRange.height.optimalMax}mm`)
      }
      if (!this.isDiameterOptimal) {
        messages.push(`口径尺寸推荐区间：${this.sizeRange.diameter.optimalMin}-${this.sizeRange.diameter.optimalMax}mm`)
      }
      return {
        title: '尺寸工艺建议',
        type: 'warning',
        description: messages.join('；') + '，此范围更适合锡制工艺加工和茶叶保存。'
      }
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.newOrder = orderStore.addOrder(this.orderForm)
            this.submitting = false
            this.successDialogVisible = true
          }, 1000)
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
    },
    goToAdmin() {
      this.successDialogVisible = false
      this.$router.push('/admin')
    },
    continueOrder() {
      this.successDialogVisible = false
      this.resetForm()
    }
  }
}
</script>

<style scoped>
.order-page {
  max-width: 800px;
  margin: 0 auto;
}

.order-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.card-header {
  text-align: center;
}

.card-header h2 {
  color: #303133;
  font-size: 24px;
  margin-bottom: 8px;
}

.card-header p {
  color: #909399;
  font-size: 14px;
}

.divider-title {
  font-size: 16px;
  font-weight: 600;
  color: #409eff;
}

.order-form {
  padding: 10px 0;
}

.unit {
  margin-left: 10px;
  color: #909399;
}

.el-radio-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.success-content {
  padding: 20px 0;
}

.order-info {
  text-align: left;
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.order-info p {
  margin: 8px 0;
  color: #606266;
}

.dialog-footer {
  text-align: center;
}

.range-hint {
  font-size: 12px;
  margin-top: 5px;
  padding: 4px 8px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.range-valid {
  color: #67c23a;
  background: #f0f9eb;
}

.range-invalid {
  color: #f56c6c;
  background: #fef0f0;
}

.warning-text {
  font-weight: bold;
  margin-left: 5px;
}
</style>
