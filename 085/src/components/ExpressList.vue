<template>
  <div class="page-card">
    <h2 class="page-title">
      <i class="el-icon-search"></i>
      快递查询
    </h2>

    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="取件码">
        <el-input
          v-model="searchForm.pickupCode"
          placeholder="请输入取件码"
          clearable
          style="width: 120px"
        ></el-input>
      </el-form-item>
      <el-form-item label="快递单号">
        <el-input
          v-model="searchForm.expressNo"
          placeholder="请输入快递单号"
          clearable
          style="width: 180px"
        ></el-input>
      </el-form-item>
      <el-form-item label="收件人">
        <el-input
          v-model="searchForm.receiverName"
          placeholder="请输入收件人姓名"
          clearable
          style="width: 120px"
        ></el-input>
      </el-form-item>
      <el-form-item label="手机号">
        <el-input
          v-model="searchForm.receiverPhone"
          placeholder="请输入手机号"
          clearable
          style="width: 130px"
        ></el-input>
      </el-form-item>
      <el-form-item label="状态">
        <el-select
          v-model="searchForm.status"
          placeholder="请选择状态"
          clearable
          style="width: 120px"
        >
          <el-option label="全部" value=""></el-option>
          <el-option label="未签收" value="待取件"></el-option>
          <el-option label="已签收" value="已签收"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="入库时间">
        <el-date-picker
          v-model="searchForm.dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          style="width: 240px"
          format="yyyy-MM-dd"
          value-format="yyyy-MM-dd"
        ></el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchExpress">
          <i class="el-icon-search"></i>
          查询
        </el-button>
        <el-button @click="resetSearch">
          <i class="el-icon-refresh"></i>
          重置
        </el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-label">快递总数</div>
            <div class="stat-value">{{ stats.total }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-label">未签收</div>
            <div class="stat-value" style="color: #e6a23c">{{ stats.pending }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-label">已签收</div>
            <div class="stat-value" style="color: #67c23a">{{ stats.signed }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-label">今日新增</div>
            <div class="stat-value" style="color: #409eff">{{ stats.today }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div class="table-section">
      <el-table
        :data="tableData"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="expressNo" label="快递单号" width="180" show-overflow-tooltip></el-table-column>
        <el-table-column prop="company" label="快递公司" width="120"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
        <el-table-column prop="receiverPhone" label="联系电话" width="130"></el-table-column>
        <el-table-column prop="pickupCode" label="取件码" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="small">{{ scope.row.pickupCode }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="weight" label="重量(kg)" width="100" align="center"></el-table-column>
        <el-table-column prop="type" label="类型" width="100"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '待取件' ? 'warning' : 'success'" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="inboundTime" label="入库时间" width="180"></el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="small"
              icon="el-icon-view"
              @click="viewDetail(scope.row)"
            >查看</el-button>
            <el-button
              v-if="scope.row.status === '待取件'"
              type="success"
              size="small"
              icon="el-icon-check"
              @click="quickSign(scope.row)"
            >签收</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-pagination
      v-if="total > 0"
      class="pagination"
      background
      :current-page="pageInfo.page"
      :page-size="pageInfo.pageSize"
      :page-sizes="[10, 20, 50, 100]"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handlePageChange"
    ></el-pagination>

    <el-dialog
      title="快递详情" :width="600px"
      v-model="detailVisible"
      :before-close="closeDetail"
    >
      <el-descriptions :column="2" border v-if="currentExpress">
        <el-descriptions-item label="快递单号">{{ currentExpress.expressNo }}</el-descriptions-item>
        <el-descriptions-item label="快递公司">{{ currentExpress.company }}</el-descriptions-item>
        <el-descriptions-item label="收件人">{{ currentExpress.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentExpress.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="收件地址" :span="2">{{ currentExpress.receiverAddress }}</el-descriptions-item>
        <el-descriptions-item label="取件码">
          <el-tag type="success" size="medium">{{ currentExpress.pickupCode }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="快递重量">{{ currentExpress.weight }} kg</el-descriptions-item>
        <el-descriptions-item label="快递类型">{{ currentExpress.type }}</el-descriptions-item>
        <el-descriptions-item label="当前状态">
          <el-tag :type="currentExpress.status === '待取件' ? 'warning' : 'success'" size="medium">
            {{ currentExpress.status }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="入库时间">{{ currentExpress.inboundTime }}</el-descriptions-item>
        <el-descriptions-item v-if="currentExpress.status === '已签收'" label="签收人">
          {{ currentExpress.signerName }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentExpress.status === '已签收'" label="签收时间">
          {{ currentExpress.signTime }}
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentExpress.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'ExpressList',
  data() {
    return {
      loading: false,
      searchForm: {
        pickupCode: '',
        expressNo: '',
        receiverName: '',
        receiverPhone: '',
        status: '',
        dateRange: []
      },
      pageInfo: {
        page: 1,
        pageSize: 10
      },
      total: 0,
      tableData: [],
      allData: [],
      stats: {
        total: 0,
        pending: 0,
        signed: 0,
        today: 0
      },
      detailVisible: false,
      currentExpress: null
    };
  },
  methods: {
    loadData() {
      this.allData = JSON.parse(localStorage.getItem('expressList') || '[]');
      this.calculateStats();
      this.searchExpress();
    },
    calculateStats() {
      const today = moment().format('YYYY-MM-DD');
      this.stats.total = this.allData.length;
      this.stats.pending = this.allData.filter(item => item.status === '待取件').length;
      this.stats.signed = this.allData.filter(item => item.status === '已签收').length;
      this.stats.today = this.allData.filter(item => {
        return item.inboundTime && item.inboundTime.startsWith(today);
      }).length;
    },
    searchExpress() {
      this.loading = true;
      setTimeout(() => {
        let filtered = [...this.allData];
        const keyword = (str) => (str || '').toString().toUpperCase().trim();

        if (this.searchForm.pickupCode) {
          const searchCode = keyword(this.searchForm.pickupCode);
          filtered = filtered.filter(item => 
            keyword(item.pickupCode).includes(searchCode)
          );
        }
        if (this.searchForm.expressNo) {
          const searchNo = keyword(this.searchForm.expressNo);
          filtered = filtered.filter(item => 
            keyword(item.expressNo).includes(searchNo)
          );
        }
        if (this.searchForm.receiverName) {
          const searchName = keyword(this.searchForm.receiverName);
          filtered = filtered.filter(item => 
            keyword(item.receiverName).includes(searchName)
          );
        }
        if (this.searchForm.receiverPhone) {
          const searchPhone = keyword(this.searchForm.receiverPhone);
          filtered = filtered.filter(item => 
            keyword(item.receiverPhone).includes(searchPhone)
          );
        }
        if (this.searchForm.status) {
          filtered = filtered.filter(item => 
            item.status === this.searchForm.status);
        }
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          const [startDate, endDate] = this.searchForm.dateRange;
          filtered = filtered.filter(item => {
            const inboundDate = item.inboundTime.split(' ')[0];
            return inboundDate >= startDate && inboundDate <= endDate;
          });
        }

        this.total = filtered.length;
        const start = (this.pageInfo.page - 1) * this.pageInfo.pageSize;
        const end = start + this.pageInfo.pageSize;
        this.tableData = filtered.slice(start, end);
        this.loading = false;
      }, 300);
    },
    resetSearch() {
      this.searchForm = {
        pickupCode: '',
        expressNo: '',
        receiverName: '',
        receiverPhone: '',
        status: '',
        dateRange: []
      };
      this.pageInfo.page = 1;
      this.searchExpress();
    },
    handleSizeChange(val) {
      this.pageInfo.pageSize = val;
      this.pageInfo.page = 1;
      this.searchExpress();
    },
    handlePageChange(val) {
      this.pageInfo.page = val;
      this.searchExpress();
    },
    viewDetail(row) {
      this.currentExpress = row;
      this.detailVisible = true;
    },
    closeDetail() {
      this.detailVisible = false;
    },
    quickSign(row) {
      this.$prompt('请输入签收人姓名', '快速签收', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /\S+/,
        inputErrorMessage: '签收人姓名不能为空'
      }).then(({ value }) => {
        const list = JSON.parse(localStorage.getItem('expressList') || '[]');
        const index = list.findIndex(item => item.id === row.id);
        if (index !== -1) {
          list[index].status = '已签收';
          list[index].signerName = value;
          list[index].signTime = moment().format('YYYY-MM-DD HH:mm:ss');
          localStorage.setItem('expressList', JSON.stringify(list));
          
          this.$message.success('签收成功');
          this.loadData();
        }
      }).catch(() => {});
    }
  },
  mounted() {
    this.loadData();
  }
};
</script>

<style scoped>
.search-form {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  text-align: center;
}

.stat-item {
  padding: 10px 0;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.table-section {
  margin-bottom: 20px;
}

.pagination {
  text-align: right;
}

.el-icon-check {
  color: #67c23a;
}
</style>
