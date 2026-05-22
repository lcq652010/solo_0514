<template>
  <div class="admin-page">
    <el-card>
      <div slot="header" class="card-header">
        <span>⚙️ 生产工序管理</span>
      </div>

      <div class="order-table-section">
        <el-table :data="orderList" border style="width: 100%;" @row-click="handleRowClick" ref="orderTable" :row-class-name="tableRowClassName">
          <el-table-column label="状态" width="80" align="center">
            <template slot-scope="scope">
              <div v-if="scope.row.orderNo === newOrderHighlight" class="new-order-badge">
                <span class="badge-text">NEW</span>
              </div>
              <el-tag v-else :type="getStepTagType(scope.row.currentStep)" size="mini">
                {{ getStepStatusText(scope.row.currentStep) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="orderNo" label="订单编号" width="140"></el-table-column>
          <el-table-column prop="bambooGrade" label="竹篾等级" width="180">
            <template slot-scope="scope">
              {{ getBambooGradeText(scope.row.bambooGrade) }}
            </template>
          </el-table-column>
          <el-table-column prop="height" label="高度(cm)" width="100"></el-table-column>
          <el-table-column prop="style" label="造型" width="120">
            <template slot-scope="scope">
              {{ getStyleText(scope.row.style) }}
            </template>
          </el-table-column>
          <el-table-column prop="currentStep" label="当前工序" width="150">
            <template slot-scope="scope">
              <el-tag :type="getStepType(scope.row.currentStep)">{{ steps[scope.row.currentStep] }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="orderTime" label="下单时间" width="180"></el-table-column>
          <el-table-column label="操作" width="200">
            <template slot-scope="scope">
              <el-button type="primary" size="small" @click.stop="nextStep(scope.row)" :disabled="scope.row.currentStep >= 7">
                下一工序
              </el-button>
              <el-button type="success" size="small" @click.stop="viewProcess(scope.row)">
                查看进度
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <el-dialog title="📊 生产工序进度" :visible.sync="processDialogVisible" width="900px">
      <div class="process-timeline">
        <el-steps :active="selectedOrder.currentStep" direction="vertical" finish-status="success">
          <el-step v-for="(step, index) in steps" :key="index" :title="step">
            <template slot="description">
              <div v-if="selectedOrder.processRecords && selectedOrder.processRecords[index]" class="record-info">
                <span style="color: #67C23A; font-weight: bold;">✓ 已完成</span>
                <div class="operator-info">
                  <div class="info-row">
                    <i class="el-icon-user" style="margin-right: 4px;"></i>
                    <span>操作人：{{ selectedOrder.processRecords[index].operatorName }} ({{ selectedOrder.processRecords[index].operator }})</span>
                  </div>
                  <div class="info-row">
                    <i class="el-icon-location-outline" style="margin-right: 4px;"></i>
                    <span>操作IP：{{ selectedOrder.processRecords[index].ip || '未知' }}</span>
                  </div>
                  <div class="info-row">
                    <i class="el-icon-time" style="margin-right: 4px;"></i>
                    <span>操作时间：{{ selectedOrder.processRecords[index].time }}</span>
                  </div>
                </div>
              </div>
              <span v-else-if="index === selectedOrder.currentStep" style="color: #409EFF;">⏳ 进行中</span>
              <span v-else style="color: #909399;">○ 待处理</span>
            </template>
          </el-step>
        </el-steps>
      </div>

      <div class="order-detail" style="margin-top: 30px;">
        <el-divider content-position="left">订单详情</el-divider>
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="订单编号">{{ selectedOrder.orderNo }}</el-descriptions-item>
          <el-descriptions-item label="下单时间">{{ selectedOrder.orderTime }}</el-descriptions-item>
          <el-descriptions-item label="竹篾等级">{{ getBambooGradeText(selectedOrder.bambooGrade) }}</el-descriptions-item>
          <el-descriptions-item label="笼体高度">{{ selectedOrder.height }} cm</el-descriptions-item>
          <el-descriptions-item label="编织密度">{{ getDensityText(selectedOrder.density) }}</el-descriptions-item>
          <el-descriptions-item label="造型款式">{{ getStyleText(selectedOrder.style) }}</el-descriptions-item>
          <el-descriptions-item label="底座配置" :span="2">{{ getBaseConfigText(selectedOrder.baseConfig) }}</el-descriptions-item>
        </el-descriptions>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="processDialogVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AdminPage',
  data() {
    return {
      steps: [
        '破篾',
        '防霉处理',
        '起底',
        '编织',
        '收口',
        '装配底座',
        '打磨',
        '完工'
      ],
      orderList: [
        {
          orderNo: 'BC17790250',
          bambooGrade: 'special',
          height: 30,
          density: 'normal',
          style: 'cylinder',
          baseConfig: ['wooden', 'lacquer'],
          currentStep: 3,
          orderTime: '2026/5/17 10:30:00',
          processRecords: [
            { step: 0, operator: 'admin', operatorName: '管理员', time: '2026/5/17 10:35:00', ip: '192.168.1.100' },
            { step: 1, operator: 'admin', operatorName: '管理员', time: '2026/5/17 11:00:00', ip: '192.168.1.100' },
            { step: 2, operator: 'admin', operatorName: '管理员', time: '2026/5/17 11:30:00', ip: '192.168.1.101' },
            { step: 3, operator: 'admin', operatorName: '管理员', time: '2026/5/17 14:00:00', ip: '192.168.1.101' }
          ],
          lastStep: 3
        },
        {
          orderNo: 'BC17790251',
          bambooGrade: 'first',
          height: 25,
          density: 'dense',
          style: 'hexagon',
          baseConfig: ['wooden', 'carving'],
          currentStep: 5,
          orderTime: '2026/5/17 11:15:00',
          processRecords: [
            { step: 0, operator: 'worker1', operatorName: '张师傅', time: '2026/5/17 11:20:00' },
            { step: 1, operator: 'worker1', operatorName: '张师傅', time: '2026/5/17 11:45:00' },
            { step: 2, operator: 'worker1', operatorName: '张师傅', time: '2026/5/17 12:10:00' },
            { step: 3, operator: 'worker1', operatorName: '张师傅', time: '2026/5/17 14:30:00' },
            { step: 4, operator: 'worker2', operatorName: '李师傅', time: '2026/5/17 15:00:00' },
            { step: 5, operator: 'worker2', operatorName: '李师傅', time: '2026/5/17 15:30:00' }
          ],
          lastStep: 5
        },
        {
          orderNo: 'BC17790252',
          bambooGrade: 'second',
          height: 20,
          density: 'sparse',
          style: 'square',
          baseConfig: ['mat'],
          currentStep: 0,
          orderTime: '2026/5/17 14:20:00',
          processRecords: [],
          lastStep: -1
        },
        {
          orderNo: 'BC17790253',
          bambooGrade: 'special',
          height: 35,
          density: 'normal',
          style: 'oval',
          baseConfig: ['wooden', 'lacquer', 'carving'],
          currentStep: 7,
          orderTime: '2026/5/16 09:00:00',
          processRecords: [
            { step: 0, operator: 'admin', operatorName: '管理员', time: '2026/5/16 09:05:00' },
            { step: 1, operator: 'admin', operatorName: '管理员', time: '2026/5/16 09:30:00' },
            { step: 2, operator: 'admin', operatorName: '管理员', time: '2026/5/16 10:00:00' },
            { step: 3, operator: 'admin', operatorName: '管理员', time: '2026/5/16 10:45:00' },
            { step: 4, operator: 'admin', operatorName: '管理员', time: '2026/5/16 11:30:00' },
            { step: 5, operator: 'admin', operatorName: '管理员', time: '2026/5/16 14:00:00' },
            { step: 6, operator: 'admin', operatorName: '管理员', time: '2026/5/16 15:00:00' },
            { step: 7, operator: 'admin', operatorName: '管理员', time: '2026/5/16 15:30:00' }
          ],
          lastStep: 7
        }
      ],
      newOrderHighlight: '',
      processDialogVisible: false,
      selectedOrder: {
        orderNo: '',
        bambooGrade: '',
        height: 0,
        density: '',
        style: '',
        baseConfig: [],
        currentStep: 0,
        orderTime: ''
      }
    }
  },
  mounted() {
    this.$eventBus.$on('new-order', (newOrder) => {
      this.addNewOrder(newOrder)
    })
  },
  beforeDestroy() {
    this.$eventBus.$off('new-order')
  },
  methods: {
    addNewOrder(newOrder) {
      const orderWithMeta = {
        ...newOrder,
        processRecords: [],
        lastStep: -1
      }
      this.orderList.unshift(orderWithMeta)
      this.newOrderHighlight = orderWithMeta.orderNo
      this.$nextTick(() => {
        this.scrollToNewOrder()
      })
      this.$message.success('新订单已加入生产队列！')
      setTimeout(() => {
        this.newOrderHighlight = ''
      }, 3000)
    },
    scrollToNewOrder() {
      const tableBody = this.$refs.orderTable.$el.querySelector('.el-table__body-wrapper')
      if (tableBody) {
        tableBody.scrollTop = 0
      }
    },
    tableRowClassName({ row }) {
      if (row.orderNo === this.newOrderHighlight) {
        return 'new-order-highlight'
      }
      return ''
    },
    handleRowClick(row) {
      this.selectedOrder = { ...row }
    },
    async nextStep(row) {
      if (row.currentStep >= 7) {
        this.$message.warning('该订单已完工，无需继续推进')
        return
      }
      if (row.lastStep === row.currentStep) {
        this.$message.warning('当前工序状态已处理，请勿重复提交')
        return
      }
      const nextStepIndex = row.currentStep
      const clientIP = await this.$getClientIP()
      const now = new Date()
      const timeStr = now.toLocaleString('zh-CN')
      const timestamp = now.getTime()
      row.processRecords.push({
        step: nextStepIndex,
        operator: this.$currentUser.account,
        operatorName: this.$currentUser.name,
        ip: clientIP,
        time: timeStr,
        timestamp: timestamp
      })
      row.lastStep = row.currentStep
      if (row.currentStep < 7) {
        row.currentStep++
      }
      if (row.currentStep >= 7) {
        this.$message.success(`订单 ${row.orderNo} 已完工！操作人：${this.$currentUser.name}，IP：${clientIP}`)
      } else {
        this.$message.info(`已进入工序：${this.steps[row.currentStep]}，操作人：${this.$currentUser.name}，IP：${clientIP}`)
      }
    },
    viewProcess(row) {
      this.selectedOrder = { ...row }
      this.processDialogVisible = true
    },
    getStepType(step) {
      if (step >= 7) return 'success'
      if (step >= 0) return 'warning'
      return 'info'
    },
    getBambooGradeText(val) {
      const map = {
        special: '特级 - 五年生毛竹',
        first: '一级 - 四年生毛竹',
        second: '二级 - 三年生毛竹'
      }
      return map[val] || val
    },
    getDensityText(val) {
      const map = {
        sparse: '稀疏',
        normal: '适中',
        dense: '紧密'
      }
      return map[val] || val
    },
    getStyleText(val) {
      const map = {
        cylinder: '传统圆筒形',
        hexagon: '六角形',
        square: '方形',
        oval: '椭圆形'
      }
      return map[val] || val
    },
    getBaseConfigText(arr) {
      if (!arr || arr.length === 0) return '无配置'
      const map = {
        wooden: '实木底座',
        lacquer: '上漆防水',
        carving: '雕花装饰',
        mat: '竹制衬垫'
      }
      return arr.map(item => map[item]).join('、')
    },
    getStepTagType(step) {
      if (step >= 7) return 'success'
      if (step >= 4) return 'warning'
      return 'info'
    },
    getStepStatusText(step) {
      if (step >= 7) return '完工'
      if (step === 0) return '待开工'
      return `第${step}道`
    }
  }
}
</script>

<style scoped>
.admin-page {
  padding: 10px;
}
.card-header {
  font-size: 20px;
  font-weight: bold;
  color: #2E7D32;
}
.order-table-section {
  margin-top: 10px;
}
.process-timeline {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 8px;
}
.order-detail {
  margin-top: 20px;
}
.record-info {
  font-size: 12px;
  line-height: 1.8;
}
.operator-info {
  margin-top: 8px;
  padding: 8px 12px;
  background: #f0f9ff;
  border-radius: 4px;
  border-left: 3px solid #409EFF;
}
.info-row {
  display: flex;
  align-items: center;
  color: #606266;
  margin: 2px 0;
}
</style>

<style>
.el-table .new-order-highlight {
  background: linear-gradient(135deg, #fff7e6 0%, #fff1f0 50%, #e6f7ff 100%) !important;
  animation: highlightPulse 1.5s ease-in-out infinite;
  position: relative;
}
.el-table .new-order-highlight td:first-child {
  position: relative;
  overflow: visible;
}
.new-order-badge {
  display: inline-block;
  position: relative;
  padding: 4px 10px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(238, 90, 111, 0.4);
  animation: badgeBounce 0.6s ease-in-out infinite alternate;
}
.badge-text {
  color: white;
  font-size: 10px;
  font-weight: bold;
  letter-spacing: 1px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}
@keyframes highlightPulse {
  0%, 100% {
    background: linear-gradient(135deg, #fff7e6 0%, #fff1f0 50%, #e6f7ff 100%);
  }
  50% {
    background: linear-gradient(135deg, #ffe7ba 0%, #ffccc7 50%, #bae7ff 100%);
  }
}
@keyframes badgeBounce {
  from {
    transform: scale(1);
  }
  to {
    transform: scale(1.1);
  }
}
</style>
