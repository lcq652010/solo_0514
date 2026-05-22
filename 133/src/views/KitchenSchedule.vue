<template>
  <div>
    <h2 class="page-title">后厨排菜</h2>
    
    <el-card style="margin-bottom: 20px;">
      <div slot="header" class="card-header">
        <i class="el-icon-menu" style="color: #409EFF;"></i>
        <span style="margin-left: 8px;">批量制作（相同菜品合并）</span>
        <el-button 
          size="mini" 
          type="primary" 
          style="float: right;"
          :disabled="mergedWaitingDishes.length === 0"
          @click="startAllCooking"
        >
          <i class="el-icon-video-play"></i> 一键开始制作
        </el-button>
      </div>
      <div class="merged-dish-list">
        <div 
          v-for="group in mergedWaitingDishes" 
          :key="group.name"
          class="merged-dish-card"
          :class="{ urgent: group.hasUrgent }"
        >
          <div class="merged-dish-header">
            <span class="merged-dish-name">{{ group.name }}</span>
            <el-tag size="mini" type="danger" v-if="group.hasUrgent">含加急</el-tag>
            <el-tag size="mini" type="primary">共{{ group.totalQuantity }}份</el-tag>
          </div>
          <div class="merged-dish-items">
            <div v-for="item in group.items" :key="item.itemId" class="merged-item">
              <span>{{ item.orderId }} - {{ item.tableNo }}桌 ×{{ item.quantity }}</span>
            </div>
          </div>
          <div class="merged-dish-actions">
            <el-button size="mini" type="primary" @click="startGroupCooking(group)">
              批量开始制作
            </el-button>
          </div>
        </div>
        <el-empty v-if="mergedWaitingDishes.length === 0" description="暂无待制作菜品" :image-size="60"></el-empty>
      </div>
    </el-card>
    
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="card">
          <div slot="header" class="card-header">
            <i class="el-icon-time" style="color: #909399;"></i>
            <span style="margin-left: 8px;">待制作</span>
            <el-badge :value="waitingDishes.length" class="item" style="float: right;"></el-badge>
          </div>
          <div class="dish-list">
            <div 
              v-for="item in waitingDishes" 
              :key="item.itemId" 
              class="dish-card"
              :class="{ urgent: item.urgency }"
              draggable="true"
              @dragstart="handleDragStart($event, item, 'waiting')"
            >
              <div class="dish-header">
                <span class="dish-name">{{ item.name }}</span>
                <el-tag size="mini" type="danger" v-if="item.urgency">加急</el-tag>
              </div>
              <div class="dish-info">
                <span><i class="el-icon-date"></i> {{ item.orderId }}</span>
                <span><i class="el-icon-location-outline"></i> {{ item.tableNo }}</span>
                <span><i class="el-icon-goods"></i> ×{{ item.quantity }}</span>
              </div>
              <div class="dish-remark" v-if="item.remark">
                <i class="el-icon-chat-dot-round"></i> {{ item.remark }}
              </div>
              <div class="dish-actions">
                <el-button size="mini" type="primary" @click="startCooking(item)">
                  开始制作
                </el-button>
              </div>
            </div>
            <el-empty v-if="waitingDishes.length === 0" description="暂无待制作菜品" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="card">
          <div slot="header" class="card-header">
            <i class="el-icon-loading" style="color: #409EFF;"></i>
            <span style="margin-left: 8px;">制作中</span>
            <el-badge :value="cookingDishes.length" class="item" type="primary" style="float: right;"></el-badge>
          </div>
          <div class="dish-list">
            <div 
              v-for="item in cookingDishes" 
              :key="item.itemId" 
              class="dish-card cooking"
              draggable="true"
              @dragstart="handleDragStart($event, item, 'cooking')"
            >
              <div class="dish-header">
                <span class="dish-name">{{ item.name }}</span>
                <el-tag size="mini" type="danger" v-if="item.urgency">加急</el-tag>
              </div>
              <div class="dish-info">
                <span><i class="el-icon-date"></i> {{ item.orderId }}</span>
                <span><i class="el-icon-location-outline"></i> {{ item.tableNo }}</span>
                <span><i class="el-icon-goods"></i> ×{{ item.quantity }}</span>
              </div>
              <div class="dish-remark" v-if="item.remark">
                <i class="el-icon-chat-dot-round"></i> {{ item.remark }}
              </div>
              <div class="cooking-progress">
                <el-progress :percentage="item.progress || 50" :stroke-width="8"></el-progress>
              </div>
              <div class="dish-actions">
                <el-button size="mini" type="success" @click="finishDish(item)">
                  制作完成
                </el-button>
              </div>
            </div>
            <el-empty v-if="cookingDishes.length === 0" description="暂无制作中菜品" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="card">
          <div slot="header" class="card-header">
            <i class="el-icon-check" style="color: #67c23a;"></i>
            <span style="margin-left: 8px;">已完成</span>
            <el-badge :value="doneDishes.length" class="item" type="success" style="float: right;"></el-badge>
          </div>
          <div class="dish-list">
            <div 
              v-for="item in doneDishes.slice(0, 10)" 
              :key="item.itemId" 
              class="dish-card done"
            >
              <div class="dish-header">
                <span class="dish-name">{{ item.name }}</span>
                <el-tag size="mini" type="success">已完成</el-tag>
              </div>
              <div class="dish-info">
                <span><i class="el-icon-date"></i> {{ item.orderId }}</span>
                <span><i class="el-icon-location-outline"></i> {{ item.tableNo }}</span>
                <span><i class="el-icon-goods"></i> ×{{ item.quantity }}</span>
              </div>
              <div class="finish-time">
                <i class="el-icon-time"></i> {{ item.finishTime || '刚刚' }}
              </div>
            </div>
            <el-empty v-if="doneDishes.length === 0" description="暂无已完成菜品" :image-size="80"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-card style="margin-top: 20px;">
      <div slot="header" class="card-header">
        <i class="el-icon-s-data"></i>
        <span style="margin-left: 8px;">今日统计</span>
      </div>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-number" style="color: #909399;">{{ totalDishes }}</div>
            <div class="stat-label">今日总菜品</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-number" style="color: #409EFF;">{{ cookingDishes.length }}</div>
            <div class="stat-label">制作中</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-number" style="color: #67c23a;">{{ doneDishes.length }}</div>
            <div class="stat-label">已完成</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <div class="stat-number" style="color: #f56c6c;">{{ urgentCount }}</div>
            <div class="stat-label">加急订单</div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { mockOrders } from '@/mock/data'

