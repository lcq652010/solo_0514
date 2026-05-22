<template>
  <div class="page-container">
    <el-card class="card-wrapper">
      <div slot="header">
        <span>续费充值</span>
      </div>

      <el-row :gutter="20">
        <el-col :span="16">
          <div class="form-container">
            <h3 class="form-title">学员充值信息</h3>
            <el-form :model="rechargeForm" :rules="rules" ref="rechargeForm" label-width="120px" size="medium">
              <el-form-item label="选择学员" prop="studentId">
                <el-select 
                  v-model="rechargeForm.studentId" 
                  placeholder="请搜索或选择学员" 
                  style="width: 100%;" 
                  filterable
                  @change="handleStudentChange">
                  <el-option 
                    v-for="student in studentList" 
                    :key="student.id" 
                    :label="`${student.name} - ${student.className}`" 
                    :value="student.id">
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item v-if="selectedStudent" label="当前信息">
                <el-descriptions :column="2" size="small" border>
                  <el-descriptions-item label="学员姓名">{{ selectedStudent.name }}</el-descriptions-item>
                  <el-descriptions-item label="所属班级">{{ selectedStudent.className }}</el-descriptions-item>
                  <el-descriptions-item label="总课时">
                    <span style="color: #409EFF;">{{ selectedStudent.totalHours }}</span>
                  </el-descriptions-item>
                  <el-descriptions-item label="剩余课时">
                    <span :style="{ color: selectedStudent.remainHours < 10 ? '#f56c6c' : '#67c23a', fontWeight: 'bold' }">
                      {{ selectedStudent.remainHours }}
                    </span>
                  </el-descriptions-item>
                </el-descriptions>
              </el-form-item>

              <el-form-item label="充值类型" prop="rechargeType">
                <el-radio-group v-model="rechargeForm.rechargeType">
                  <el-radio label="hours">按课时充值</el-radio>
                  <el-radio label="amount">按金额充值</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item v-if="rechargeForm.rechargeType === 'hours'" label="充值课时" prop="rechargeHours">
                <el-input-number v-model="rechargeForm.rechargeHours" :min="5" :step="5" style="width: 200px;"></el-input-number>
                <span style="margin-left: 15px; color: #606266;">
                  共 <strong style="color: #f56c6c; font-size: 18px;">{{ calculateAmount }}</strong> 元（1课时 = 100元）
                </span>
              </el-form-item>

              <el-form-item v-if="rechargeForm.rechargeType === 'amount'" label="充值金额" prop="rechargeAmount">
                <el-input-number v-model="rechargeForm.rechargeAmount" :min="500" :step="500" style="width: 200px;"></el-input-number>
                <span style="margin-left: 15px; color: #606266;">
                  共 <strong style="color: #67c23a; font-size: 18px;">{{ calculateHours }}</strong> 课时（100元 = 1课时）
                </span>
              </el-form-item>

              <el-form-item label="赠送课时">
                <el-input-number v-model="rechargeForm.bonusHours" :min="0" :step="1" style="width: 200px;"></el-input-number>
                <span style="margin-left: 15px; color: #909399;">（可填写0）</span>
              </el-form-item>

              <el-form-item label="支付方式" prop="paymentMethod">
                <el-select v-model="rechargeForm.paymentMethod" placeholder="请选择支付方式" style="width: 200px;">
                  <el-option label="微信支付" value="wechat"></el-option>
                  <el-option label="支付宝" value="alipay"></el-option>
                  <el-option label="银行卡" value="bank"></el-option>
                  <el-option label="现金" value="cash"></el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="备注">
                <el-input type="textarea" v-model="rechargeForm.remark" :rows="3" placeholder="请输入备注信息"></el-input>
              </el-form-item>

              <el-form-item>
                <el-button type="primary" size="large" @click="submitRecharge" :loading="submitting">
                  确认充值
                </el-button>
                <el-button size="large" @click="resetForm">重置表单</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-col>

        <el-col :span="8">
          <div class="history-container">
            <h3 class="form-title">充值记录</h3>
            <el-timeline>
              <el-timeline-item 
                v-for="(record, index) in rechargeHistory.slice(0, 8)" 
                :key="record.id"
                :timestamp="record.date"
                placement="top">
                <el-card>
                  <h4>{{ record.studentName }}</h4>
                  <p style="color: #67c23a;">+{{ record.totalHours }} 课时</p>
                  <p style="color: #909399; font-size: 12px;">{{ record.paymentMethodText }} · {{ record.amount }}元</p>
                </el-card>
              </el-timeline-item>
            </el-timeline>
            <div v-if="rechargeHistory.length === 0" class="empty-text">
              暂无充值记录
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-dialog title="充值成功" :visible.sync="successDialogVisible" width="500px" @close="handleDialogClose">
      <div class="success-content">
        <el-result icon="success" title="充值成功" sub-title="已为该学员添加课时">
          <template slot="extra">
            <el-descriptions :column="2" border size="small">
              <el-descriptions-item label="学员姓名">{{ successData.studentName }}</el-descriptions-item>
              <el-descriptions-item label="所属班级">{{ successData.className }}</el-descriptions-item>
              <el-descriptions-item label="充值课时">+{{ successData.rechargeHours }}</el-descriptions-item>
              <el-descriptions-item label="赠送课时">+{{ successData.bonusHours }}</el-descriptions-item>
              <el-descriptions-item label="充值金额">{{ successData.amount }}元</el-descriptions-item>
              <el-descriptions-item label="剩余课时">{{ successData.newRemainHours }}</el-descriptions-item>
            </el-descriptions>
          </template>
        </el-result>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="successDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="continueRecharge">继续充值</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockStudents } from '@/mock/data.js';

