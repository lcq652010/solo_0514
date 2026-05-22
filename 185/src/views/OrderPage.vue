<template>
  <div class="order-page">
    <el-card class="order-card">
      <div slot="header" class="card-header">
        <span>🎋 竹编茶笼定制下单</span>
      </div>

      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="140px" class="order-form" validate-on-rule-change>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="竹篾选材等级" prop="bambooGrade">
              <el-select v-model="orderForm.bambooGrade" placeholder="请选择竹篾等级" style="width: 100%;">
                <el-option label="特级 - 五年生毛竹（韧性强）" value="special"></el-option>
                <el-option label="一级 - 四年生毛竹（品质佳）" value="first"></el-option>
                <el-option label="二级 - 三年生毛竹（经济实惠）" value="second"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="笼体高度 (cm)" prop="height" :class="{'form-item-valid': validateStatus.height.startsWith('✓')}">
              <el-input-number v-model="orderForm.height" :min="15" :max="50" :step="1" style="width: 100%;"></el-input-number>
              <div class="validate-tip" :class="{'tip-success': validateStatus.height.startsWith('✓'), 'tip-warning': validateStatus.height && !validateStatus.height.startsWith('✓')}">
                {{ validateStatus.height }}
              </div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="编织密度" prop="density">
              <el-radio-group v-model="orderForm.density">
                <el-radio label="sparse">稀疏（透气好）</el-radio>
                <el-radio label="normal">适中（推荐）</el-radio>
                <el-radio label="dense">紧密（耐用）</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="造型款式" prop="style">
              <el-select v-model="orderForm.style" placeholder="请选择造型款式" style="width: 100%;">
                <el-option label="传统圆筒形" value="cylinder"></el-option>
                <el-option label="六角形" value="hexagon"></el-option>
                <el-option label="方形" value="square"></el-option>
                <el-option label="椭圆形" value="oval"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="底座配置" prop="baseConfig">
          <el-checkbox-group v-model="orderForm.baseConfig">
            <el-checkbox label="wooden">实木底座</el-checkbox>
            <el-checkbox label="lacquer">上漆防水</el-checkbox>
            <el-checkbox label="carving">雕花装饰</el-checkbox>
            <el-checkbox label="mat">竹制衬垫</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="备注说明">
          <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="请输入其他定制要求..."></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitOrder" size="large" style="width: 200px;">提交订单</el-button>
          <el-button @click="resetForm" size="large" style="margin-left: 20px;">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="preview-card" style="margin-top: 20px;" v-if="showPreview">
      <div slot="header">
        <span>📋 订单预览</span>
      </div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="订单编号">{{ previewData.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ previewData.orderTime }}</el-descriptions-item>
        <el-descriptions-item label="竹篾等级">{{ getBambooGradeText(previewData.bambooGrade) }}</el-descriptions-item>
        <el-descriptions-item label="笼体高度">{{ previewData.height }} cm</el-descriptions-item>
        <el-descriptions-item label="编织密度">{{ getDensityText(previewData.density) }}</el-descriptions-item>
        <el-descriptions-item label="造型款式">{{ getStyleText(previewData.style) }}</el-descriptions-item>
        <el-descriptions-item label="底座配置" :span="2">{{ getBaseConfigText(previewData.baseConfig) }}</el-descriptions-item>
        <el-descriptions-item label="备注说明" :span="2">{{ previewData.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'OrderPage',
  data() {
    return {
      orderForm: {
        bambooGrade: '',
        height: 25,
        density: 'normal',
        style: '',
        baseConfig: [],
        remark: ''
      },
      rules: {
        bambooGrade: [
          { required: true, message: '请选择竹篾选材等级', trigger: 'change' }
        ],
        height: [
          { required: true, message: '请输入笼体高度', trigger: 'blur' },
          { type: 'number', min: 15, max: 50, message: '高度需在15-50cm之间', trigger: 'blur' }
        ],
        density: [
          { required: true, message: '请选择编织密度', trigger: 'change' }
        ],
        style: [
          { required: true, message: '请选择造型款式', trigger: 'change' }
        ]
      },
      validateStatus: {
        bambooGrade: '',
        height: '',
        density: '',
        style: ''
      },
      showPreview: false,
      previewData: {}
    }
  },
  watch: {
    'orderForm.bambooGrade': {
      handler(val) {
        this.validateBambooGradeRealtime(val)
      },
      immediate: true
    },
    'orderForm.height': {
      handler(val) {
        this.validateHeightRealtime(val)
      },
      immediate: true
    },
    'orderForm.density': {
      handler(val) {
        this.validateDensityRealtime(val)
        this.validateHeightRealtime(this.orderForm.height)
      },
      immediate: true
    },
    'orderForm.style': {
      handler(val) {
        this.validateStyleRealtime(val)
      },
      immediate: true
    }
  },
  methods: {
    validateBambooGradeRealtime(val) {
      if (!val) {
        this.validateStatus.bambooGrade = '请选择竹篾等级'
      } else if (!['special', 'first', 'second'].includes(val)) {
        this.validateStatus.bambooGrade = '无效的竹篾等级'
      } else {
        this.validateStatus.bambooGrade = ''
      }
    },
    getHeightRangeByDensity(density) {
      const rangeMap = {
        sparse: { min: 15, max: 30, desc: '15-30cm（稀疏编织适合矮款茶笼）' },
        normal: { min: 25, max: 40, desc: '25-40cm（适中编织适用范围最广）' },
        dense: { min: 35, max: 50, desc: '35-50cm（紧密编织适合高款茶笼）' }
      }
      return rangeMap[density] || { min: 15, max: 50, desc: '15-50cm' }
    },
    validateHeightRealtime(val) {
      const range = this.getHeightRangeByDensity(this.orderForm.density)
      if (!val) {
        this.validateStatus.height = `请输入笼体高度，建议范围：${range.desc}`
      } else if (isNaN(val)) {
        this.validateStatus.height = '请输入有效的数字'
      } else if (val < range.min || val > range.max) {
        this.validateStatus.height = `当前编织密度建议高度：${range.desc}`
      } else {
        this.validateStatus.height = `✓ 高度符合工艺要求，建议范围：${range.desc}`
      }
    },
    validateDensityRealtime(val) {
      if (!val) {
        this.validateStatus.density = '请选择编织密度'
      } else if (!['sparse', 'normal', 'dense'].includes(val)) {
        this.validateStatus.density = '无效的编织密度'
      } else {
        this.validateStatus.density = ''
      }
    },
    validateStyleRealtime(val) {
      if (!val) {
        this.validateStatus.style = '请选择造型款式'
      } else if (!['cylinder', 'hexagon', 'square', 'oval'].includes(val)) {
        this.validateStatus.style = '无效的造型款式'
      } else {
        this.validateStatus.style = ''
      }
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const orderNo = 'BC' + Date.now().toString().slice(-8)
          const orderTime = new Date().toLocaleString('zh-CN')
          const newOrder = {
            orderNo,
            orderTime,
            ...this.orderForm,
            currentStep: 0,
            processRecords: []
          }
          this.previewData = newOrder
          this.showPreview = true
          this.$eventBus.$emit('new-order', newOrder)
          this.$message.success('订单提交成功！')
        } else {
          this.$message.error('请完善表单信息')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.showPreview = false
    },
    getBambooGradeText(val) {
      const map = {
        special: '特级 - 五年生毛竹（韧性强）',
        first: '一级 - 四年生毛竹（品质佳）',
        second: '二级 - 三年生毛竹（经济实惠）'
      }
      return map[val] || val
    },
    getDensityText(val) {
      const map = {
        sparse: '稀疏（透气好）',
        normal: '适中（推荐）',
        dense: '紧密（耐用）'
      }
      return map[val] || val
    },
    getStyleText(val) {
      const map = {
        cylinder: '传统圆筒形',
        hexagon: '六角形',
        square: '方形',
        oval: '椭圆形'
      }
      return map[val] || val
    },
    getBaseConfigText(arr) {
      if (!arr || arr.length === 0) return '无配置'
      const map = {
        wooden: '实木底座',
        lacquer: '上漆防水',
        carving: '雕花装饰',
        mat: '竹制衬垫'
      }
      return arr.map(item => map[item]).join('、')
    }
  }
}
</script>

<style scoped>
.order-page {
  padding: 10px;
}
.card-header {
  font-size: 20px;
  font-weight: bold;
  color: #2E7D32;
}
.order-form {
  padding: 20px 0;
}
.el-checkbox {
  margin-right: 30px;
}
.validate-tip {
  font-size: 12px;
  margin-top: 4px;
  line-height: 1.5;
}
.tip-success {
  color: #67C23A;
}
.tip-warning {
  color: #E6A23C;
}
.form-item-valid .el-form-item__label {
  color: #67C23A;
}
</style>
