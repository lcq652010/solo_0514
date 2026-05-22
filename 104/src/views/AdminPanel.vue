<template>
  <div class="admin-panel">
    <el-card class="admin-card" shadow="hover">
      <div slot="header" class="card-header">
        <i class="el-icon-s-order"></i>
        <span>订单管理中心</span>
        <el-badge :value="orders.length" class="item" type="warning">
          <span class="badge-text">订单总数</span>
        </el-badge>
      </div>

      <div class="stats-row">
        <el-row :gutter="20">
          <el-col :span="6" v-for="(stage, index) in productionStages.slice(0, 4)" :key="'stat-' + stage.id">
            <div class="stat-card" :class="'stat-' + stage.id">
              <div class="stat-icon">
                <i :class="stage.icon"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ getOrderCountByStage(stage.id) }}</div>
                <div class="stat-label">{{ stage.name }}</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <el-table
        :data="orders"
        border
        stripe
        style="width: 100%"
        class="order-table"
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="id" label="订单编号" width="160" align="center">
          <template slot-scope="scope">
            <span class="order-id">{{ scope.row.id }}</span>
          </template>
        </el-table-column>

        <el-table-column label="客户信息" width="180">
          <template slot-scope="scope">
            <div class="customer-info">
              <div class="customer-name">{{ scope.row.customerName }}</div>
              <div class="customer-phone">{{ scope.row.phone }}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="产品规格" min-width="220">
          <template slot-scope="scope">
            <div class="spec-info">
              <el-tag size="mini" type="success">{{ scope.row.tinPurityLabel }}</el-tag>
              <span class="spec-text">
                {{ scope.row.height }}×{{ scope.row.diameter }}mm
              </span>
              <el-tag size="mini" type="info">{{ scope.row.lidStyleLabel }}</el-tag>
            </div>
            <div class="pattern-info">
              <span>錾刻：{{ scope.row.patternLabel }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="totalPrice" label="金额" width="100" align="center">
          <template slot-scope="scope">
            <span class="price-text">¥{{ scope.row.totalPrice }}</span>
          </template>
        </el-table-column>

        <el-table-column label="生产进度" min-width="320">
          <template slot-scope="scope">
            <div class="progress-container">
              <el-steps
                :active="scope.row.currentStage"
                finish-status="success"
                align-center
                class="steps-inline"
              >
                <el-step
                  v-for="stage in productionStages"
                  :key="stage.id"
                  :title="stage.name"
                  :icon="stage.icon"
                ></el-step>
              </el-steps>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="orderTime" label="下单时间" width="170" align="center">
          <template slot-scope="scope">
            <span class="time-text">{{ scope.row.orderTime }}</span>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="small"
              icon="el-icon-setting"
              @click="openStageDialog(scope.row)"
            >
              更新工序
            </el-button>
            <el-button
              type="info"
              size="small"
              icon="el-icon-view"
              @click="viewOrderDetail(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      title="更新生产工序"
      :visible.sync="stageDialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <div v-if="currentOrder" class="stage-dialog">
        <div class="order-summary">
          <span class="label">订单编号：</span>
          <span class="value order-id-text">{{ currentOrder.id }}</span>
          <span class="label" style="margin-left: 30px;">客户：</span>
          <span class="value">{{ currentOrder.customerName }}</span>
        </div>

        <el-divider></el-divider>

        <div class="stage-selector">
          <div class="selector-title">
            <i class="el-icon-info" style="color: #409eff; margin-right: 5px;"></i>
            当前工序：<span style="color: #d4af37; font-weight: bold;">{{ productionStages[currentOrder.currentStage].name }}</span>
            <span style="color: #909399; margin-left: 10px; font-size: 12px;">（仅可按顺序推进，不可跳步）</span>
          </div>
          <div class="stage-time-info">
            <i class="el-icon-time" style="color: #67c23a; margin-right: 5px;"></i>
            上次更新：{{ currentOrder.stageUpdateTime || '暂无记录' }}
          </div>
          <el-radio-group v-model="selectedStage" class="stage-radio-group">
            <el-radio
              v-for="stage in productionStages"
              :key="stage.id"
              :label="stage.id"
              :disabled="isStageDisabled(stage.id)"
              class="stage-radio"
            >
              <div class="stage-option" :class="{ 'stage-completed': stage.id < currentOrder.currentStage, 'stage-current': stage.id === currentOrder.currentStage, 'stage-next': stage.id === currentOrder.currentStage + 1 }">
                <i :class="stage.icon" class="stage-icon"></i>
                <span class="stage-name">{{ stage.name }}</span>
                <el-tag v-if="stage.id < currentOrder.currentStage" type="success" size="mini" style="margin-left: 5px;">已完成</el-tag>
                <el-tag v-else-if="stage.id === currentOrder.currentStage" type="warning" size="mini" style="margin-left: 5px;">当前</el-tag>
                <el-tag v-else-if="stage.id === currentOrder.currentStage + 1" type="primary" size="mini" style="margin-left: 5px;">下一步</el-tag>
              </div>
            </el-radio>
          </el-radio-group>
        </div>

        <el-divider v-if="currentOrder.remark"></el-divider>

        <div v-if="currentOrder.remark" class="remark-section">
          <div class="remark-title"><i class="el-icon-document"></i> 备注说明：</div>
          <div class="remark-content">{{ currentOrder.remark }}</div>
        </div>
      </div>

      <div slot="footer" class="dialog-footer">
        <el-button @click="stageDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmUpdateStage" :loading="updatingStage">
          确认更新
        </el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="订单详情"
      :visible.sync="detailDialogVisible"
      width="550px"
    >
      <div v-if="currentOrder" class="detail-dialog">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="订单编号" :label-style="{ width: '100px' }">
            {{ currentOrder.id }}
          </el-descriptions-item>
          <el-descriptions-item label="客户姓名">
            {{ currentOrder.customerName }}
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">
            {{ currentOrder.phone }}
          </el-descriptions-item>
          <el-descriptions-item label="订单金额">
            <span style="color: #e74c3c; font-weight: bold;">¥{{ currentOrder.totalPrice }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="锡料纯度">
            {{ currentOrder.tinPurityLabel }}
          </el-descriptions-item>
          <el-descriptions-item label="产品规格">
            {{ currentOrder.height }}mm × {{ currentOrder.diameter }}mm
          </el-descriptions-item>
          <el-descriptions-item label="盖型样式">
            {{ currentOrder.lidStyleLabel }}
          </el-descriptions-item>
          <el-descriptions-item label="錾刻花纹">
            {{ currentOrder.patternLabel }}
          </el-descriptions-item>
          <el-descriptions-item label="下单时间" :span="2">
            {{ currentOrder.orderTime }}
          </el-descriptions-item>
          <el-descriptions-item label="工序更新时间" :span="2">
            <i class="el-icon-time" style="color: #409eff; margin-right: 5px;"></i>
            {{ currentOrder.stageUpdateTime || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="备注说明" :span="2">
            {{ currentOrder.remark || '无' }}
          </el-descriptions-item>
        </el-descriptions>

        <el-divider></el-divider>

        <div class="detail-progress">
          <h4>当前生产进度：</h4>
          <el-steps
            :active="currentOrder.currentStage"
            finish-status="success"
            align-center
          >
            <el-step
              v-for="stage in productionStages"
              :key="stage.id"
              :title="stage.name"
              :icon="stage.icon"
            ></el-step>
          </el-steps>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import orderStore from '../store/orderStore'

export default {
  name: 'AdminPanel',
  data() {
    return {
      orders: [],
      productionStages: orderStore.getProductionStages(),
      stageDialogVisible: false,
      detailDialogVisible: false,
      currentOrder: null,
      selectedStage: 0,
      updatingStage: false
    }
  },
  created() {
    this.loadOrders()
  },
  methods: {
    isStageDisabled(stageId) {
      if (!this.currentOrder) return true
      const currentStage = this.currentOrder.currentStage
      return stageId > currentStage + 1 || stageId < currentStage
    },
    loadOrders() {
      this.orders = orderStore.getOrders()
    },
    getOrderCountByStage(stageId) {
      return this.orders.filter(o => o.currentStage === stageId).length
    },
    tableRowClassName({ row, rowIndex }) {
      if (row.currentStage === 7) {
        return 'completed-row'
      }
      return ''
    },
    openStageDialog(row) {
      this.currentOrder = { ...row }
      this.selectedStage = row.currentStage
      this.stageDialogVisible = true
    },
    viewOrderDetail(row) {
      this.currentOrder = { ...row }
      this.detailDialogVisible = true
    },
    confirmUpdateStage() {
      if (this.selectedStage === this.currentOrder.currentStage) {
        this.$message.info('工序未发生变化')
        return
      }

      this.updatingStage = true

      setTimeout(() => {
        orderStore.updateStage(this.currentOrder.id, this.selectedStage)
        this.loadOrders()

        this.updatingStage = false
        this.stageDialogVisible = false

        const isCompleted = this.selectedStage === this.productionStages.length - 1
        this.$alert(
          `<div style="text-align: center;">
            <p style="font-size: 16px; margin-bottom: 10px;">${isCompleted ? '🎉 订单生产完成！' : '工序更新成功！'}</p>
            <p style="color: #606266;">当前工序：<strong style="color: #d4af37;">${this.productionStages[this.selectedStage].name}</strong></p>
            ${isCompleted ? '<p style="color: #67c23a; margin-top: 5px;">可以通知客户取货了</p>' : ''}
          </div>`,
          '提示',
          {
            confirmButtonText: '确定',
            dangerouslyUseHTMLString: true,
            type: isCompleted ? 'success' : 'info'
          }
        )
      }, 800)
    }
  }
}
</script>

<style scoped>
.admin-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  align-items: center;
  font-size: 20px;
  font-weight: bold;
  color: #2c3e50;
}

.card-header i {
  font-size: 24px;
  margin-right: 10px;
  color: #d4af37;
}

.badge-text {
  font-size: 14px;
  font-weight: normal;
  margin-left: 10px;
}

.stats-row {
  margin-bottom: 25px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 8px;
  background: #f8f9fa;
}

.stat-0 {
  background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
}

.stat-1 {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
}

.stat-2 {
  background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
}

.stat-3 {
  background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
}

.stat-icon {
  font-size: 32px;
  color: #666;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #2c3e50;
}

.stat-label {
  font-size: 14px;
  color: #7f8c8d;
}

.order-table {
  margin-top: 15px;
}

.order-id {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #2c3e50;
}

.customer-info {
  line-height: 1.6;
}

.customer-name {
  font-weight: 600;
  color: #2c3e50;
}

.customer-phone {
  font-size: 12px;
  color: #7f8c8d;
}

.spec-info {
  margin-bottom: 5px;
}

.spec-text {
  margin: 0 8px;
  font-size: 13px;
}

.pattern-info {
  font-size: 12px;
  color: #7f8c8d;
}

.price-text {
  font-weight: bold;
  color: #e74c3c;
  font-size: 16px;
}

.time-text {
  font-size: 12px;
  color: #7f8c8d;
}

.progress-container {
  padding: 10px 0;
}

.steps-inline >>> .el-step__title {
  font-size: 12px;
}

.completed-row {
  background: #f0f9eb !important;
}

.stage-dialog {
  padding: 10px 0;
}

.order-summary {
  font-size: 14px;
}

.order-summary .label {
  color: #7f8c8d;
}

.order-summary .value {
  font-weight: 600;
  color: #2c3e50;
}

.order-id-text {
  font-family: 'Courier New', monospace;
}

.stage-selector {
  padding: 10px 0;
}

.selector-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #2c3e50;
}

.stage-time-info {
  font-size: 12px;
  color: #606266;
  margin-bottom: 15px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.stage-radio-group {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.stage-radio {
  margin: 0;
}

.stage-option {
  display: flex;
  align-items: center;
  padding: 12px 15px;
  border-radius: 6px;
  background: #f5f7fa;
  transition: all 0.3s;
}

.stage-option:hover {
  background: #e4e7ed;
}

.stage-completed {
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
}

.stage-completed .stage-icon {
  color: #67c23a;
}

.stage-current {
  background: #fdf6ec;
  border: 1px solid #faecd8;
}

.stage-current .stage-icon {
  color: #e6a23c;
}

.stage-next {
  background: #ecf5ff;
  border: 1px solid #d9ecff;
}

.stage-next .stage-icon {
  color: #409eff;
}

.stage-icon {
  font-size: 18px;
  margin-right: 8px;
  color: #606266;
}

.stage-name {
  font-size: 14px;
}

.remark-section {
  padding: 10px 0;
}

.remark-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #2c3e50;
}

.remark-title i {
  margin-right: 5px;
}

.remark-content {
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 13px;
  color: #606266;
}

.detail-dialog {
  padding: 10px 0;
}

.detail-progress h4 {
  margin-bottom: 15px;
  font-size: 14px;
  color: #2c3e50;
}
</style>
