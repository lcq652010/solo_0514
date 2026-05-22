<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-s-order"></i>
      医生排班
    </h2>

    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="科室">
        <el-select v-model="searchForm.department" placeholder="请选择科室" clearable>
          <el-option label="全部科室" value=""></el-option>
          <el-option v-for="dept in departments" :key="dept.id" :label="dept.name" :value="dept.name"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="日期">
        <el-date-picker
          v-model="searchForm.date"
          type="date"
          placeholder="选择日期"
          value-format="yyyy-MM-dd"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">查询</el-button>
        <el-button @click="reset">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border stripe style="width: 100%">
      <el-table-column prop="doctorName" label="医生姓名" align="center" width="100"></el-table-column>
      <el-table-column prop="department" label="所属科室" align="center" width="100"></el-table-column>
      <el-table-column prop="date" label="排班日期" align="center" width="120"></el-table-column>
      <el-table-column prop="time" label="时段" align="center" width="80">
        <template slot-scope="scope">
          <el-tag :type="scope.row.time === '上午' ? 'success' : 'primary'" size="small">
            {{ scope.row.time }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="period" label="出诊时间" align="center" width="130"></el-table-column>
      <el-table-column prop="total" label="总号源" align="center" width="80"></el-table-column>
      <el-table-column prop="remaining" label="剩余号源" align="center" width="100">
        <template slot-scope="scope">
          <el-tag :type="scope.row.remaining > 10 ? 'success' : scope.row.remaining > 0 ? 'warning' : 'danger'" size="small">
            {{ scope.row.remaining }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="fee" label="挂号费" align="center" width="80">
        <template slot-scope="scope">
          <span style="color: #E6A23C; font-weight: 600;">¥{{ scope.row.fee }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" fixed="right" width="120">
        <template slot-scope="scope">
          <el-button
            type="primary"
            size="mini"
            @click="goRegister(scope.row)"
            :disabled="scope.row.remaining <= 0"
          >
            {{ scope.row.remaining <= 0 ? '已约满' : '挂号' }}
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
  </div>
</template>

<script>
import { departments } from '@/mock/data';
import { store } from '@/store';

export default {
  name: 'DoctorSchedule',
  data() {
    return {
      departments: departments.filter(d => d.status === 1),
      searchForm: {
        department: '',
        date: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      refreshTimer: null,
      unsubscribe: null
    };
  },
  computed: {
    scheduleList() {
      return store.getSchedules();
    },
    filteredData() {
      let data = [...this.scheduleList];
      if (this.searchForm.department) {
        data = data.filter(item => item.department === this.searchForm.department);
      }
      if (this.searchForm.date) {
        data = data.filter(item => item.date === this.searchForm.date);
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
    if (this.$route.query.department) {
      this.searchForm.department = this.$route.query.department;
    }
    this.pagination.total = this.filteredData.length;
    // 订阅数据变化
    this.unsubscribe = store.subscribe(() => {
      this.pagination.total = this.filteredData.length;
    });
    // 启动自动刷新
    this.startAutoRefresh();
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
    if (this.unsubscribe) {
      this.unsubscribe();
    }
  },
  methods: {
    startAutoRefresh() {
      // 每30秒自动刷新一次号源状态
      this.refreshTimer = setInterval(() => {
        this.$forceUpdate();
        this.$message({
          message: '号源状态已刷新',
          type: 'info',
          duration: 1000
        });
      }, 30000);
    },
    search() {
      this.pagination.currentPage = 1;
      this.pagination.total = this.filteredData.length;
    },
    reset() {
      this.searchForm = {
        department: '',
        date: ''
      };
      this.pagination.currentPage = 1;
      this.pagination.total = this.filteredData.length;
    },
    goRegister(row) {
      if (row.remaining <= 0) {
        this.$message.warning('该时段号源已满，无法挂号！');
        return;
      }
      this.$router.push({
        path: '/register',
        query: {
          department: row.department,
          doctor: row.doctorName,
          date: row.date,
          time: row.time
        }
      });
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
