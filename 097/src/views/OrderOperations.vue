<template>
  <div class="order-operations-container">
    <div class="action-bar">
      <el-button type="primary" icon="el-icon-plus" @click="simulateNewOrder">
        模拟新订单
      </el-button>
      <el-switch v-model="autoReminder" active-text="自动提醒" @change="toggleAutoReminder"></el-switch>
    </div>
    
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="operation-card">
          <div slot="header" class="card-header">
            <span>待接单订单</span>
            <el-badge :value="pendingOrders.length" class="item" type="danger">
              <span style="font-size: 14px; color: #909399;">新订单</span>
            </el-badge>
          </div>
          <div class="order-list" ref="pendingList">
            <div v-for="order in pendingOrders" :key="order.id" class="order-item" :class="{ 'new-order-highlight': order.isNew }">
              <div class="order-header">
                <span class="order-id">{{ order.id }}</span>
                <el-tag type="warning">{{ orderTypeMap[order.type] }}</el-tag>
              </div>
              <div class="order-info">
                <p><i class="el-icon-user"></i> {{ order.customerName }} ({{ order.phone }})</p>
                <p><i class="el-icon-location-outline"></i> {{ order.address }}</p>
                <p v-if="order.remark"><i class="el-icon-document"></i> 备注：{{ order.remark }}</p>
              </div>
              <div class="order-dishes">
                <div v-for="(dish, index) in order.dishes" :key="index" class="dish-item">
                  <span>{{ dish.name }} x {{ dish.quantity }}</span>
                  <span>¥{{ dish.price * dish.quantity }}</span>
                </div>
              </div>
              <div class="order-footer">
                <span class="total-price">总计：¥{{ order.totalPrice }}</span>
                <el-button type="primary" size="small" icon="el-icon-check" @click="handleAccept(order)">接单</el-button>
              </div>
            </div>
            <el-empty v-if="pendingOrders.length === 0" description="暂无待接单订单"></el-empty>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card class="operation-card">
          <div slot="header" class="card-header">
            <span>制作中订单</span>
            <el-badge :value="cookingOrders.length" class="item">
              <span style="font-size: 14px; color: #909399;">进行中</span>
            </el-badge>
          </div>
          <div class="order-list">
            <div v-for="order in cookingOrders" :key="order.id" class="order-item">
              <div class="order-header">
                <span class="order-id">{{ order.id }}</span>
                <el-tag type="primary">已接单</el-tag>
              </div>
              <div class="order-info">
                <p><i class="el-icon-user"></i> {{ order.customerName }} ({{ order.phone }})</p>
                <p><i class="el-icon-location-outline"></i> {{ order.address }}</p>
              </div>
              <div class="order-dishes">
                <div v-for="(dish, index) in order.dishes" :key="index" class="dish-item">
                  <span>{{ dish.name }} x {{ dish.quantity }}</span>
                </div>
              </div>
              <div class="order-footer">
                <el-button type="success" size="small" icon="el-icon-thumb" @click="handleStartCooking(order)" v-if="order.status === 2">开始制作</el-button>
                <el-button type="warning" size="small" icon="el-icon-check" @click="handleComplete(order)" v-if="order.status === 3">制作完成</el-button>
              </div>
            </div>
            <el-empty v-if="cookingOrders.length === 0" description="暂无进行中订单"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <div slot="header" class="card-header">
            <span>待配送订单</span>
          </div>
          <div class="order-list horizontal">
            <div v-for="order in readyOrders" :key="order.id" class="order-item horizontal">
              <div class="order-main">
                <div class="order-header">
                  <span class="order-id">{{ order.id }}</span>
                  <el-tag type="success">待配送</el-tag>
                </div>
                <div class="order-info">
                  <p><i class="el-icon-user"></i> {{ order.customerName }} ({{ order.phone }})</p>
                  <p><i class="el-icon-location-outline"></i> {{ order.address }}</p>
                </div>
                <div class="order-dishes">
                  <span v-for="(dish, index) in order.dishes" :key="index" class="dish-tag">
                    {{ dish.name }} x {{ dish.quantity }}
                  </span>
                </div>
              </div>
              <div class="order-action">
                <el-button type="primary" size="medium" icon="el-icon-sell" @click="handleDeliver(order)">配送完成</el-button>
              </div>
            </div>
            <el-empty v-if="readyOrders.length === 0" description="暂无待配送订单"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog title="新订单提醒" :visible.sync="newOrderDialogVisible" width="500px" @close="closeNewOrderDialog" class="new-order-dialog">
      <div class="new-order-content">
        <div class="new-order-icon">
          <i class="el-icon-bell"></i>
        </div>
        <h3>您有新的订单，请及时处理！</h3>
        <el-descriptions :column="1" border v-if="latestOrder">
          <el-descriptions-item label="订单号">{{ latestOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="顾客姓名">{{ latestOrder.customerName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ latestOrder.phone }}</el-descriptions-item>
          <el-descriptions-item label="收货地址">{{ latestOrder.address }}</el-descriptions-item>
          <el-descriptions-item label="订单金额">
            <span style="color: #f56c6c; font-weight: bold;">¥{{ latestOrder.totalPrice }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="订单类型">
            <el-tag :type="latestOrder.type === 1 ? 'success' : 'primary'">{{ orderTypeMap[latestOrder.type] }}</el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div class="new-order-dishes" v-if="latestOrder">
          <h4>订单菜品：</h4>
          <ul>
            <li v-for="(dish, index) in latestOrder.dishes" :key="index">
              {{ dish.name }} x {{ dish.quantity }}
            </li>
          </ul>
        </div>
      </div>
      <div slot="footer" class="dialog-footer">
        <el-button @click="newOrderDialogVisible = false">稍后处理</el-button>
        <el-button type="primary" @click="handleQuickAccept">立即接单</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockOrders, orderTypeMap } from '../data/mockData'

export default {
  name: 'OrderOperations',
  data() {
    return {
      orders: [],
      orderTypeMap,
      newOrderDialogVisible: false,
      latestOrder: null,
      autoReminder: true,
      audioContext: null,
      orderCounter: 6,
      simulatedCustomerNames: ['王小明', '李小红', '张大山', '刘美丽', '陈建国', '赵秀兰', '孙志强', '周文静'],
      simulatedAddresses: [
        '北京市朝阳区建国路88号',
        '北京市海淀区中关村大街1号',
        '北京市西城区金融街10号',
        '北京市东城区王府井大街20号',
        '北京市丰台区南三环西路50号'
      ],
      simulatedDishes: [
        { name: '宫保鸡丁', price: 38 },
        { name: '麻婆豆腐', price: 28 },
        { name: '凉拌黄瓜', price: 18 },
        { name: '西红柿鸡蛋汤', price: 15 },
        { name: '米饭', price: 3 },
        { name: '可乐', price: 5 }
      ]
    }
  },
  computed: {
    pendingOrders() {
      return this.orders.filter(order => order.status === 1)
    },
    cookingOrders() {
      return this.orders.filter(order => order.status === 2 || order.status === 3)
    },
    readyOrders() {
      return this.orders.filter(order => order.status === 4)
    }
  },
  created() {
    this.orders = [...mockOrders]
    this.initAudio()
  },
  beforeDestroy() {
    if (this.audioContext) {
      this.audioContext.close()
    }
  },
  methods: {
    initAudio() {
      try {
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)()
      } catch (e) {
        console.log('Web Audio API is not supported')
      }
    },
    playNotificationSound() {
      if (!this.audioContext) {
        this.initAudio()
      }
      if (!this.audioContext) return
      
      const oscillator = this.audioContext.createOscillator()
      const gainNode = this.audioContext.createGain()
      
      oscillator.connect(gainNode)
      gainNode.connect(this.audioContext.destination)
      
      oscillator.frequency.setValueAtTime(880, this.audioContext.currentTime)
      oscillator.type = 'sine'
      
      gainNode.gain.setValueAtTime(0.3, this.audioContext.currentTime)
      gainNode.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5)
      
      oscillator.start(this.audioContext.currentTime)
      oscillator.stop(this.audioContext.currentTime + 0.5)
      
      setTimeout(() => {
        const osc2 = this.audioContext.createOscillator()
        const gain2 = this.audioContext.createGain()
        osc2.connect(gain2)
        gain2.connect(this.audioContext.destination)
        osc2.frequency.setValueAtTime(1100, this.audioContext.currentTime)
        osc2.type = 'sine'
        gain2.gain.setValueAtTime(0.3, this.audioContext.currentTime)
        gain2.gain.exponentialRampToValueAtTime(0.01, this.audioContext.currentTime + 0.5)
        osc2.start(this.audioContext.currentTime)
        osc2.stop(this.audioContext.currentTime + 0.5)
      }, 200)
    },
    showNewOrderNotification(order) {
      this.latestOrder = order
      this.newOrderDialogVisible = true
      this.playNotificationSound()
      
      if (this.autoReminder) {
        this.$notify({
          title: '新订单提醒',
          message: `订单号：${order.id}，金额：¥${order.totalPrice}`,
          type: 'warning',
          duration: 5000,
          position: 'top-right'
        })
      }
    },
    simulateNewOrder() {
      const randomName = this.simulatedCustomerNames[Math.floor(Math.random() * this.simulatedCustomerNames.length)]
      const randomAddress = this.simulatedAddresses[Math.floor(Math.random() * this.simulatedAddresses.length)]
      const dishCount = Math.floor(Math.random() * 3) + 1
      const selectedDishes = []
      let totalPrice = 0
      
      for (let i = 0; i < dishCount; i++) {
        const dish = this.simulatedDishes[Math.floor(Math.random() * this.simulatedDishes.length)]
        const quantity = Math.floor(Math.random() * 2) + 1
        selectedDishes.push({ ...dish, quantity })
        totalPrice += dish.price * quantity
      }
      
      const newOrder = {
        id: `ORD${new Date().getFullYear()}${String(new Date().getMonth() + 1).padStart(2, '0')}${String(new Date().getDate()).padStart(2, '0')}${String(this.orderCounter).padStart(4, '0')}`,
        customerName: randomName,
        phone: `13${Math.floor(Math.random() * 1000000000).toString().padStart(9, '0')}`,
        address: randomAddress,
        totalPrice: totalPrice,
        status: 1,
        type: Math.random() > 0.5 ? 1 : 2,
        remark: Math.random() > 0.7 ? '少放辣' : '',
        createTime: new Date().toLocaleString(),
        dishes: selectedDishes,
        isNew: true
      }
      
      this.orderCounter++
      this.orders.unshift(newOrder)
      this.showNewOrderNotification(newOrder)
      this.$bus.$emit('newOrderReceived', newOrder)
      
      this.$nextTick(() => {
        const pendingList = this.$refs.pendingList
        if (pendingList) {
          pendingList.scrollTop = 0
        }
      })
      
      setTimeout(() => {
        newOrder.isNew = false
      }, 5000)
    },
    toggleAutoReminder(value) {
      this.autoReminder = value
      this.$message.success(value ? '已开启自动提醒' : '已关闭自动提醒')
    },
    closeNewOrderDialog() {
      this.latestOrder = null
    },
    handleQuickAccept() {
      if (this.latestOrder) {
        this.handleAccept(this.latestOrder)
        this.newOrderDialogVisible = false
      }
    },
    handleAccept(order) {
      this.$confirm('确认接单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = 2
        order.isNew = false
        this.$message.success('接单成功')
        this.$bus.$emit('orderStatusChanged', order.id)
      }).catch(() => {})
    },
    handleStartCooking(order) {
      order.status = 3
      this.$message.success('已开始制作')
      this.$bus.$emit('orderStatusChanged', order.id)
    },
    handleComplete(order) {
      this.$confirm('确认制作完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = 4
        this.$message.success('制作完成，等待配送')
        this.$bus.$emit('orderStatusChanged', order.id)
      }).catch(() => {})
    },
    handleDeliver(order) {
      this.$confirm('确认配送完成吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = 5
        this.$message.success('订单已完成')
        this.$bus.$emit('orderStatusChanged', order.id)
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-operations-container {
  padding: 0;
}

.action-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.new-order-content {
  text-align: center;
}

.new-order-icon {
  font-size: 60px;
  color: #e6a23c;
  margin-bottom: 15px;
  animation: shake 0.5s ease-in-out infinite;
}

@keyframes shake {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-15deg); }
  75% { transform: rotate(15deg); }
}

