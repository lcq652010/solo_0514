<template>
  <div class="admin-page">
    <el-card class="admin-card" shadow="hover">
      <div slot="header" class="card-header">
        <span><i class="el-icon-s-order"></i> 订单管理</span>
        <el-button type="primary" size="small" @click="refreshOrders">
          <i class="el-icon-refresh"></i> 刷新
        </el-button>
      </div>

      <el-table :data="orders" border style="width: 100%" v-loading="loading">
        <el-table-column prop="orderNo" label="订单编号" width="160" align="center"></el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" align="center"></el-table-column>
        <el-table-column prop="bambooType" label="竹材种类" width="100" align="center"></el-table-column>
        <el-table-column label="印章尺寸" width="140" align="center">
          <template slot-scope="scope">
            直径{{ scope.row.diameter }}×高{{ scope.row.height }}mm
          </template>
        </el-table-column>
        <el-table-column prop="sealContent" label="印文内容" width="120" align="center" show-overflow-tooltip></el-table-column>
        <el-table-column prop="pattern" label="图案" width="100" align="center"></el-table-column>
        <el-table-column prop="fontType" label="字体" width="80" align="center"></el-table-column>
        <el-table-column prop="craft" label="工艺" width="100" align="center"></el-table-column>
        <el-table-column label="生产工序" align="center">
          <template slot-scope="scope">
            <el-steps :active="getStepIndex(scope.row.status)" finish-status="success" align-center size="small">
              <el-step title="选料"></el-step>
              <el-step title="裁切"></el-step>
              <el-step title="打磨"></el-step>
              <el-step title="设计"></el-step>
              <el-step title="雕刻"></el-step>
              <el-step title="上漆"></el-step>
              <el-step title="完工"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="160" align="center"></el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="viewDetail(scope.row)">
              <i class="el-icon-view"></i> 详情
            </el-button>
            <el-dropdown trigger="click" @command="(cmd) => updateStatus(scope.row, cmd)">
              <el-button type="primary" size="small" :disabled="scope.row.status === '完工'">
                <i class="el-icon-setting"></i> 更新工序 <i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item :command="'选料'" :disabled="!canUpdateTo(scope.row.status, '选料')">选料</el-dropdown-item>
                <el-dropdown-item :command="'裁切'" :disabled="!canUpdateTo(scope.row.status, '裁切')">裁切</el-dropdown-item>
                <el-dropdown-item :command="'打磨'" :disabled="!canUpdateTo(scope.row.status, '打磨')">打磨</el-dropdown-item>
                <el-dropdown-item :command="'设计'" :disabled="!canUpdateTo(scope.row.status, '设计')">设计</el-dropdown-item>
                <el-dropdown-item :command="'雕刻'" :disabled="!canUpdateTo(scope.row.status, '雕刻')">雕刻</el-dropdown-item>
                <el-dropdown-item :command="'上漆'" :disabled="!canUpdateTo(scope.row.status, '上漆')">上漆</el-dropdown-item>
                <el-dropdown-item :command="'完工'" :disabled="!canUpdateTo(scope.row.status, '完工')">完工</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0 && !loading" description="暂无订单数据"></el-empty>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailVisible" width="700px">
      <div v-if="currentOrder">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单编号" :span="2">{{ currentOrder.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
          <el-descriptions-item label="竹材种类">{{ currentOrder.bambooType }}</el-descriptions-item>
          <el-descriptions-item label="印章尺寸">直径{{ currentOrder.diameter }}×高{{ currentOrder.height }}mm</el-descriptions-item>
          <el-descriptions-item label="印文内容" :span="2">{{ currentOrder.sealContent }}</el-descriptions-item>
          <el-descriptions-item label="图案选择">{{ currentOrder.pattern }}</el-descriptions-item>
          <el-descriptions-item label="字体选择">{{ currentOrder.fontType }}</el-descriptions-item>
          <el-descriptions-item label="工艺选择">{{ currentOrder.craft }}</el-descriptions-item>
          <el-descriptions-item label="当前工序">
            <el-tag :type="getTagType(currentOrder.status)">{{ currentOrder.status }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
          <el-descriptions-item label="备注说明" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
        </el-descriptions>
        
        <div class="process-timeline">
          <h4 style="margin: 20px 0 10px; color: #606266;">生产进度</h4>
          <el-steps :active="getStepIndex(currentOrder.status)" finish-status="success" direction="vertical">
            <el-step title="选料" description="选择合适的竹材原料"></el-step>
            <el-step title="裁切" description="按尺寸裁切竹材毛坯"></el-step>
            <el-step title="打磨" description="精细打磨竹材表面"></el-step>
            <el-step title="设计" description="设计印文布局和样式"></el-step>
            <el-step title="雕刻" description="手工雕刻印文图案"></el-step>
            <el-step title="上漆" description="上漆保护，提升光泽"></el-step>
            <el-step title="完工" description="订单完成，准备交付"></el-step>
          </el-steps>
        </div>
        
        <div class="status-history">
          <h4 style="margin: 20px 0 10px; color: #606266;">操作历史记录</h4>
          <el-timeline>
            <el-timeline-item
              v-for="(item, index) in currentOrder.statusHistory"
              :key="index"
              :timestamp="item.time"
              placement="top"
            >
              <el-tag :type="getTagType(item.status)" size="small">{{ item.status }}</el-tag>
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminPage',
  data() {
    return {
      orders: [],
      loading: false,
      detailVisible: false,
      currentOrder: null,
      steps: ['选料', '裁切', '打磨', '设计', '雕刻', '上漆', '完工']
    }
  },
  created() {
    this.loadOrders()
    this.initSampleData()
    window.addEventListener('orderUpdated', this.handleOrderUpdated)
  },
  beforeDestroy() {
    window.removeEventListener('orderUpdated', this.handleOrderUpdated)
  },
  methods: {
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        this.orders = JSON.parse(localStorage.getItem('sealOrders') || '[]')
        this.loading = false
      }, 500)
    },
    handleOrderUpdated() {
      this.loadOrders()
    },
    refreshOrders() {
      this.loadOrders()
      this.$message.success('刷新成功')
    },
    getStepIndex(status) {
      return this.steps.indexOf(status)
    },
    canUpdateTo(currentStatus, targetStatus) {
      if (currentStatus === '完工') return false
      const currentIndex = this.getStepIndex(currentStatus)
      const targetIndex = this.getStepIndex(targetStatus)
      return targetIndex === currentIndex + 1
    },
    getTagType(status) {
      const typeMap = {
        '选料': 'info',
        '裁切': 'warning',
        '打磨': 'warning',
        '设计': 'primary',
        '雕刻': 'primary',
        '上漆': 'success',
        '完工': 'success'
      }
      return typeMap[status] || 'info'
    },
    viewDetail(order) {
      this.currentOrder = order
      this.detailVisible = true
    },
    updateStatus(order, newStatus) {
      this.$confirm(`确认将订单 ${order.orderNo} 的工序更新为"${newStatus}"吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.orders.findIndex(o => o.id === order.id)
        if (index !== -1) {
          const now = this.formatDate(new Date())
          this.orders[index].status = newStatus
          if (!this.orders[index].statusHistory) {
            this.orders[index].statusHistory = []
          }
          this.orders[index].statusHistory.push({
            status: newStatus,
            time: now
          })
          localStorage.setItem('sealOrders', JSON.stringify(this.orders))
          window.dispatchEvent(new CustomEvent('orderUpdated'))
          this.$message.success(`工序已更新为"${newStatus}"`)
        }
      }).catch(() => {
        this.$message.info('已取消操作')
      })
    },
    formatDate(date) {
      const y = date.getFullYear()
      const m = String(date.getMonth() + 1).padStart(2, '0')
      const d = String(date.getDate()).padStart(2, '0')
      const h = String(date.getHours()).padStart(2, '0')
      const min = String(date.getMinutes()).padStart(2, '0')
      return `${y}-${m}-${d} ${h}:${min}`
    },
    initSampleData() {
      const orders = JSON.parse(localStorage.getItem('sealOrders') || '[]')
      if (orders.length === 0) {
        const sampleOrders = [
          {
            id: Date.now() - 3,
            orderNo: 'SEAL20240001',
            customerName: '张三',
            phone: '13800138001',
            bambooType: '毛竹',
            diameter: 30,
            height: 60,
            sealContent: '宁静致远',
            pattern: '祥云瑞气',
            fontType: '小篆',
            craft: '手工雕刻',
            remark: '希望刻得深一些',
            status: '完工',
            createTime: '2024-01-15 10:30',
            statusHistory: [
              { status: '选料', time: '2024-01-15 10:30' },
              { status: '裁切', time: '2024-01-15 11:00' },
              { status: '打磨', time: '2024-01-15 14:00' },
              { status: '设计', time: '2024-01-15 15:30' },
              { status: '雕刻', time: '2024-01-16 09:00' },
              { status: '上漆', time: '2024-01-16 14:00' },
              { status: '完工', time: '2024-01-17 10:00' }
            ]
          },
          {
            id: Date.now() - 2,
            orderNo: 'SEAL20240002',
            customerName: '李四',
            phone: '13800138002',
            bambooType: '紫竹',
            diameter: 25,
            height: 50,
            sealContent: '上善若水',
            pattern: '梅兰竹菊',
            fontType: '大篆',
            craft: '阴刻工艺',
            remark: '',
            status: '雕刻',
            createTime: '2024-01-16 14:20',
            statusHistory: [
              { status: '选料', time: '2024-01-16 14:20' },
              { status: '裁切', time: '2024-01-16 15:00' },
              { status: '打磨', time: '2024-01-16 16:30' },
              { status: '设计', time: '2024-01-17 09:00' },
              { status: '雕刻', time: '2024-01-17 11:00' }
            ]
          },
          {
            id: Date.now() - 1,
            orderNo: 'SEAL20240003',
            customerName: '王五',
            phone: '13800138003',
            bambooType: '湘妃竹',
            diameter: 40,
            height: 80,
            sealContent: '厚德载物',
            pattern: '龙凤呈祥',
            fontType: '隶书',
            craft: '浮雕工艺',
            remark: '送给老师的礼物，麻烦做精致些',
            status: '设计',
            createTime: '2024-01-17 09:15',
            statusHistory: [
              { status: '选料', time: '2024-01-17 09:15' },
              { status: '裁切', time: '2024-01-17 10:00' },
              { status: '打磨', time: '2024-01-17 11:30' },
              { status: '设计', time: '2024-01-17 14:00' }
            ]
          }
        ]
        localStorage.setItem('sealOrders', JSON.stringify(sampleOrders))
        this.orders = sampleOrders
      }
    }
  }
}
</script>

<style scoped>
.admin-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.admin-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.card-header i {
  margin-right: 8px;
  color: #409EFF;
}

.process-timeline {
  margin-top: 20px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}
</style>
