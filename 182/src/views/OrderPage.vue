<template>
  <div class="order-page">
    <el-card shadow="hover">
      <div slot="header" class="card-header">
        <span>香包定制下单</span>
      </div>
      
      <el-form ref="orderForm" :model="orderForm" :rules="rules" label-width="120px">
        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-user"></i> 客户信息</span>
        </el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-collection"></i> 面料材质</span>
        </el-divider>
        
        <el-form-item label="选择面料" prop="fabric" ref="fabricItem">
          <el-radio-group 
            v-model="orderForm.fabric" 
            @change="validateField('fabric')"
            @blur.native.capture="validateField('fabric')"
          >
            <el-radio-button label="棉麻">
              <div class="fabric-option">
                <i class="el-icon-document"></i>
                <span>棉麻</span>
                <span class="price">¥20</span>
              </div>
            </el-radio-button>
            <el-radio-button label="丝绸">
              <div class="fabric-option">
                <i class="el-icon-picture"></i>
                <span>丝绸</span>
                <span class="price">¥35</span>
              </div>
            </el-radio-button>
            <el-radio-button label="绸缎">
              <div class="fabric-option">
                <i class="el-icon-star-on"></i>
                <span>绸缎</span>
                <span class="price">¥50</span>
              </div>
            </el-radio-button>
            <el-radio-button label="亚麻">
              <div class="fabric-option">
                <i class="el-icon-menu"></i>
                <span>亚麻</span>
                <span class="price">¥25</span>
              </div>
            </el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-crop"></i> 造型与尺寸</span>
        </el-divider>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="香包造型" prop="shape" ref="shapeItem">
              <el-select 
                v-model="orderForm.shape" 
                placeholder="请选择造型" 
                style="width: 100%"
                @change="onShapeChange"
                @blur="validateField('shape')"
              >
                <el-option label="圆形" value="圆形">
                  <span style="float: left">⚪ 圆形</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">经典款</span>
                </el-option>
                <el-option label="方形" value="方形">
                  <span style="float: left">⬜ 方形</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">传统款</span>
                </el-option>
                <el-option label="心形" value="心形">
                  <span style="float: left">❤ 心形</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">情侣款</span>
                </el-option>
                <el-option label="三角形" value="三角形">
                  <span style="float: left">🔺 三角形</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">个性款</span>
                </el-option>
                <el-option label="菱形" value="菱形">
                  <span style="float: left">💎 菱形</span>
                  <span style="float: right; color: #8492a6; font-size: 13px">时尚款</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="尺寸(cm)" prop="size">
              <el-input-number 
                v-model="orderForm.size" 
                :min="sizeRange.min" 
                :max="sizeRange.max" 
                :step="1" 
                style="width: 100%"
                @change="onSizeChange"
              ></el-input-number>
              <div class="size-tip" :class="sizeTip.type">
                <i :class="sizeTip.icon"></i>
                <span>{{ sizeTip.text }}</span>
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-magic-stick"></i> 内料配方</span>
        </el-divider>
        
        <el-form-item label="香料配方" prop="formula" ref="formulaItem">
          <el-checkbox-group 
            v-model="selectedFormulas" 
            @change="validateFormula"
          >
            <el-checkbox label="薰衣草" @change.native="blurFormula">
              <div class="formula-option">
                <span class="formula-name">薰衣草</span>
                <span class="formula-desc">安神助眠</span>
              </div>
            </el-checkbox>
            <el-checkbox label="艾草" @change.native="blurFormula">
              <div class="formula-option">
                <span class="formula-name">艾草</span>
                <span class="formula-desc">驱蚊防虫</span>
              </div>
            </el-checkbox>
            <el-checkbox label="檀香" @change.native="blurFormula">
              <div class="formula-option">
                <span class="formula-name">檀香</span>
                <span class="formula-desc">静心宁神</span>
              </div>
            </el-checkbox>
            <el-checkbox label="薄荷" @change.native="blurFormula">
              <div class="formula-option">
                <span class="formula-name">薄荷</span>
                <span class="formula-desc">清凉解暑</span>
              </div>
            </el-checkbox>
            <el-checkbox label="玫瑰" @change.native="blurFormula">
              <div class="formula-option">
                <span class="formula-name">玫瑰</span>
                <span class="formula-desc">芳香养颜</span>
              </div>
            </el-checkbox>
            <el-checkbox label="桂花" @change.native="blurFormula">
              <div class="formula-option">
                <span class="formula-name">桂花</span>
                <span class="formula-desc">清香怡人</span>
              </div>
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-divider content-position="left">
          <span class="divider-title"><i class="el-icon-link"></i> 挂绳样式</span>
        </el-divider>
        
        <el-form-item label="选择挂绳" prop="rope">
          <el-radio-group v-model="orderForm.rope">
            <el-radio label="中国结">
              <div class="rope-option">
                <div class="rope-icon rope-knot"></div>
                <span>中国结</span>
              </div>
            </el-radio>
            <el-radio label="流苏">
              <div class="rope-option">
                <div class="rope-icon rope-tassel"></div>
                <span>流苏</span>
              </div>
            </el-radio>
            <el-radio label="皮绳">
              <div class="rope-option">
                <div class="rope-icon rope-leather"></div>
                <span>皮绳</span>
              </div>
            </el-radio>
            <el-radio label="编织绳">
              <div class="rope-option">
                <div class="rope-icon rope-braid"></div>
                <span>编织绳</span>
              </div>
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="订购数量" prop="quantity">
              <el-input-number v-model="orderForm.quantity" :min="1" :max="100" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="备注说明">
          <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="请输入其他特殊要求..."></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
            <i class="el-icon-check"></i> 提交订单
          </el-button>
          <el-button size="large" @click="resetForm">
            <i class="el-icon-refresh"></i> 重置表单
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import orderStore from '../store/orders'

