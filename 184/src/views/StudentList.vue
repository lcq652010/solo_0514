<template>
  <div class="page-container">
    <el-card class="card-wrapper">
      <div slot="header" class="clearfix">
        <span>学员列表</span>
        <el-button style="float: right; padding: 3px 0;" type="primary" size="small" @click="showAddDialog">
          新增学员
        </el-button>
      </div>
      
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="学员姓名">
            <el-input v-model="searchForm.name" placeholder="请输入姓名" clearable></el-input>
          </el-form-item>
          <el-form-item label="所属班级">
            <el-select v-model="searchForm.className" placeholder="请选择班级" clearable>
              <el-option label="全部班级" value=""></el-option>
              <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="学员状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
              <el-option label="全部状态" value=""></el-option>
              <el-option label="在读" value="在读"></el-option>
              <el-option label="停课" value="停课"></el-option>
              <el-option label="毕业" value="毕业"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="resetSearch">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-wrapper">
        <el-table :data="tableData" border stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
          <el-table-column prop="name" label="姓名" align="center"></el-table-column>
          <el-table-column prop="phone" label="联系电话" align="center"></el-table-column>
          <el-table-column prop="className" label="所属班级" align="center"></el-table-column>
          <el-table-column prop="totalHours" label="总课时" align="center"></el-table-column>
          <el-table-column prop="remainHours" label="剩余课时" align="center">
            <template slot-scope="scope">
              <span :style="{ color: scope.row.remainHours < 10 ? '#f56c6c' : '#67c23a' }">
                {{ scope.row.remainHours }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="enrollDate" label="入学日期" align="center"></el-table-column>
          <el-table-column prop="status" label="状态" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.status === '在读' ? 'success' : 'danger'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" width="200">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
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

    <el-dialog :title="dialogTitle" :visible.sync="dialogVisible" width="500px">
      <el-form :model="studentForm" :rules="rules" ref="studentForm" label-width="100px">
        <el-form-item label="学员姓名" prop="name">
          <el-input v-model="studentForm.name" placeholder="请输入学员姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="studentForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="所属班级" prop="className">
          <el-select v-model="studentForm.className" placeholder="请选择班级" style="width: 100%">
            <el-option v-for="cls in classOptions" :key="cls" :label="cls" :value="cls"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="总课时" prop="totalHours">
          <el-input-number v-model="studentForm.totalHours" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="剩余课时" prop="remainHours">
          <el-input-number v-model="studentForm.remainHours" :min="0" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="学员状态" prop="status">
          <el-select v-model="studentForm.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="在读" value="在读"></el-option>
            <el-option label="停课" value="停课"></el-option>
            <el-option label="毕业" value="毕业"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockStudents, classOptions } from '@/mock/data.js';

export default {
  name: 'StudentList',
  data() {
    return {
      searchForm: {
        name: '',
        className: '',
        status: ''
      },
      studentList: [...mockStudents],
      classOptions,
      dialogVisible: false,
      dialogTitle: '新增学员',
      isEdit: false,
      studentForm: {
        id: null,
        name: '',
        phone: '',
        className: '',
        totalHours: 0,
        remainHours: 0,
        status: '在读'
      },
      rules: {
        name: [
          { required: true, message: '请输入学员姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        className: [
          { required: true, message: '请选择所属班级', trigger: 'change' }
        ],
        totalHours: [
          { required: true, message: '请输入总课时', trigger: 'blur' }
        ],
        remainHours: [
          { required: true, message: '请输入剩余课时', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '请选择学员状态', trigger: 'change' }
        ]
      },
      pagination: {
        page: 1,
        size: 10,
        total: mockStudents.length
      }
    };
  },
  computed: {
    tableData() {
      let data = [...this.studentList];
      
      if (this.searchForm.name) {
        data = data.filter(item => item.name.includes(this.searchForm.name));
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
    }
  },
  methods: {
    handleSearch() {
      this.pagination.page = 1;
    },
    resetSearch() {
      this.searchForm = {
        name: '',
        className: '',
        status: ''
      };
      this.pagination.page = 1;
    },
    handleSizeChange(val) {
      this.pagination.size = val;
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
    },
    showAddDialog() {
      this.isEdit = false;
      this.dialogTitle = '新增学员';
      this.studentForm = {
        id: null,
        name: '',
        phone: '',
        className: '',
        totalHours: 0,
        remainHours: 0,
        status: '在读',
        enrollDate: new Date().toISOString().split('T')[0]
      };
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs.studentForm.clearValidate();
      });
    },
    handleEdit(row) {
      this.isEdit = true;
      this.dialogTitle = '编辑学员';
      this.studentForm = { ...row };
      this.dialogVisible = true;
      this.$nextTick(() => {
        this.$refs.studentForm.clearValidate();
      });
    },
    handleDelete(row) {
      this.$confirm('确认删除该学员信息吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.studentList.findIndex(item => item.id === row.id);
        if (index > -1) {
          this.studentList.splice(index, 1);
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
        }
      }).catch(() => {});
    },
    submitForm() {
      this.$refs.studentForm.validate((valid) => {
        if (valid) {
          if (this.isEdit) {
            const index = this.studentList.findIndex(item => item.id === this.studentForm.id);
            if (index > -1) {
              this.studentList[index] = { ...this.studentForm };
            }
            this.$message.success('编辑成功');
          } else {
            const newId = Math.max(...this.studentList.map(item => item.id)) + 1;
            this.studentForm.id = newId;
            this.studentForm.enrollDate = new Date().toISOString().split('T')[0];
            this.studentList.push({ ...this.studentForm });
            this.$message.success('新增成功');
          }
          this.dialogVisible = false;
        }
      });
    }
  }
};
</script>
