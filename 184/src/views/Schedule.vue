<template>
  <div class="page-container">
    <el-card class="card-wrapper">
      <div slot="header" class="clearfix">
        <span>班级课程表</span>
        <el-button style="float: right; padding: 3px 0;" type="primary" size="small" @click="showAddDialog">
          新增课程
        </el-button>
      </div>
      
      <div class="view-toggle">
        <el-radio-group v-model="viewMode" size="small">
          <el-radio-button label="table">表格视图</el-radio-button>
          <el-radio-button label="calendar">日历视图</el-radio-button>
        </el-radio-group>
      </div>

      <div class="filter-bar">
        <el-form :inline="true" :model="filterForm">
          <el-form-item label="选择班级">
            <el-select v-model="filterForm.className" placeholder="全部班级" clearable style="width: 150px;">
              <el-option label="全部班级" value=""></el-option>
              <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="授课老师">
            <el-select v-model="filterForm.teacher" placeholder="全部老师" clearable style="width: 120px;">
              <el-option label="全部老师" value=""></el-option>
              <el-option v-for="teacher in teacherOptions" :key="teacher" :label="teacher" :value="teacher"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="viewMode === 'table'" class="table-wrapper">
        <el-table :data="tableData" border stripe style="width: 100%">
          <el-table-column prop="className" label="班级名称" align="center" width="130"></el-table-column>
          <el-table-column prop="weekDay" label="星期" align="center" width="80"></el-table-column>
          <el-table-column prop="time" label="上课时间" align="center" width="130"></el-table-column>
          <el-table-column prop="courseName" label="课程名称" align="center"></el-table-column>
          <el-table-column prop="teacher" label="授课老师" align="center" width="100"></el-table-column>
          <el-table-column prop="classroom" label="教室" align="center" width="100"></el-table-column>
          <el-table-column label="操作" align="center" width="150">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div v-if="viewMode === 'calendar'" class="calendar-view">
        <el-row :gutter="10">
          <el-col :span="24">
            <div class="calendar-header">
              <div v-for="day in weekDays" :key="day" class="day-header">{{ day }}</div>
            </div>
            <div class="calendar-body">
              <div v-for="day in weekDays" :key="day" class="day-column">
                <div 
                  v-for="course in getCoursesByDay(day)" 
                  :key="course.id" 
                  class="course-card"
                  :class="getClassColor(course.className)"
                  @click="showCourseDetail(course)">
                  <div class="course-time">{{ course.time }}</div>
                  <div class="course-name">{{ course.courseName }}</div>
                  <div class="course-class">{{ course.className }}</div>
                  <div class="course-teacher">{{ course.teacher }}</div>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="courseForm" :rules="rules" ref="courseForm" label-width="100px">
        <el-form-item label="班级名称" prop="className">
          <el-select v-model="courseForm.className" placeholder="请选择班级" style="width: 100%;">
            <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="星期" prop="weekDay">
          <el-select v-model="courseForm.weekDay" placeholder="请选择星期" style="width: 100%;">
            <el-option v-for="day in weekDays" :key="day" :label="day" :value="day"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="上课时间" prop="time">
          <el-time-picker
            is-range
            v-model="courseForm.timeRange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="HH:mm"
            value-format="HH:mm"
            style="width: 100%;">
          </el-time-picker>
        </el-form-item>
        <el-form-item label="课程名称" prop="courseName">
          <el-input v-model="courseForm.courseName" placeholder="请输入课程名称"></el-input>
        </el-form-item>
        <el-form-item label="授课老师" prop="teacher">
          <el-input v-model="courseForm.teacher" placeholder="请输入授课老师姓名"></el-input>
        </el-form-item>
        <el-form-item label="教室" prop="classroom">
          <el-input v-model="courseForm.classroom" placeholder="请输入教室"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="课程详情" :visible.sync="detailDialogVisible" width="400px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="班级名称">{{ detailCourse.className }}</el-descriptions-item>
        <el-descriptions-item label="星期">{{ detailCourse.weekDay }}</el-descriptions-item>
        <el-descriptions-item label="上课时间">{{ detailCourse.time }}</el-descriptions-item>
        <el-descriptions-item label="课程名称">{{ detailCourse.courseName }}</el-descriptions-item>
        <el-descriptions-item label="授课老师">{{ detailCourse.teacher }}</el-descriptions-item>
        <el-descriptions-item label="教室">{{ detailCourse.classroom }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockSchedule, classOptions, weekDays } from '@/mock/data.js';

