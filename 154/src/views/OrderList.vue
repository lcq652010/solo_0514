<template>
  <div class="order-list-page">
    <div class="page-header">
      <h1 class="page-title">订单列表</h1>
      <p class="page-subtitle">查看和管理所有门票订单</p>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="门票类型">
          <el-select v-model="filters.ticketName" placeholder="全部" clearable style="width: 140px">
            <el-option
              v-for="ticket in ticketTypes"
              :key="ticket.id"
              :label="ticket.name"
              :value="ticket.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="filters.status" placeholder="全部" clearable style="width: 120px">
            <el-option label="待支付" value="pending" />
            <el-option label="已支付" value="paid" />
            <el-option label="已使用" value="used" />
            <el-option label="已退款" value="refunded" />
          </el-select>
        </el-form-item>
        <el-form-item label="核销状态">
          <el-select v-model="filters.checkedStatus" placeholder="全部" clearable style="width: 120px">
            <el-option label="已核销" value="checked" />
            <el-option label="未核销" value="unchecked" />
          </el-select>
        </el-form-item>
        <el-form-item label="预订日期">
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item label="出游日期">
          <el-date-picker
            v-model="filters.visitDate"
            type="date"
            placeholder="选择日期"
            style="width: 160px"
            value-format="yyyy-MM-dd"
          />
        </el-form-item>
        <el-form-item label="订单编号">
          <el-input
            v-model="filters.orderId"
            placeholder="请输入订单编号"
            clearable
            style="width: 200px"
            @keyup.enter.native="searchOrders"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="searchOrders">
            <i class="el-icon-search"></i>
            搜索
          </el-button>
          <el-button @click="resetFilters">重置</el-button>
          <el-button @click="refreshOrders">
            <i class="el-icon-refresh"></i>
            刷新
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <div class="table-header">
        <span class="table-title">订单列表</span>
        <span class="table-stats">
          共 <strong>{{ total }}</strong> 条记录，
          当前显示第 <strong>{{ (currentPage - 1) * pageSize + 1 }}</strong> -
          <strong>{{ Math.min(currentPage * pageSize, total) }}</strong> 条
        </span>
      </div>
      <el-table
        :data="filteredOrders"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
        :default-sort="{ prop: 'createTime', order: 'descending' }"
      >
        <el-table-column prop="id" label="订单编号" width="180" sortable />
        <el-table-column prop="ticketName" label="门票类型" width="120" sortable />
        <el-table-column prop="quantity" label="数量" width="80" align="center" sortable />
        <el-table-column prop="totalPrice" label="金额" width="100" align="center" sortable>
          <template slot-scope="scope">
            <span class="price-text">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="visitorName" label="游客姓名" width="100" />
        <el-table-column prop="visitorPhone" label="手机号" width="120" />
        <el-table-column prop="visitDate" label="出游日期" width="120" sortable />
        <el-table-column prop="status" label="状态" width="100" align="center" sortable>
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusLabel(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="核销状态" width="100" align="center" sortable>
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === 'used' ? 'success' : 'info'" size="small">
              {{ scope.row.status === 'used' ? '已核销' : '未核销' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="ticketCode" label="取票码" width="130" align="center">
          <template slot-scope="scope">
            <span class="ticket-code">{{ scope.row.ticketCode }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160" sortable />
        <el-table-column prop="useTime" label="核销时间" width="160" sortable />
        <el-table-column label="操作" width="180" fixed="right" align="center">
          <template slot-scope="scope">
            <el-button
              type="text"
              size="small"
              @click="viewDetail(scope.row)"
            >
              详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'paid'"
              type="text"
              size="small"
              @click="refundOrder(scope.row)"
            >
              退款
            </el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="text"
              size="small"
              @click="cancelOrder(scope.row)"
            >
              取消
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          background
          :current-page="currentPage"
          :page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        />
      </div>
    </el-card>

    <el-dialog
      title="订单详情"
      :visible.sync="detailVisible"
      width="500px"
    >
      <div class="order-detail" v-if="currentOrder">
        <div class="detail-item">
          <span class="label">订单编号：</span>
          <span class="value">{{ currentOrder.id }}</span>
        </div>
        <div class="detail-item">
          <span class="label">门票类型：</span>
          <span class="value">{{ currentOrder.ticketName }}</span>
        </div>
        <div class="detail-item">
          <span class="label">购买数量：</span>
          <span class="value">{{ currentOrder.quantity }}张</span>
        </div>
        <div class="detail-item">
          <span class="label">订单金额：</span>
          <span class="value price">¥{{ currentOrder.totalPrice }}</span>
        </div>
        <div class="detail-item">
          <span class="label">游客姓名：</span>
          <span class="value">{{ currentOrder.visitorName }}</span>
        </div>
        <div class="detail-item">
          <span class="label">手机号码：</span>
          <span class="value">{{ currentOrder.visitorPhone }}</span>
        </div>
        <div class="detail-item">
          <span class="label">出游日期：</span>
          <span class="value">{{ currentOrder.visitDate }}</span>
        </div>
        <div class="detail-item">
          <span class="label">取票码：</span>
          <span class="value ticket-code">{{ currentOrder.ticketCode }}</span>
        </div>
        <div class="detail-item">
          <span class="label">订单状态：</span>
          <el-tag :type="getStatusType(currentOrder.status)" size="small">
            {{ getStatusLabel(currentOrder.status) }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">核销状态：</span>
          <el-tag :type="currentOrder.status === 'used' ? 'success' : 'info'" size="small">
            {{ currentOrder.status === 'used' ? '已核销' : '未核销' }}
          </el-tag>
        </div>
        <div class="detail-item">
          <span class="label">创建时间：</span>
          <span class="value">{{ currentOrder.createTime }}</span>
        </div>
        <div class="detail-item" v-if="currentOrder.useTime">
          <span class="label">核销时间：</span>
          <span class="value">{{ currentOrder.useTime }}</span>
        </div>
        <div class="detail-item" v-if="currentOrder.refundTime">
          <span class="label">退款时间：</span>
          <span class="value">{{ currentOrder.refundTime }}</span>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { orders, statusMap, formatDateTime, ticketTypes } from '@/mock/data';

export default {
  name: 'OrderList',
  data() {
    return {
      orders: [],
      ticketTypes,
      filters: {
        ticketName: '',
        status: '',
        checkedStatus: '',
        dateRange: [],
        visitDate: '',
        orderId: ''
      },
      loading: false,
      currentPage: 1,
      pageSize: 10,
      detailVisible: false,
      currentOrder: null,
      refreshTimer: null
    };
  },
  computed: {
    filteredOrders() {
      let result = [...this.orders];

      if (this.filters.ticketName) {
        result = result.filter(item => item.ticketName === this.filters.ticketName);
      }

      if (this.filters.status) {
        result = result.filter(item => item.status === this.filters.status);
      }

      if (this.filters.checkedStatus) {
        if (this.filters.checkedStatus === 'checked') {
          result = result.filter(item => item.status === 'used');
        } else {
          result = result.filter(item => item.status !== 'used');
        }
      }

      if (this.filters.dateRange && this.filters.dateRange.length === 2) {
        const [startDate, endDate] = this.filters.dateRange;
        result = result.filter(item => {
          const orderDate = item.createTime.split(' ')[0];
          return orderDate >= startDate && orderDate <= endDate;
        });
      }

      if (this.filters.visitDate) {
        result = result.filter(item => item.visitDate === this.filters.visitDate);
      }

      if (this.filters.orderId) {
        result = result.filter(item =>
          item.id.toLowerCase().includes(this.filters.orderId.toLowerCase())
        );
      }

      result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime));

      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return result.slice(start, end);
    },
    total() {
      let result = [...this.orders];

      if (this.filters.ticketName) {
        result = result.filter(item => item.ticketName === this.filters.ticketName);
      }

      if (this.filters.status) {
        result = result.filter(item => item.status === this.filters.status);
      }

      if (this.filters.checkedStatus) {
        if (this.filters.checkedStatus === 'checked') {
          result = result.filter(item => item.status === 'used');
        } else {
          result = result.filter(item => item.status !== 'used');
        }
      }

      if (this.filters.dateRange && this.filters.dateRange.length === 2) {
        const [startDate, endDate] = this.filters.dateRange;
        result = result.filter(item => {
          const orderDate = item.createTime.split(' ')[0];
          return orderDate >= startDate && orderDate <= endDate;
        });
      }

      if (this.filters.visitDate) {
        result = result.filter(item => item.visitDate === this.filters.visitDate);
      }

      if (this.filters.orderId) {
        result = result.filter(item =>
          item.id.toLowerCase().includes(this.filters.orderId.toLowerCase())
        );
      }

      return result.length;
    }
  },
  mounted() {
    this.loadOrders();
    this.startAutoRefresh();
  },
  beforeDestroy() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }
  },
  methods: {
    loadOrders() {
      this.loading = true;
      setTimeout(() => {
        const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
        this.orders = [...localOrders, ...orders];
        this.loading = false;
      }, 300);
    },
    refreshOrders() {
      this.loadOrders();
      this.$message.success('数据已刷新');
    },
    startAutoRefresh() {
      this.refreshTimer = setInterval(() => {
        this.syncOrdersFromStorage();
      }, 3000);
    },
    syncOrdersFromStorage() {
      const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
      let hasChanges = false;

      localOrders.forEach(localOrder => {
        const existingOrder = this.orders.find(o => o.id === localOrder.id);
        if (existingOrder && existingOrder.status !== localOrder.status) {
          existingOrder.status = localOrder.status;
          existingOrder.useTime = localOrder.useTime;
          existingOrder.refundTime = localOrder.refundTime;
          hasChanges = true;
        }
      });

      if (hasChanges) {
        this.orders = [...this.orders];
      }
    },
    getStatusType(status) {
      return statusMap[status]?.type || 'info';
    },
    getStatusLabel(status) {
      return statusMap[status]?.label || '未知';
    },
    searchOrders() {
      this.currentPage = 1;
    },
    resetFilters() {
      this.filters = {
        ticketName: '',
        status: '',
        checkedStatus: '',
        dateRange: [],
        visitDate: '',
        orderId: ''
      };
      this.currentPage = 1;
    },
    handlePageChange(page) {
      this.currentPage = page;
    },
    handleSizeChange(size) {
      this.pageSize = size;
      this.currentPage = 1;
    },
    viewDetail(order) {
      this.currentOrder = order;
      this.detailVisible = true;
    },
    refundOrder(order) {
      this.$confirm('确认要退款该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = 'refunded';
        order.refundTime = formatDateTime(new Date());
        this.updateLocalOrders();
        this.$message({
          type: 'success',
          message: '退款成功！'
        });
      }).catch(() => {});
    },
    cancelOrder(order) {
      this.$confirm('确认要取消该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.orders.findIndex(item => item.id === order.id);
        if (index > -1) {
          this.orders.splice(index, 1);
        }
        this.updateLocalOrders();
        this.$message({
          type: 'success',
          message: '订单已取消！'
        });
      }).catch(() => {});
    },
    updateLocalOrders() {
      const localOrders = this.orders.filter(order =>
        !orders.find(o => o.id === order.id)
      );
      localStorage.setItem('orders', JSON.stringify(localOrders));
    }
  }
};
</script>

<style scoped>
.order-list-page {
  padding: 0;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  margin: 0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #EBEEF5;
}

.table-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.table-stats {
  font-size: 14px;
  color: #606266;
}

.table-stats strong {
  color: #409EFF;
  margin: 0 2px;
}

.table-card /deep/ .el-card__body {
  padding: 0;
}

.price-text {
  color: #F56C6C;
  font-weight: 600;
}

.ticket-code {
  color: #409EFF;
  font-family: monospace;
  font-weight: 600;
}

.pagination-wrapper {
  padding: 20px;
  text-align: right;
}

.order-detail {
  padding: 10px 0;
}

.detail-item {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px solid #F5F7FA;
}

.detail-item:last-child {
  border-bottom: none;
}

.label {
  width: 100px;
  color: #909399;
  flex-shrink: 0;
}

.value {
  color: #303133;
  flex: 1;
}

.value.price {
  color: #F56C6C;
  font-weight: 600;
  font-size: 16px;
}

.value.ticket-code {
  color: #409EFF;
  font-family: monospace;
  font-weight: 600;
}
</style>
