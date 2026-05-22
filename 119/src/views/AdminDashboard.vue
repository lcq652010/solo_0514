<template>
  <div>
    <h2 class="page-title">📋 订单管理后台</h2>
    <el-card class="page-card" style="max-width: 1200px;">
      <div style="margin-bottom: 20px;">
        <el-button type="primary" icon="el-icon-refresh" @click="refreshData">刷新数据</el-button>
        <span style="margin-left: 20px; color: #6D4C41;">
          <strong>订单总数：</strong>{{ orders.length }} 单
        </span>
      </div>

      <el-table :data="orders" border style="width: 100%" stripe>
        <el-table-column prop="id" label="订单编号" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="info" size="small">{{ scope.row.id }}</el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="customerName" label="客户信息" width="180">
          <template slot-scope="scope">
            <div><strong>{{ scope.row.customerName }}</strong></div>
            <div style="font-size: 12px; color: #999;">{{ scope.row.phone }}</div>
          </template>
        </el-table-column>

        <el-table-column label="茶宠详情" width="220">
          <template slot-scope="scope">
            <div><strong>造型：</strong>{{ scope.row.shape }}</div>
            <div><strong>泥料：</strong>{{ scope.row.clayType }}</div>
            <div style="font-size: 12px; color: #999;">
              尺寸：{{ scope.row.height }}×{{ scope.row.width }}cm | {{ scope.row.glazeEffect }}
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="status" label="生产进度" width="400">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" align-center size="small">
              <el-step v-for="(step, index) in processSteps" :key="index" :title="step">
                <template slot="icon" slot-scope="{ active }">
                  <span :class="['step-icon', { active: index <= scope.row.status }]">
                    {{ index + 1 }}
                  </span>
                </template>
              </el-step>
            </el-steps>
          </template>
        </el-table-column>

        <el-table-column prop="createTime" label="下单时间" width="160" align="center">
          <template slot-scope="scope">
            <div style="font-size: 12px;">{{ scope.row.createTime }}</div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="primary"
              icon="el-icon-edit"
              @click="openProcessDialog(scope.row)">
              更新工序
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="更新生产工序" :visible.sync="dialogVisible" width="500px">
      <div v-if="currentOrder">
        <div style="margin-bottom: 20px; padding: 15px; background: #FAF6F0; border-radius: 8px;">
          <p><strong>订单编号：</strong>{{ currentOrder.id }}</p>
          <p><strong>客户姓名：</strong>{{ currentOrder.customerName }}</p>
          <p><strong>茶宠造型：</strong>{{ currentOrder.shape }}</p>
        </div>

        <div class="section-title">当前生产进度</div>
        <el-steps :active="currentOrder.status" finish-status="success" direction="vertical" style="margin-bottom: 20px;">
          <el-step v-for="(step, index) in processSteps" :key="index" :title="step">
            <template slot="description">
              <span v-if="index <= currentOrder.status" style="color: #67C23A;">已完成</span>
              <span v-else style="color: #999;">待处理</span>
            </template>
          </el-step>
        </el-steps>

        <div class="section-title">更新至</div>
        <el-radio-group v-model="newStatus">
          <el-radio v-for="(step, index) in processSteps" :key="index" :label="index" :disabled="index < currentOrder.status">
            {{ step }}
            <span v-if="index === processSteps.length - 1" style="color: #67C23A;">(最终工序)</span>
          </el-radio>
        </el-radio-group>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="updateProcess" :disabled="newStatus === currentOrder?.status">
          确认更新
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { store, mutations } from '../store'

export default {
  name: 'AdminDashboard',
  data() {
    return {
      dialogVisible: false,
      currentOrder: null,
      newStatus: 0
    }
  },
  computed: {
    orders() {
      return store.orders
    },
    processSteps() {
      return store.processSteps
    }
  },
  methods: {
    refreshData() {
      this.$message({
        message: '数据已刷新',
        type: 'success',
        duration: 1500
      })
    },
    openProcessDialog(order) {
      this.currentOrder = { ...order }
      this.newStatus = order.status
      this.dialogVisible = true
    },
    updateProcess() {
      mutations.updateOrderStatus(this.currentOrder.id, this.newStatus)
      this.dialogVisible = false
      this.$message({
        message: `订单 ${this.currentOrder.id} 已更新至「${this.processSteps[this.newStatus]}」工序`,
        type: 'success'
      })
    }
  }
}
</script>

<style scoped>
.el-steps--small {
  padding: 10px 0;
}
.step-icon {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 50%;
  background: #E0E0E0;
  color: #999;
  font-size: 12px;
  font-weight: 600;
  transition: all 0.3s;
}
.step-icon.active {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: white;
}
.el-step__title {
  font-size: 12px;
  white-space: nowrap;
}
.el-radio {
  display: block;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 4px;
  transition: all 0.2s;
}
.el-radio:hover {
  background: #FAF6F0;
}
</style>
