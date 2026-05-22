<template>
  <div class="ticket-page">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="ticket-card">
          <div slot="header" class="card-header">
            <i class="el-icon-tickets"></i> 取号服务
          </div>

          <div class="business-type">
            <h4>请选择办理业务类型</h4>
            <el-row :gutter="15">
              <el-col :span="8" v-for="(item, index) in businessTypes" :key="index">
                <div
                  class="type-item"
                  :class="{ active: selectedType === item.code }"
                  @click="selectBusinessType(item)">
                  <i :class="item.icon"></i>
                  <span>{{ item.name }}</span>
                  <div class="type-desc">{{ item.desc }}</div>
                </div>
              </el-col>
            </el-row>
          </div>

          <el-divider></el-divider>

          <div class="ticket-info" v-if="selectedType">
            <el-alert
              title="温馨提示"
              type="info"
              :closable="false"
              show-icon>
              <div slot="default">
                <p>当前排队人数：<strong>{{ waitingCount }}</strong> 人</p>
                <p>预计等待时间：<strong>{{ estimatedTime }}</strong> 分钟</p>
              </div>
            </el-alert>

            <div class="ticket-preview">
              <div class="ticket-preview-title">排队号预览</div>
              <div class="ticket-number">{{ ticketNumber }}</div>
              <div class="ticket-detail">
                <p>业务类型：{{ getBusinessTypeName() }}</p>
                <p>取号时间：{{ currentTime }}</p>
                <p>办理窗口：请留意叫号屏幕</p>
              </div>
            </div>

            <div class="ticket-actions">
              <el-button type="primary" size="large" @click="handleGetTicket" :loading="getTicketLoading">
                <i class="el-icon-document-add"></i> 确认取号
              </el-button>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="queue-card">
          <div slot="header" class="card-header">
            <i class="el-icon-s-order"></i> 当前排队情况
          </div>

          <div class="queue-stats">
            <el-row :gutter="10">
              <el-col :span="12">
                <div class="stat-item">
                  <div class="stat-number">{{ waitingCount }}</div>
                  <div class="stat-label">等待人数</div>
                </div>
              </el-col>
              <el-col :span="12">
                <div class="stat-item">
                  <div class="stat-number">{{ servedCount }}</div>
                  <div class="stat-label">已办理</div>
                </div>
              </el-col>
            </el-row>
          </div>

          <el-divider></el-divider>

          <div class="recent-calling">
            <h4>最近叫号</h4>
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in recentCalled"
                :key="index"
                :timestamp="item.time"
                placement="top"
                :type="index === 0 ? 'primary' : ''">
                <el-tag size="small">{{ item.number }}</el-tag>
                <span class="calling-info">{{ item.window }}</span>
              </el-timeline-item>
            </el-timeline>
          </div>
        </el-card>

        <el-card class="notice-card" style="margin-top: 20px">
          <div slot="header" class="card-header">
            <i class="el-icon-warning-outline"></i> 取号须知
          </div>
          <div class="notice-content">
            <ul>
              <li>请携带有效身份证件办理业务</li>
              <li>过号作废，请重新取号排队</li>
              <li>请留意叫号屏幕和广播提示</li>
              <li>如有疑问，请咨询导服人员</li>
              <li>排队号仅限本人使用，不得转让</li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      title="取号成功"
      :visible.sync="ticketDialogVisible"
      width="400px"
      :close-on-click-modal="false"
      center>
      <div class="ticket-success">
        <div class="success-icon">
          <i class="el-icon-success"></i>
        </div>
        <div class="success-number">{{ generatedTicket }}</div>
        <div class="success-info">
          <p>业务类型：{{ getBusinessTypeName() }}</p>
          <p>取号时间：{{ currentTime }}</p>
          <p>前方等待：{{ waitingCount }} 人</p>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="ticketDialogVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Ticket',
  data() {
    return {
      businessTypes: [
        { code: 'A', name: '综合业务', desc: '各类综合服务事项', icon: 'el-icon-document' },
        { code: 'B', name: '户政业务', desc: '身份证、户口本等', icon: 'el-icon-user' },
        { code: 'C', name: '社保业务', desc: '社保、医保相关', icon: 'el-icon-s-custom' },
        { code: 'D', name: '不动产', desc: '房产登记、过户等', icon: 'el-icon-office-building' },
        { code: 'E', name: '市场监管', desc: '营业执照、经营许可', icon: 'el-icon-s-shop' },
        { code: 'F', name: '出入境', desc: '护照、签证办理', icon: 'el-icon-place' }
      ],
      selectedType: '',
      ticketNumber: 'A001',
      waitingCount: 15,
      estimatedTime: 45,
      servedCount: 32,
      recentCalled: [
        { number: 'A032', window: '1号窗口', time: '10:15' },
        { number: 'B018', window: '2号窗口', time: '10:12' },
        { number: 'C025', window: '3号窗口', time: '10:10' },
        { number: 'D008', window: '4号窗口', time: '10:05' }
      ],
      getTicketLoading: false,
      ticketDialogVisible: false,
      generatedTicket: ''
    }
  },
  computed: {
    currentTime() {
      const now = new Date()
      return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
    }
  },
  methods: {
    selectBusinessType(item) {
      this.selectedType = item.code
      this.ticketNumber = item.code + String(Math.floor(Math.random() * 100)).padStart(3, '0')
      this.waitingCount = Math.floor(Math.random() * 20) + 5
      this.estimatedTime = this.waitingCount * 3
    },
    getBusinessTypeName() {
      const type = this.businessTypes.find(t => t.code === this.selectedType)
      return type ? type.name : ''
    },
    handleGetTicket() {
      if (!this.selectedType) {
        this.$message.warning('请先选择办理业务类型')
        return
      }
      this.getTicketLoading = true
      setTimeout(() => {
        this.getTicketLoading = false
        this.generatedTicket = this.ticketNumber
        this.ticketDialogVisible = true
        this.waitingCount++
        
        this.$bus.$emit('newTicket', {
          number: this.ticketNumber,
          businessType: this.getBusinessTypeName()
        })
      }, 1000)
    }
  }
}
</script>

