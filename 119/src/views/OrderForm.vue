<template>
  <div>
    <h2 class="page-title">🍵 茶宠定制下单</h2>
    <el-card class="page-card">
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <div class="section-title">客户信息</div>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <div class="section-title">茶宠规格选择</div>
        <el-form-item label="泥料类型" prop="clayType">
          <el-radio-group v-model="orderForm.clayType">
            <el-radio label="紫砂泥">
              <span class="radio-label">紫砂泥</span>
              <span class="radio-desc">- 透气性好，质感细腻</span>
            </el-radio>
            <el-radio label="陶泥">
              <span class="radio-label">陶泥</span>
              <span class="radio-desc">- 可塑性强，古朴典雅</span>
            </el-radio>
            <el-radio label="瓷泥">
              <span class="radio-label">瓷泥</span>
              <span class="radio-desc">- 质地洁白，细腻光滑</span>
            </el-radio>
            <el-radio label="粗陶泥">
              <span class="radio-label">粗陶泥</span>
              <span class="radio-desc">- 粗犷自然，复古风格</span>
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="茶宠造型" prop="shape">
          <el-select v-model="orderForm.shape" placeholder="请选择茶宠造型" style="width: 100%">
            <el-option label="貔貅" value="貔貅">
              <span style="float: left">貔貅</span>
              <span style="float: right; color: #8492a6; font-size: 13px">招财进宝</span>
            </el-option>
            <el-option label="金蟾" value="金蟾">
              <span style="float: left">金蟾</span>
              <span style="float: right; color: #8492a6; font-size: 13px">财源广进</span>
            </el-option>
            <el-option label="麒麟" value="麒麟">
              <span style="float: left">麒麟</span>
              <span style="float: right; color: #8492a6; font-size: 13px">吉祥如意</span>
            </el-option>
            <el-option label="龙龟" value="龙龟">
              <span style="float: left">龙龟</span>
              <span style="float: right; color: #8492a6; font-size: 13px">镇宅辟邪</span>
            </el-option>
            <el-option label="佛手" value="佛手">
              <span style="float: left">佛手</span>
              <span style="float: right; color: #8492a6; font-size: 13px">福在眼前</span>
            </el-option>
            <el-option label="莲花" value="莲花">
              <span style="float: left">莲花</span>
              <span style="float: right; color: #8492a6; font-size: 13px">清净高洁</span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="高度 (cm)" prop="height">
              <el-input-number v-model="orderForm.height" :min="5" :max="30" :step="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="宽度 (cm)" prop="width">
              <el-input-number v-model="orderForm.width" :min="5" :max="30" :step="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="釉面效果" prop="glazeEffect">
          <el-radio-group v-model="orderForm.glazeEffect">
            <el-radio-button label="哑光釉">哑光釉</el-radio-button>
            <el-radio-button label="亮面釉">亮面釉</el-radio-button>
            <el-radio-button label="窑变釉">窑变釉</el-radio-button>
            <el-radio-button label="裂纹釉">裂纹釉</el-radio-button>
            <el-radio-button label="无釉">无釉</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input
            type="textarea"
            :rows="4"
            placeholder="请输入其他定制要求或备注信息..."
            v-model="orderForm.remark">
          </el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" style="width: 100%; background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%); border: none;">
            <i class="el-icon-check"></i> 提交定制订单
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { store, mutations } from '../store'

export default {
  name: 'OrderForm',
  data() {
    return {
      orderForm: {
        customerName: '',
        phone: '',
        clayType: '',
        shape: '',
        height: 10,
        width: 10,
        glazeEffect: '',
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        clayType: [
          { required: true, message: '请选择泥料类型', trigger: 'change' }
        ],
        shape: [
          { required: true, message: '请选择茶宠造型', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入高度', trigger: 'blur' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' }
        ],
        glazeEffect: [
          { required: true, message: '请选择釉面效果', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          mutations.addOrder({ ...this.orderForm })
          this.$message({
            message: '订单提交成功！我们将尽快为您安排生产。',
            type: 'success',
            duration: 3000
          })
          this.$refs.orderForm.resetFields()
        } else {
          this.$message.error('请完善订单信息后再提交')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.el-radio {
  display: block;
  margin-bottom: 12px;
  padding: 12px;
  border: 1px solid #D7CCC8;
  border-radius: 8px;
  transition: all 0.3s;
}
.el-radio:hover {
  border-color: #8B4513;
  background: #FAF6F0;
}
.el-radio.is-checked {
  border-color: #8B4513;
  background: #FAF6F0;
}
.radio-label {
  font-weight: 600;
  color: #5D4037;
  margin-right: 10px;
}
.radio-desc {
  font-size: 13px;
  color: #8D6E63;
}
.el-radio-button__inner {
  padding: 12px 20px;
  border-radius: 4px !important;
}
.el-radio-button__orig-radio:checked + .el-radio-button__inner {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  border-color: #8B4513;
}
</style>
