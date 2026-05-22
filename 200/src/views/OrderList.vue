<template>
  <div class="order-list-container">
    <div class="page-header">
      <h2>订单管理</h2>
      <p class="subtitle">实时跟踪订单生产进度</p>
    </div>

    <div class="search-bar">
      <el-input 
        v-model="searchText" 
        placeholder="搜索订单编号" 
        class="search-input"
        prefix-icon="el-icon-search"
      />
      <el-select v-model="statusFilter" placeholder="按状态筛选">
        <el-option label="全部" value="" />
        <el-option v-for="(label, key) in statusLabels" :key="key" :label="label" :value="key" />
      </el-select>
    </div>

    <el-table 
      :data="filteredOrders" 
      border 
      stripe 
      class="order-table"
      :default-sort="{ prop: 'createdAt', order: 'descending' }"
      :row-class-name="getRowClassName"
    >
      <el-table-column prop="id" label="订单编号" sortable width="180">
        <template slot-scope="scope">
          <div class="order-id-cell">
            <span class="order-id">{{ scope.row.id }}</span>
            <el-tag v-if="isNewOrder(scope.row)" type="danger" size="mini" class="new-tag">新</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="stoneType" label="砚石材">
        <template slot-scope="scope">
          {{ getLabel(stoneTypes, scope.row.stoneType) }}
        </template>
      </el-table-column>
      <el-table-column label="尺寸">
        <template slot-scope="scope">
          {{ scope.row.length }} × {{ scope.row.width }} cm
        </template>
      </el-table-column>
      <el-table-column prop="carvingStyle" label="雕刻样式">
        <template slot-scope="scope">
          {{ getLabel(carvingStyles, scope.row.carvingStyle) }}
        </template>
      </el-table-column>
      <el-table-column prop="inkPoolShape" label="砚池形制">
        <template slot-scope="scope">
          {{ getLabel(inkPoolShapes, scope.row.inkPoolShape) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="当前状态" sortable>
        <template slot-scope="scope">
          <el-tag :type="statusColors[scope.row.status]">
            {{ statusLabels[scope.row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createdAt" label="下单时间" sortable />
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button 
            size="small" 
            type="primary" 
            @click="showDetail(scope.row)"
          >
            <i class="el-icon-eye"></i>
            详情
          </el-button>
          <el-button 
            v-if="scope.row.status !== 'completed'"
            size="small" 
            type="success" 
            @click="nextStep(scope.row)"
          >
            <i class="el-icon-arrow-right"></i>
            下一步
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination 
        @size-change="handleSizeChange" 
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50]"
        :page-size="pageSize"
        :total="filteredOrders.length"
        layout="total, sizes, prev, pager, next, jumper"
      />
    </div>

    <el-dialog title="订单详情" :visible.sync="showDetailDialog" width="600px">
      <div v-if="selectedOrder" class="detail-content">
        <div class="detail-header">
          <span class="detail-id">{{ selectedOrder.id }}</span>
          <el-tag :type="statusColors[selectedOrder.status]" class="detail-status">
            {{ statusLabels[selectedOrder.status] }}
          </el-tag>
        </div>
        
        <div class="detail-info">
          <div class="info-row">
            <span class="info-label">砚石材：</span>
            <span>{{ getLabel(stoneTypes, selectedOrder.stoneType) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">尺寸规格：</span>
            <span>{{ selectedOrder.length }} × {{ selectedOrder.width }} cm</span>
          </div>
          <div class="info-row">
            <span class="info-label">雕刻样式：</span>
            <span>{{ getLabel(carvingStyles, selectedOrder.carvingStyle) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">砚池形制：</span>
            <span>{{ getLabel(inkPoolShapes, selectedOrder.inkPoolShape) }}</span>
          </div>
          <div class="info-row">
            <span class="info-label">下单时间：</span>
            <span>{{ selectedOrder.createdAt }}</span>
          </div>
        </div>

        <div class="process-section">
          <h4>生产工序进度</h4>
          <ProcessSteps :current-status="selectedOrder.status" />
          
          <div v-if="selectedOrder.processSteps.length > 0" class="process-history">
            <h5>工序记录</h5>
            <div v-for="(step, index) in selectedOrder.processSteps" :key="index" class="history-item">
              <span class="history-status">{{ statusLabels[step.status] }}</span>
              <span class="history-time">{{ step.time }}</span>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import { stoneTypes, carvingStyles, inkPoolShapes, statusLabels, statusColors, processSteps } from '../data/mockData'
import ProcessSteps from '../components/ProcessSteps.vue'

export default {
  name: 'OrderList',
  components: {
    ProcessSteps
  },
  data() {
    return {
      stoneTypes,
      carvingStyles,
      inkPoolShapes,
      statusLabels,
      statusColors,
      searchText: '',
      statusFilter: '',
      currentPage: 1,
      pageSize: 10,
      showDetailDialog: false,
      selectedOrder: null
    }
  },
  computed: {
    ...mapGetters(['getOrders']),
    filteredOrders() {
      let orders = this.getOrders
      if (this.searchText) {
        orders = orders.filter(order => order.id.toLowerCase().includes(this.searchText.toLowerCase()))
      }
      if (this.statusFilter) {
        orders = orders.filter(order => order.status === this.statusFilter)
      }
      return orders
    },
    paginatedOrders() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredOrders.slice(start, end)
    }
  },
  methods: {
    ...mapActions(['updateStatus']),
    getRowClassName({ row }) {
      if (this.isNewOrder(row)) {
        return 'new-order-row'
      }
      return ''
    },
    isNewOrder(order) {
      if (!order.createdAt) return false
      const orderTime = new Date(order.createdAt.replace(/-/g, '/')).getTime()
      const now = Date.now()
      return (now - orderTime) < 24 * 60 * 60 * 1000
    },
    getLabel(list, value) {
      const item = list.find(item => item.value === value)
      return item ? item.label : '未知'
    },
    showDetail(order) {
      this.selectedOrder = order
      this.showDetailDialog = true
    },
    nextStep(order) {
      const stepOrder = ['pending', 'quarrying', 'cutting', 'shaping', 'carving', 'polishing', 'waxing', 'inspecting', 'completed']
      const currentIndex = stepOrder.indexOf(order.status)
      if (currentIndex < stepOrder.length - 1) {
        const nextStatus = stepOrder[currentIndex + 1]
        this.updateStatus({ orderId: order.id, status: nextStatus })
        this.$message.success(`已更新为：${this.statusLabels[nextStatus]}`)
      }
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style scoped>
.order-list-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  font-size: 24px;
  color: #8B4513;
  margin-bottom: 5px;
}

.subtitle {
  color: #999;
  font-size: 14px;
}

.search-bar {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  justify-content: flex-end;
}

.search-input {
  width: 250px;
}

.order-table {
  background: #fff;
  border-radius: 8px;
}

.order-id-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.order-id {
  font-family: monospace;
  color: #409EFF;
}

.new-tag {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
}

::v-deep .new-order-row {
  background-color: #fff7e6 !important;
}

::v-deep .new-order-row:hover > td {
  background-color: #ffe7ba !important;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.detail-content {
  padding: 10px;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.detail-id {
  font-family: monospace;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.detail-status {
  font-size: 14px;
}

.detail-info {
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  padding: 10px 0;
  border-bottom: 1px dashed #eee;
}

.info-label {
  width: 100px;
  color: #999;
  font-weight: bold;
}

.info-row span:last-child {
  color: #333;
}

.process-section {
  margin-top: 20px;
}

.process-section h4 {
  margin-bottom: 15px;
  color: #333;
}

.process-section h5 {
  margin: 15px 0 10px;
  color: #666;
  font-size: 14px;
}

.process-history {
  background: #f9f9f9;
  border-radius: 8px;
  padding: 15px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px dashed #eee;
}

.history-item:last-child {
  border-bottom: none;
}

.history-status {
  color: #333;
  font-weight: 500;
}

.history-time {
  color: #999;
  font-size: 12px;
}
</style>
