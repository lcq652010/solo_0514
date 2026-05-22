<template>
  <div class="page-container">
    <el-card class="card-wrapper">
      <div slot="header" class="clearfix">
        <span>课时扣费记录</span>
        <el-button style="float: right; padding: 3px 0;" type="primary" size="small" @click="showDeductDialog">
          课时扣费
        </el-button>
      </div>
      
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="学员姓名">
            <el-input v-model="searchForm.studentName" placeholder="请输入姓名" clearable style="width: 120px;"></el-input>
          </el-form-item>
          <el-form-item label="所属班级">
            <el-select v-model="searchForm.className" placeholder="请选择班级" clearable style="width: 150px;">
              <el-option label="全部班级" value=""></el-option>
              <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="扣费日期">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              style="width: 240px;">
            </el-date-picker>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="summary-bar">
        <el-alert
          title="扣费统计"
          type="info"
          :closable="false"
          show-icon>
          <div slot="default">
            <span>本周扣费：<strong>{{ weeklyTotal }}</strong> 课时</span>
            <span style="margin-left: 30px;">本月扣费：<strong>{{ monthlyTotal }}</strong> 课时</span>
            <span style="margin-left: 30px;">总扣费记录：<strong>{{ deductionList.length }}</strong> 条</span>
          </div>
        </el-alert>
      </div>

      <div class="table-wrapper">
        <el-table :data="tableData" border stripe style="width: 100%">
          <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
          <el-table-column prop="studentName" label="学员姓名" align="center" width="100"></el-table-column>
          <el-table-column prop="className" label="所属班级" align="center"></el-table-column>
          <el-table-column prop="date" label="扣费日期" align="center" width="120"></el-table-column>
          <el-table-column prop="courseName" label="课程名称" align="center"></el-table-column>
          <el-table-column prop="hours" label="扣课时长" align="center" width="100">
            <template slot-scope="scope">
              <span style="color: #f56c6c; font-weight: bold;">-{{ scope.row.hours }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="remainHours" label="剩余课时" align="center" width="100">
            <template slot-scope="scope">
              <span :style="{ color: scope.row.remainHours < 10 ? '#f56c6c' : '#67c23a' }">
                {{ scope.row.remainHours }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="operator" label="操作人" align="center" width="100"></el-table-column>
        </el-table>
      </div>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>

    <el-dialog title="课时扣费" :visible.sync="deductDialogVisible" width="550px">
      <el-form :model="deductForm" :rules="deductRules" ref="deductForm" label-width="100px">
        <el-form-item label="选择学员" prop="studentId">
          <el-select v-model="deductForm.studentId" placeholder="请选择学员" style="width: 100%;" filterable @change="handleStudentChange">
            <el-option v-for="student in activeStudents" :key="student.id" :label="student.name" :value="student.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="selectedStudent" label="当前课时">
          <span style="color: #409EFF; font-size: 16px; font-weight: bold;">
            {{ selectedStudent.remainHours }} / {{ selectedStudent.totalHours }} 课时
          </span>
        </el-form-item>
        <el-form-item label="课程名称" prop="courseName">
          <el-input v-model="deductForm.courseName" placeholder="请输入课程名称"></el-input>
        </el-form-item>
        <el-form-item label="扣课时长" prop="hours">
          <el-input-number v-model="deductForm.hours" :min="0.5" :step="0.5" style="width: 100%;"></el-input-number>
        </el-form-item>
        <el-form-item label="扣费日期" prop="date">
          <el-date-picker
            v-model="deductForm.date"
            type="date"
            placeholder="选择日期"
            format="yyyy-MM-dd"
            value-format="yyyy-MM-dd"
            style="width: 100%;">
          </el-date-picker>
        </el-form-item>
        <el-form-item label="操作人" prop="operator">
          <el-input v-model="deductForm.operator" placeholder="请输入操作人姓名"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="deductDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitDeduct">确认扣费</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockDeductions, mockStudents, classOptions } from '@/mock/data.js';

export default {
  name: 'DeductionRecords',
  data() {
    return {
      searchForm: {
        studentName: '',
        className: '',
        dateRange: []
      },
      deductionList: [...mockDeductions],
      studentList: [...mockStudents],
      classOptions,
      deductDialogVisible: false,
      deductForm: {
        studentId: null,
        courseName: '',
        hours: 2.5,
        date: new Date().toISOString().split('T')[0],
        operator: ''
      },
      deductRules: {
        studentId: [
          { required: true, message: '请选择学员', trigger: 'change' }
        ],
        courseName: [
          { required: true, message: '请输入课程名称', trigger: 'blur' }
        ],
        hours: [
          { required: true, message: '请输入扣课时长', trigger: 'blur' }
        ],
        date: [
          { required: true, message: '请选择扣费日期', trigger: 'change' }
        ],
        operator: [
          { required: true, message: '请输入操作人姓名', trigger: 'blur' }
        ]
      },
      pagination: {
        page: 1,
        size: 10,
        total: mockDeductions.length
      }
    };
  },
  computed: {
    activeStudents() {
      return this.studentList.filter(item => item.status === '在读');
    },
    selectedStudent() {
      if (!this.deductForm.studentId) return null;
      return this.studentList.find(item => item.id === this.deductForm.studentId);
    },
    tableData() {
      let data = [...this.deductionList];
      
      if (this.searchForm.studentName) {
        data = data.filter(item => item.studentName.includes(this.searchForm.studentName));
      }
      if (this.searchForm.className) {
        data = data.filter(item => item.className === this.searchForm.className);
      }
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        data = data.filter(item => 
          item.date >= this.searchForm.dateRange[0] && 
          item.date <= this.searchForm.dateRange[1]
        );
      }
      
      this.pagination.total = data.length;
      
      const start = (this.pagination.page - 1) * this.pagination.size;
      const end = start + this.pagination.size;
      return data.slice(start, end);
    },
    weeklyTotal() {
      const now = new Date();
      const weekStart = new Date(now.getTime() - now.getDay() * 24 * 60 * 60 * 1000);
      const weekStartStr = weekStart.toISOString().split('T')[0];
      return this.deductionList
        .filter(item => item.date >= weekStartStr)
        .reduce((sum, item) => sum + item.hours, 0);
    },
    monthlyTotal() {
      const now = new Date();
      const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
      const monthStartStr = monthStart.toISOString().split('T')[0];
      return this.deductionList
        .filter(item => item.date >= monthStartStr)
        .reduce((sum, item) => sum + item.hours, 0);
    }
  },
  methods: {
    handleSearch() {
      this.pagination.page = 1;
    },
    resetSearch() {
      this.searchForm = {
        studentName: '',
        className: '',
        dateRange: []
      };
      this.pagination.page = 1;
    },
    handleSizeChange(val) {
      this.pagination.size = val;
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
    },
    showDeductDialog() {
      this.deductForm = {
        studentId: null,
        courseName: '',
        hours: 2.5,
        date: new Date().toISOString().split('T')[0],
        operator: ''
      };
      this.deductDialogVisible = true;
      this.$nextTick(() => {
        this.$refs.deductForm.clearValidate();
      });
    },
    handleStudentChange() {
      if (this.selectedStudent && this.selectedStudent.remainHours < this.deductForm.hours) {
        this.$message.warning('该学员剩余课时不足！');
      }
    },
    submitDeduct() {
      this.$refs.deductForm.validate((valid) => {
        if (valid) {
          if (this.selectedStudent.remainHours < this.deductForm.hours) {
            this.$message.error('该学员剩余课时不足，无法扣费！');
            return;
          }
          
          const studentIndex = this.studentList.findIndex(item => item.id === this.deductForm.studentId);
          if (studentIndex > -1) {
            this.studentList[studentIndex].remainHours -= this.deductForm.hours;
          }
          
          const newRecord = {
            id: Date.now(),
            studentName: this.selectedStudent.name,
            className: this.selectedStudent.className,
            date: this.deductForm.date,
            courseName: this.deductForm.courseName,
            hours: this.deductForm.hours,
            remainHours: this.selectedStudent.remainHours,
            operator: this.deductForm.operator
          };
          
          this.deductionList.unshift(newRecord);
          this.$message.success('扣费成功！');
          this.deductDialogVisible = false;
        }
      });
    }
  }
};
</script>

<style scoped>
.summary-bar {
  margin-bottom: 20px;
}
</style>
