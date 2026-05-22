<template>
  <div class="page-container">
    <div class="page-title">准考证管理</div>
    
    <el-card>
      <div slot="header">
        <span>查询准考证</span>
      </div>
      <el-form :inline="true" :model="queryForm" label-width="100px">
        <el-form-item label="身份证号">
          <el-input v-model="queryForm.idCard" placeholder="请输入身份证号" maxlength="18"></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="queryForm.name" placeholder="请输入姓名" maxlength="20"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="queryTicket" :loading="queryLoading">查询</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div v-if="ticketData" style="margin-top: 20px;">
      <el-card>
        <div slot="header" style="display: flex; justify-content: space-between; align-items: center;">
          <span>准考证信息</span>
          <div>
            <el-button type="primary" size="small" icon="el-icon-printer" @click="printTicket">
              打印准考证
            </el-button>
            <el-button type="success" size="small" icon="el-icon-download" @click="downloadTicket">
              下载PDF
            </el-button>
          </div>
        </div>
        
        <div id="ticket-content" class="ticket-content">
          <div class="ticket-header">
            <h1>全国统一考试准考证</h1>
            <p>NATIONAL EXAMINATION ADMISSION TICKET</p>
          </div>
          
          <div class="ticket-body">
            <div class="ticket-info">
              <div class="info-row">
                <div class="info-item">
                  <span class="label">准考证号：</span>
                  <span class="value">{{ ticketData.ticketNo }}</span>
                </div>
                <div class="info-item">
                  <span class="label">姓名：</span>
                  <span class="value">{{ ticketData.applicantName }}</span>
                </div>
              </div>
              <div class="info-row">
                <div class="info-item">
                  <span class="label">性别：</span>
                  <span class="value">{{ ticketData.gender || '男' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">身份证号：</span>
                  <span class="value">{{ ticketData.idCard }}</span>
                </div>
              </div>
              <div class="info-row">
                <div class="info-item full-width">
                  <span class="label">考试科目：</span>
                  <span class="value">{{ ticketData.subjectName }}</span>
                </div>
              </div>
              <div class="info-row">
                <div class="info-item">
                  <span class="label">科目代码：</span>
                  <span class="value">{{ ticketData.subjectCode }}</span>
                </div>
                <div class="info-item">
                  <span class="label">考试日期：</span>
                  <span class="value">{{ ticketData.examDate }}</span>
                </div>
              </div>
              <div class="info-row">
                <div class="info-item">
                  <span class="label">考试时间：</span>
                  <span class="value">{{ ticketData.examTime }}</span>
                </div>
                <div class="info-item">
                  <span class="label">考场号：</span>
                  <span class="value">{{ ticketData.roomNo || '第01考场' }}</span>
                </div>
              </div>
              <div class="info-row">
                <div class="info-item">
                  <span class="label">座位号：</span>
                  <span class="value">{{ ticketData.seatNo || '15号' }}</span>
                </div>
                <div class="info-item">
                  <span class="label">考点名称：</span>
                  <span class="value">{{ ticketData.examSite || '第一考点' }}</span>
                </div>
              </div>
              <div class="info-row">
                <div class="info-item full-width">
                  <span class="label">考点地址：</span>
                  <span class="value">{{ ticketData.examAddress || '北京市海淀区中关村大街1号' }}</span>
                </div>
              </div>
            </div>
            
            <div class="ticket-photo">
              <div class="photo-placeholder">
                <i class="el-icon-picture-outline"></i>
                <p>证件照</p>
              </div>
            </div>
          </div>
          
          <div class="ticket-footer">
            <div class="notice-title">考生须知：</div>
            <ul class="notice-content">
              <li>1. 考生须凭准考证和有效身份证件原件进入考场。</li>
              <li>2. 请提前30分钟到达考场，开考15分钟后禁止入场。</li>
              <li>3. 严禁携带手机、智能手表等电子设备进入考场。</li>
              <li>4. 请自觉遵守考场纪律，服从监考人员管理。</li>
              <li>5. 准考证请妥善保管，涂改或转借无效。</li>
            </ul>
            <div class="ticket-seal">
              <span>考试中心专用章</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <el-empty v-else-if="queryCompleted && !ticketData" description="未找到准考证信息，请检查输入信息是否正确"></el-empty>
  </div>
</template>

<script>
import { applicationRecords } from '@/mock/data.js'

export default {
  name: 'TicketPage',
  data() {
    return {
      queryForm: {
        idCard: '',
        name: ''
      },
      queryLoading: false,
      ticketData: null,
      queryCompleted: false
    }
  },
  mounted() {
    const { idCard, name, autoQuery } = this.$route.query
    if (idCard && name) {
      this.queryForm.idCard = idCard
      this.queryForm.name = name
      if (autoQuery === 'true') {
        this.$nextTick(() => {
          this.queryTicket()
        })
      }
    }
  },
  methods: {
    queryTicket() {
      if (!this.queryForm.idCard.trim()) {
        this.$message.warning('请输入身份证号')
        return
      }
      if (!this.queryForm.name.trim()) {
        this.$message.warning('请输入姓名')
        return
      }
      
      this.queryLoading = true
      
      setTimeout(() => {
        this.queryLoading = false
        this.queryCompleted = true
        
        const record = applicationRecords.find(item => 
          item.idCard === this.queryForm.idCard.trim() && 
          item.applicantName === this.queryForm.name.trim() &&
          item.status === 2
        )
        
        if (record) {
          this.ticketData = {
            ...record,
            ticketNo: record.ticketNo || this.generateTicketNo(record.id),
            roomNo: record.roomNo || '第' + String(Math.floor(Math.random() * 30) + 1).padStart(2, '0') + '考场',
            seatNo: record.seatNo || String(Math.floor(Math.random() * 30) + 1).padStart(2, '0') + '号',
            examSite: record.examSite || '第一考点',
            examAddress: record.examAddress || '北京市海淀区中关村大街1号',
            gender: '男'
          }
          this.$message.success('查询成功')
        } else {
          this.ticketData = null
          this.$message.warning('未找到准考证信息，可能是信息有误或审核未通过')
        }
      }, 1000)
    },
    generateTicketNo(id) {
      const now = new Date()
      const year = now.getFullYear()
      return `${year}${String(id).padStart(6, '0')}${Math.floor(Math.random() * 10000).toString().padStart(4, '0')}`
    },
    printTicket() {
      window.print()
    },
    downloadTicket() {
      this.$message.info('PDF下载功能需要后端支持')
    }
  }
}
</script>

<style scoped>
.ticket-content {
  background: #fff;
  padding: 30px;
  border: 2px solid #409EFF;
}

.ticket-header {
  text-align: center;
  border-bottom: 2px solid #409EFF;
  padding-bottom: 20px;
  margin-bottom: 20px;
}

.ticket-header h1 {
  font-size: 28px;
  color: #303133;
  margin: 0 0 10px 0;
  letter-spacing: 5px;
}

.ticket-header p {
  font-size: 14px;
  color: #909399;
  margin: 0;
  letter-spacing: 2px;
}

.ticket-body {
  display: flex;
  gap: 30px;
}

.ticket-info {
  flex: 1;
}

.info-row {
  display: flex;
  gap: 20px;
  margin-bottom: 15px;
}

.info-item {
  flex: 1;
}

.info-item.full-width {
  flex: 2;
}

.info-item .label {
  color: #606266;
  font-weight: 500;
}

.info-item .value {
  color: #303133;
  font-size: 14px;
}

.ticket-photo {
  width: 120px;
}

.photo-placeholder {
  width: 120px;
  height: 160px;
  border: 1px dashed #dcdfe6;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}

.photo-placeholder i {
  font-size: 40px;
  color: #c0c4cc;
  margin-bottom: 10px;
}

.photo-placeholder p {
  margin: 0;
  color: #909399;
  font-size: 12px;
}

.ticket-footer {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.notice-title {
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.notice-content {
  margin: 0;
  padding-left: 20px;
}

.notice-content li {
  font-size: 13px;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 5px;
}

.ticket-seal {
  text-align: right;
  margin-top: 30px;
}

.ticket-seal span {
  display: inline-block;
  padding: 5px 15px;
  border: 2px solid #f56c6c;
  color: #f56c6c;
  transform: rotate(-15deg);
  font-weight: 600;
}

@media print {
  .el-card__header {
    display: none !important;
  }
  .ticket-content {
    border: none;
    padding: 0;
  }
}
</style>