export default {
  name: 'Schedule',
  data() {
    return {
      viewMode: 'table',
      filterForm: {
        className: '',
        teacher: ''
      },
      scheduleList: [...mockSchedule],
      classOptions,
      weekDays,
      dialogVisible: false,
      detailDialogVisible: false,
      dialogTitle: '新增课程',
      isEdit: false,
      courseForm: {
        id: null,
        className: '',
        weekDay: '',
        timeRange: [],
        time: '',
        courseName: '',
        teacher: '',
        classroom: ''
      },
      detailCourse: {},
      rules: {
        className: [
          { required: true, message: '请选择班级', trigger: 'change' }
        ],
        weekDay: [
          { required: true, message: '请选择星期', trigger: 'change' }
        ],
        timeRange: [
          { required: true, message: '请选择上课时间', trigger: 'change' }
        ],
        courseName: [
          { required: true, message: '请输入课程名称', trigger: 'blur' }
        ],
        teacher: [
          { required: true, message: '请输入授课老师姓名', trigger: 'blur' }
        ],
        classroom: [
          { required: true, message: '请输入教室', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    teacherOptions() {
      return [...new Set(this.scheduleList.map(item => item.teacher))];
    },
    tableData() {
      let data = [...this.scheduleList];
      
      if (this.filterForm.className) {
        data = data.filter(item => item.className === this.filterForm.className);
      }
      if (this.filterForm.teacher) {
        data = data.filter(item => item.teacher === this.filterForm.teacher);
      }
      
      const weekOrder = { '周一': 1, '周二': 2, '周三': 3, '周四': 4, '周五': 5, '周六': 6, '周日': 7 };
      data.sort((a, b) => weekOrder[a.weekDay] - weekOrder[b.weekDay]);
      
      return data;
    }
  },
  methods: {
    getCoursesByDay(day) {
      let data = this.scheduleList.filter(item => item.weekDay === day);
      if (this.filterForm.className) {
        data = data.filter(item => item.className === this.filterForm.className);
      }
      if (this.filterForm.teacher) {
        data = data.filter(item => item.teacher === this.filterForm.teacher);
      }
      return data;
    },
    getClassColor(className) {
      const colorMap = {
        'Python入门班': 'color-python',
        'Java进阶班': 'color-java',
        'Web前端班': 'color-web',
        'UI设计班': 'color-ui'
      };
      return colorMap[className] || 'color-default';
    },
    showAddDialog() {
      this.isEdit = false;
      this.dialogTitle = '新增课程';
      this.courseForm = {
        id: null,
        className: '',
        weekDay: '',
        timeRange: [],
        time: '',
        courseName: '',
        teacher: '',
        classroom: ''
      };
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs.courseForm.clearValidate();
      });
    },
    handleEdit(row) {
      this.isEdit = true;
      this.dialogTitle = '编辑课程';
      const times = row.time.split('-');
      this.courseForm = {
        ...row,
        timeRange: times
      };
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs.courseForm.clearValidate();
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除该课程吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.scheduleList.findIndex(item => item.id === row.id);
        if (index > -1) {
          this.scheduleList.splice(index, 1);
          this.$message.success('删除成功');
        }
      }).catch(() => {});
    },
    showCourseDetail(course) {
      this.detailCourse = { ...course };
      this.detailDialogVisible = true;
    },
    submitForm() {
      this.$refs.courseForm.validate((valid) => {
        if (valid) {
          this.courseForm.time = this.courseForm.timeRange.join('-');
          if (this.isEdit) {
            const index = this.scheduleList.findIndex(item => item.id === this.courseForm.id);
            if (index > -1) {
              this.scheduleList[index] = { ...this.courseForm };
            }
            this.$message.success('编辑成功');
          } else {
            const newId = Math.max(...this.scheduleList.map(item => item.id)) + 1;
            this.courseForm.id = newId;
            this.scheduleList.push({ ...this.courseForm });
            this.$message.success('新增成功');
          }
          this.dialogVisible = false;
        }
      });
    }
  }
};
</script>

<style scoped>
.view-toggle {
  margin-bottom: 15px;
}
.filter-bar {
  margin-bottom: 20px;
}
.calendar-view {
  margin-top: 20px;
}
.calendar-header {
  display: flex;
  border-bottom: 2px solid #ebeef5;
}
.day-header {
  flex: 1;
  text-align: center;
  padding: 15px 0;
  font-weight: bold;
  font-size: 16px;
  color: #303133;
  background: #f5f7fa;
}
.calendar-body {
  display: flex;
  min-height: 500px;
}
.day-column {
  flex: 1;
  border-right: 1px solid #ebeef5;
  padding: 10px;
  min-height: 500px;
}
.day-column:last-child {
  border-right: none;
}
.course-card {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  color: #fff;
  font-size: 12px;
  cursor: pointer;
  transition: transform 0.2s;
}
.course-card:hover {
  transform: scale(1.02);
}
.course-time {
  font-weight: bold;
  margin-bottom: 5px;
}
.course-name {
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 3px;
}
.course-class {
  margin-bottom: 2px;
}
.color-python {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.color-java {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}
.color-web {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}
.color-ui {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}
.color-default {
  background: #909399;
}
</style>
