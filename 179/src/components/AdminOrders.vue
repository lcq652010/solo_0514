<template>
  <div class="admin-container">
    <div class="page-header">
      <h2>订单管理中心</h2>
      <p>生产工序：选料 → 切料 → 粗胚 → 细磨 → 掏膛 → 精抛 → 质检 → 完工</p>
    </div>

    <el-card>
      <el-table :data="orders" border stripe style="width: 100%" ref="orderTable" :row-class-name="tableRowClassName">
        <el-table-column prop="id" label="订单号" width="150">
          <template slot-scope="scope">
            <div class="order-id-cell">
              <span>{{ scope.row.id }}</span>
              <el-badge v-if="isNewOrder(scope.row)" class="new-order-badge" value="NEW" type="success" effect="dark"></el-badge>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
        <el-table-column prop="jadeType" label="玉料种类" width="100"></el-table-column>
        <el-table-column prop="diameter" label="直径(mm)" width="90"></el-table-column>
        <el-table-column prop="thickness" label="厚度规格" width="140"></el-table-column>
        <el-table-column prop="carvingPattern" label="雕刻纹路" width="100"></el-table-column>
        <el-table-column prop="polishLevel" label="抛光等级" width="100"></el-table-column>
        <el-table-column label="生产进度" width="320">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" size="small">
              <el-step title="选料"></el-step>
              <el-step title="切料"></el-step>
              <el-step title="粗胚"></el-step>
              <el-step title="细磨"></el-step>
              <el-step title="掏膛"></el-step>
              <el-step title="精抛"></el-step>
              <el-step title="质检"></el-step>
              <el-step title="完工"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180"></el-table-column>
        <el-table-column label="操作" width="280">
          <template slot-scope="scope">
            <el-button 
              v-if="scope.row.status < 8" 
              type="primary" 
              size="small" 
              @click="nextStep(scope.row, scope.$index)"
            >
              下一工序
            </el-button>
            <el-tag v-else type="success" size="small">已完成</el-tag>
            <el-button 
              type="info" 
              size="small" 
              @click="showStatusHistory(scope.row)"
              style="margin-left: 5px"
            >
              进度记录
            </el-button>
            <el-button 
              type="danger" 
              size="small" 
              @click="deleteOrder(scope.$index)"
              style="margin-left: 5px"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>
    </el-card>

    <el-dialog title="工序进度记录" :visible.sync="historyDialogVisible" width="550px">
      <el-timeline>
        <el-timeline-item 
          v-for="(item, index) in currentHistory" 
          :key="index"
          :timestamp="item.time"
          placement="top"
        >
          <el-tag :type="getStatusType(index)" size="small">{{ getStatusName(item.status) }}</el-tag>
          <span style="margin-left: 10px">{{ item.remark }}</span>
          <el-tag v-if="item.operator" type="info" size="mini" style="margin-left: 10px">
            <i class="el-icon-user"></i> {{ item.operator }}
          </el-tag>
        </el-timeline-item>
      </el-timeline>
    </el-dialog>

    <el-dialog title="推进工序" :visible.sync="stepDialogVisible" width="400px" @close="stepDialogVisible = false">
      <el-form :model="stepForm" label-width="80px">
        <el-form-item label="当前工序">
          <el-tag type="info">{{ statusNames[currentOrder.status - 1] || '订单创建' }}</el-tag>
        </el-form-item>
        <el-form-item label="下一工序">
          <el-tag type="success">{{ statusNames[currentOrder.status] || '完工' }}</el-tag>
        </el-form-item>
        <el-form-item label="操作人员" prop="operator">
          <el-select v-model="stepForm.operator" placeholder="请选择操作人员" style="width: 100%">
            <el-option label="张师傅" value="张师傅"></el-option>
            <el-option label="李师傅" value="李师傅"></el-option>
            <el-option label="王师傅" value="王师傅"></el-option>
            <el-option label="赵师傅" value="赵师傅"></el-option>
            <el-option label="管理员" value="管理员"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="stepForm.remark" :rows="2" placeholder="可选备注信息"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="stepDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="confirmNextStep" :loading="stepLoading">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminOrders',
  data() {
    return {
      orders: [],
      historyDialogVisible: false,
      stepDialogVisible: false,
      currentHistory: [],
      currentOrder: {},
      currentIndex: -1,
      stepLoading: false,
      stepForm: {
        operator: '',
        remark: ''
      },
      newOrderId: null,
      statusNames: ['选料', '切料', '粗胚', '细磨', '掏膛', '精抛', '质检', '完工']
    }
  },
  mounted() {
    this.loadOrders()
    if (this.$route.query.newOrderId) {
      this.newOrderId = parseInt(this.$route.query.newOrderId)
      this.$nextTick(() => {
        this.scrollToNewOrder()
      })
    }
  },
  watch: {
    '$route.query.newOrderId'(newVal) {
      if (newVal) {
        this.newOrderId = parseInt(newVal)
        this.loadOrders()
        this.$nextTick(() => {
          this.scrollToNewOrder()
        })
      }
    }
  },
  methods: {
    loadOrders() {
      const orders = JSON.parse(localStorage.getItem('jadeOrders') || '[]')
      orders.forEach(order => {
        if (!order.statusHistory) {
          order.statusHistory = [
            { status: 0, time: order.createTime, remark: '订单创建' }
          ]
        }
      })
      this.orders = orders
    },
    scrollToNewOrder() {
      if (!this.newOrderId) return
      const index = this.orders.findIndex(o => o.id === this.newOrderId)
      if (index !== -1 && this.$refs.orderTable) {
        const table = this.$refs.orderTable.$el
        const rows = table.querySelectorAll('.el-table__row')
        if (rows[index]) {
          rows[index].scrollIntoView({ behavior: 'smooth', block: 'center' })
          this.$message.success('已定位到最新订单！')
        }
      }
    },
    tableRowClassName({ row }) {
      return row.id === this.newOrderId ? 'new-order-row' : ''
    },
    isNewOrder(order) {
      return order.id === this.newOrderId
    },
    nextStep(order, index) {
      if (order.status >= 8) {
        this.$message.warning('订单已完成，无法继续推进！')
        return
      }
      
      this.currentOrder = { ...order }
      this.currentIndex = index
      this.stepForm = {
        operator: '',
        remark: ''
      }
      this.stepDialogVisible = true
    },
    confirmNextStep() {
      if (!this.stepForm.operator) {
        this.$message.warning('请选择操作人员！')
        return
      }
      
      this.stepLoading = true
      const nextStatus = this.currentOrder.status + 1
      
      setTimeout(() => {
        this.orders[this.currentIndex].status = nextStatus
        
        if (!this.orders[this.currentIndex].statusHistory) {
          this.orders[this.currentIndex].statusHistory = []
        }
        
        this.orders[this.currentIndex].statusHistory.push({
          status: nextStatus,
          time: new Date().toLocaleString(),
          operator: this.stepForm.operator,
          remark: this.stepForm.remark || `推进到「${this.statusNames[nextStatus - 1] || '完成'}」工序`
        })
        
        localStorage.setItem('jadeOrders', JSON.stringify(this.orders))
        this.stepDialogVisible = false
        this.stepLoading = false
        this.$message.success('工序已更新！')
      }, 500)
    },
    showStatusHistory(order) {
      this.currentHistory = order.statusHistory || []
      this.historyDialogVisible = true
    },
    getStatusType(index) {
      const types = ['', 'primary', 'success', 'warning', 'danger', 'info']
      return types[index % types.length] || 'info'
    },
    getStatusName(status) {
      if (status === 0) return '订单创建'
      return this.statusNames[status - 1] || '未知工序'
    },
    deleteOrder(index) {
      this.$confirm('确认删除该订单？此操作不可撤销！', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orders.splice(index, 1)
        localStorage.setItem('jadeOrders', JSON.stringify(this.orders))
        this.$message.success('删除成功！')
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.admin-container {
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h2 {
  color: #409EFF;
  margin-bottom: 10px;
}

.page-header p {
  color: #606266;
}

.order-id-cell {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.new-order-badge {
  margin-right: 5px;
}

::v-deep .new-order-row {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  color: #fff !important;
  animation: gradientPulse 3s ease infinite;
}

::v-deep .new-order-row .el-tag,
::v-deep .new-order-row .el-button {
  filter: brightness(1.1);
}

::v-deep .new-order-row td {
  color: #fff !important;
  font-weight: 500;
}

@keyframes gradientPulse {
  0% { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  50% { 
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  }
  100% { 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
}

.dialog-footer {
  text-align: right;
}
</style>
