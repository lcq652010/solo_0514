<template>
  <div class="page-container">
    <h2 class="page-title">团长订单管理</h2>
    
    <div class="stats-card">
      <div class="stat-item">
        <div class="stat-value">{{ stats.total }}</div>
        <div class="stat-label">全部订单</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ stats.pending }}</div>
        <div class="stat-label">待付款</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ stats.shipped }}</div>
        <div class="stat-label">待提货</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">{{ stats.completed }}</div>
        <div class="stat-label">已完成</div>
      </div>
    </div>

    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索订单号/商品名/收货人"
        style="width: 250px;"
        clearable
      ></el-input>
      <el-select v-model="categoryFilter" placeholder="商品分类" clearable>
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat"></el-option>
      </el-select>
      <el-select v-model="groupStatusFilter" placeholder="拼团状态" clearable>
        <el-option label="已成团" value="success"></el-option>
        <el-option label="拼团中" value="going"></el-option>
        <el-option label="拼团失败" value="fail"></el-option>
      </el-select>
      <el-date-picker
        v-model="pickUpDateFilter"
        type="date"
        placeholder="提货日期"
        value-format="yyyy-MM-dd"
        style="width: 150px;"
        clearable
      ></el-date-picker>
      <el-select v-model="statusFilter" placeholder="订单状态" clearable>
        <el-option label="待付款" value="pending"></el-option>
        <el-option label="已付款" value="paid"></el-option>
        <el-option label="已发货" value="shipped"></el-option>
        <el-option label="已提货" value="picked"></el-option>
        <el-option label="已完成" value="completed"></el-option>
      </el-select>
      <el-button type="primary" @click="resetFilters">重置筛选</el-button>
    </div>

    <div class="table-container">
      <el-table
        :data="paginatedOrders"
        border
        style="width: 100%;"
      >
        <el-table-column
          prop="id"
          label="订单号"
          width="180"
        ></el-table-column>
        <el-table-column
          prop="goodsName"
          label="商品名称"
          min-width="180"
          show-overflow-tooltip
        ></el-table-column>
        <el-table-column
          prop="category"
          label="分类"
          width="100"
        ></el-table-column>
        <el-table-column
          prop="buyerName"
          label="收货人"
          width="100"
        ></el-table-column>
        <el-table-column
          prop="phone"
          label="联系电话"
          width="120"
        ></el-table-column>
        <el-table-column
          prop="quantity"
          label="数量"
          width="80"
        ></el-table-column>
        <el-table-column
          prop="totalPrice"
          label="金额"
          width="100"
        >
          <template slot-scope="scope">
            <span style="color: #ff6b00; font-weight: bold;">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="pickUpDate"
          label="提货日期"
          width="120"
        ></el-table-column>
        <el-table-column
          prop="orderTime"
          label="下单时间"
          width="180"
        ></el-table-column>
        <el-table-column
          label="拼团状态"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag :type="getGroupStatusType(scope.row.groupStatus)" size="small">
              {{ getGroupStatusText(scope.row.groupStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="status"
          label="订单状态"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="提货码"
          width="100"
        >
          <template slot-scope="scope">
            <el-tag size="small" type="warning">{{ scope.row.pickUpCode }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="200"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              @click="viewDetail(scope.row)"
            >
              详情
            </el-button>
            <el-button
              size="mini"
              type="success"
              :disabled="scope.row.status === 'completed'"
              @click="updateStatus(scope.row)"
            >
              更新状态
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-pagination
      style="margin-top: 20px; text-align: right;"
      background
      :page-size="pageSize"
      :current-page="currentPage"
      :total="filteredOrders.length"
      :page-sizes="[5, 10, 20, 50]"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    ></el-pagination>
  </div>
</template>

<script>
import { ordersList, categories } from '../data/mock.js'

export default {
  name: 'LeaderManage',
  data() {
    return {
      ordersList: ordersList,
      categories: categories,
      searchKeyword: '',
      categoryFilter: '',
      groupStatusFilter: '',
      pickUpDateFilter: '',
      statusFilter: '',
      currentPage: 1,
      pageSize: 10
    }
  },
  computed: {
    filteredOrders() {
      return this.ordersList.filter(item => {
        const matchKeyword = !this.searchKeyword || 
          item.id.includes(this.searchKeyword) ||
          item.goodsName.includes(this.searchKeyword) ||
          item.buyerName.includes(this.searchKeyword)
        const matchCategory = !this.categoryFilter || this.categoryFilter === '全部' || item.category === this.categoryFilter
        const matchGroupStatus = !this.groupStatusFilter || item.groupStatus === this.groupStatusFilter
        const matchPickUpDate = !this.pickUpDateFilter || item.pickUpDate === this.pickUpDateFilter
        const matchStatus = !this.statusFilter || item.status === this.statusFilter
        return matchKeyword && matchCategory && matchGroupStatus && matchPickUpDate && matchStatus
      })
    },
    paginatedOrders() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredOrders.slice(start, end)
    },
    stats() {
      return {
        total: this.ordersList.length,
        pending: this.ordersList.filter(item => item.status === 'pending').length,
        shipped: this.ordersList.filter(item => item.status === 'shipped').length,
        completed: this.ordersList.filter(item => item.status === 'completed').length
      }
    }
  },
  mounted() {
    this.$root.$on('newOrder', (newOrder) => {
      this.ordersList.unshift(newOrder)
      this.$message.success('新订单已同步')
    })
    this.$root.$on('orderPicked', (orderId) => {
      const order = this.ordersList.find(o => o.id === orderId)
      if (order) {
        order.status = 'picked'
        this.$message.success('订单状态已更新')
      }
    })
  },
  methods: {
    getStatusText(status) {
      const map = {
        pending: '待付款',
        paid: '已付款',
        shipped: '已发货',
        picked: '已提货',
        completed: '已完成'
      }
      return map[status]
    },
    getStatusType(status) {
      const map = {
        pending: 'info',
        paid: 'warning',
        shipped: 'primary',
        picked: 'success',
        completed: 'success'
      }
      return map[status]
    },
    getGroupStatusText(status) {
      const map = {
        success: '已成团',
        going: '拼团中',
        fail: '拼团失败'
      }
      return map[status]
    },
    getGroupStatusType(status) {
      const map = {
        success: 'success',
        going: 'warning',
        fail: 'danger'
      }
      return map[status]
    },
    resetFilters() {
      this.searchKeyword = ''
      this.categoryFilter = ''
      this.groupStatusFilter = ''
      this.pickUpDateFilter = ''
      this.statusFilter = ''
      this.currentPage = 1
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    viewDetail(row) {
      this.$alert(`
        <p><strong>订单号：</strong>${row.id}</p>
        <p><strong>商品：</strong>${row.goodsName}</p>
        <p><strong>分类：</strong>${row.category}</p>
        <p><strong>收货人：</strong>${row.buyerName}</p>
        <p><strong>电话：</strong>${row.phone}</p>
        <p><strong>数量：</strong>${row.quantity} 件</p>
        <p><strong>金额：</strong>¥${row.totalPrice}</p>
        <p><strong>提货日期：</strong>${row.pickUpDate}</p>
        <p><strong>下单时间：</strong>${row.orderTime}</p>
        <p><strong>提货码：</strong>${row.pickUpCode}</p>
      `, '订单详情', {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '确定'
      })
    },
    updateStatus(row) {
      this.$prompt('请选择新的状态', '更新订单状态', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputType: 'select',
        inputPattern: /.+/,
        inputErrorMessage: '请选择状态',
        inputValidator: (value) => !!value,
        inputValue: row.status,
        inputOptions: [
          { value: 'pending', label: '待付款' },
          { value: 'paid', label: '已付款' },
          { value: 'shipped', label: '已发货' },
          { value: 'picked', label: '已提货' },
          { value: 'completed', label: '已完成' }
        ]
      }).then(({ value }) => {
        row.status = value
        this.$message.success('状态更新成功')
      }).catch(() => {
      })
    }
  }
}
</script>