export default {
  name: 'RechargeForm',
  data() {
    return {
      studentList: [...mockStudents],
      rechargeForm: {
        studentId: null,
        rechargeType: 'hours',
        rechargeHours: 20,
        rechargeAmount: 2000,
        bonusHours: 0,
        paymentMethod: '',
        remark: ''
      },
      rules: {
        studentId: [
          { required: true, message: '请选择学员', trigger: 'change' }
        ],
        rechargeHours: [
          { required: true, message: '请输入充值课时', trigger: 'blur' }
        ],
        rechargeAmount: [
          { required: true, message: '请输入充值金额', trigger: 'blur' }
        ],
        paymentMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ]
      },
      submitting: false,
      successDialogVisible: false,
      successData: {},
      rechargeHistory: []
    };
  },
  computed: {
    selectedStudent() {
      if (!this.rechargeForm.studentId) return null;
      return this.studentList.find(item => item.id === this.rechargeForm.studentId);
    },
    calculateAmount() {
      return this.rechargeForm.rechargeHours * 100;
    },
    calculateHours() {
      return Math.floor(this.rechargeForm.rechargeAmount / 100);
    }
  },
  methods: {
    handleStudentChange() {
      if (this.selectedStudent && this.selectedStudent.remainHours < 10) {
        this.$message.warning('该学员课时不足，建议充值！');
      }
    },
    submitRecharge() {
      this.$refs.rechargeForm.validate((valid) => {
        if (valid) {
          this.submitting = true;
          
          setTimeout(() => {
            const studentIndex = this.studentList.findIndex(item => item.id === this.rechargeForm.studentId);
            const addHours = this.rechargeForm.rechargeType === 'hours' 
              ? this.rechargeForm.rechargeHours 
              : this.calculateHours;
            const totalAddHours = addHours + this.rechargeForm.bonusHours;
            const totalAmount = this.rechargeForm.rechargeType === 'hours'
              ? this.calculateAmount
              : this.rechargeForm.rechargeAmount;
            
            if (studentIndex > -1) {
              this.studentList[studentIndex].remainHours += totalAddHours;
              this.studentList[studentIndex].totalHours += totalAddHours;
            }

            const paymentMethodMap = {
              wechat: '微信支付',
              alipay: '支付宝',
              bank: '银行卡',
              cash: '现金'
            };

            const historyRecord = {
              id: Date.now(),
              studentName: this.selectedStudent.name,
              className: this.selectedStudent.className,
              date: new Date().toLocaleString(),
              totalHours: totalAddHours,
              amount: totalAmount,
              paymentMethodText: paymentMethodMap[this.rechargeForm.paymentMethod]
            };
            this.rechargeHistory.unshift(historyRecord);

            this.successData = {
              studentName: this.selectedStudent.name,
              className: this.selectedStudent.className,
              rechargeHours: addHours,
              bonusHours: this.rechargeForm.bonusHours,
              amount: totalAmount,
              newRemainHours: this.selectedStudent.remainHours
            };

            this.submitting = false;
            this.successDialogVisible = true;
          }, 1000);
        }
      });
    },
    resetForm() {
      this.$refs.rechargeForm.resetFields();
      this.rechargeForm.bonusHours = 0;
    },
    handleDialogClose() {
      this.resetForm();
    },
    continueRecharge() {
      this.successDialogVisible = false;
      this.resetForm();
    }
  }
};
</script>

<style scoped>
.form-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
}
.form-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #409EFF;
}
.history-container {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  max-height: 600px;
  overflow-y: auto;
}
.empty-text {
  text-align: center;
  padding: 40px;
  color: #909399;
}
.success-content {
  text-align: center;
}
.el-card {
  box-shadow: none;
}
</style>
