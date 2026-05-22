<template>
  <div class="admin-panel-container">
    <el-card shadow="never">
      <div slot="header" class="card-header">
        <h2>订单管理</h2>
        <el-button type="primary" @click="goToOrder">新增订单</el-button>
      </div>

      <el-table :data="orders" border style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="订单编号" width="160" align="center"></el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column label="玉料信息" width="200" align="center">
          <template slot-scope="scope">
            <div>{{ getJadeLabel(scope.row.jadeType) }}</div>
            <div style="font-size: 12px; color: #999">
              {{ scope.row.outerDiameter }}mm × {{ scope.row.thickness }}mm
            </div>
          </template>
        </el-table-column>
        <el-table-column label="纹饰/挂绳" width="150" align="center">
          <template slot-scope="scope">
            <div>{{ getPatternLabel(scope.row.pattern) }}</div>
            <div style="font-size: 12px; color: #999">{{ getRopeLabel(scope.row.ropeStyle) }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180" align="center"></el-table-column>
        <el-table-column label="生产进度" align="center">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" align-center size="small" class="progress-steps">
              <el-step title="选料" v-tooltip="'选择玉料'"></el-step>
              <el-step title="切坯" v-tooltip="'切割坯料'"></el-step>
              <el-step title="粗磨" v-tooltip="'粗磨成型'"></el-step>
              <el-step title="打孔" v-tooltip="'打孔处理'"></el-step>
              <el-step title="精雕" v-tooltip="'精细雕刻'"></el-step>
              <el-step title="抛光" v-tooltip="'抛光处理'"></el-step>
              <el-step title="穿绳" v-tooltip="'穿挂绳'"></el-step>
              <el-step title="完工" v-tooltip="'订单完成'"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="viewDetail(scope.row)">详情</el-button>
            <el-button type="success" size="mini" @click="nextStep(scope.row)" :disabled="scope.row.status >= 8">
              下一工序
            </el-button>
            <el-button type="danger" size="mini" @click="deleteOrder(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailVisible" width="750px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="订单编号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentOrder.phone }}</el-descriptions-item>
        <el-descriptions-item label="收货地址" :span="2">{{ currentOrder.address }}</el-descriptions-item>
        <el-descriptions-item label="玉料种类">{{ getJadeLabel(currentOrder.jadeType) }}</el-descriptions-item>
        <el-descriptions-item label="规格尺寸">{{ currentOrder.outerDiameter }}mm × {{ currentOrder.thickness }}mm</el-descriptions-item>
        <el-descriptions-item label="雕刻纹饰">{{ getPatternLabel(currentOrder.pattern) }}</el-descriptions-item>
        <el-descriptions-item label="挂绳款式">{{ getRopeLabel(currentOrder.ropeStyle) }}</el-descriptions-item>
        <el-descriptions-item label="备注信息" :span="2">{{ currentOrder.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      
      <div v-if="currentOrder && currentOrder.stepHistory && currentOrder.stepHistory.length > 0" style="margin-top: 20px;">
        <h4 style="margin-bottom: 10px; color: #606266;">工序操作历史</h4>
        <el-timeline>
          <el-timeline-item
            v-for="(step, index) in currentOrder.stepHistory"
            :key="index"
            :timestamp="step.time"
            placement="top"
          >
            <div>
              <span style="font-weight: bold; color: #409EFF;">{{ step.stepName }}</span>
              <span style="margin-left: 10px; color: #909399;">操作人：{{ step.operator }}</span>
            </div>
          </el-timeline-item>
        </el-timeline>
      </div>
      
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminPanel',
  data() {
    return {
      loading: false,
      orders: [],
      detailVisible: false,
      currentOrder: null,
      jadeTypes: [
        { value: 'hetian', label: '和田玉' },
        { value: 'xiuyu', label: '岫玉' },
        { value: 'dushan', label: '独山玉' },
        { value: 'nanhong', label: '南红玛瑙' },
        { value: 'feicui', label: '翡翠' }
      ],
      patterns: [
        { value: 'plain', label: '素面无纹' },
        { value: 'yunwen', label: '云纹' },
        { value: 'huawen', label: '花纹' },
        { value: 'longwen', label: '龙纹' }
      ],
      ropeStyles: [
        { value: 'red', label: '中国红' },
        { value: 'black', label: '典雅黑' },
        { value: 'brown', label: '咖啡棕' },
        { value: 'green', label: '翡翠绿' }
      ],
      stepNames: ['选料', '切坯', '粗磨', '打孔', '精雕', '抛光', '穿绳', '完工'],
      currentOperator: '管理员'
    }
  },
  mounted() {
    this.loadOrders()
  },
  activated() {
    this.loadOrders()
  },
  methods: {
    loadOrders() {
      this.loading = true
      setTimeout(() => {
        this.orders = JSON.parse(localStorage.getItem('jadeOrders') || '[]')
        this.loading = false
      }, 300)
    },
    getJadeLabel(value) {
      const item = this.jadeTypes.find(t => t.value === value)
      return item ? item.label : value
    },
    getPatternLabel(value) {
      const item = this.patterns.find(t => t.value === value)
      return item ? item.label : value
    },
    getRopeLabel(value) {
      const item = this.ropeStyles.find(t => t.value === value)
      return item ? item.label : value
    },
    viewDetail(row) {
      this.currentOrder = row
      this.detailVisible = true
    },
    nextStep(row) {
      if (row.status < 8) {
        const nextStepName = this.stepNames[row.status]
        this.$confirm(`确定将订单 ${row.id} 推进到「${nextStepName}」工序吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          row.status++
          if (!row.stepHistory) {
            row.stepHistory = []
          }
          row.stepHistory.push({
            step: row.status,
            stepName: nextStepName,
            operator: this.currentOperator,
            time: new Date().toLocaleString()
          })
          this.saveOrders()
          this.$message.success(`已成功推进到「${nextStepName}」工序！`)
        }).catch(() => {})
      }
    },
    deleteOrder(index, row) {
      this.$confirm(`确定删除订单 ${row.id} 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orders.splice(index, 1)
        this.saveOrders()
        this.$message.success('订单删除成功！')
      }).catch(() => {})
    },
    saveOrders() {
      localStorage.setItem('jadeOrders', JSON.stringify(this.orders))
    },
    goToOrder() {
      this.$router.push('/order')
    }
  }
}
</script>

<style scoped>
.admin-panel-container {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  color: #8B4513;
  margin: 0;
}

.progress-steps {
  margin: 10px 0;
}

::v-deep .el-step__title {
  font-size: 12px;
}

.dialog-footer {
  text-align: center;
}
</style>
