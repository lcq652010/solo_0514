<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-success"></i>
      就诊签到
    </h2>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="checkin-card">
          <div slot="header" class="card-header">
            <span>签到入口</span>
          </div>
          <div class="checkin-form">
            <el-form :model="checkinForm" :rules="checkinRules" ref="checkinForm" label-width="100px">
              <el-form-item label="挂号单号" prop="registerNo">
                <el-input v-model="checkinForm.registerNo" placeholder="请输入挂号单号" style="width: 100%;"></el-input>
              </el-form-item>
              <el-form-item label="患者姓名" prop="patientName">
                <el-input v-model="checkinForm.patientName" placeholder="请输入患者姓名" style="width: 100%;"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="doCheckin" style="width: 100%;" size="large">
                  <i class="el-icon-check"></i> 立即签到
                </el-button>
              </el-form-item>
            </el-form>

            <el-divider content-position="center">或者</el-divider>

            <div class="qr-section">
              <p class="qr-tip">扫描挂号单二维码签到</p>
              <div class="qr-placeholder">
                <i class="el-icon-picture-outline"></i>
                <p>扫码区域</p>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card class="today-card">
          <div slot="header" class="card-header">
            <span>今日签到记录</span>
            <el-tag type="success" size="small">已签到：{{ checkedInCount }}人</el-tag>
          </div>
          <el-table :data="todayRecords" border stripe style="width: 100%" size="small">
            <el-table-column prop="number" label="排队号" align="center" width="70"></el-table-column>
            <el-table-column prop="patientName" label="患者姓名" align="center" width="90"></el-table-column>
            <el-table-column prop="department" label="科室" align="center" width="90"></el-table-column>
            <el-table-column prop="doctor" label="医生" align="center" width="90"></el-table-column>
            <el-table-column prop="time" label="时段" align="center" width="70">
              <template slot-scope="scope">
                <el-tag :type="scope.row.time === '上午' ? 'success' : 'primary'" size="mini">
                  {{ scope.row.time }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="checkinTime" label="签到时间" align="center" width="100"></el-table-column>
          </el-table>
          <el-empty v-if="todayRecords.length === 0" description="暂无签到记录" :image-size="80"></el-empty>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog title="签到成功" :visible.sync="successDialogVisible" width="450px" center>
      <div class="success-content">
        <div class="success-icon">
          <i class="el-icon-success"></i>
        </div>
        <h3>签到成功！</h3>
        <el-descriptions :column="1" border v-if="checkedInRecord" size="small">
          <el-descriptions-item label="排队号">{{ checkedInRecord.number }}</el-descriptions-item>
          <el-descriptions-item label="患者姓名">{{ checkedInRecord.patientName }}</el-descriptions-item>
          <el-descriptions-item label="就诊科室">{{ checkedInRecord.department }}</el-descriptions-item>
          <el-descriptions-item label="就诊医生">{{ checkedInRecord.doctor }}</el-descriptions-item>
          <el-descriptions-item label="就诊时段">{{ checkedInRecord.time }}</el-descriptions-item>
          <el-descriptions-item label="签到时间">{{ checkedInRecord.checkinTime }}</el-descriptions-item>
        </el-descriptions>
        <p class="tip-text">请在候诊区耐心等待叫号</p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="successDialogVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { store } from '@/store';

export default {
  name: 'CheckIn',
  data() {
    return {
      checkinForm: {
        registerNo: '',
        patientName: ''
      },
      checkinRules: {
        registerNo: [{ required: true, message: '请输入挂号单号', trigger: 'blur' }],
        patientName: [{ required: true, message: '请输入患者姓名', trigger: 'blur' }]
      },
      successDialogVisible: false,
      checkedInRecord: null,
      todayCheckInList: [],
      unsubscribe: null
    };
  },
  computed: {
    recordList() {
      return store.getRegistrations();
    },
    todayRecords() {
      return this.todayCheckInList;
    },
    checkedInCount() {
      return this.todayCheckInList.length;
    }
  },
  mounted() {
    // 订阅数据变化
    this.unsubscribe = store.subscribe(() => {
      this.$forceUpdate();
    });
  },
  beforeDestroy() {
    if (this.unsubscribe) {
      this.unsubscribe();
    }
  },
  methods: {
    doCheckIn() {
      this.$refs.checkinForm.validate(valid => {
        if (valid) {
          const record = this.recordList.find(r => 
            r.patientName === this.checkinForm.patientName && r.status === 0
          );
          
          if (!record) {
            this.$message.error('未找到待就诊的挂号记录，请核对信息');
            return;
          }

          record.status = 1;
          record.checkinTime = new Date().toLocaleTimeString();
          this.checkedInRecord = record;
          
          this.todayCheckInList.unshift({
            number: record.number,
            patientName: record.patientName,
            department: record.department,
            doctor: record.doctor,
            time: record.time,
            checkinTime: record.checkinTime
          });

          store.notify();
          this.successDialogVisible = true;
          this.$refs.checkinForm.resetFields();
        }
      });
    }
  }
};
</script>

<style scoped>
.card-header {
  font-weight: 600;
  color: #303133;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.checkin-card, .today-card {
  height: 100%;
}

.checkin-form {
  padding: 20px 0;
}

.qr-section {
  text-align: center;
}

.qr-tip {
  color: #606266;
  margin-bottom: 15px;
}

.qr-placeholder {
  width: 180px;
  height: 180px;
  margin: 0 auto;
  border: 2px dashed #DCDFE6;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: #909399;
  background: #FAFAFA;
}

.qr-placeholder i {
  font-size: 48px;
  margin-bottom: 10px;
}

.success-content {
  text-align: center;
  padding: 20px 0;
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
  font-size: 48px;
  color: #67c23a;
}

.success-content h3 {
  color: #303133;
  margin-bottom: 20px;
  font-size: 20px;
}

.tip-text {
  margin-top: 20px;
  color: #909399;
  font-size: 14px;
}
</style>