<style scoped>
.ticket-page {
  height: 100%;
}

.card-header {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.business-type h4 {
  margin-bottom: 20px;
  color: #606266;
}

.type-item {
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  padding: 20px 15px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 15px;
}

.type-item:hover {
  border-color: #409EFF;
  background: #ecf5ff;
}

.type-item.active {
  border-color: #409EFF;
  background: #409EFF;
  color: #fff;
}

.type-item i {
  font-size: 32px;
  display: block;
  margin-bottom: 10px;
}

.type-item span {
  display: block;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 5px;
}

.type-desc {
  font-size: 12px;
  opacity: 0.8;
}

.ticket-preview {
  margin: 30px 0;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #fff;
  text-align: center;
}

.ticket-preview-title {
  font-size: 16px;
  opacity: 0.9;
  margin-bottom: 15px;
}

.ticket-number {
  font-size: 64px;
  font-weight: bold;
  letter-spacing: 10px;
  margin-bottom: 20px;
}

.ticket-detail p {
  margin: 8px 0;
  opacity: 0.9;
}

.ticket-actions {
  text-align: center;
}

.queue-stats {
  padding: 20px 0;
}

.stat-item {
  text-align: center;
  padding: 20px 10px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.recent-calling h4 {
  margin-bottom: 15px;
  color: #606266;
}

.calling-info {
  margin-left: 10px;
  color: #606266;
}

.notice-content ul {
  padding-left: 20px;
  margin: 0;
}

.notice-content li {
  margin: 10px 0;
  color: #606266;
  line-height: 1.6;
}

.ticket-success {
  text-align: center;
  padding: 20px 0;
}

.success-icon {
  margin-bottom: 20px;
}

.success-icon i {
  font-size: 64px;
  color: #67c23a;
}

.success-number {
  font-size: 48px;
  font-weight: bold;
  color: #409EFF;
  letter-spacing: 5px;
  margin-bottom: 20px;
}

.success-info p {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}
</style>