export default {
  name: 'OrderPage',
  data() {
    return {
      submitting: false,
      selectedFormulas: [],
      orderForm: {
        customerName: '',
        phone: '',
        fabric: '',
        shape: '',
        size: 8,
        formula: '',
        rope: '',
        quantity: 1,
        remark: ''
      },
      shapeSizeConfig: {
        '圆形': { min: 6, max: 15, optimal: [8, 10] },
        '方形': { min: 5, max: 14, optimal: [7, 9] },
        '心形': { min: 7, max: 16, optimal: [9, 12] },
        '三角形': { min: 6, max: 13, optimal: [8, 10] },
        '菱形': { min: 5, max: 12, optimal: [7, 9] }
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        fabric: [
          { required: true, message: '请选择面料材质', trigger: 'blur' }
        ],
        shape: [
          { required: true, message: '请选择香包造型', trigger: 'blur' }
        ],
        formula: [
          { required: true, message: '请至少选择一种香料配方', trigger: 'blur' }
        ],
        rope: [
          { required: true, message: '请选择挂绳样式', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    sizeRange() {
      if (!this.orderForm.shape || !this.shapeSizeConfig[this.orderForm.shape]) {
        return { min: 5, max: 20 }
      }
      return this.shapeSizeConfig[this.orderForm.shape]
    },
    sizeTip() {
      if (!this.orderForm.shape) {
        return { type: 'info', icon: 'el-icon-info', text: '请先选择香包造型' }
      }
      const config = this.shapeSizeConfig[this.orderForm.shape]
      const size = this.orderForm.size
      const isOptimal = size >= config.optimal[0] && size <= config.optimal[1]
      const isNearLimit = size === config.min || size === config.max
      
      if (isOptimal) {
        return { 
          type: 'success', 
          icon: 'el-icon-success', 
          text: `✅ ${size}cm 为最佳工艺尺寸，制作效果最佳` 
        }
      } else if (isNearLimit) {
        return { 
          type: 'warning', 
          icon: 'el-icon-warning', 
          text: `⚠️ ${size}cm 接近工艺极限，制作难度较高，建议调整至 ${config.optimal[0]}-${config.optimal[1]}cm` 
        }
      } else if (size < config.optimal[0]) {
        return { 
          type: 'info', 
          icon: 'el-icon-info', 
          text: `📏 推荐工艺区间：${config.optimal[0]}-${config.optimal[1]}cm，制作更精美` 
        }
      } else {
        return { 
          type: 'info', 
          icon: 'el-icon-info', 
          text: `📏 推荐工艺区间：${config.optimal[0]}-${config.optimal[1]}cm，香气更持久` 
        }
      }
    }
  },
  watch: {
    selectedFormulas(val) {
      this.orderForm.formula = val.join('、')
    }
  },
  methods: {
    onShapeChange() {
      this.validateField('shape')
      const config = this.shapeSizeConfig[this.orderForm.shape]
      if (config) {
        if (this.orderForm.size < config.min) {
          this.orderForm.size = config.min
        } else if (this.orderForm.size > config.max) {
          this.orderForm.size = config.max
        }
      }
    },
    onSizeChange() {
    },
    validateField(field) {
      this.$refs.orderForm.validateField(field)
    },
    validateFormula() {
      if (this.selectedFormulas.length === 0) {
        if (!this.$refs.formulaItem) return
        this.$refs.formulaItem.validateState = 'error'
        this.$refs.formulaItem.validateMessage = '请至少选择一种香料配方'
      } else {
        if (!this.$refs.formulaItem) return
        this.$refs.formulaItem.validateState = 'success'
        this.$refs.formulaItem.validateMessage = ''
      }
    },
    blurFormula() {
      setTimeout(() => {
        this.validateFormula()
      }, 100)
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          if (this.selectedFormulas.length === 0) {
            this.$message.warning('请至少选择一种香料配方')
            return
          }
          this.submitting = true
          setTimeout(() => {
            const newOrder = orderStore.addOrder(this.orderForm)
            this.submitting = false
            this.$message.success(`订单提交成功！订单号：${newOrder.id}`)
            this.resetForm()
            this.$router.push({ path: '/admin', query: { newOrderId: newOrder.id } })
          }, 1000)
        } else {
          this.$message.error('请完善订单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.selectedFormulas = []
    }
  }
}
</script>

<style scoped>
.order-page {
  max-width: 900px;
  margin: 0 auto;
}

.card-header {
  font-size: 20px;
  font-weight: 500;
  color: #667eea;
}

.divider-title {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}

.fabric-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 5px;
}

.fabric-option i {
  font-size: 24px;
  margin-bottom: 5px;
  color: #667eea;
}

.fabric-option .price {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 3px;
}

.formula-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 20px;
}

.formula-name {
  font-weight: 500;
  font-size: 14px;
}

.formula-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 3px;
}

.rope-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
}

.rope-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
}

.rope-knot {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.rope-knot::before {
  content: '🎀';
}

.rope-tassel {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.rope-tassel::before {
  content: '🎋';
}

.rope-leather {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.rope-leather::before {
  content: '🔗';
}

.rope-braid {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.rope-braid::before {
  content: '🧶';
}

.size-tip {
  margin-top: 8px;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.size-tip.info {
  background: #f0f9ff;
  color: #409eff;
  border: 1px solid #b3d8ff;
}

.size-tip.success {
  background: #f0f9eb;
  color: #67c23a;
  border: 1px solid #c2e7b0;
}

.size-tip.warning {
  background: #fdf6ec;
  color: #e6a23c;
  border: 1px solid #f5dab1;
}
</style>
