<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-document"></i>
      挂号记录
    </h2>

    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="患者姓名">
        <el-input v-model="searchForm.patientName" placeholder="请输入姓名" clearable style="width: 120px;"></el-input>
      </el-form-item>
      <el-form-item label="就诊科室">
        <el-select v-model="searchForm.department" placeholder="请选择科室" clearable style="width: 120px;" @change="onDepartmentChange">
          <el-option label="全部科室" value=""></el-option>
          <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.name"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="就诊医生">
        <el-select v-model="searchForm.doctor" placeholder="请选择医生" clearable style="width: 120px;">
          <el-option label="全部医生" value=""></el-option>
          <el-option v-for="doc in filteredDoctors" :key="doc" :label="doc" :value="doc"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="就诊日期">
        <el-date-picker
          v-model="searchForm.date"
          type="date"
          placeholder="选择日期"
          style="width: 140px;"
          value-format="yyyy-MM-dd"
          clearable
        ></el-date-picker>
      </el-form-item>
      <el-form-item label="状态">
        <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px;">
          <el-option label="全部状态" value=""></el-option>
          <el-option v-for="(item, key) in statusMap" :key="key" :label="item.label" :value="Number(key)"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">查询</el-button>
        <el-button @click="reset">重置</el-button>
        <el-button type="success" @click="refreshData">刷新</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column type="index" label="序号" align="center" width="60"></el-table-column>
      <el-table-column prop="patientName" label="患者姓名" align="center" width="100"></el-table-column>
      <el-table-column prop="department" label="就诊科室" align="center" width="100"></el-table-column>
      <el-table-column prop="doctor" label="就诊医生" align="center" width="100"></el-table-column>
      <el-table-column prop="date" label="就诊日期" align="center" width="120"></el-table-column>
      <el-table-column prop="time" label="就诊时段" align="center" width="80">
        <template slot-scope="scope">
          <el-tag :type="scope.row.time === '上午' ? 'success' : 'primary'" size="small">
            {{ scope.row.time }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="number" label="排队号" align="center" width="80"></el-table-column>
      <el-table-column prop="status" label="状态" align="center" width="100">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type" size="small">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="挂号时间" align="center" width="160"></el-table-column>
      <el-table-column label="操作" align="center" fixed="right" width="180">
        <template slot-scope="scope">
          <el-button
            type="success"
            size="mini"
            @click="viewDetail(scope.row)"
          >
            详情
          </el-button>
          <el-button
            type="danger"
            size="mini"
            @click="cancelRegister(scope.row)"
            :disabled="scope.row.status !== 0"
          >
            取消挂号
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pagination.currentPage"
      :page-sizes="[10, 20, 50]"
      :page-size="pagination.pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="pagination.total"
    >
    </el-pagination>

    <el-dialog title="挂号详情" :visible.sync="dialogVisible" width="500px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="患者姓名">{{ currentRecord.patientName }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentRecord.idCard }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentRecord.phone }}</el-descriptions-item>
        <el-descriptions-item label="就诊科室">{{ currentRecord.department }}</el-descriptions-item>
        <el-descriptions-item label="就诊医生">{{ currentRecord.doctor }}</el-descriptions-item>
        <el-descriptions-item label="就诊日期">{{ currentRecord.date }}</el-descriptions-item>
        <el-descriptions-item label="就诊时段">{{ currentRecord.time }}</el-descriptions-item>
        <el-descriptions-item label="排队号">{{ currentRecord.number }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusMap[currentRecord.status].type" size="small">
            {{ statusMap[currentRecord.status].label }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="挂号时间">{{ currentRecord.createTime }}</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { departments, doctors, statusMap } from '@/mock/data';
import { store } from '@/store';

export default {
  name: 'RegistrationRecord',
  data() {
    return {
      departments: departments,
      doctors: doctors,
      statusMap: statusMap,
      recordList: [],
      searchForm: {
        patientName: '',
        department: '',
        doctor: '',
        date: '',
        status: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      currentRecord: null,
      unsubscribe: null
    };
  },
  computed: {
    filteredDoctors() {
      if (!this.searchForm.department) {
        return [...new Set(this.recordList.map(item => item.doctor))];
      }
      return this.doctors
        .filter(doc => doc.department === this.searchForm.department)
        .map(doc => doc.name);
    },
    filteredData() {
      let data = [...this.recordList];
      if (this.searchForm.patientName) {
        data = data.filter(item => item.patientName.includes(this.searchForm.patientName));
      }
      if (this.searchForm.department) {
        data = data.filter(item => item.department === this.searchForm.department);
      }
      if (this.searchForm.doctor) {
        data = data.filter(item => item.doctor === this.searchForm.doctor);
      }
      if (this.searchForm.date) {
        data = data.filter(item => item.date === this.searchForm.date);
      }
      if (this.searchForm.status !== '') {
        data = data.filter(item => item.status === this.searchForm.status);
      }
      return data;
    },
    tableData() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize;
      const end = start + this.pagination.pageSize;
      return this.filteredData.slice(start, end);
    }
  },
  mounted() {
    this.loadData();
    // 订阅数据变化
    this.unsubscribe = store.subscribe(() => {
      this.loadData();
    });
  },
  beforeDestroy() {
    if (this.unsubscribe) {
      this.unsubscribe();
    }
  },
  methods: {
    loadData() {
      this.recordList = store.getRegistrations();
      this.pagination.total = this.filteredData.length;
    },
    refreshData() {
      this.loadData();
      this.$message.success('数据已刷新！');
    },
    onDepartmentChange() {
      this.searchForm.doctor = '';
    },
    search() {
      this.pagination.currentPage = 1;
      this.pagination.total = this.filteredData.length;
    },
    reset() {
      this.searchForm = {
        patientName: '',
        department: '',
        doctor: '',
        date: '',
        status: ''
      };
      this.pagination.currentPage = 1;
      this.pagination.total = this.filteredData.length;
    },
    viewDetail(row) {
      this.currentRecord = row;
      this.dialogVisible = true;
    },
    cancelRegister(row) {
      this.$confirm('确定要取消该挂号记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = 3;
        // 取消挂号时回加号源
        store.updateScheduleRemaining(row.doctor, row.date, row.time, 1);
        store.notify();
        this.$message.success('取消挂号成功！');
      }).catch(() => {});
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val;
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val;
    }
  }
};
</script>

<style scoped>
.search-form {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 10px;
}
</style>
