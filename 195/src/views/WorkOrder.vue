<template>
  <div class="work-order">
    <el-card class="table-card">
      <div class="table-header">
        <div class="table-title">
          <i class="el-icon-document"></i>
          <span>工单管理</span>
          <span class="count-badge">共 {{ total }} 条</span>
        </div>
      </div>

      <el-table
        :data="workOrders"
        border
        stripe
        style="width: 100%"
        v-loading="loading"
      >
        <el-table-column prop="workOrderNo" label="工单编号" width="220" align="center">
          <template slot-scope="scope">
            <span class="work-order-no">{{ scope.row.workOrderNo }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="deviceCode" label="设备编号" width="160" align="center"></el-table-column>
        <el-table-column prop="community" label="所属社区" min-width="160" align="center"></el-table-column>
        <el-table-column prop="faultDescription" label="故障说明" min-width="250" show-overflow-tooltip></el-table-column>
        <el-table-column prop="reportTime" label="上报时间" width="180" align="center"></el-table-column>
        <el-table-column prop="statusText" label="工单状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" effect="light" size="medium">
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140" align="center">
          <template slot-scope="scope">
            <el-button type="text" size="small" icon="el-icon-view">详情</el-button>
            <el-button
              v-if="scope.row.status === 'pending'"
              type="text"
              size="small"
              icon="el-icon-check"
              class="process-btn"
            >
              处理
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { mockWorkOrders, type WorkOrder } from '@/mock/data'

export default Vue.extend({
  name: 'WorkOrder',
  data() {
    return {
      loading: false,
      workOrders: [] as WorkOrder[]
    }
  },
  computed: {
    total(): number {
      return this.workOrders.length
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        this.workOrders = mockWorkOrders
        this.loading = false
      }, 300)
    },
    getStatusType(status: string): string {
      const typeMap: Record<string, string> = {
        pending: 'warning',
        processing: 'primary',
        completed: 'success'
      }
      return typeMap[status] || 'info'
    }
  }
})
</script>

<style scoped>
.work-order {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.table-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.table-title i {
  font-size: 22px;
  color: #1890ff;
}

.count-badge {
  font-size: 14px;
  font-weight: normal;
  color: #909399;
  background: #f0f2f5;
  padding: 4px 12px;
  border-radius: 12px;
}

.work-order-no {
  font-family: 'Courier New', monospace;
  font-weight: 600;
  color: #1890ff;
}

.process-btn {
  color: #52c41a !important;
}

.process-btn:hover {
  color: #73d13d !important;
}

::v-deep .el-table .cell {
  text-align: center;
}
</style>
