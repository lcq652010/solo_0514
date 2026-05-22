<template>
  <div class="page-container">
    <el-button @click="goBack" class="back-btn">
      <i class="el-icon-arrow-left"></i> 返回
    </el-button>

    <el-card v-if="activity" class="checkin-card card-shadow">
      <div class="checkin-header">
        <h2 class="checkin-title">活动签到</h2>
        <div class="activity-brief">
          <h3>{{ activity.title }}</h3>
          <p>
            <i class="el-icon-date"></i> {{ activity.date }} {{ activity.time }}
            <span class="separator">|</span>
            <i class="el-icon-location-outline"></i> {{ activity.location }}
          </p>
        </div>
      </div>

      <div class="checkin-content">
        <div class="qr-section" v-if="!checkedIn">
          <div class="qr-placeholder">
            <i class="el-icon-scan"></i>
          </div>
          <p class="qr-tip">请使用手机扫描二维码完成签到</p>
        </div>

        <div class="success-section" v-else>
          <div class="success-icon">
            <i class="el-icon-success"></i>
          </div>
          <h3 class="success-title">签到成功！</h3>
          <p class="success-time">签到时间：{{ checkInTime }}</p>
        </div>

        <el-divider></el-divider>

        <div class="manual-checkin">
          <h4 class="section-title">手动签到</h4>
          <el-form :model="checkinForm" :rules="rules" ref="checkinForm" inline>
            <el-form-item label="姓名" prop="name">
              <el-input v-model="checkinForm.name" placeholder="请输入姓名"></el-input>
            </el-form-item>
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="checkinForm.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="handleCheckIn" :loading="checkingIn" :disabled="checkedIn">
                {{ checkedIn ? '已签到' : '确认签到' }}
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <el-divider></el-divider>

      <div class="checkin-list">
        <h4 class="section-title">签到列表</h4>
        <el-table :data="checkinList" style="width: 100%" border>
          <el-table-column prop="id" label="序号" width="80" align="center"></el-table-column>
          <el-table-column prop="name" label="姓名" align="center"></el-table-column>
          <el-table-column prop="studentId" label="学号" align="center"></el-table-column>
          <el-table-column prop="college" label="学院" align="center"></el-table-column>
          <el-table-column prop="checkinTime" label="签到时间" align="center"></el-table-column>
          <el-table-column label="状态" align="center">
            <template slot-scope="scope">
              <el-tag type="success" size="small">已签到</el-tag>
            </template>
          </el-table-column>
        </el-table>
        <div class="list-footer">
          <span>已签到人数：{{ checkinList.length }} 人</span>
        </div>
      </div>
    </el-card>

    <el-empty v-else description="活动不存在"></el-empty>
  </div>
</template>

<script>
import { activities } from '../mock/data'

export default {
  name: 'ActivityCheckIn',
  data() {
    return {
      activity: null,
      checkedIn: false,
      checkingIn: false,
      checkInTime: '',
      checkinForm: {
        name: '',
        phone: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
        ]
      },
      checkinList: [
        { id: 1, name: '张三', studentId: '2024001', college: '计算机学院', checkinTime: '2024-09-10 09:15:30' },
        { id: 2, name: '李四', studentId: '2024002', college: '文学院', checkinTime: '2024-09-10 09:20:15' },
        { id: 3, name: '王五', studentId: '2024003', college: '理学院', checkinTime: '2024-09-10 09:25:45' },
        { id: 4, name: '赵六', studentId: '2024004', college: '工学院', checkinTime: '2024-09-10 09:30:20' },
        { id: 5, name: '钱七', studentId: '2024005', college: '商学院', checkinTime: '2024-09-10 09:35:10' }
      ]
    }
  },
  mounted() {
    this.loadActivity()
  },
  methods: {
    loadActivity() {
      const id = parseInt(this.$route.params.id)
      this.activity = activities.find(item => item.id === id)
    },
    goBack() {
      this.$router.push(`/activity/${this.$route.params.id}`)
    },
    handleCheckIn() {
      this.$refs.checkinForm.validate((valid) => {
        if (valid) {
          this.checkingIn = true
          setTimeout(() => {
            this.checkingIn = false
            this.checkedIn = true
            const now = new Date()
            this.checkInTime = now.toLocaleString('zh-CN')
            this.checkinList.unshift({
              id: this.checkinList.length + 1,
              name: this.checkinForm.name,
              studentId: '2024' + String(this.checkinList.length + 1).padStart(3, '0'),
              college: '计算机学院',
              checkinTime: this.checkInTime
            })
            this.$message.success('签到成功！')
          }, 1000)
        } else {
          this.$message.error('请完善签到信息')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.back-btn {
  margin-bottom: 20px;
}

.checkin-card {
  background: white;
  max-width: 800px;
  margin: 0 auto;
}

.checkin-header {
  text-align: center;
  margin-bottom: 30px;
}

.checkin-title {
  font-size: 22px;
  color: #303133;
  margin: 0 0 20px 0;
}

.activity-brief {
  background: #f5f7fa;
  padding: 15px 20px;
  border-radius: 8px;
}

.activity-brief h3 {
  font-size: 16px;
  color: #303133;
  margin: 0 0 10px 0;
}

.activity-brief p {
  font-size: 14px;
  color: #606266;
  margin: 0;
}

.activity-brief i {
  margin-right: 5px;
}

.separator {
  margin: 0 10px;
  color: #c0c4cc;
}

.qr-section {
  text-align: center;
  padding: 40px 0;
}

.qr-placeholder {
  width: 200px;
  height: 200px;
  margin: 0 auto 20px;
  background: #f5f7fa;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qr-placeholder i {
  font-size: 60px;
  color: #c0c4cc;
}

.qr-tip {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.success-section {
  text-align: center;
  padding: 40px 0;
}

.success-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 20px;
  background: #f0f9eb;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-icon i {
  font-size: 40px;
  color: #67c23a;
}

.success-title {
  font-size: 20px;
  color: #67c23a;
  margin: 0 0 10px 0;
}

.success-time {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.section-title {
  font-size: 16px;
  color: #303133;
  margin: 0 0 20px 0;
}

.manual-checkin {
  padding: 20px 0;
}

.checkin-list {
  padding-top: 10px;
}

.list-footer {
  text-align: right;
  padding: 15px 0 0;
  font-size: 14px;
  color: #606266;
}
</style>
