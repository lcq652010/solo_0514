<template>
  <div class="orders">
    <div class="page-header flex-between">
      <h1 class="page-title">订单列表</h1>
      <el-button type="primary" @click="goToBooking">新建预订</el-button>
    </div>
    
    <el-card class="mb-20">
      <el-form :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单号" clearable></el-input>
        </el-form-item>
        <el-form-item label="客人姓名">
          <el-input v-model="searchForm.guestName" placeholder="请输入姓名" clearable></el-input>
        </el-form-item>
        <el-form-item label="房型">
          <el-select v-model="searchForm.roomType" placeholder="请选择房型" clearable>
            <el-option label="标准单人间" value="标准单人间"></el-option>
            <el-option label="标准双人间" value="标准双人间"></el-option>
            <el-option label="豪华大床房" value="豪华大床房"></el-option>
            <el-option label="家庭套房" value="家庭套房"></el-option>
            <el-option label="总统套房" value="总统套房"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
            <el-option label="待确认" value="pending"></el-option>
            <el-option label="已确认" value="confirmed"></el-option>
            <el-option label="已入住" value="checked_in"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="入住日期">
          <el-date-picker
            v-model="searchForm.checkInDate"
            type="date"
            placeholder="选择入住日期"
            style="width: 140px;"
            clearable
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="search">查询</el-button>
          <el-button @click="reset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card>
      <el-table :data="paginatedOrders" style="width: 100%" border>
        <el-table-column prop="id" label="订单号" width="160"></el-table-column>
        <el-table-column prop="guestName" label="客人姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="手机号" width="130"></el-table-column>
        <el-table-column prop="roomType" label="房型" width="120"></el-table-column>
        <el-table-column prop="roomNumber" label="房间号" width="80"></el-table-column>
        <el-table-column label="入住/退房" width="220">
          <template slot-scope="scope">
            <div>{{ scope.row.checkInDate }} 至</div>
            <div>{{ scope.row.checkOutDate }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="totalPrice" label="金额" width="100">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 500;">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="orderStatusMap[scope.row.status].type" size="small">
              {{ orderStatusMap[scope.row.status].label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="small" type="primary" @click="viewDetail(scope.row)">详情</el-button>
            <el-button size="small" type="success" @click="editOrder(scope.row)" v-if="['pending', 'confirmed'].includes(scope.row.status)">编辑</el-button>
            <el-button size="small" type="danger" @click="cancelOrder(scope.row)" v-if="['pending', 'confirmed'].includes(scope.row.status)">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination mt-20">
        <el-pagination
          background
          :page-size="pageSize"
          :current-page="currentPage"
          :total="totalOrders"
          layout="total, prev, pager, next, jumper"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </el-card>
    
    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="700px">
      <el-descriptions v-if="currentOrder" :column="2" border>
        <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="客人姓名">{{ currentOrder.guestName }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentOrder.phone }}</el-descriptions-item>
        <el-descriptions-item label="身份证号">{{ currentOrder.idCard }}</el-descriptions-item>
        <el-descriptions-item label="房型">{{ currentOrder.roomType }}</el-descriptions-item>
        <el-descriptions-item label="房间号">{{ currentOrder.roomNumber }}</el-descriptions-item>
        <el-descriptions-item label="入住天数">{{ currentOrder.days }} 天</el-descriptions-item>
        <el-descriptions-item label="入住日期">{{ currentOrder.checkInDate }}</el-descriptions-item>
        <el-descriptions-item label="退房日期">{{ currentOrder.checkOutDate }}</el-descriptions-item>
        <el-descriptions-item label="订单金额" :span="2">
          <span style="font-size: 24px; color: #f56c6c; font-weight: bold;">¥{{ currentOrder.totalPrice }}</span>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { orders, orderStatusMap } from '../mock/data'

export default {
  name: 'Orders',
  data() {
    return {
      orders: orders,
      orderStatusMap: orderStatusMap,
      searchForm: {
        orderId: '',
        guestName: '',
        roomType: '',
        status: '',
        checkInDate: ''
      },
      pageSize: 5,
      currentPage: 1,
      detailDialogVisible: false,
      currentOrder: null
    }
  },
  computed: {
    filteredOrders() {
      let result = [...this.orders]
      
      if (this.searchForm.orderId) {
        result = result.filter(order => order.id.includes(this.searchForm.orderId))
      }
      
      if (this.searchForm.guestName) {
        result = result.filter(order => order.guestName.includes(this.searchForm.guestName))
      }
      
      if (this.searchForm.roomType) {
        result = result.filter(order => order.roomType === this.searchForm.roomType)
      }
      
      if (this.searchForm.status) {
        result = result.filter(order => order.status === this.searchForm.status)
      }
      
      if (this.searchForm.checkInDate) {
        const dateStr = this.formatDate(this.searchForm.checkInDate)
        result = result.filter(order => order.checkInDate === dateStr)
      }
      
      return result
    },
    totalOrders() {
      return this.filteredOrders.length
    },
    paginatedOrders() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredOrders.slice(start, end)
    }
  },
  methods: {
    formatDate(date) {
      if (!date) return ''
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    goToBooking() {
      this.$router.push('/booking')
    },
    search() {
      this.currentPage = 1
    },
    reset() {
      this.searchForm.orderId = ''
      this.searchForm.guestName = ''
      this.searchForm.roomType = ''
      this.searchForm.status = ''
      this.searchForm.checkInDate = ''
      this.currentPage = 1
    },
    handlePageChange(page) {
      this.currentPage = page
    },
    viewDetail(order) {
      this.currentOrder = order
      this.detailDialogVisible = true
    },
    editOrder(order) {
      this.$message.info('编辑功能开发中')
    },
    cancelOrder(order) {
      this.$confirm('确认取消该订单吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = 'cancelled'
        this.$message.success('订单已取消')
      }).catch(() => {
        
      })
    }
  }
}
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: flex-end;
}
</style>