.new-order-content h3 {
  margin: 0 0 20px 0;
  color: #f56c6c;
  font-size: 20px;
}

.new-order-dishes {
  margin-top: 15px;
  text-align: left;
}

.new-order-dishes h4 {
  margin: 0 0 10px 0;
  color: #606266;
}

.new-order-dishes ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.new-order-dishes li {
  padding: 5px 0;
  border-bottom: 1px dashed #dcdfe6;
  color: #606266;
}

.new-order-dishes li:last-child {
  border-bottom: none;
}

.new-order-highlight {
  border: 2px solid #e6a23c !important;
  background-color: #fff7e6 !important;
  animation: orderPulse 2s ease-in-out infinite;
}

@keyframes orderPulse {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(230, 162, 60, 0.4);
  }
  50% {
    box-shadow: 0 0 0 10px rgba(230, 162, 60, 0);
  }
}

.operation-card {
  height: 500px;
  overflow-y: auto;
}

.order-list {
  max-height: 420px;
  overflow-y: auto;
}

.order-list.horizontal {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.order-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fafafa;
}

.order-item.horizontal {
  width: calc(50% - 8px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0;
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #dcdfe6;
}

.order-id {
  font-weight: bold;
  color: #409eff;
}

.order-info p {
  margin: 5px 0;
  color: #606266;
  font-size: 13px;
}

.order-dishes {
  margin: 10px 0;
  padding: 10px;
  background-color: #fff;
  border-radius: 4px;
}

.dish-item {
  display: flex;
  justify-content: space-between;
  padding: 3px 0;
  font-size: 13px;
}

.dish-tag {
  display: inline-block;
  padding: 2px 8px;
  margin: 2px;
  background-color: #ecf5ff;
  color: #409eff;
  border-radius: 4px;
  font-size: 12px;
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed #dcdfe6;
}

.total-price {
  font-size: 16px;
  font-weight: bold;
  color: #f56c6c;
}

.order-main {
  flex: 1;
}

.order-action {
  margin-left: 20px;
}
</style>