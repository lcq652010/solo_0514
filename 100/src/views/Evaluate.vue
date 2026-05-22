<template>
  <div class="page-container">
    <h1 class="page-title">服务评价</h1>
    
    <div class="card-wrapper" v-if="currentRecord">
      <div class="evaluate-header">
        <div class="car-info">
          <i class="el-icon-car"></i>
          <div class="info-text">
            <h3>{{ currentRecord.carNumber }}</h3>
            <p>{{ currentRecord.carBrand }} · {{ getPackageName(currentRecord.packageId) }}</p>
          </div>
        </div>
        <el-tag type="success">服务已完成</el-tag>
      </div>
      
      <el-form 
        ref="evaluateForm"
        :model="form"
        :rules="rules"
        label-width="100px"
        class="evaluate-form"
      >
        <el-form-item label="总体评分" prop="score">
          <div class="rate-wrapper">
            <el-rate 
              v-model="form.score" 
              show-score 
              text-color="#ff9900"
              :max="5"
            ></el-rate>
          </div>
        </el-form-item>
        
        <el-form-item label="分项评分">
          <div class="sub-rates">
            <div class="rate-item">
              <span>服务态度</span>
              <el-rate v-model="form.serviceScore" :max="5"></el-rate>
            </div>
            <div class="rate-item">
              <span>专业技术</span>
              <el-rate v-model="form.techScore" :max="5"></el-rate>
            </div>
            <div class="rate-item">
              <span>施工效率</span>
              <el-rate v-model="form.efficiencyScore" :max="5"></el-rate>
            </div>
            <div class="rate-item">
              <span>环境整洁</span>
              <el-rate v-model="form.envScore" :max="5"></el-rate>
            </div>
          </div>
        </el-form-item>
        
        <el-form-item label="评价内容" prop="content">
          <el-input
            type="textarea"
            :rows="5"
            v-model="form.content"
            placeholder="请详细描述您的服务体验，帮助我们改进服务质量..."
          ></el-input>
        </el-form-item>
        
        <el-form-item label="是否推荐">
          <el-radio-group v-model="form.recommend">
            <el-radio :label="true">是，我推荐</el-radio>
            <el-radio :label="false">否，暂不推荐</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="匿名评价">
          <el-switch v-model="form.anonymous" active-text="是" inactive-text="否"></el-switch>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" size="large" @click="submitEvaluate" class="submit-btn">
            提交评价
          </el-button>
          <el-button size="large" @click="goBack">返回</el-button>
        </el-form-item>
      </el-form>
    </div>
    
    <div class="card-wrapper" v-if="hasEvaluatedRecords">
      <h3 class="section-title">
        <i class="el-icon-document"></i> 我的评价
      </h3>
      
      <div v-for="record in evaluatedRecords" :key="record.id" class="evaluate-item">
        <div class="evaluate-header">
          <div class="car-info-small">
            <span class="car-number">{{ record.carNumber }}</span>
            <span class="package-name">{{ getPackageName(record.packageId) }}</span>
          </div>
          <div class="evaluate-score">
            <el-rate :value="record.score || 5" disabled show-score text-color="#ff9900"></el-rate>
          </div>
        </div>
        <div class="evaluate-content">
          {{ record.evaluateContent || '用户未填写评价内容' }}
        </div>
        <div class="evaluate-footer">
          <span class="evaluate-time">{{ record.evaluateTime }}</span>
          <el-tag v-if="record.recommend" type="success" size="mini">推荐</el-tag>
        </div>
      </div>
    </div>
    
    <div class="card-wrapper" v-if="!currentRecord && !hasEvaluatedRecords">
      <el-empty description="暂无可评价的服务订单"></el-empty>
      <div style="text-align: center; margin-top: 20px;">
        <el-button type="primary" @click="$router.push('/records')">前往预约记录</el-button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Evaluate',
  data() {
    return {
      records: [],
      currentRecord: null,
      form: {
        score: 5,
        serviceScore: 5,
        techScore: 5,
        efficiencyScore: 5,
        envScore: 5,
        content: '',
        recommend: true,
        anonymous: false
      },
      rules: {
        score: [
          { required: true, message: '请给出总体评分', trigger: 'change' }
        ],
        content: [
          { required: true, message: '请填写评价内容', trigger: 'blur' },
          { min: 10, message: '评价内容至少10个字符', trigger: 'blur' }
        ]
      },
      packages: [
        { id: 1, name: '基础保养套餐' },
        { id: 2, name: '标准保养套餐' },
        { id: 3, name: '尊享保养套餐' },
        { id: 4, name: '刹车系统养护' },
        { id: 5, name: '空调系统养护' },
        { id: 6, name: '漆面养护套餐' }
      ]
    }
  },
  computed: {
    evaluatedRecords() {
      return this.records.filter(r => r.evaluated)
    },
    hasEvaluatedRecords() {
      return this.evaluatedRecords.length > 0
    }
  },
  mounted() {
    this.loadRecords()
  },
  methods: {
    loadRecords() {
      this.records = JSON.parse(localStorage.getItem('reserveRecords') || '[]')
      const recordId = this.$route.query.id
      if (recordId) {
        this.currentRecord = this.records.find(r => r.id == recordId)
      } else {
        this.currentRecord = this.records.find(r => r.status === 3 && !r.evaluated)
      }
    },
    getPackageName(id) {
      const pkg = this.packages.find(p => p.id === id)
      return pkg ? pkg.name : '未知套餐'
    },
    submitEvaluate() {
      this.$refs.evaluateForm.validate((valid) => {
        if (valid) {
          const index = this.records.findIndex(r => r.id === this.currentRecord.id)
          if (index > -1) {
            this.records[index].evaluated = true
            this.records[index].score = this.form.score
            this.records[index].evaluateContent = this.form.content
            this.records[index].recommend = this.form.recommend
            this.records[index].evaluateTime = new Date().toLocaleString()
            
            localStorage.setItem('reserveRecords', JSON.stringify(this.records))
            
            this.$message({
              type: 'success',
              message: '评价提交成功！感谢您的反馈！'
            })
            
            setTimeout(() => {
              this.$router.push('/records')
            }, 1000)
          }
        } else {
          this.$message.error('请完善评价信息')
          return false
        }
      })
    },
    goBack() {
      this.$router.push('/records')
    }
  }
}
</script>

<style scoped>
.evaluate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 30px;
}

.car-info {
  display: flex;
  align-items: center;
  gap: 15px;
}

.car-info i {
  font-size: 40px;
  color: #409eff;
}

.info-text h3 {
  margin: 0 0 5px 0;
  font-size: 20px;
  color: #303133;
}

.info-text p {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

.rate-wrapper {
  padding: 10px 0;
}

.sub-rates {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  padding: 10px 0;
}

.rate-item {
  display: flex;
  align-items: center;
  gap: 15px;
}

.rate-item span {
  width: 80px;
  color: #606266;
}

.submit-btn {
  width: 180px;
  height: 44px;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.section-title i {
  color: #409eff;
  margin-right: 8px;
}

.evaluate-item {
  padding: 20px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 15px;
}

.car-info-small {
  display: flex;
  gap: 15px;
  align-items: center;
}

.car-number {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.package-name {
  color: #909399;
  font-size: 14px;
}

.evaluate-score {
  display: flex;
  align-items: center;
}

.evaluate-content {
  padding: 15px 0;
  color: #606266;
  line-height: 1.6;
}

.evaluate-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #f5f7fa;
}

.evaluate-time {
  color: #909399;
  font-size: 12px;
}
</style>
