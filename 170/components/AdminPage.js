Vue.component('AdminPage', {
  props: ['orders', 'currentOperator'],
  template: `
    <div class="admin-page" ref="adminPage">
      <el-card class="admin-card">
        <div slot="header" class="card-header">
          <span>管理员 - 订单管理</span>
          <el-tag type="success" style="margin-left: 10px">共 {{ orders.length }} 个订单</el-tag>
          <el-tag v-if="currentOperator" type="info" style="margin-left: 10px">
            当前操作：{{ currentOperator }}
          </el-tag>
        </div>
        
        <el-table :data="orders" stripe border style="width: 100%" v-loading="!orders.length" ref="orderTable" row-key="id" :row-class-name="getRowClassName">
          <el-table-column label="状态" width="80">
            <template slot-scope="scope">
              <el-badge v-if="scope.row.isNew" value="新单" class="new-badge" type="danger">
                <span></span>
              </el-badge>
            </template>
          </el-table-column>
          
          <el-table-column prop="id" label="订单号" width="180" sortable>
            <template slot-scope="scope">
              <span style="color: #409EFF; font-weight: bold;">#{{ scope.row.id }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="customerName" label="客户" width="100"></el-table-column>
          
          <el-table-column label="麦秆等级" width="120">
            <template slot-scope="scope">
              <el-tag :type="getMaterialTagType(scope.row.materialLevel)">
                {{ scope.row.materialLevel }}级
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="尺寸" width="100">
            <template slot-scope="scope">
              {{ scope.row.width }} × {{ scope.row.height }} cm
            </template>
          </el-table-column>
          
          <el-table-column prop="style" label="题材" width="100"></el-table-column>
          
          <el-table-column label="工序进度" min-width="350">
            <template slot-scope="scope">
              <el-steps :active="scope.row.status" finish-status="success" size="small" align-center>
                <el-step title="选料"></el-step>
                <el-step title="熏蒸"></el-step>
                <el-step title="劈刮"></el-step>
                <el-step title="拼贴"></el-step>
                <el-step title="熨烫"></el-step>
                <el-step title="装裱"></el-step>
                <el-step title="质检"></el-step>
                <el-step title="完工"></el-step>
              </el-steps>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" fixed="right">
            <template slot-scope="scope">
              <el-button 
                v-if="scope.row.status < 8" 
                type="primary" 
                size="mini" 
                @click="nextStep(scope.row)"
              >
                下一工序
              </el-button>
              <el-button 
                v-if="scope.row.status > 0 && scope.row.status === getMaxReachedStatus(scope.row)" 
                type="warning" 
                size="mini" 
                @click="prevStep(scope.row)"
              >
                上一步
              </el-button>
              <el-button type="info" size="mini" @click="viewDetail(scope.row)">详情</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-if="!orders.length" description="暂无订单数据" style="padding: 50px 0;"></el-empty>
      </el-card>
      
      <el-dialog title="订单详情" :visible.sync="detailVisible" width="700px">
        <el-descriptions :column="2" border v-if="currentOrder">
          <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
          <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
          <el-descriptions-item label="麦秆等级">{{ currentOrder.materialLevel }}级</el-descriptions-item>
          <el-descriptions-item label="画面尺寸">{{ currentOrder.width }} × {{ currentOrder.height }} cm</el-descriptions-item>
          <el-descriptions-item label="题材风格">{{ currentOrder.style }}</el-descriptions-item>
          <el-descriptions-item label="裱框类型">{{ getFrameLabel(currentOrder.frameType) }}</el-descriptions-item>
          <el-descriptions-item label="加签名款">{{ currentOrder.withSignature ? '是' : '否' }}</el-descriptions-item>
          <el-descriptions-item label="当前工序">{{ getStatusLabel(currentOrder.status) }}</el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">{{ currentOrder.remarks || '无' }}</el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;" v-if="currentOrder && currentOrder.statusHistory">
          <h4 style="margin-bottom: 10px; color: #303133;">工序历史记录</h4>
          <el-timeline>
            <el-timeline-item 
              v-for="(item, index) in currentOrder.statusHistory" 
              :key="index"
              :timestamp="item.time"
              placement="top"
              :type="item.status === 8 ? 'success' : 'primary'"
            >
              <strong>{{ getStatusLabel(item.status) }}</strong>
              <span style="color: #909399; margin-left: 10px;">{{ item.remark }}</span>
              <el-tag v-if="item.operator" size="mini" type="info" style="margin-left: 10px;">
                {{ item.operator }}
              </el-tag>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      detailVisible: false,
      currentOrder: null,
      statusLabels: ['待开工', '选料', '熏蒸', '劈刮', '拼贴', '熨烫', '装裱', '质检', '完工'],
      frameLabels: {
        walnut: '实木框（胡桃木）',
        oak: '实木框（橡木）',
        aluminum: '铝合金框',
        none: '无框'
      }
    }
  },
  methods: {
    getMaterialTagType(level) {
      const types = { A: 'success', B: 'warning', C: 'info' }
      return types[level] || 'info'
    },
    getStatusLabel(status) {
      return this.statusLabels[status] || '未知'
    },
    getFrameLabel(type) {
      return this.frameLabels[type] || type
    },
    getMaxReachedStatus(order) {
      if (!order.statusHistory || order.statusHistory.length === 0) return 0
      return Math.max(...order.statusHistory.map(h => h.status))
    },
    getRowClassName({ row, rowIndex }) {
      if (row.isNew) {
        return 'new-order-row'
      }
      return ''
    },
    nextStep(order) {
      if (order.status < 8) {
        const newStatus = order.status + 1
        const historyItem = {
          status: newStatus,
          time: new Date().toLocaleString(),
          remark: `进入${this.getStatusLabel(newStatus)}工序`,
          operator: this.currentOperator || '未登录'
        }
        this.$emit('update-status', order.id, newStatus, historyItem)
        this.$message.success(`已进入「${this.getStatusLabel(newStatus)}」工序`)
      }
    },
    prevStep(order) {
      if (order.status > 0) {
        const maxReached = this.getMaxReachedStatus(order)
        if (order.status !== maxReached) {
          this.$message.error('只能从当前最高工序回退，禁止跨工序回退！')
          return
        }
        const newStatus = order.status - 1
        const historyItem = {
          status: newStatus,
          time: new Date().toLocaleString(),
          remark: `从${this.getStatusLabel(order.status)}退回至${this.getStatusLabel(newStatus)}`,
          operator: this.currentOperator || '未登录'
        }
        this.$emit('update-status', order.id, newStatus, historyItem)
        this.$message.warning(`退回「${this.getStatusLabel(newStatus)}」工序`)
      }
    },
    viewDetail(order) {
      this.currentOrder = order
      order.isNew = false
      this.detailVisible = true
    },
    scrollToFirstRow() {
      this.$nextTick(() => {
        if (this.$refs.orderTable && this.$refs.orderTable.bodyWrapper) {
          this.$refs.orderTable.bodyWrapper.scrollTop = 0
        }
      })
    }
  },
  watch: {
    orders: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.scrollToFirstRow()
        }
      },
      deep: true
    }
  }
})
