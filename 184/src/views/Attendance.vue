<template>
  <div class="page-container">
    <el-card class="card-wrapper">
      <div slot="header" class="clearfix">
        <span>考勤签到</span>
        <el-button style="float: right; padding: 3px 0;" type="primary" size="small" @click="showSignDialog">
          批量签到
        </el-button>
      </div>
      
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="calendar-wrapper">
            <el-date-picker
              v-model="selectedDate"
              type="date"
              placeholder="选择日期"
              format="yyyy-MM-dd"
              value-format="yyyy-MM-dd"
              style="width: 100%; margin-bottom: 15px;"
              @change="handleDateChange">
            </el-date-picker>
            <el-calendar v-model="selectedDate">
              <template slot="dateCell" slot-scope="{date, data}">
                <div :class="getDateClass(data.day)">
                  {{ date.day }}
                </div>
              </template>
            </el-calendar>
          </div>
        </el-col>
        
        <el-col :span="18">
          <div class="search-bar">
            <el-form :inline="true" :model="searchForm">
              <el-form-item label="所属班级">
                <el-select v-model="searchForm.className" placeholder="请选择班级" clearable style="width: 130px;">
                  <el-option label="全部班级" value=""></el-option>
                  <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="课程名称">
                <el-select v-model="searchForm.courseName" placeholder="请选择课程" clearable style="width: 130px;">
                  <el-option label="全部课程" value=""></el-option>
                  <el-option v-for="course in courseOptions" :key="course" :label="course" :value="course"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="考勤日期">
                <el-date-picker
                  v-model="searchForm.dateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  format="yyyy-MM-dd"
                  value-format="yyyy-MM-dd"
                  style="width: 220px;">
                </el-date-picker>
              </el-form-item>
              <el-form-item label="签到状态">
                <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 100px;">
                  <el-option label="全部状态" value=""></el-option>
                  <el-option label="正常" value="正常"></el-option>
                  <el-option label="迟到" value="迟到"></el-option>
                  <el-option label="缺勤" value="缺勤"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="handleSearch">搜索</el-button>
                <el-button @click="resetSearch">重置</el-button>
              </el-form-item>
            </el-form>
          </div>

          <div class="statistics-bar">
            <el-statistic title="应到人数" :value="statistics.should" style="margin-right: 40px;"></el-statistic>
            <el-statistic title="实到人数" :value="statistics.actual" style="margin-right: 40px;"></el-statistic>
            <el-statistic title="迟到人数" :value="statistics.late" style="margin-right: 40px;" value-color="#E6A23C"></el-statistic>
            <el-statistic title="缺勤人数" :value="statistics.absent" value-color="#F56C6C"></el-statistic>
          </div>

          <div class="table-wrapper">
            <el-table :data="tableData" border stripe style="width: 100%">
              <el-table-column prop="date" label="考勤日期" align="center" width="110"></el-table-column>
              <el-table-column prop="studentName" label="学员姓名" align="center" width="100"></el-table-column>
              <el-table-column prop="className" label="所属班级" align="center"></el-table-column>
              <el-table-column label="剩余课时" align="center" width="100">
                <template slot-scope="scope">
                  <span :style="{ color: getStudentRemainHours(scope.row.studentId) < 2 ? '#f56c6c' : '#67c23a', fontWeight: 'bold' }">
                    {{ getStudentRemainHours(scope.row.studentId) }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column prop="signInTime" label="签到时间" align="center" width="120"></el-table-column>
              <el-table-column prop="signOutTime" label="签退时间" align="center" width="120"></el-table-column>
              <el-table-column prop="status" label="签到状态" align="center" width="100">
                <template slot-scope="scope">
                  <el-tag :type="getStatusType(scope.row.status)">
                    {{ scope.row.status }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" align="center" width="220">
                <template slot-scope="scope">
                  <el-tooltip 
                    v-if="scope.row.status !== '缺勤'"
                    content="该学员今日已签到" 
                    placement="top">
                    <el-button 
                      size="mini" 
                      type="success" 
                      disabled>
                      已签到
                    </el-button>
                  </el-tooltip>
                  <el-tooltip 
                    v-else-if="getStudentRemainHours(scope.row.studentId) < 1"
                    content="课时不足，请先续费" 
                    placement="top">
                    <el-button 
                      size="mini" 
                      type="danger" 
                      disabled>
                      课时不足
                    </el-button>
                  </el-tooltip>
                  <el-button 
                    v-else
                    size="mini" 
                    type="success" 
                    @click="handleSignIn(scope.row)">
                    签到
                  </el-button>
                  <el-button 
                    v-if="scope.row.status !== '缺勤' && scope.row.signOutTime === '-'"
                    size="mini" 
                    type="primary" 
                    @click="handleSignOut(scope.row)">
                    签退
                  </el-button>
                  <el-button size="mini" type="warning" @click="handleEdit(scope.row)">修改</el-button>
                </template>
              </el-table-column>
            </el-table>
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
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-dialog title="批量签到" :visible.sync="signDialogVisible" width="600px">
      <el-form :model="batchForm" label-width="100px">
        <el-form-item label="签到班级">
          <el-select v-model="batchForm.className" placeholder="请选择班级" style="width: 100%;">
            <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="签到时间">
          <el-time-picker
            v-model="batchForm.signTime"
            format="HH:mm"
            value-format="HH:mm"
            placeholder="选择时间"
            style="width: 100%;">
          </el-time-picker>
        </el-form-item>
        <el-form-item label="选择学员">
          <el-checkbox-group v-model="batchForm.selectedStudents">
            <el-checkbox 
              v-for="student in classStudents" 
              :key="student.id" 
              :label="student.name"
              :disabled="student.remainHours < 1">
              {{ student.name }}
              <span :style="{ color: student.remainHours < 2 ? '#f56c6c' : '#67c23a', marginLeft: '5px', fontSize: '12px' }">
                (剩余{{ student.remainHours }}课时)
              </span>
            </el-checkbox>
          </el-checkbox-group>
          <div v-if="classStudents.some(s => s.remainHours < 1)" style="margin-top: 10px; color: #f56c6c; font-size: 12px;">
            <i class="el-icon-warning"></i> 灰色显示的学员课时不足，无法签到
          </div>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="signDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBatchSign">确定签到</el-button>
      </div>
    </el-dialog>

    <el-dialog title="修改考勤" :visible.sync="editDialogVisible" width="500px">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="签到状态">
          <el-select v-model="editForm.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="正常" value="正常"></el-option>
            <el-option label="迟到" value="迟到"></el-option>
            <el-option label="缺勤" value="缺勤"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="签到时间">
          <el-time-picker
            v-model="editForm.signInTime"
            format="HH:mm"
            value-format="HH:mm"
            placeholder="选择签到时间"
            style="width: 100%;">
          </el-time-picker>
        </el-form-item>
        <el-form-item label="签退时间">
          <el-time-picker
            v-model="editForm.signOutTime"
            format="HH:mm"
            value-format="HH:mm"
            placeholder="选择签退时间"
            style="width: 100%;">
          </el-time-picker>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockAttendance, mockStudents, classOptions } from '@/mock/data.js';

export default {
  name: 'Attendance',
  data() {
    return {
      selectedDate: new Date().toISOString().split('T')[0],
      searchForm: {
        className: '',
        courseName: '',
        dateRange: [],
        status: ''
      },
      attendanceList: [...mockAttendance],
      studentList: [...mockStudents],
      classOptions,
      courseOptions: ['Python基础语法', 'Java框架', 'Web前端开发', 'UI设计基础'],
      signDialogVisible: false,
      editDialogVisible: false,
      batchForm: {
        className: '',
        signTime: '',
        selectedStudents: []
      },
      editForm: {
        id: null,
        status: '',
        signInTime: '',
        signOutTime: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      }
    };
  },
  computed: {
    tableData() {
      let data = [...this.attendanceList];
      
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        data = data.filter(item => 
          item.date >= this.searchForm.dateRange[0] && 
          item.date <= this.searchForm.dateRange[1]
        );
      } else {
        data = data.filter(item => item.date === this.selectedDate);
      }
      
      if (this.searchForm.className) {
        data = data.filter(item => item.className === this.searchForm.className);
      }
      if (this.searchForm.status) {
        data = data.filter(item => item.status === this.searchForm.status);
      }
      
      this.pagination.total = data.length;
      
      const start = (this.pagination.page - 1) * this.pagination.size;
      const end = start + this.pagination.size;
      return data.slice(start, end);
    },
    statistics() {
      let data = [...this.attendanceList];
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        data = data.filter(item => 
          item.date >= this.searchForm.dateRange[0] && 
          item.date <= this.searchForm.dateRange[1]
        );
      } else {
        data = data.filter(item => item.date === this.selectedDate);
      }
      return {
        should: data.length || this.studentList.length,
        actual: data.filter(item => item.status !== '缺勤').length,
        late: data.filter(item => item.status === '迟到').length,
        absent: data.filter(item => item.status === '缺勤').length
      };
    },
    classStudents() {
      if (!this.batchForm.className) return [];
      return this.studentList.filter(item => item.className === this.batchForm.className && item.status === '在读');
    }
  },
  methods: {
    handleDateChange() {
      const existingRecords = this.attendanceList.filter(item => item.date === this.selectedDate);
      if (existingRecords.length === 0) {
        this.studentList.filter(s => s.status === '在读').forEach(student => {
          this.attendanceList.push({
            id: Date.now() + student.id,
            studentId: student.id,
            studentName: student.name,
            className: student.className,
            date: this.selectedDate,
            status: '缺勤',
            signInTime: '-',
            signOutTime: '-'
          });
        });
      }
      this.pagination.page = 1;
    },
    handleSearch() {
      this.pagination.page = 1;
      this.$message.success('搜索条件已应用');
    },
    resetSearch() {
      this.searchForm = {
        className: '',
        courseName: '',
        dateRange: [],
        status: ''
      };
      this.pagination.page = 1;
      this.$message.info('搜索条件已重置');
    },
    handleSizeChange(val) {
      this.pagination.size = val;
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
    },
    getDateClass(day) {
      const hasRecords = this.attendanceList.some(item => item.date === day);
      const hasAbsent = this.attendanceList.some(item => item.date === day && item.status === '缺勤');
      if (hasRecords && !hasAbsent) return 'calendar-day-full';
      if (hasAbsent) return 'calendar-day-partial';
      return '';
    },
    getStatusType(status) {
      const typeMap = { '正常': 'success', '迟到': 'warning', '缺勤': 'danger' };
      return typeMap[status] || 'info';
    },
    showSignDialog() {
      this.batchForm = {
        className: '',
        signTime: new Date().toTimeString().slice(0, 5),
        selectedStudents: []
      };
      this.signDialogVisible = true;
    },
    handleSignIn(row) {
      const student = this.studentList.find(s => s.id === row.studentId);
      
      if (student && student.remainHours < 1) {
        this.$message.error('课时不足，无法签到！请先续费充值。');
        return;
      }
      
      const existingRecord = this.attendanceList.find(
        item => item.date === this.selectedDate && 
                item.studentId === row.studentId && 
                item.status !== '缺勤'
      );
      
      if (existingRecord) {
        this.$message.warning('该学员今日已签到，请勿重复签到！');
        return;
      }
      
      const index = this.attendanceList.findIndex(item => item.id === row.id);
      if (index > -1) {
        const now = new Date();
        const timeStr = now.toTimeString().slice(0, 5);
        const hour = now.getHours();
        this.attendanceList[index].status = hour > 9 ? '迟到' : '正常';
        this.attendanceList[index].signInTime = timeStr;
        
        if (student) {
          const studentIndex = this.studentList.findIndex(s => s.id === student.id);
          if (studentIndex > -1) {
            this.studentList[studentIndex].remainHours -= 1;
          }
        }
        
        this.pagination.page = 1;
        this.$message.success('签到成功，已扣除1课时');
      }
    },
    handleSignOut(row) {
      const index = this.attendanceList.findIndex(item => item.id === row.id);
      if (index > -1) {
        this.attendanceList[index].signOutTime = new Date().toTimeString().slice(0, 5);
        this.$message.success('签退成功');
      }
    },
    handleEdit(row) {
      this.editForm = { ...row };
      this.editDialogVisible = true;
    },
    getStudentRemainHours(studentId) {
      const student = this.studentList.find(s => s.id === studentId);
      return student ? student.remainHours : 0;
    },
    submitBatchSign() {
      if (!this.batchForm.className || this.batchForm.selectedStudents.length === 0) {
        this.$message.warning('请选择班级和学员');
        return;
      }
      
      let successCount = 0;
      let failMessages = [];
      
      this.batchForm.selectedStudents.forEach(name => {
        const student = this.studentList.find(s => s.name === name);
        if (student) {
          if (student.remainHours < 1) {
            failMessages.push(`${name}：课时不足`);
            return;
          }
          
          const existingRecord = this.attendanceList.find(
            item => item.date === this.selectedDate && 
                    item.studentId === student.id && 
                    item.status !== '缺勤'
          );
          
          if (existingRecord) {
            failMessages.push(`${name}：今日已签到`);
            return;
          }
          
          const recordIndex = this.attendanceList.findIndex(
            item => item.date === this.selectedDate && item.studentId === student.id
          );
          const hour = parseInt(this.batchForm.signTime.split(':')[0]);
          if (recordIndex > -1) {
            this.attendanceList[recordIndex].status = hour > 9 ? '迟到' : '正常';
            this.attendanceList[recordIndex].signInTime = this.batchForm.signTime;
            
            const studentIndex = this.studentList.findIndex(s => s.id === student.id);
            if (studentIndex > -1) {
              this.studentList[studentIndex].remainHours -= 1;
            }
            
            successCount++;
          } else {
            this.attendanceList.push({
              id: Date.now() + student.id,
              studentId: student.id,
              studentName: student.name,
              className: this.batchForm.className,
              date: this.selectedDate,
              status: hour > 9 ? '迟到' : '正常',
              signInTime: this.batchForm.signTime,
              signOutTime: '-'
            });
            
            const studentIndex = this.studentList.findIndex(s => s.id === student.id);
            if (studentIndex > -1) {
              this.studentList[studentIndex].remainHours -= 1;
            }
            
            successCount++;
          }
        }
      });
      
      if (successCount > 0) {
        this.pagination.page = 1;
        this.$message.success(`批量签到成功，共 ${successCount} 人`);
      }
      if (failMessages.length > 0) {
        this.$message.warning(`以下学员签到失败：${failMessages.join('；')}`);
      }
      this.signDialogVisible = false;
    },
    submitEdit() {
      const index = this.attendanceList.findIndex(item => item.id === this.editForm.id);
      if (index > -1) {
        this.attendanceList[index] = { ...this.editForm };
        this.$message.success('修改成功');
        this.editDialogVisible = false;
      }
    }
  },
  mounted() {
    this.handleDateChange();
  }
};
</script>

<style scoped>
.calendar-wrapper {
  background: #fff;
  padding: 15px;
  border-radius: 4px;
}
.statistics-bar {
  display: flex;
  padding: 15px;
  background: #f9fafc;
  border-radius: 4px;
  margin-bottom: 15px;
}
.calendar-day-full {
  color: #67c23a;
  font-weight: bold;
}
.calendar-day-partial {
  color: #e6a23c;
}
</style>