export default {
  name: 'KitchenSchedule',
  data() {
    return {
      orders: [],
      dragItem: null,
      dragFrom: ''
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
            quantity: item.quantity,
            status: item.status,
            remark: order.remark,
            urgency: order.urgency,
            progress: item.status === 'cooking' ? Math.floor(Math.random() * 50) + 30 : 0,
            finishTime: item.status === 'done' ? '刚刚' : null
          })
        })
      })
      return dishes.sort((a, b) => {
        if (a.urgency && !b.urgency) return -1
        if (!a.urgency && b.urgency) return 1
        return 0
      })
    },
    waitingDishes() {
      return this.allDishes.filter(d => d.status === 'waiting')
    },
    cookingDishes() {
      return this.allDishes.filter(d => d.status === 'cooking')
    },
    doneDishes() {
      return this.allDishes.filter(d => d.status === 'done')
    },
    totalDishes() {
      return this.allDishes.length
    },
    urgentCount() {
      return this.allDishes.filter(d => d.urgency && d.status !== 'done').length
    },
    mergedWaitingDishes() {
      const groups = {}
      this.waitingDishes.forEach(dish => {
        if (!groups[dish.name]) {
          groups[dish.name] = {
            name: dish.name,
            items: [],
            totalQuantity: 0,
            hasUrgent: false
          }
        }
        groups[dish.name].items.push(dish)
        groups[dish.name].totalQuantity += dish.quantity
        if (dish.urgency) {
          groups[dish.name].hasUrgent = true
        }
      })
      return Object.values(groups).sort((a, b) => {
        if (a.hasUrgent && !b.hasUrgent) return -1
        if (!a.hasUrgent && b.hasUrgent) return 1
        return 0
      })
    }
  },
  created() {
    this.orders = JSON.parse(JSON.stringify(mockOrders))
  },
  methods: {
    startGroupCooking(group) {
      group.items.forEach(item => {
        this.updateDishStatus(item, 'cooking')
      })
      this.$message.success(`批量开始制作：${group.name}（共${group.totalQuantity}份）`)
    },
    startAllCooking() {
      this.mergedWaitingDishes.forEach(group => {
        group.items.forEach(item => {
          this.updateDishStatus(item, 'cooking')
        })
      })
      this.$message.success('所有待制作菜品已开始制作！')
    },
    handleDragStart(event, item, from) {
      this.dragItem = item
      this.dragFrom = from
    },
    startCooking(item) {
      this.updateDishStatus(item, 'cooking')
      this.$message.success(`开始制作：${item.name}`)
    },
    finishDish(item) {
      this.updateDishStatus(item, 'done')
      const now = new Date()
      item.finishTime = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
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
    }
  }
}
</script>

<style scoped>
.merged-dish-list {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  padding: 10px;
}

.merged-dish-card {
  flex: 1;
  min-width: 300px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 15px;
  transition: all 0.3s;
}

.merged-dish-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.merged-dish-card.urgent {
  border-left: 4px solid #f56c6c;
  background: linear-gradient(to right, #fef0f0, #fff);
}

.merged-dish-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.merged-dish-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  flex: 1;
}

.merged-dish-items {
  margin-bottom: 12px;
}

.merged-item {
  padding: 5px 0;
  font-size: 13px;
  color: #606266;
  display: flex;
  align-items: center;
}

.merged-dish-actions {
  text-align: right;
}

.dish-list {
  min-height: 400px;
  max-height: 500px;
  overflow-y: auto;
  padding: 10px;
}

.dish-card {
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.dish-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.dish-card.urgent {
  border-left: 4px solid #f56c6c;
  background: linear-gradient(to right, #fef0f0, #fff);
}

.dish-card.cooking {
  border-left: 4px solid #409EFF;
  background: linear-gradient(to right, #ecf5ff, #fff);
}

.dish-card.done {
  border-left: 4px solid #67c23a;
  background: linear-gradient(to right, #f0f9eb, #fff);
  opacity: 0.8;
}

.dish-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dish-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.dish-info {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
}

.dish-remark {
  font-size: 12px;
  color: #f56c6c;
  background: #fef0f0;
  padding: 5px 10px;
  border-radius: 4px;
  margin-bottom: 10px;
}

.cooking-progress {
  margin: 10px 0;
}

.dish-actions {
  text-align: right;
}

.finish-time {
  font-size: 12px;
  color: #909399;
  text-align: right;
}

.stat-item {
  text-align: center;
  padding: 20px;
}

.stat-number {
  font-size: 36px;
  font-weight: 600;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
}
</style>
