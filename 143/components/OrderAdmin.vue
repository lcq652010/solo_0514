<template>
  <div class="order-admin-container">
    <div class="page-header">
      <h1>订单管理中心</h1>
      <p class="subtitle">景泰蓝手镯定制订单管理系统</p>
    </div>

    <el-card class="admin-card">
      <div class="table-toolbar">
        <el-button type="primary" @click="refreshOrders" icon="el-icon-refresh">
          刷新订单
        </el-button>
        <span class="order-stats">
          共 <strong>{{ orders.length }}</strong> 条订单
        </span>
      </div>

      <el-table :data="orders" border stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="订单编号" width="150" sortable>
        </el-table-column>

        <el-table-column label="客户信息" width="200">
          <template slot-scope="scope">
            <div><strong>{{ scope.row.customerName }}</strong></div>
            <div style="color: #666; font-size: 12px;">{{ scope.row.phone }}</div>
          </template>
        </el-table-column>

        <el-table-column label="产品规格" min-width="220">
          <template slot-scope="scope">
            <el-tag size="mini" type="info">{{ scope.row.material }}</el-tag>
            <div style="margin-top: 5px; font-size: 12px;">
              内径: {{ scope.row.innerDiameter }}mm · 粗细: {{ scope.row.thickness }}mm
            </div>
          </template>
        </el-table-column>

        <el-table-column label="工艺详情" min-width="200">
          <template slot-scope="scope">
            <div>
              <span style="color: #8B4513; font-weight: 500;">{{ scope.row.pattern }}</span>
            </div>
            <div style="font-size: 12px; color: #666; margin-top: 3px;">
              {{ scope.row.enamelColors.join('、') }}
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="createTime" label="下单时间" width="180" sortable>
        </el-table-column>

        <el-table-column label="生产进度" width="280">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" size="small">
              <el-step title="制胎"></el-step>
              <el-step title="掐丝"></el-step>
              <el-step title="点蓝"></el-step>
              <el-step title="烧蓝"></el-step>
              <el-step title="磨光"></el-step>
              <el-step title="镀金"></el-step>
              <el-step title="质检"></el-step>
              <el-step title="完工"></el-step>
            </el-steps>
          </template>
        </el-table-column>

        <el-table-column label="当前状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ scope.row.statusText }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="viewDetail(scope.row)" icon="el-icon-view">
              详情
            </el-button>
            <el-dropdown @command="(status) => updateStatus(scope.row, status)" v-if="scope.row.status < 8">
              <el-button size="mini" type="success" icon="el-icon-s-promotion">
                更新状态<i class="el-icon-arrow-down el-icon--right"></i>
              </el-button>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item :command="1" v-if="scope.row.status < 1">制胎完成</el-dropdown-item>
                <el-dropdown-item :command="2" v-if="scope.row.status < 2">掐丝完成</el-dropdown-item>
                <el-dropdown-item :command="3" v-if="scope.row.status < 3">点蓝完成</el-dropdown-item>
                <el-dropdown-item :command="4" v-if="scope.row.status < 4">烧蓝完成</el-dropdown-item>
                <el-dropdown-item :command="5" v-if="scope.row.status < 5">磨光完成</el-dropdown-item>
                <el-dropdown-item :command="6" v-if="scope.row.status < 6">镀金完成</el-dropdown-item>
                <el-dropdown-item :command="7" v-if="scope.row.status < 7">质检完成</el-dropdown-item>
                <el-dropdown-item :command="8" v-if="scope.row.status < 8">订单完工</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentOrder">
        <el-descriptions-item label="订单编号" :span="2">
          {{ currentOrder.id }}
        </el-descriptions-item>
        <el-descriptions-item label="客户姓名">
          {{ currentOrder.customerName }}
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          {{ currentOrder.phone }}
        </el-descriptions-item>
        <el-descriptions-item label="胎体材质">
          {{ currentOrder.material }}
        </el-descriptions-item>
        <el-descriptions-item label="手镯规格">
          {{ currentOrder.innerDiameter }}mm / {{ currentOrder.thickness }}mm
        </el-descriptions-item>
        <el-descriptions-item label="珐琅釉色" :span="2">
          {{ currentOrder.enamelColors ? currentOrder.enamelColors.join('、') : '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="掐丝纹样" :span="2">
          {{ currentOrder.pattern }}
        </el-descriptions-item>
        <el-descriptions-item label="下单时间" :span="2">
          {{ currentOrder.createTime }}
        </el-descriptions-item>
        <el-descriptions-item label="备注说明" :span="2">
          {{ currentOrder.remark || '无' }}
        </el-descriptions-item>
      </el-descriptions>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
const statusList = ['制胎', '掐丝', '点蓝', '烧蓝', '磨光', '镀金', '质检', '完工'];

export default {
  name: 'OrderAdmin',
  data() {
    return {
      loading: false,
      orders: [],
      detailVisible: false,
      currentOrder: null
    }
  },
  mounted() {
    this.loadOrders();
  },
  methods: {
    loadOrders() {
      this.loading = true;
      setTimeout(() => {
        this.orders = JSON.parse(localStorage.getItem('cloisonneOrders') || '[]');
        this.loading = false;
      }, 500);
    },
    refreshOrders() {
      this.loadOrders();
      this.$message.success('订单已刷新');
    },
    getStatusType(status) {
      if (status >= 8) return 'success';
      if (status >= 6) return 'warning';
      return 'primary';
    },
    updateStatus(order, newStatus) {
      this.$confirm(`确认将订单 ${order.id} 更新为「${statusList[newStatus - 1]}」状态？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = newStatus;
        order.statusText = statusList[newStatus - 1];
        localStorage.setItem('cloisonneOrders', JSON.stringify(this.orders));
        this.$message.success('状态更新成功');
      }).catch(() => {});
    },
    viewDetail(order) {
      this.currentOrder = order;
      this.detailVisible = true;
    }
  }
}
</script>

<style scoped>
.order-admin-container {
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 20px;
}

.page-header h1 {
  color: #8B4513;
  font-size: 28px;
  margin-bottom: 8px;
  font-weight: 600;
}

.subtitle {
  color: #666;
  font-size: 14px;
}

.admin-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.order-stats {
  color: #666;
  font-size: 14px;
}
</style>
