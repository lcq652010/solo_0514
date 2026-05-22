<template>
  <div class="page-container">
    <div class="header-section">
      <el-button type="text" icon="el-icon-arrow-left" @click="goBack">返回</el-button>
      <h2 class="page-title">业主评价</h2>
    </div>

    <el-card v-loading="loading" class="info-card" v-if="!isEvaluated">
      <div slot="header">
        <span>报修信息</span>
      </div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="报修编号">{{ repairInfo.id }}</el-descriptions-item>
        <el-descriptions-item label="报修标题">{{ repairInfo.title }}</el-descriptions-item>
        <el-descriptions-item label="报修类型">{{ repairInfo.typeName }}</el-descriptions-item>
        <el-descriptions-item label="维修人员" v-if="repairInfo.worker">{{ repairInfo.worker }}</el-descriptions-item>
        <el-descriptions-item label="完成时间" v-if="repairInfo.completeTime">{{ repairInfo.completeTime }}</el-descriptions-item>
        <el-descriptions-item label="维修地址" :span="2">{{ repairInfo.address }}</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="evaluation-card" v-if="!isEvaluated">
      <div slot="header">
        <span>评价信息</span>
      </div>
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="总体评分" prop="rating">
          <el-rate v-model="form.rating" :max="5" show-text :texts="ratingTexts"></el-rate>
        </el-form-item>
        
        <el-form-item label="服务态度" prop="attitude">
          <el-rate v-model="form.attitude" :max="5" show-score></el-rate>
        </el-form-item>
        
        <el-form-item label="响应速度" prop="speed">
          <el-rate v-model="form.speed" :max="5" show-score></el-rate>
        </el-form-item>
        
        <el-form-item label="维修质量" prop="quality">
          <el-rate v-model="form.quality" :max="5" show-score></el-rate>
        </el-form-item>
        
        <el-form-item label="评价内容" prop="content">
          <el-input type="textarea" v-model="form.content" :rows="5" placeholder="请输入您的评价内容，分享您的维修体验..." maxlength="500" show-word-limit></el-input>
        </el-form-item>
        
        <el-form-item label="是否解决问题" prop="isSolved">
          <el-radio-group v-model="form.isSolved">
            <el-radio label="1">是，问题已完全解决</el-radio>
            <el-radio label="2">基本解决，还有小问题</el-radio>
            <el-radio label="3">未解决，需要重新处理</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" @click="submitEvaluation">提交评价</el-button>
          <el-button size="large" @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="result-card" v-if="isEvaluated">
      <div class="result-header">
        <i class="el-icon-circle-check success-icon"></i>
        <h3>感谢您的评价！</h3>
      </div>
      
      <div class="evaluation-summary">
        <div class="rating-display">
          <span class="label">总体评分：</span>
          <el-rate v-model="form.rating" disabled show-text :texts="ratingTexts"></el-rate>
        </div>
        
        <div class="sub-ratings">
          <div class="rating-item">
            <span class="label">服务态度：</span>
            <el-rate v-model="form.attitude" disabled show-score></el-rate>
          </div>
          <div class="rating-item">
            <span class="label">响应速度：</span>
            <el-rate v-model="form.speed" disabled show-score></el-rate>
          </div>
          <div class="rating-item">
            <span class="label">维修质量：</span>
            <el-rate v-model="form.quality" disabled show-score></el-rate>
          </div>
        </div>
        
        <div class="content-section" v-if="form.content">
          <div class="label">评价内容：</div>
          <div class="content">{{ form.content }}</div>
        </div>
        
        <div class="solve-section">
          <div class="label">问题解决情况：</div>
          <div>{{ getSolveText(form.isSolved) }}</div>
        </div>
      </div>

      <div class="action-buttons">
        <el-button type="primary" @click="goToMyRepairs">查看我的报修</el-button>
        <el-button @click="goToApply">再次报修</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import { RepairStore } from '../store/repairStore'
import { EventBus, Events } from '../utils/eventBus'

export default {
  name: 'Evaluation',
  data() {
    return {
      loading: false,
      isEvaluated: false,
      form: {
        rating: 5,
        attitude: 5,
        speed: 5,
        quality: 5,
        content: '',
        isSolved: '1'
      },
      rules: {
        rating: [
          { required: true, message: '请进行总体评分', trigger: 'change' }
        ],
        attitude: [
          { required: true, message: '请对服务态度评分', trigger: 'change' }
        ],
        speed: [
          { required: true, message: '请对响应速度评分', trigger: 'change' }
        ],
        quality: [
          { required: true, message: '请对维修质量评分', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请输入评价内容', trigger: 'blur' },
          { min: 5, message: '评价内容至少5个字符', trigger: 'blur' }
        ],
        isSolved: [
          { required: true, message: '请选择问题是否解决', trigger: 'change' }
        ]
      },
      ratingTexts: ['非常差', '较差', '一般', '满意', '非常满意']
    }
  },
  computed: {
    repairId() {
      return this.$route.params.id
    },
    repairInfo() {
      return RepairStore.getRepairById(this.repairId) || {}
    }
  },
  mounted() {
    this.loadRepairInfo()
    this.listenToStatusUpdates()
  },
  beforeDestroy() {
    EventBus.$off(Events.REPAIR_STATUS_UPDATED)
  },
  methods: {
    listenToStatusUpdates() {
      EventBus.$on(Events.REPAIR_STATUS_UPDATED, (data) => {
        if (data.id === this.repairId) {
          this.$message.info(`报修单状态已更新`)
        }
      })
    },
    loadRepairInfo() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 300)
    },
    getSolveText(value) {
      const map = {
        '1': '是，问题已完全解决',
        '2': '基本解决，还有小问题',
        '3': '未解决，需要重新处理'
      }
      return map[value] || '未知'
    },
    submitEvaluation() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          RepairStore.evaluateRepair(this.repairId, { ...this.form })
          this.$message.success('评价提交成功！')
          this.isEvaluated = true
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
    },
    goBack() {
      this.$router.back()
    },
    goToMyRepairs() {
      this.$router.push('/my-repairs')
    },
    goToApply() {
      this.$router.push('/apply')
    }
  }
}
</script>

<style scoped>
.header-section {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.header-section .el-button {
  margin-right: 15px;
  font-size: 14px;
}

.header-section .page-title {
  margin: 0;
  padding: 0;
  border: none;
}

.info-card,
.evaluation-card,
.result-card {
  margin-bottom: 20px;
}

.result-header {
  text-align: center;
  padding: 30px 0;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 30px;
}

.success-icon {
  font-size: 64px;
  color: #67C23A;
  display: block;
  margin-bottom: 15px;
}

.result-header h3 {
  font-size: 24px;
  color: #303133;
  margin: 0;
}

.evaluation-summary {
  max-width: 600px;
  margin: 0 auto;
}

.rating-display {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
}

.rating-display .label {
  font-size: 14px;
  color: #606266;
  margin-right: 10px;
}

.sub-ratings {
  margin-bottom: 20px;
}

.rating-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.rating-item .label {
  width: 80px;
  font-size: 14px;
  color: #606266;
}

.content-section,
.solve-section {
  margin-bottom: 20px;
}

.content-section .label,
.solve-section .label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
  display: block;
}

.content-section .content {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  line-height: 1.6;
  color: #303133;
}

.action-buttons {
  text-align: center;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.action-buttons .el-button {
  margin: 0 10px;
}
</style>
