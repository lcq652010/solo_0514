<template>
  <div class="overtime-apply">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>加班申请</span>
      </div>
      <el-form :model="form" :rules="rules" ref="form" label-width="120px">
        <el-form-item label="加班类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择加班类型" style="width: 100%">
            <el-option label="工作日加班" value="weekday"></el-option>
            <el-option label="周末加班" value="weekend"></el-option>
            <el-option label="节假日加班" value="holiday"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="startTime">
          <el-date-picker
            v-model="form.startTime"
            type="datetime"
            placeholder="选择开始时间"
            style="width: 100%"
            format="yyyy-MM-dd HH:mm"
            value-format="yyyy-MM-dd HH:mm"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="结束时间" prop="endTime">
          <el-date-picker
            v-model="form.endTime"
            type="datetime"
            placeholder="选择结束时间"
            style="width: 100%"
            format="yyyy-MM-dd HH:mm"
            value-format="yyyy-MM-dd HH:mm"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="加班时长">
          <el-input v-model="duration" disabled></el-input>
        </el-form-item>
        <el-form-item label="加班原因" prop="reason">
          <el-input
            type="textarea"
            v-model="form.reason"
            placeholder="请输入加班原因"
            rows="4"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交申请</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { applyOvertime } from '@/api/overtime';

export default {
  name: 'OvertimeApply',
  data() {
    return {
      form: {
        type: '',
        startTime: '',
        endTime: '',
        reason: ''
      },
      rules: {
        type: [
          { required: true, message: '请选择加班类型', trigger: 'change' }
        ],
        startTime: [
          { required: true, message: '请选择开始时间', trigger: 'change' }
        ],
        endTime: [
          { required: true, message: '请选择结束时间', trigger: 'change' }
        ],
        reason: [
          { required: true, message: '请输入加班原因', trigger: 'blur' },
          { min: 5, message: '加班原因不能少于5个字', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    duration() {
      if (this.form.startTime && this.form.endTime) {
        const start = new Date(this.form.startTime);
        const end = new Date(this.form.endTime);
        const diff = (end - start) / (1000 * 60 * 60);
        return diff > 0 ? diff.toFixed(1) + ' 小时' : '0 小时';
      }
      return '0 小时';
    }
  },
  methods: {
    calculateDailyTotal(targetDate) {
      const dateStr = targetDate.split(' ')[0];
      const userRecords = this.$store ? this.$store.state.records || [] : [];
      const sameDayRecords = userRecords.filter(r => {
        if (r.applicant !== '张三') return false;
        const recordDate = r.startTime.split(' ')[0];
        return recordDate === dateStr && r.status !== 'rejected';
      });
      const totalHours = sameDayRecords.reduce((sum, r) => sum + r.duration, 0);
      return totalHours;
    },
    submitForm() {
      this.$refs.form.validate(async valid => {
        if (valid) {
          const start = new Date(this.form.startTime);
          const end = new Date(this.form.endTime);
          if (end <= start) {
            this.$message.error('结束时间必须晚于开始时间');
            return;
          }
          const duration = (end - start) / (1000 * 60 * 60);
          if (duration <= 0) {
            this.$message.error('加班时长必须大于0小时');
            return;
          }
          if (duration < 0.25) {
            this.$message.error('加班时长不能少于15分钟');
            return;
          }
          if (duration > 24) {
            this.$message.error('加班时长不能超过24小时');
            return;
          }
          const dailyLimit = 12;
          const existingTotal = this.calculateDailyTotal(this.form.startTime);
          const newTotal = existingTotal + duration;
          if (newTotal > dailyLimit) {
            this.$message.error(`单日累计加班时长不能超过${dailyLimit}小时，当前已累计${existingTotal.toFixed(1)}小时`);
            return;
          }
          try {
            const res = await applyOvertime({ ...this.form, duration });
            if (res.data.code === 200) {
              this.$message.success('申请提交成功');
              this.resetForm();
            }
          } catch (error) {
            this.$message.error('申请提交失败');
          }
        }
      });
    },
    resetForm() {
      this.$refs.form.resetFields();
    }
  }
};
</script>

<style scoped>
.overtime-apply {
  padding: 20px;
}

.box-card {
  max-width: 800px;
  margin: 0 auto;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: '';
}
.clearfix:after {
  clear: both;
}
</style>
