<template>
  <div class="admin-orders">
    <div class="page-header">
      <h1>订单管理</h1>
      <p>琉璃吊坠生产流程管控</p>
    </div>
    
    <el-card class="table-card">
      <el-table :data="orders" stripe border style="width: 100%" :row-class-name="getRowClassName" ref="orderTable">
        <el-table-column prop="id" label="订单号" width="130">
          <template slot-scope="scope">
            {{ scope.row.id }}
          </template>
        </el-table-column>
        
        <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
        
        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
        
        <el-table-column label="色料" width="100">
          <template slot-scope="scope">
            <span class="color-dot" :style="{ backgroundColor: scope.row.color }"></span>
            {{ getColorLabel(scope.row.color) }}
          </template>
        </el-table-column>
        
        <el-table-column label="形状" width="80">
          <template slot-scope="scope">
            {{ getShapeLabel(scope.row.shape) }}
          </template>
        </el-table-column>
        
        <el-table-column label="尺寸" width="100">
          <template slot-scope="scope">
            {{ scope.row.length }}×{{ scope.row.width }}mm
          </template>
        </el-table-column>
        
        <el-table-column prop="createTime" label="下单时间" width="160"></el-table-column>
        
        <el-table-column label="生产状态" width="200">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" size="small" finish-status="success" direction="horizontal" class="mini-steps">
              <el-step v-for="(step, index) in statusSteps" :key="index" :title="step.short"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="220">
          <template slot-scope="scope">
            <el-button v-if="scope.row.status < statusSteps.length - 1" 
                       type="primary" size="small" @click="nextStep(scope.row)">
              下一工序: {{ statusSteps[scope.row.status + 1].label }}
            </el-button>
            <el-tag v-else type="success" size="small">已完工</el-tag>
            <el-button type="danger" size="small" @click="deleteOrder(scope.row)" style="margin-left: 5px;">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-if="orders.length === 0" description="暂无订单"></el-empty>
    </el-card>
    
    <el-dialog title="订单详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions v-if="currentOrder" :column="2" border>
        <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="琉璃色料">
          <span class="color-dot" :style="{ backgroundColor: currentOrder.color }"></span>
          {{ getColorLabel(currentOrder.color) }}
        </el-descriptions-item>
        <el-descriptions-item label="吊坠形状">{{ getShapeLabel(currentOrder.shape) }}</el-descriptions-item>
        <el-descriptions-item label="尺寸规格">{{ currentOrder.length }}×{{ currentOrder.width }}mm</el-descriptions-item>
        <el-descriptions-item label="内包花纹">{{ getPatternLabel(currentOrder.pattern) }}</el-descriptions-item>
        <el-descriptions-item label="挂扣类型">{{ getClaspLabel(currentOrder.clasp) }}</el-descriptions-item>
        <el-descriptions-item label="生产进度" :span="2">
          <el-steps :active="currentOrder.status" finish-status="success">
            <el-step v-for="(step, index) in statusSteps" :key="index" :title="step.label" :description="getStepDescription(currentOrder, index)"></el-step>
          </el-steps>
        </el-descriptions-item>
        <el-descriptions-item label="备注" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminOrders',
  mounted() {
    const newOrderId = this.$route.query.newOrderId
    if (newOrderId) {
      this.$nextTick(() => {
        this.scrollToOrder(parseInt(newOrderId))
      })
    }
  },
  data() {
    return {
      currentOperator: {
        id: 'OP001',
        name: '张师傅',
        role: '工艺师'
      },
      detailVisible: false,
      currentOrder: null,
      statusSteps: [
        { label: '配料', short: '配料', desc: '准备色料' },
        { label: '熔料', short: '熔料', desc: '高温熔化' },
        { label: '塑形', short: '塑形', desc: '成型加工' },
        { label: '退火', short: '退火', desc: '冷却处理' },
        { label: '冷加工', short: '冷加工', desc: '精细打磨' },
        { label: '打孔', short: '打孔', desc: '钻孔穿线' },
        { label: '抛光', short: '抛光', desc: '表面抛光' },
        { label: '完工', short: '完工', desc: '成品检验' }
      ],
      colorOptions: [
        { label: '宝石红', value: '#E74C3C' },
        { label: '天空蓝', value: '#3498DB' },
        { label: '翡翠绿', value: '#2ECC71' },
        { label: '皇家紫', value: '#9B59B6' },
        { label: '琥珀金', value: '#F39C12' },
        { label: '水晶透明', value: '#ECF0F1' }
      ],
      shapeOptions: [
        { label: '心形', value: 'heart' },
        { label: '圆形', value: 'circle' },
        { label: '椭圆形', value: 'oval' },
        { label: '水滴形', value: 'drop' },
        { label: '方形', value: 'square' },
        { label: '菱形', value: 'diamond' }
      ],
      patternOptions: [
        { label: '祥云纹', value: 'cloud' },
        { label: '莲花纹', value: 'lotus' },
        { label: '龙凤纹', value: 'dragon' },
        { label: '水波纹', value: 'wave' },
        { label: '无花纹', value: 'none' }
      ],
      claspOptions: [
        { label: '银质龙虾扣', value: 'silver_lobster' },
        { label: '金色弹簧扣', value: 'gold_spring' },
        { label: '玫瑰金卡扣', value: 'rose_gold' },
        { label: '编织绳结', value: 'rope' }
      ]
    }
  },
  computed: {
    orders() {
      return JSON.parse(localStorage.getItem('glassOrders') || '[]')
    }
  },
  methods: {
    getColorLabel(value) {
      const item = this.colorOptions.find(c => c.value === value)
      return item ? item.label : value
    },
    getShapeLabel(value) {
      const item = this.shapeOptions.find(s => s.value === value)
      return item ? item.label : value
    },
    getPatternLabel(value) {
      const item = this.patternOptions.find(p => p.value === value)
      return item ? item.label : value
    },
    getClaspLabel(value) {
      const item = this.claspOptions.find(c => c.value === value)
      return item ? item.label : value
    },
    getStepDescription(order, index) {
      if (order.statusTimestamps && order.statusTimestamps[index] && order.statusOperators && order.statusOperators[index]) {
        const operator = order.statusOperators[index]
        return `${order.statusTimestamps[index]} - ${operator.name}`
      }
      if (order.statusTimestamps && order.statusTimestamps[index]) {
        return order.statusTimestamps[index]
      }
      return this.statusSteps[index].desc
    },
    getRowClassName({ row }) {
      const newOrderId = this.$route.query.newOrderId
      if (newOrderId && row.id === parseInt(newOrderId)) {
        return 'new-order-row'
      }
      return ''
    },
    scrollToOrder(orderId) {
      const rows = document.querySelectorAll('.el-table__row')
      const index = this.orders.findIndex(o => o.id === orderId)
      if (index !== -1 && rows[index]) {
        rows[index].scrollIntoView({ behavior: 'smooth', block: 'center' })
        setTimeout(() => {
          this.$router.replace({ path: '/admin', query: {} })
        }, 2000)
      }
    },
    nextStep(order) {
      const nextStatus = order.status + 1
      const now = new Date().toLocaleString()
      const orders = this.orders.map(o => {
        if (o.id === order.id) {
          const statusTimestamps = o.statusTimestamps || {}
          const statusOperators = o.statusOperators || {}
          statusTimestamps[nextStatus] = now
          statusOperators[nextStatus] = { ...this.currentOperator, time: now }
          return { ...o, status: nextStatus, statusTimestamps, statusOperators }
        }
        return o
      })
      localStorage.setItem('glassOrders', JSON.stringify(orders))
      this.$message.success(`已进入下一工序: ${this.statusSteps[nextStatus].label}，操作人: ${this.currentOperator.name}`)
    },
    deleteOrder(order) {
      this.$confirm('确定要删除该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const orders = this.orders.filter(o => o.id !== order.id)
        localStorage.setItem('glassOrders', JSON.stringify(orders))
        this.$message.success('删除成功')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.admin-orders {
  padding: 20px;
}
.page-header {
  text-align: center;
  margin-bottom: 30px;
}
.page-header h1 {
  color: #333;
  margin-bottom: 10px;
}
.page-header p {
  color: #666;
}
.table-card {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.color-dot {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 5px;
  vertical-align: middle;
  border: 1px solid #ddd;
}
.mini-steps {
  transform: scale(0.8);
  transform-origin: left center;
}
.new-order-row {
  background-color: #e6f7ff !important;
  animation: highlight 2s ease-in-out;
}
@keyframes highlight {
  0% {
    background-color: #bae7ff;
  }
  50% {
    background-color: #91d5ff;
  }
  100% {
    background-color: #e6f7ff;
  }
}
</style>
