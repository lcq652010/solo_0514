<template>
  <div class="reminder-page">
    <div class="page-header">
      <div class="page-title">余额提醒设置</div>
      <div class="page-subtitle">设置余额预警阈值，及时接收提醒通知</div>
    </div>

    <el-row :gutter="20">
      <el-col :span="8">
        <div class="card-wrapper balance-card water-balance">
          <div class="balance-icon">
            <i class="el-icon-water-cup"></i>
          </div>
          <div class="balance-info">
            <div class="balance-label">水费余额</div>
            <div class="balance-value">
              ¥{{ dormitoryInfo.waterBalance }}
            </div>
            <div v-if="dormitoryInfo.waterBalance <= settings.waterThreshold" class="balance-warning">
              <i class="el-icon-warning"></i>余额低于阈值
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="card-wrapper balance-card electric-balance">
          <div class="balance-icon">
            <i class="el-icon-lightning"></i>
          </div>
          <div class="balance-info">
            <div class="balance-label">电费余额</div>
            <div class="balance-value">
              ¥{{ dormitoryInfo.electricBalance }}
            </div>
            <div v-if="dormitoryInfo.electricBalance <= settings.electricThreshold" class="balance-warning">
              <i class="el-icon-warning"></i>余额低于阈值
            </div>
          </div>
        </div>
      </el-col>

      <el-col :span="8">
        <div class="card-wrapper balance-card status-card">
          <div class="balance-icon">
            <i class="el-icon-bell"></i>
          </div>
          <div class="balance-info">
            <div class="balance-label">提醒状态</div>
            <div class="balance-value" style="font-size: 18px;">
              <el-switch
                v-model="settings.enableNotification"
                active-color="#67C23A"
                inactive-color="#DCDFE6"
                @change="toggleNotification"
              />
            </div>
            <div class="balance-status">
              {{ settings.enableNotification ? '已开启提醒' : '已关闭提醒' }}
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <div class="card-wrapper">
      <div class="card-header">
        <span class="card-title">提醒参数设置</span>
      </div>
      <el-form
        ref="settingsForm"
        :model="settings"
        label-width="120px"
        class="settings-form"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="水费预警阈值">
              <el-input-number
                v-model="settings.waterThreshold"
                :min="1"
                :max="100"
                :step="1"
                style="width: 150px;"
              />
              <span class="unit-text">元</span>
              <div class="form-tip">当水费余额低于此值时发送提醒</div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="电费预警阈值">
              <el-input-number
                v-model="settings.electricThreshold"
                :min="1"
                :max="200"
                :step="1"
                style="width: 150px;"
              />
              <span class="unit-text">元</span>
              <div class="form-tip">当电费余额低于此值时发送提醒</div>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider />

        <el-form-item label="通知方式">
          <el-checkbox-group v-model="notificationMethods">
            <el-checkbox label="sms">短信通知</el-checkbox>
            <el-checkbox label="email">邮件通知</el-checkbox>
            <el-checkbox label="wechat">微信推送</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="接收手机号">
          <el-input
            v-model="settings.phone"
            placeholder="请输入接收短信的手机号"
            style="width: 300px;"
            maxlength="11"
          />
        </el-form-item>

        <el-form-item label="接收邮箱">
          <el-input
            v-model="settings.email"
            placeholder="请输入接收邮件的邮箱地址"
            style="width: 300px;"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="saveSettings">保存设置</el-button>
          <el-button size="large" @click="resetSettings">恢复默认</el-button>
          <el-button type="success" size="large" @click="testNotification">测试通知</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card-wrapper">
      <div class="card-header">
        <span class="card-title">提醒历史记录</span>
        <el-tag type="info">最近10条</el-tag>
      </div>
      <el-timeline>
        <el-timeline-item
          v-for="(item, index) in reminderHistory"
          :key="index"
          :timestamp="item.time"
          :type="item.type === 'warning' ? 'warning' : 'success'"
          placement="top"
        >
          <div class="timeline-content">
            <div class="timeline-title">
              <i :class="item.icon"></i>
              {{ item.title }}
            </div>
            <div class="timeline-desc">{{ item.content }}</div>
          </div>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script>
import { dormitoryInfo, reminderSettings } from '@/data/mock.js'

export default {
  name: 'Reminder',
  data() {
    return {
      dormitoryInfo,
      settings: { ...reminderSettings },
      notificationMethods: ['sms'],
      reminderHistory: [
        {
          time: '2024-05-15 08:30:00',
          type: 'warning',
          icon: 'el-icon-warning',
          title: '水费余额预警',
          content: '您的1号楼302宿舍水费余额仅剩15.50元，请及时充值以免影响使用。'
        },
        {
          time: '2024-05-14 18:20:00',
          type: 'success',
          icon: 'el-icon-circle-check',
          title: '电费充值成功提醒',
          content: '您的1号楼302宿舍电费充值成功，充值金额50.00元，当前余额48.30元。'
        },
        {
          time: '2024-05-12 10:15:00',
          type: 'warning',
          icon: 'el-icon-warning',
          title: '电费余额预警',
          content: '您的1号楼302宿舍电费余额仅剩18.30元，请及时充值以免影响使用。'
        },
        {
          time: '2024-05-10 09:00:00',
          type: 'success',
          icon: 'el-icon-circle-check',
          title: '水费充值成功提醒',
          content: '您的1号楼302宿舍水费充值成功，充值金额30.00元，当前余额25.50元。'
        }
      ]
    }
  },
  methods: {
    toggleNotification(val) {
      this.$message.info(val ? '已开启余额提醒' : '已关闭余额提醒')
    },
    saveSettings() {
      if (!this.settings.phone) {
        this.$message.warning('请输入接收手机号')
        return
      }
      if (!/^1[3-9]\d{9}$/.test(this.settings.phone)) {
        this.$message.error('请输入正确的手机号格式')
        return
      }
      this.$message.success('提醒设置已保存成功！')
    },
    resetSettings() {
      this.$confirm('确定要恢复默认设置吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.settings = {
          waterThreshold: 10,
          electricThreshold: 20,
          enableNotification: true,
          notificationMethod: 'sms',
          phone: '',
          email: ''
        }
        this.$message.success('已恢复默认设置')
      }).catch(() => {})
    },
    testNotification() {
      if (!this.settings.phone && !this.settings.email) {
        this.$message.warning('请先设置手机号或邮箱')
        return
      }
      this.$message.success('测试通知已发送，请查看您的手机或邮箱！')
    }
  }
}
</script>

<style scoped>
.reminder-page {
  width: 100%;
}

.balance-card {
  display: flex;
  align-items: center;
  padding: 25px 20px !important;
}

.water-balance {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.electric-balance {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
}

.status-card {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
}

.balance-icon {
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
}

.balance-icon i {
  font-size: 30px;
  color: #fff;
}

.balance-info {
  flex: 1;
  color: #fff;
}

.balance-label {
  font-size: 14px;
  opacity: 0.9;
  margin-bottom: 8px;
}

.balance-value {
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.balance-warning {
  font-size: 12px;
  background: rgba(255, 255, 255, 0.2);
  padding: 4px 10px;
  border-radius: 12px;
  display: inline-block;
}

.balance-status {
  font-size: 14px;
  opacity: 0.9;
}

.settings-form {
  padding: 20px 0;
}

.unit-text {
  margin-left: 10px;
  color: #606266;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.timeline-content {
  padding: 10px 0;
}

.timeline-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 5px;
}

.timeline-title i {
  margin-right: 5px;
}

.timeline-desc {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
}
</style>
