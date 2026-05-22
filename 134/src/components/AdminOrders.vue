<template>
  <div class="admin-orders-container">
    <el-card>
      <div slot="header" class="card-header">
        <span>砚台定制订单管理</span>
        <el-button type="primary" size="small" @click="loadOrders">刷新订单</el-button>
      </div>

      <el-table :data="orders" border stripe style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="订单编号" width="180"></el-table-column>
        <el-table-column label="砚石材质" width="120">
          <template slot-scope="scope">
            {{ getMaterialLabel(scope.row.material) }}
          </template>
        </el-table-column>
        <el-table-column label="砚台样式" width="100">
          <template slot-scope="scope">
            {{ getStyleLabel(scope.row.style) }}
          </template>
        </el-table-column>
        <el-table-column label="尺寸 (cm)" width="150">
          <template slot-scope="scope">
            {{ scope.row.length }} × {{ scope.row.width }} × {{ scope.row.thickness }}
          </template>
        </el-table-column>
        <el-table-column label="雕刻题材" width="100">
          <template slot-scope="scope">
            {{ getCarvingLabel(scope.row.carving) }}
          </template>
        </el-table-column>
        <el-table-column label="刻字" width="80">
          <template slot-scope="scope">
            <el-tag :type="scope.row.needEngraving ? 'success' : 'info'" size="small">
              {{ scope.row.needEngraving ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="下单时间" width="180"></el-table-column>
        <el-table-column label="生产工序" width="450">
          <template slot-scope="scope">
            <el-steps :active="scope.row.status" finish-status="success" align-center size="small">
              <el-step v-for="step in processSteps" :key="step.value" :title="step.label"></el-step>
            </el-steps>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template slot-scope="scope">
            <el-button-group>
              <el-button size="small" type="primary" @click="viewDetail(scope.row)">详情</el-button>
              <el-button size="small" type="success" @click="nextStep(scope.row)" :disabled="scope.row.status >= 7">
                下一工序
              </el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="orders.length === 0 && !loading" description="暂无订单数据"></el-empty>
    </el-card>

    <el-dialog title="订单详情" :visible.sync="detailVisible" width="600px">
      <el-descriptions :column="1" border v-if="currentOrder">
        <el-descriptions-item label="订单编号">{{ currentOrder.id }}</el-descriptions-item>
        <el-descriptions-item label="砚石材质">{{ getMaterialLabel(currentOrder.material) }}</el-descriptions-item>
        <el-descriptions-item label="砚台样式">{{ getStyleLabel(currentOrder.style) }}</el-descriptions-item>
        <el-descriptions-item label="尺寸规格">{{ currentOrder.length }} × {{ currentOrder.width }} × {{ currentOrder.thickness }} cm</el-descriptions-item>
        <el-descriptions-item label="雕刻题材">{{ getCarvingLabel(currentOrder.carving) }}</el-descriptions-item>
        <el-descriptions-item label="是否刻字">{{ currentOrder.needEngraving ? '是' : '否' }}</el-descriptions-item>
        <el-descriptions-item v-if="currentOrder.needEngraving" label="刻字内容">
          <span style="color: #409EFF">{{ currentOrder.engravingText }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="订单留言">{{ currentOrder.message || '无' }}</el-descriptions-item>
        <el-descriptions-item label="下单时间">{{ currentOrder.createTime }}</el-descriptions-item>
        <el-descriptions-item label="当前工序">
          <el-tag type="success">{{ processSteps[currentOrder.status].label }}</el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
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
      loading: false,
      detailVisible: false,
      currentOrder: null,
      processSteps: [
        { value: 0, label: '选石' },
        { value: 1, label: '切坯' },
        { value: 2, label: '粗雕' },
        { value: 3, label: '细雕' },
        { value: 4, label: '打磨' },
        { value: 5, label: '刻字' },
        { value: 6, label: '上蜡' },
        { value: 7, label: '完工' }
      ],
      materials: [
        { label: '端石 (广东肇庆)', value: 'duanshi' },
        { label: '歙石 (安徽歙县)', value: 'sheshi' },
        { label: '洮河石 (甘肃)', value: 'taohe' },
        { label: '澄泥 (山西绛州)', value: 'chengni' },
        { label: '红丝石 (山东)', value: 'hongsi' },
        { label: '松花石 (吉林)', value: 'songhua' }
      ],
      styles: [
        { label: '圆形', value: 'circle' },
        { label: '方形', value: 'square' },
        { label: '长方形', value: 'rectangle' },
        { label: '随形', value: 'freeform' },
        { label: '古琴式', value: 'guqin' },
        { label: '箕形', value: 'ji' }
      ],
      carvings: [
        { label: '山水风景', value: 'landscape' },
        { label: '花鸟虫鱼', value: 'flower' },
        { label: '龙凤呈祥', value: 'dragon' },
        { label: '松竹梅兰', value: 'bamboo' },
        { label: '人物典故', value: 'figure' },
        { label: '素面无雕', value: 'plain' }
      ]
    };
  },
  mounted() {
    this.loadOrders();
  },
  methods: {
    loadOrders() {
      this.loading = true;
      setTimeout(() => {
        this.orders = JSON.parse(localStorage.getItem('inkstoneOrders') || '[]');
        this.loading = false;
      }, 300);
    },
    getMaterialLabel(value) {
      const item = this.materials.find(m => m.value === value);
      return item ? item.label.split(' ')[0] : value;
    },
    getStyleLabel(value) {
      const item = this.styles.find(s => s.value === value);
      return item ? item.label : value;
    },
    getCarvingLabel(value) {
      const item = this.carvings.find(c => c.value === value);
      return item ? item.label : value;
    },
    viewDetail(row) {
      this.currentOrder = row;
      this.detailVisible = true;
    },
    nextStep(row) {
      if (row.status < 7) {
        this.$confirm(`确定将订单推进到「${this.processSteps[row.status + 1].label}」工序吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          row.status++;
          localStorage.setItem('inkstoneOrders', JSON.stringify(this.orders));
          this.$message.success('工序已更新！');
        }).catch(() => {});
      }
    }
  }
};
</script>

<style scoped>
.admin-orders-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}
</style>
