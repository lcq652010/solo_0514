<template>
  <div>
    <h2 class="page-title">菜品制作状态</h2>
    
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <div class="summary-card waiting">
          <div class="summary-icon"><i class="el-icon-time"></i></div>
          <div class="summary-info">
            <div class="summary-num">{{ waitingCount }}</div>
            <div class="summary-text">等待制作</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="summary-card cooking">
          <div class="summary-icon"><i class="el-icon-loading"></i></div>
          <div class="summary-info">
            <div class="summary-num">{{ cookingCount }}</div>
            <div class="summary-text">正在制作</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="summary-card done">
          <div class="summary-icon"><i class="el-icon-check"></i></div>
          <div class="summary-info">
            <div class="summary-num">{{ doneCount }}</div>
            <div class="summary-text">制作完成</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="summary-card urgent">
          <div class="summary-icon"><i class="el-icon-warning"></i></div>
          <div class="summary-info">
            <div class="summary-num">{{ urgentCount }}</div>
            <div class="summary-text">加急订单</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-card>
      <div slot="header" class="table-header">
        <span>菜品列表</span>
        <el-button 
          size="mini" 
          type="primary" 
          @click="startAllWaiting"
          :disabled="waitingCount === 0"
        >
          <i class="el-icon-video-play"></i> 一键开始制作
        </el-button>
      </div>
      
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="订单类型">
          <el-select v-model="filterForm.urgency" placeholder="全部" clearable>
            <el-option label="普通订单" value="normal"></el-option>
            <el-option label="加急订单" value="urgent"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="制作状态">
          <el-select v-model="filterForm.status" placeholder="全部" clearable>
            <el-option label="等待制作" value="waiting"></el-option>
            <el-option label="正在制作" value="cooking"></el-option>
            <el-option label="制作完成" value="done"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="下单时间">
          <el-date-picker
            v-model="filterForm.dateRange"
            type="datetimerange"
            range-separator="至"
            start-placeholder="开始时间"
            end-placeholder="结束时间"
            format="yyyy-MM-dd HH:mm:ss"
            value-format="yyyy-MM-dd HH:mm:ss"
            style="width: 350px;"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="paginatedDishes" border stripe style="width: 100%; margin-top: 20px;">
        <el-table-column label="序号" type="index" width="60" align="center"></el-table-column>
        <el-table-column prop="orderId" label="订单号" width="100" sortable>
          <template slot-scope="scope">
            <el-tag size="mini" type="info">{{ scope.row.orderId }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="tableNo" label="桌号" width="80" align="center">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.tableNo }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="菜品名称" min-width="150">
          <template slot-scope="scope">
            <span style="font-weight: 500;">{{ scope.row.name }}</span>
            <el-tag size="mini" type="danger" v-if="scope.row.urgency" style="margin-left: 8px;">加急</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="100" align="center"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="80" align="center"></el-table-column>
        <el-table-column label="制作状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              <i :class="getStatusIcon(scope.row.status)" style="margin-right: 4px;"></i>
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="制作进度" width="150" align="center">
          <template slot-scope="scope">
            <el-progress 
              :percentage="scope.row.progress" 
              :status="getProgressStatus(scope.row.status)"
              :stroke-width="10"
            ></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="orderTime" label="下单时间" width="160" sortable></el-table-column>
        <el-table-column label="操作" width="180" align="center">
          <template slot-scope="scope">
            <el-button 
              size="mini" 
              type="primary" 
              @click="startCooking(scope.row)"
              v-if="scope.row.status === 'waiting'"
            >
              开始制作
            </el-button>
            <el-button 
              size="mini" 
              type="success" 
              @click="finishDish(scope.row)"
              v-if="scope.row.status === 'cooking'"
            >
              制作完成
            </el-button>
            <el-button 
              size="mini" 
              type="info" 
              @click="viewDetail(scope.row)"
            >
              查看详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredDishes.length"
        ></el-pagination>
      </div>
    </el-card>

    <el-dialog title="菜品详情" :visible.sync="detailVisible" width="500px">
      <el-descriptions :column="2" border v-if="currentDish">
        <el-descriptions-item label="菜品名称" :span="2">{{ currentDish.name }}</el-descriptions-item>
        <el-descriptions-item label="订单号">{{ currentDish.orderId }}</el-descriptions-item>
        <el-descriptions-item label="桌号">{{ currentDish.tableNo }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentDish.category }}</el-descriptions-item>
        <el-descriptions-item label="数量">{{ currentDish.quantity }}</el-descriptions-item>
        <el-descriptions-item label="下单时间" :span="2">{{ currentDish.orderTime }}</el-descriptions-item>
        <el-descriptions-item label="制作状态" :span="2">
          <el-tag :type="getStatusType(currentDish.status)">
            {{ getStatusText(currentDish.status) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentDish.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockOrders } from '@/mock/data'

export default {
  name: 'CookingStatus',
  data() {
    return {
      orders: [],
      activeTab: 'all',
      detailVisible: false,
      currentDish: null,
      filterForm: {
        urgency: '',
        status: '',
        dateRange: []
      },
      filterParams: {
        urgency: '',
        status: '',
        dateRange: []
      },
      pagination: {
        currentPage: 1,
        pageSize: 10
      }
    }
  },
  computed: {
    allDishes() {
      const dishes = []
      this.orders.forEach(order => {
        order.items.forEach(item => {
          dishes.push({
            itemId: `${order.id}-${item.id}`,
            orderId: order.id,
            tableNo: order.tableNo,
            name: item.name,
            category: item.category,
            quantity: item.quantity,
            status: item.status,
            remark: order.remark,
            urgency: order.urgency,
            orderTime: order.orderTime,
            progress: this.calculateProgress(item.status)
          })
        })
      })
      return dishes.sort((a, b) => {
        if (a.urgency && !b.urgency) return -1
        if (!a.urgency && b.urgency) return 1
        return new Date(a.orderTime) - new Date(b.orderTime)
      })
    },
    filteredDishes() {
      let result = [...this.allDishes]
      
      if (this.filterParams.urgency) {
        result = result.filter(d => {
          if (this.filterParams.urgency === 'urgent') return d.urgency
          return !d.urgency
        })
      }
      
      if (this.filterParams.status) {
        result = result.filter(d => d.status === this.filterParams.status)
      }
      
      if (this.filterParams.dateRange && this.filterParams.dateRange.length === 2) {
        const [start, end] = this.filterParams.dateRange
        result = result.filter(d => {
          const time = new Date(d.orderTime).getTime()
          return time >= new Date(start).getTime() && time <= new Date(end).getTime()
        })
      }
      
      return result
    },
    paginatedDishes() {
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return this.filteredDishes.slice(start, end)
    },
    waitingCount() {
      return this.allDishes.filter(d => d.status === 'waiting').length
    },
    cookingCount() {
      return this.allDishes.filter(d => d.status === 'cooking').length
    },
    doneCount() {
      return this.allDishes.filter(d => d.status === 'done').length
    },
    urgentCount() {
      return this.allDishes.filter(d => d.urgency && d.status !== 'done').length
    }
  },
  created() {
    this.orders = JSON.parse(JSON.stringify(mockOrders))
  },
  methods: {
    calculateProgress(status) {
      if (status === 'waiting') return 0
      if (status === 'done') return 100
      return Math.floor(Math.random() * 40) + 40
    },
    handleTabClick(tab) {
      console.log(tab.name)
    },
    getStatusType(status) {
      const map = { waiting: 'info', cooking: 'primary', done: 'success' }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = { waiting: '等待制作', cooking: '正在制作', done: '制作完成' }
      return map[status] || status
    },
    getStatusIcon(status) {
      const map = { waiting: 'el-icon-time', cooking: 'el-icon-loading', done: 'el-icon-check' }
      return map[status] || ''
    },
    getProgressStatus(status) {
      if (status === 'done') return 'success'
      return status === 'cooking' ? undefined : 'exception'
    },
    startCooking(item) {
      this.updateDishStatus(item, 'cooking')
      this.$message.success(`开始制作：${item.name}`)
    },
    finishDish(item) {
      this.updateDishStatus(item, 'done')
      this.$message.success(`制作完成：${item.name}`)
    },
    updateDishStatus(item, status) {
      for (let order of this.orders) {
        if (order.id === item.orderId) {
          const dish = order.items.find(i => `${order.id}-${i.id}` === item.itemId)
          if (dish) {
            dish.status = status
          }
          const allDone = order.items.every(i => i.status === 'done')
          const hasCooking = order.items.some(i => i.status === 'cooking')
          if (allDone) {
            order.status = 'done'
          } else if (hasCooking) {
            order.status = 'cooking'
          }
          break
        }
      }
    },
    viewDetail(item) {
      this.currentDish = item
      this.detailVisible = true
    },
    startAllWaiting() {
      const waitingDishes = this.allDishes.filter(d => d.status === 'waiting')
      waitingDishes.forEach(item => {
        this.updateDishStatus(item, 'cooking')
      })
      this.$message.success(`已批量开始 ${waitingDishes.length} 道菜品的制作`)
    },
    handleSearch() {
      this.filterParams = { ...this.filterForm }
      this.pagination.currentPage = 1
      this.$message.success('筛选完成')
    },
    handleReset() {
      this.filterForm = {
        urgency: '',
        status: '',
        dateRange: []
      }
      this.filterParams = { ...this.filterForm }
      this.pagination.currentPage = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.pagination.currentPage = 1
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    }
  }
}
</script>

<style scoped>
.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-form {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 10px 0;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}

.summary-card {
  display: flex;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  color: white;
}

.summary-card.waiting {
  background: linear-gradient(135deg, #909399 0%, #606266 100%);
}

.summary-card.cooking {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
}

.summary-card.done {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.summary-card.urgent {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}

.summary-icon {
  font-size: 40px;
  margin-right: 20px;
  opacity: 0.8;
}

.summary-info {
  flex: 1;
}

.summary-num {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 5px;
}

.summary-text {
  font-size: 14px;
  opacity: 0.9;
}
</style>
