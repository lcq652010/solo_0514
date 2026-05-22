<template>
  <div class="page-card">
    <div class="page-title">包裹查询</div>
    
    <el-form :model="searchForm" class="search-form">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="快递单号">
            <el-input v-model="searchForm.orderNo" placeholder="请输入快递单号" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-form-item label="状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 100%">
              <el-option label="全部" value=""></el-option>
              <el-option label="待揽收" value="pending"></el-option>
              <el-option label="揽收中" value="picking"></el-option>
              <el-option label="派送中" value="delivering"></el-option>
              <el-option label="已签收" value="signed"></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="下单日期">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              style="width: 100%">
            </el-date-picker>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item>
            <el-button type="primary" @click="search" icon="el-icon-search">查询</el-button>
            <el-button @click="resetSearch" icon="el-icon-refresh">重置</el-button>
            <el-button @click="exportData" icon="el-icon-download" type="success">导出</el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="6">
          <el-form-item label="寄件人">
            <el-input v-model="searchForm.senderName" placeholder="请输入寄件人" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="收件人">
            <el-input v-model="searchForm.receiverName" placeholder="请输入收件人" clearable></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="统计信息">
            <span style="color: #606266;">
              共 <b style="color: #409EFF">{{ pagination.total }}</b> 条记录，
              当前显示第 <b style="color: #67C23A">{{ (pagination.page - 1) * pagination.size + 1 }}</b> - 
              <b style="color: #67C23A">{{ Math.min(pagination.page * pagination.size, pagination.total) }}</b> 条
            </span>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading" @sort-change="handleSortChange" :default-sort="{prop: 'createTime', order: 'descending'}">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="orderNo" label="快递单号" width="180" sortable="custom"></el-table-column>
      <el-table-column prop="senderName" label="寄件人" width="100"></el-table-column>
      <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
      <el-table-column prop="packageName" label="包裹名称" width="120"></el-table-column>
      <el-table-column prop="weight" label="重量(kg)" width="100" sortable="custom"></el-table-column>
      <el-table-column prop="createTime" label="下单时间" width="160" sortable="custom"></el-table-column>
      <el-table-column label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type" size="small">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template slot-scope="scope">
          <el-button size="small" @click="handleDetail(scope.row)" icon="el-icon-view">详情</el-button>
          <el-button size="small" type="text" @click="goTracking(scope.row)">跟踪</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="pagination"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="pagination.page"
      :page-sizes="[5, 10, 20, 50, 100]"
      :page-size.sync="pagination.size"
      layout="total, sizes, prev, pager, next, jumper, slot"
      :total="pagination.total"
      background
    >
      <span class="pagination-info" style="margin-left: 15px;">
        跳至 <el-input v-model.number="jumpPage" size="mini" @keyup.enter="jumpToPage" style="width: 50px; margin: 0 5px;"></el-input> 页
      </span>
    </el-pagination>

    <el-dialog title="包裹详情" :visible.sync="detailVisible" width="700px">
      <el-descriptions :column="2" border v-if="currentDetail">
        <el-descriptions-item label="订单号">{{ currentDetail.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentDetail.createTime }}</el-descriptions-item>
        <el-descriptions-item label="包裹名称">{{ currentDetail.packageName }}</el-descriptions-item>
        <el-descriptions-item label="包裹重量">{{ currentDetail.weight }}kg</el-descriptions-item>
        <el-descriptions-item label="寄件人">{{ currentDetail.senderName }}</el-descriptions-item>
        <el-descriptions-item label="寄件电话">{{ currentDetail.senderPhone }}</el-descriptions-item>
        <el-descriptions-item label="寄件地址" :span="2">{{ currentDetail.senderAddress }}</el-descriptions-item>
        <el-descriptions-item label="收件人">{{ currentDetail.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="收件电话">{{ currentDetail.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="收件地址" :span="2">{{ currentDetail.receiverAddress }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockPackages, statusMap } from '@/mock/data.js';
import { EventBus } from '@/utils/eventBus.js';

export default {
  name: 'PackageQuery',
  data() {
    return {
      loading: false,
      searchForm: {
        orderNo: '',
        senderName: '',
        receiverName: '',
        status: '',
        dateRange: []
      },
      tableData: [],
      allData: [],
      statusMap: statusMap,
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      jumpPage: 1,
      sort: {
        prop: 'createTime',
        order: 'descending'
      },
      detailVisible: false,
      currentDetail: null
    };
  },
  created() {
    this.loadData();
    EventBus.$on('packageStatusUpdated', () => {
      this.loadData();
    });
  },
  beforeDestroy() {
    EventBus.$off('packageStatusUpdated');
  },
  methods: {
    loadData() {
      this.loading = true;
      setTimeout(() => {
        let data = [...mockPackages];
        
        if (this.searchForm.orderNo) {
          data = data.filter(item => item.orderNo.toLowerCase().includes(this.searchForm.orderNo.toLowerCase()));
        }
        if (this.searchForm.senderName) {
          data = data.filter(item => item.senderName.includes(this.searchForm.senderName));
        }
        if (this.searchForm.receiverName) {
          data = data.filter(item => item.receiverName.includes(this.searchForm.receiverName));
        }
        if (this.searchForm.status) {
          data = data.filter(item => item.status === this.searchForm.status);
        }
        if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
          const startDate = new Date(this.searchForm.dateRange[0]);
          startDate.setHours(0, 0, 0, 0);
          const endDate = new Date(this.searchForm.dateRange[1]);
          endDate.setHours(23, 59, 59, 999);
          data = data.filter(item => {
            const itemDate = new Date(item.createTime);
            return itemDate >= startDate && itemDate <= endDate;
          });
        }
        
        if (this.sort.prop && this.sort.order) {
          data.sort((a, b) => {
            let valA = a[this.sort.prop];
            let valB = b[this.sort.prop];
            
            if (this.sort.prop === 'weight') {
              valA = Number(valA);
              valB = Number(valB);
            } else if (this.sort.prop === 'createTime') {
              valA = new Date(valA).getTime();
              valB = new Date(valB).getTime();
            }
            
            if (valA < valB) return this.sort.order === 'ascending' ? -1 : 1;
            if (valA > valB) return this.sort.order === 'ascending' ? 1 : -1;
            return 0;
          });
        }
        
        this.allData = data;
        this.pagination.total = data.length;
        this.updateTableData();
        this.loading = false;
      }, 300);
    },
    updateTableData() {
      const start = (this.pagination.page - 1) * this.pagination.size;
      const end = start + this.pagination.size;
      this.tableData = this.allData.slice(start, end);
    },
    search() {
      this.pagination.page = 1;
      this.loadData();
    },
    resetSearch() {
      this.searchForm = {
        orderNo: '',
        senderName: '',
        receiverName: '',
        status: '',
        dateRange: []
      };
      this.sort = {
        prop: 'createTime',
        order: 'descending'
      };
      this.pagination.page = 1;
      this.loadData();
    },
    handleSortChange(sortInfo) {
      this.sort = sortInfo;
      this.loadData();
    },
    handleSizeChange(size) {
      this.pagination.size = size;
      this.pagination.page = 1;
      this.updateTableData();
    },
    handleCurrentChange(page) {
      this.pagination.page = page;
      this.updateTableData();
    },
    jumpToPage() {
      const maxPage = Math.ceil(this.pagination.total / this.pagination.size);
      if (this.jumpPage < 1) {
        this.jumpPage = 1;
      } else if (this.jumpPage > maxPage) {
        this.jumpPage = maxPage;
      }
      this.pagination.page = this.jumpPage;
      this.updateTableData();
    },
    handleDetail(row) {
      this.currentDetail = row;
      this.detailVisible = true;
    },
    goTracking(row) {
      this.$router.push({
        path: '/tracking',
        query: { orderNo: row.orderNo }
      });
    },
    exportData() {
      if (this.allData.length === 0) {
        this.$message.warning('没有数据可导出');
        return;
      }
      
      const headers = ['快递单号', '寄件人', '收件人', '包裹名称', '重量(kg)', '状态', '下单时间'];
      const rows = this.allData.map(item => [
        item.orderNo,
        item.senderName,
        item.receiverName,
        item.packageName,
        item.weight,
        this.statusMap[item.status].label,
        item.createTime
      ]);
      
      const csvContent = [headers, ...rows].map(row => row.join(',')).join('\n');
      const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `包裹列表_${new Date().toISOString().slice(0, 10)}.csv`;
      link.click();
      
      this.$message.success('导出成功！');
    }
  }
};
</script>

<style scoped>
.search-form {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  text-align: right;
}
</style>
