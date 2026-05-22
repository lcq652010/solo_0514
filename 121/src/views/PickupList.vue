<template>
  <div class="page-card">
    <div class="page-title">揽收任务列表</div>
    
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="订单号">
        <el-input v-model="searchForm.orderNo" placeholder="请输入订单号" clearable></el-input>
      </el-form-item>
      <el-form-item label="寄件人">
        <el-input v-model="searchForm.senderName" placeholder="请输入寄件人" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">查询</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
      <el-table-column prop="orderNo" label="订单号" width="180"></el-table-column>
      <el-table-column prop="senderName" label="寄件人" width="100"></el-table-column>
      <el-table-column prop="senderPhone" label="联系电话" width="130"></el-table-column>
      <el-table-column prop="senderAddress" label="寄件地址" show-overflow-tooltip></el-table-column>
      <el-table-column prop="packageName" label="包裹名称" width="120"></el-table-column>
      <el-table-column prop="weight" label="重量(kg)" width="100"></el-table-column>
      <el-table-column prop="createTime" label="下单时间" width="160"></el-table-column>
      <el-table-column label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type" size="small">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.status === 'pending'"
            type="primary"
            size="small"
            @click="handlePickup(scope.row)"
          >
            揽收
          </el-button>
          <el-button size="small" @click="handleDetail(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="pagination"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pagination.page"
      :page-sizes="[10, 20, 50, 100]"
      :page-size="pagination.size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="pagination.total"
    ></el-pagination>
  </div>
</template>

<script>
import { mockPackages, statusMap, mockTracking } from '@/mock/data.js';
import { EventBus } from '@/utils/eventBus.js';

export default {
  name: 'PickupList',
  data() {
    return {
      loading: false,
      searchForm: {
        orderNo: '',
        senderName: ''
      },
      tableData: [],
      statusMap: statusMap,
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      pickingIds: new Set()
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
        let data = [...mockPackages].filter(item => 
          item.status === 'pending' || item.status === 'picking'
        );
        
        if (this.searchForm.orderNo) {
          data = data.filter(item => item.orderNo.includes(this.searchForm.orderNo));
        }
        if (this.searchForm.senderName) {
          data = data.filter(item => item.senderName.includes(this.searchForm.senderName));
        }
        
        this.pagination.total = data.length;
        const start = (this.pagination.page - 1) * this.pagination.size;
        const end = start + this.pagination.size;
        this.tableData = data.slice(start, end);
        this.loading = false;
      }, 500);
    },
    search() {
      this.pagination.page = 1;
      this.loadData();
    },
    resetSearch() {
      this.searchForm = {
        orderNo: '',
        senderName: ''
      };
      this.search();
    },
    handlePickup(row) {
      if (row.status !== 'pending') {
        this.$message.warning('该订单状态不支持揽收');
        return;
      }
      if (this.pickingIds.has(row.id)) {
        this.$message.warning('该订单正在揽收中，请稍候');
        return;
      }
      
      this.$confirm(`确认揽收订单 ${row.orderNo}？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const item = mockPackages.find(p => p.id === row.id);
        if (!item) {
          this.$message.error('未找到该订单信息');
          return;
        }
        
        if (item.status !== 'pending') {
          this.$message.warning('该订单状态已变更，请刷新后重试');
          this.loadData();
          return;
        }
        
        this.pickingIds.add(item.id);
        
        item.status = 'picking';
        
        const tracking = mockTracking.find(t => t.orderNo === item.orderNo);
        if (tracking) {
          tracking.tracks.unshift({
            time: this.formatDate(new Date()),
            status: '揽收中',
            location: item.senderAddress,
            operator: '快递员',
            remark: '快递员正在前往揽收'
          });
        }
        
        EventBus.$emit('packageStatusUpdated', {
          orderNo: item.orderNo,
          status: 'picking'
        });
        
        this.$message.success('揽收成功！');
        this.loadData();
        setTimeout(() => {
          this.pickingIds.delete(item.id);
        }, 1000);
      }).catch(() => {});
    },
    formatDate(date) {
      const d = new Date(date);
      const pad = n => n.toString().padStart(2, '0');
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    },
    handleDetail(row) {
      this.$alert(`
        订单号：${row.orderNo}\n
        寄件人：${row.senderName}\n
        联系电话：${row.senderPhone}\n
        寄件地址：${row.senderAddress}\n
        收件人：${row.receiverName}\n
        联系电话：${row.receiverPhone}\n
        收件地址：${row.receiverAddress}\n
        包裹名称：${row.packageName}\n
        包裹重量：${row.weight}kg
      `, '订单详情');
    },
    handleSizeChange(size) {
      this.pagination.size = size;
      this.loadData();
    },
    handleCurrentChange(page) {
      this.pagination.page = page;
      this.loadData();
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
</style>
