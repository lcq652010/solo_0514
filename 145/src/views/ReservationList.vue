<template>
  <div class="reservation-list">
    <div class="page-title">预约记录</div>
    <div class="card-wrapper">
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="请输入学员姓名搜索"
          style="width: 200px; margin-right: 10px"
          clearable
        >
        </el-input>
        <el-select v-model="searchCoach" placeholder="选择教练" style="width: 150px; margin-right: 10px" clearable>
          <el-option label="全部教练" value=""></el-option>
          <el-option label="张教练" value="张教练"></el-option>
          <el-option label="李教练" value="李教练"></el-option>
          <el-option label="王教练" value="王教练"></el-option>
          <el-option label="赵教练" value="赵教练"></el-option>
          <el-option label="周教练" value="周教练"></el-option>
          <el-option label="郑教练" value="郑教练"></el-option>
        </el-select>
        <el-date-picker
          v-model="reserveDate"
          type="date"
          placeholder="选择预约日期"
          style="width: 180px; margin-right: 10px"
          clearable
        >
        </el-date-picker>
        <el-select v-model="searchStatus" placeholder="预约状态" style="width: 150px; margin-right: 10px" clearable>
          <el-option label="全部状态" value=""></el-option>
          <el-option label="待确认" value="待确认"></el-option>
          <el-option label="已确认" value="已确认"></el-option>
          <el-option label="已完成" value="已完成"></el-option>
          <el-option label="已取消" value="已取消"></el-option>
        </el-select>
        <el-button type="primary" @click="searchRecord">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>

      <el-table
        :data="tableData"
        border
        style="width: 100%; margin-top: 20px"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="studentName" label="学员姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column prop="coach" label="教练" width="100" align="center"></el-table-column>
        <el-table-column prop="subject" label="科目" width="80" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="mini">{{ scope.row.subject }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="reserveDate" label="预约日期" width="120" align="center"></el-table-column>
        <el-table-column prop="timeSlot" label="预约时段" width="120" align="center"></el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="danger"
              @click="cancelReservation(scope.row)"
              :disabled="scope.row.status === '已取消' || scope.row.status === '已完成'"
            >
              取消预约
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </div>
    </div>

    <div class="card-wrapper" style="margin-top: 20px">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ statData.total }}</div>
            <div class="stat-label">总预约数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #e6a23c">{{ statData.pending }}</div>
            <div class="stat-label">待确认</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #409eff">{{ statData.confirmed }}</div>
            <div class="stat-label">已确认</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #67c23a">{{ statData.completed }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReservationList',
  data() {
    return {
      searchKeyword: '',
      searchCoach: '',
      reserveDate: '',
      searchStatus: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      statData: {
        total: 0,
        pending: 0,
        confirmed: 0,
        completed: 0
      },
      baseRecords: [
        {
          id: 1,
          studentName: '张三',
          phone: '13800138101',
          coach: '张教练',
          subject: '科目二',
          reserveDate: '2024-01-15',
          timeSlot: '08:00-10:00',
          createTime: '2024-01-13 10:30:00',
          status: '已完成'
        },
        {
          id: 2,
          studentName: '李四',
          phone: '13800138102',
          coach: '李教练',
          subject: '科目三',
          reserveDate: '2024-01-16',
          timeSlot: '10:00-12:00',
          createTime: '2024-01-14 14:20:00',
          status: '已确认'
        },
        {
          id: 3,
          studentName: '王五',
          phone: '13800138103',
          coach: '王教练',
          subject: '科目二',
          reserveDate: '2024-01-17',
          timeSlot: '14:00-16:00',
          createTime: '2024-01-15 09:15:00',
          status: '待确认'
        },
        {
          id: 4,
          studentName: '赵六',
          phone: '13800138104',
          coach: '张教练',
          subject: '科目二',
          reserveDate: '2024-01-18',
          timeSlot: '16:00-18:00',
          createTime: '2024-01-16 16:45:00',
          status: '已取消'
        },
        {
          id: 5,
          studentName: '孙七',
          phone: '13800138105',
          coach: '周教练',
          subject: '科目三',
          reserveDate: '2024-01-19',
          timeSlot: '08:00-10:00',
          createTime: '2024-01-17 11:30:00',
          status: '已完成'
        },
        {
          id: 6,
          studentName: '周八',
          phone: '13800138106',
          coach: '李教练',
          subject: '科目三',
          reserveDate: '2024-01-20',
          timeSlot: '10:00-12:00',
          createTime: '2024-01-18 08:00:00',
          status: '已确认'
        },
        {
          id: 7,
          studentName: '吴九',
          phone: '13800138107',
          coach: '王教练',
          subject: '科目二',
          reserveDate: '2024-01-21',
          timeSlot: '14:00-16:00',
          createTime: '2024-01-19 15:20:00',
          status: '待确认'
        },
        {
          id: 8,
          studentName: '郑十',
          phone: '13800138108',
          coach: '郑教练',
          subject: '科目三',
          reserveDate: '2024-01-22',
          timeSlot: '18:00-20:00',
          createTime: '2024-01-20 10:10:00',
          status: '已完成'
        }
      ],
      allRecords: []
    };
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.loadAllRecords();
      vm.loadData();
      vm.calculateStats();
    });
  },
  mounted() {
    this.loadAllRecords();
    this.loadData();
    this.calculateStats();
  },
  activated() {
    this.loadAllRecords();
    this.loadData();
    this.calculateStats();
  },
  watch: {
    searchKeyword() {
      this.searchRecord();
    },
    searchCoach() {
      this.searchRecord();
    },
    reserveDate() {
      this.searchRecord();
    },
    searchStatus() {
      this.searchRecord();
    }
  },
  methods: {
    loadAllRecords() {
      const storedRecords = JSON.parse(localStorage.getItem('reservations') || '[]');
      const allIds = new Set(this.baseRecords.map(r => r.id));
      const newRecords = storedRecords.filter(r => !allIds.has(r.id));
      this.allRecords = [...newRecords, ...this.baseRecords];
    },
    tableRowClassName({ rowIndex }) {
      if (rowIndex % 2 === 1) {
        return 'bg-gray-row';
      }
      return '';
    },
    getStatusType(status) {
      const typeMap = {
        '待确认': 'warning',
        '已确认': 'primary',
        '已完成': 'success',
        '已取消': 'info'
      };
      return typeMap[status] || '';
    },
    calculateStats() {
      this.statData.total = this.allRecords.length;
      this.statData.pending = this.allRecords.filter(r => r.status === '待确认').length;
      this.statData.confirmed = this.allRecords.filter(r => r.status === '已确认').length;
      this.statData.completed = this.allRecords.filter(r => r.status === '已完成').length;
    },
    loadData() {
      let data = [...this.allRecords];
      
      if (this.searchKeyword) {
        data = data.filter(item => item.studentName && item.studentName.includes(this.searchKeyword));
      }
      
      if (this.searchCoach) {
        data = data.filter(item => item.coach === this.searchCoach);
      }
      
      if (this.reserveDate) {
        const dateStr = typeof this.reserveDate === 'string' 
          ? this.reserveDate 
          : this.reserveDate.toISOString().split('T')[0];
        data = data.filter(item => item.reserveDate === dateStr);
      }
      
      if (this.searchStatus) {
        data = data.filter(item => item.status === this.searchStatus);
      }
      
      data.sort((a, b) => b.id - a.id);
      
      this.total = data.length;
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.tableData = data.slice(start, end);
    },
    searchRecord() {
      this.currentPage = 1;
      this.loadData();
    },
    resetSearch() {
      this.searchKeyword = '';
      this.searchCoach = '';
      this.reserveDate = '';
      this.searchStatus = '';
      this.currentPage = 1;
      this.loadData();
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.loadData();
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.loadData();
    },
    cancelReservation(row) {
      this.$confirm('确定要取消此预约吗？取消后将无法恢复。', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = '已取消';
        const storedRecords = JSON.parse(localStorage.getItem('reservations') || '[]');
        const index = storedRecords.findIndex(r => r.id === row.id);
        if (index !== -1) {
          storedRecords[index].status = '已取消';
          localStorage.setItem('reservations', JSON.stringify(storedRecords));
        }
        this.$message({
          type: 'success',
          message: '预约已取消'
        });
        this.calculateStats();
      }).catch(() => {});
    }
  }
};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.bg-gray-row {
  background-color: #f5f7fa;
}

.stat-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  color: #fff;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #fff;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}
</style>
