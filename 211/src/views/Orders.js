window.Orders = {
  template: `
    <div class="orders-page">
      <h2 class="page-title">
        <i class="el-icon-document"></i>
        订单管理
      </h2>

      <el-card class="card-shadow mb-20">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="订单号">
            <el-input
              v-model="searchForm.orderId"
              placeholder="请输入订单号"
              clearable />
          </el-form-item>
          <el-form-item label="客户姓名">
            <el-input
              v-model="searchForm.customerName"
              placeholder="请输入客户姓名"
              clearable />
          </el-form-item>
          <el-form-item label="订单状态">
            <el-select
              v-model="searchForm.status"
              placeholder="全部"
              clearable>
              <el-option label="待支付" value="待支付" />
              <el-option label="已支付" value="已支付" />
              <el-option label="拍摄中" value="拍摄中" />
              <el-option label="已完成" value="已完成" />
              <el-option label="已取消" value="已取消" />
            </el-select>
          </el-form-item>
          <el-form-item label="拍摄日期">
            <el-date-picker
              v-model="searchForm.dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              value-format="YYYY-MM-DD" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="searchOrders">
              <i class="el-icon-search"></i> 搜索
            </el-button>
            <el-button @click="resetSearch">
              <i class="el-icon-refresh"></i> 重置
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="card-shadow">
        <el-table
          :data="filteredOrders"
          border
          class="orders-table"
          stripe>
          <el-table-column prop="id" label="订单号" width="160" />
          <el-table-column prop="packageName" label="套餐名称" min-width="180" />
          <el-table-column prop="customerName" label="客户姓名" width="120" />
          <el-table-column prop="photographerName" label="摄影师" width="100" />
          <el-table-column label="拍摄信息" width="220">
            <template slot-scope="scope">
              <div>日期：{{ scope.row.shootDate }}</div>
              <div>时段：{{ scope.row.shootTime }}</div>
              <div>地点：{{ scope.row.location }}</div>
            </template>
          </el-table-column>
          <el-table-column label="金额" width="100">
            <template slot-scope="scope">
              <span class="price">¥{{ scope.row.price }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" effect="dark">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column label="操作" width="180" fixed="right">
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="viewOrder(scope.row)">
                查看
              </el-button>
              <el-button
                type="text"
                size="small"
                :disabled="scope.row.status !== '待支付'"
                @click="payOrder(scope.row)">
                支付
              </el-button>
              <el-button
                type="text"
                size="small"
                :disabled="scope.row.status === '已完成' || scope.row.status === '已取消'"
                @click="editStatus(scope.row)">
                状态
              </el-button>
              <el-button
                type="text"
                size="small"
                style="color: #f56c6c"
                :disabled="scope.row.status === '已完成' || scope.row.status === '已取消'"
                @click="deleteOrder(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination">
          <el-pagination
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pagination.currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="filteredOrders.length">
          </el-pagination>
        </div>
      </el-card>

      <el-dialog
        :visible.sync="detailVisible"
        title="订单详情"
        width="600px">
        <el-descriptions v-if="currentOrder" :column="2" border>
          <el-descriptions-item label="订单号">
            {{ currentOrder.id }}
          </el-descriptions-item>
          <el-descriptions-item label="订单状态">
            <el-tag :type="getStatusType(currentOrder.status)" effect="dark">
              {{ currentOrder.status }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="套餐名称">
            {{ currentOrder.packageName }}
          </el-descriptions-item>
          <el-descriptions-item label="订单金额">
            <span class="price">¥{{ currentOrder.price }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="客户姓名">
            {{ currentOrder.customerName }}
          </el-descriptions-item>
          <el-descriptions-item label="摄影师">
            {{ currentOrder.photographerName }}
          </el-descriptions-item>
          <el-descriptions-item label="拍摄日期">
            {{ currentOrder.shootDate }}
          </el-descriptions-item>
          <el-descriptions-item label="拍摄时段">
            {{ currentOrder.shootTime }}
          </el-descriptions-item>
          <el-descriptions-item label="拍摄地点" :span="2">
            {{ currentOrder.location }}
          </el-descriptions-item>
          <el-descriptions-item label="备注信息" :span="2">
            {{ currentOrder.remark || '无' }}
          </el-descriptions-item>
          <el-descriptions-item label="创建时间" :span="2">
            {{ currentOrder.createTime }}
          </el-descriptions-item>
        </el-descriptions>
        <span slot="footer" class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </el-dialog>

      <el-dialog
        :visible.sync="statusVisible"
        title="修改订单状态"
        width="400px">
        <el-form label-width="100px">
          <el-form-item label="订单号">
            <span>{{ currentOrder?.id }}</span>
          </el-form-item>
          <el-form-item label="当前状态">
            <el-tag :type="getStatusType(currentOrder?.status)" effect="dark">
              {{ currentOrder?.status }}
            </el-tag>
          </el-form-item>
          <el-form-item label="新状态">
            <el-select v-model="newStatus" style="width: 100%">
              <el-option label="待支付" value="待支付" />
              <el-option label="已支付" value="已支付" />
              <el-option label="拍摄中" value="拍摄中" />
              <el-option label="已完成" value="已完成" />
              <el-option label="已取消" value="已取消" />
            </el-select>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="statusVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmStatus">确认</el-button>
        </span>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      searchForm: {
        orderId: '',
        customerName: '',
        status: '',
        dateRange: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 10
      },
      detailVisible: false,
      statusVisible: false,
      currentOrder: null,
      newStatus: ''
    };
  },
  computed: {
    orders() {
      return this.$store.state.orders;
    },
    filteredOrders() {
      let result = [...this.orders];
      
      if (this.searchForm.orderId) {
        result = result.filter(o => o.id.includes(this.searchForm.orderId));
      }
      
      if (this.searchForm.customerName) {
        result = result.filter(o => o.customerName.includes(this.searchForm.customerName));
      }
      
      if (this.searchForm.status) {
        result = result.filter(o => o.status === this.searchForm.status);
      }
      
      if (this.searchForm.dateRange && this.searchForm.dateRange.length === 2) {
        result = result.filter(o => {
          return o.shootDate >= this.searchForm.dateRange[0] && o.shootDate <= this.searchForm.dateRange[1];
        });
      }
      
      return result;
    }
  },
  methods: {
    getStatusType(status) {
      const types = {
        '待支付': 'warning',
        '已支付': 'primary',
        '拍摄中': 'success',
        '已完成': 'success',
        '已取消': 'info'
      };
      return types[status] || 'info';
    },
    searchOrders() {
      this.pagination.currentPage = 1;
    },
    resetSearch() {
      this.searchForm = {
        orderId: '',
        customerName: '',
        status: '',
        dateRange: []
      };
      this.pagination.currentPage = 1;
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val;
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val;
    },
    viewOrder(order) {
      this.currentOrder = order;
      this.detailVisible = true;
    },
    payOrder(order) {
      this.$confirm('确认支付订单 ' + order.id + ' 金额 ¥' + order.price + ' 吗？', '支付确认', {
        confirmButtonText: '确认支付',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$store.dispatch('updateOrder', { id: order.id, status: '已支付' });
        this.$message.success('支付成功！');
      }).catch(() => {});
    },
    editStatus(order) {
      this.currentOrder = order;
      this.newStatus = order.status;
      this.statusVisible = true;
    },
    confirmStatus() {
      if (this.newStatus === this.currentOrder.status) {
        this.$message.info('状态未发生变化');
        return;
      }
      this.$store.dispatch('updateOrder', { id: this.currentOrder.id, status: this.newStatus });
      this.$message.success('状态更新成功！');
      this.statusVisible = false;
    },
    deleteOrder(order) {
      this.$confirm('确认删除订单 ' + order.id + ' 吗？此操作不可恢复。', '删除确认', {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'error'
      }).then(() => {
        this.$store.dispatch('deleteOrder', order.id);
        this.$message.success('删除成功！');
      }).catch(() => {});
    }
  }
};
