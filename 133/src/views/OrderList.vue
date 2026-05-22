<template>
  <div>
    <h2 class="page-title">订单菜品列表</h2>
    
    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="订单号">
          <el-input v-model="searchForm.orderId" placeholder="请输入订单号" clearable></el-input>
        </el-form-item>
        <el-form-item label="桌号">
          <el-input v-model="searchForm.tableNo" placeholder="请输入桌号" clearable></el-input>
        </el-form-item>
        <el-form-item label="订单状态">
          <el-select v-model="searchForm.status" placeholder="请选择" clearable>
            <el-option label="全部" value=""></el-option>
            <el-option label="等待中" value="waiting"></el-option>
            <el-option label="制作中" value="cooking"></el-option>
            <el-option label="已完成" value="done"></el-option>
            <el-option label="加急" value="urgent"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="showAddDialog = true">新增订单</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-card>
      <el-table :data="filteredOrders" border stripe style="width: 100%">
        <el-table-column prop="id" label="订单号" width="120" sortable></el-table-column>
        <el-table-column prop="tableNo" label="桌号" width="80">
          <template slot-scope="scope">
            <el-tag type="info">{{ scope.row.tableNo }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="customerName" label="顾客姓名" width="100"></el-table-column>
        <el-table-column prop="orderTime" label="下单时间" width="180"></el-table-column>
        <el-table-column label="菜品详情" min-width="250">
          <template slot-scope="scope">
            <div v-for="item in scope.row.items" :key="item.id" style="margin-bottom: 5px;">
              <span>{{ item.name }} × {{ item.quantity }}</span>
              <el-tag :type="getStatusType(item.status)" size="mini" style="margin-left: 10px;">
                {{ getStatusText(item.status) }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="remark" label="备注" width="150" show-overflow-tooltip></el-table-column>
        <el-table-column label="订单状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getOrderStatusType(scope.row)" size="small">
              {{ getOrderStatusText(scope.row) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">查看</el-button>
            <el-button size="mini" type="warning" @click="handleUrgent(scope.row)" v-if="!scope.row.urgency">
              催单
            </el-button>
            <el-button size="mini" type="danger" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div style="margin-top: 20px; text-align: right;">
        <el-pagination
          :total="filteredOrders.length"
          :page-size="10"
          layout="total, prev, pager, next, jumper"
        ></el-pagination>
      </div>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="桌号">{{ currentOrder.tableNo }}</el-descriptions-item>
        <el-descriptions-item label="顾客姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.orderTime }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <el-table :data="currentOrder?.items || []" border style="margin-top: 20px;">
        <el-table-column prop="name" label="菜品名称"></el-table-column>
        <el-table-column prop="category" label="分类" width="100"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
        <el-table-column prop="price" label="单价" width="80"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>

    <el-dialog title="新增订单" :visible.sync="showAddDialog" width="700px">
      <el-form :model="newOrder" :rules="rules" ref="orderForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="桌号" prop="tableNo">
              <el-input v-model="newOrder.tableNo" placeholder="请输入桌号"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="顾客姓名" prop="customerName">
              <el-input v-model="newOrder.customerName" placeholder="请输入顾客姓名"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="选择菜品">
          <div v-for="(dish, index) in newOrder.items" :key="index" style="margin-bottom: 10px; display: flex; align-items: center;">
            <el-select v-model="dish.dishId" placeholder="选择菜品" style="width: 200px; margin-right: 10px;" @change="onDishChange(index)">
              <el-option v-for="d in dishList" :key="d.id" :label="d.name" :value="d.id"></el-option>
            </el-select>
            <el-input-number v-model="dish.quantity" :min="1" :max="10" style="margin-right: 10px;"></el-input-number>
            <el-button type="danger" icon="el-icon-delete" circle @click="removeDish(index)"></el-button>
          </div>
          <el-button type="primary" icon="el-icon-plus" @click="addDish" style="margin-top: 10px;">添加菜品</el-button>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="newOrder.remark" :rows="3" placeholder="请输入备注信息"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="submitOrder">提交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockOrders, dishes } from '@/mock/data'

export default {
  name: 'OrderList',
  data() {
    return {
      orders: [],
      dishList: dishes,
      searchForm: {
        orderId: '',
        tableNo: '',
        status: ''
      },
      detailDialogVisible: false,
      showAddDialog: false,
      currentOrder: null,
      newOrder: {
        tableNo: '',
        customerName: '',
        items: [{ dishId: '', quantity: 1 }],
        remark: ''
      },
      rules: {
        tableNo: [
          { required: true, message: '请输入桌号', trigger: 'blur' }
        ],
        customerName: [
          { required: true, message: '请输入顾客姓名', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => {
        const matchId = !this.searchForm.orderId || order.id.includes(this.searchForm.orderId)
        const matchTable = !this.searchForm.tableNo || order.tableNo.includes(this.searchForm.tableNo)
        const matchStatus = !this.searchForm.status || order.status === this.searchForm.status
        return matchId && matchTable && matchStatus
      })
    }
  },
  created() {
    this.orders = JSON.parse(JSON.stringify(mockOrders))
  },
  methods: {
    handleSearch() {
      this.$message.success('搜索完成')
    },
    handleReset() {
      this.searchForm = {
        orderId: '',
        tableNo: '',
        status: ''
      }
    },
    handleView(row) {
      this.currentOrder = row
      this.detailDialogVisible = true
    },
    handleUrgent(row) {
      this.$confirm('确认催单吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.urgency = true
        row.status = 'urgent'
        this.$message.success('催单成功')
      }).catch(() => {})
    },
    handleDelete(row) {
      this.$confirm('确认删除该订单吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.orders.findIndex(o => o.id === row.id)
        if (index > -1) {
          this.orders.splice(index, 1)
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    getStatusType(status) {
      const map = { waiting: 'info', cooking: 'primary', done: 'success' }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = { waiting: '等待中', cooking: '制作中', done: '已完成' }
      return map[status] || status
    },
    getOrderStatusType(row) {
      if (row.urgency) return 'danger'
      const map = { waiting: 'info', cooking: 'primary', done: 'success' }
      return map[row.status] || 'info'
    },
    getOrderStatusText(row) {
      if (row.urgency) return '加急'
      const map = { waiting: '等待中', cooking: '制作中', done: '已完成' }
      return map[row.status] || row.status
    },
    addDish() {
      this.newOrder.items.push({ dishId: '', quantity: 1 })
    },
    removeDish(index) {
      if (this.newOrder.items.length > 1) {
        this.newOrder.items.splice(index, 1)
      } else {
        this.$message.warning('至少需要选择一个菜品')
      }
    },
    onDishChange(index) {
      const dish = this.dishList.find(d => d.id === this.newOrder.items[index].dishId)
      if (dish) {
        this.newOrder.items[index].name = dish.name
        this.newOrder.items[index].price = dish.price
        this.newOrder.items[index].category = dish.category
      }
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const validItems = this.newOrder.items.filter(item => item.dishId && item.name)
          if (validItems.length === 0) {
            this.$message.error('请至少选择一个菜品')
            return
          }
          
          const newId = 'ORD' + String(this.orders.length + 1).padStart(3, '0')
          const now = new Date()
          const orderTime = now.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
          }).replace(/\//g, '-')
          
          const order = {
            id: newId,
            tableNo: this.newOrder.tableNo,
            customerName: this.newOrder.customerName,
            orderTime: orderTime,
            status: 'waiting',
            items: validItems.map((item, idx) => ({
              id: Date.now() + idx,
              name: item.name,
              quantity: item.quantity,
              price: item.price,
              status: 'waiting',
              category: item.category
            })),
            remark: this.newOrder.remark,
            urgency: false
          }
          
          this.orders.unshift(order)
          this.showAddDialog = false
          this.$message.success('订单添加成功')
          
          this.newOrder = {
            tableNo: '',
            customerName: '',
            items: [{ dishId: '', quantity: 1 }],
            remark: ''
          }
          this.$refs.orderForm.resetFields()
        }
      })
    }
  }
}
</script>

<style scoped>
</style>
