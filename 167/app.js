Vue.use(VueRouter);

const EventBus = new Vue();

const OrderForm = {
  template: `
    <div class="order-form-container">
      <el-header class="page-header">
        <div class="header-content">
          <h1>花丝银坠定制</h1>
          <el-button type="primary" @click="goToAdmin">管理员入口</el-button>
        </div>
      </el-header>
      
      <el-main class="form-main">
        <el-card class="order-card" shadow="hover">
          <div slot="header" class="card-header">
            <span>定制信息填写</span>
          </div>
          
          <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
            <el-divider content-position="left">银胚纯度</el-divider>
            <el-form-item label="银胚纯度" prop="purity">
              <el-radio-group v-model="orderForm.purity" @change="validateField('purity')">
                <el-radio label="999足银">999足银</el-radio>
                <el-radio label="925银">925银</el-radio>
                <el-radio label="990足银">990足银</el-radio>
              </el-radio-group>
            </el-form-item>

            <el-divider content-position="left">坠型款式</el-divider>
            <el-form-item label="坠型款式" prop="style">
              <el-select v-model="orderForm.style" placeholder="请选择坠型款式" style="width: 100%" @change="validateField('style')">
                <el-option label="圆形" value="圆形"></el-option>
                <el-option label="心形" value="心形"></el-option>
                <el-option label="水滴形" value="水滴形"></el-option>
                <el-option label="方形" value="方形"></el-option>
                <el-option label="叶子形" value="叶子形"></el-option>
                <el-option label="蝴蝶形" value="蝴蝶形"></el-option>
              </el-select>
            </el-form-item>

            <el-divider content-position="left">花丝纹样</el-divider>
            <el-form-item label="花丝纹样" prop="pattern">
              <el-checkbox-group v-model="orderForm.pattern" @change="validateField('pattern')">
                <el-checkbox label="祥云纹">祥云纹</el-checkbox>
                <el-checkbox label="缠枝纹">缠枝纹</el-checkbox>
                <el-checkbox label="回字纹">回字纹</el-checkbox>
                <el-checkbox label="牡丹纹">牡丹纹</el-checkbox>
                <el-checkbox label="莲花纹">莲花纹</el-checkbox>
                <el-checkbox label="龙凤纹">龙凤纹</el-checkbox>
              </el-checkbox-group>
            </el-form-item>

            <el-divider content-position="left">尺寸规格</el-divider>
            <el-alert 
              title="工艺建议区间" 
              type="info" 
              :closable="false" 
              show-icon
              style="margin-bottom: 15px;"
            >
              <span slot="description">
                推荐尺寸：长度 <b>20-50mm</b>，宽度 <b>15-40mm</b>，厚度 <b>1.5-3mm</b>
                <br>
                <span style="color: #67c23a">✓ 此范围花丝工艺效果最佳，变形风险最低</span>
              </span>
            </el-alert>
            <el-form-item label="长度(mm)" prop="length">
              <el-input-number 
                v-model="orderForm.length" 
                :min="10" 
                :max="100" 
                :step="1" 
                @change="validateField('length'); checkSizeRange('length')"
              ></el-input-number>
              <span 
                :class="['size-tip', getSizeTipClass('length')]"
                v-if="orderForm.length"
              >
                {{ getSizeTip('length') }}
              </span>
            </el-form-item>
            <el-form-item label="宽度(mm)" prop="width">
              <el-input-number 
                v-model="orderForm.width" 
                :min="10" 
                :max="80" 
                :step="1" 
                @change="validateField('width'); checkSizeRange('width')"
              ></el-input-number>
              <span 
                :class="['size-tip', getSizeTipClass('width')]"
                v-if="orderForm.width"
              >
                {{ getSizeTip('width') }}
              </span>
            </el-form-item>
            <el-form-item label="厚度(mm)" prop="thickness">
              <el-input-number 
                v-model="orderForm.thickness" 
                :min="1" 
                :max="10" 
                :step="0.5" 
                @change="validateField('thickness'); checkSizeRange('thickness')"
              ></el-input-number>
              <span 
                :class="['size-tip', getSizeTipClass('thickness')]"
                v-if="orderForm.thickness"
              >
                {{ getSizeTip('thickness') }}
              </span>
            </el-form-item>

            <el-divider content-position="left">镶石选项</el-divider>
            <el-form-item label="是否镶石" prop="hasStone">
              <el-switch v-model="orderForm.hasStone" active-text="是" inactive-text="否"></el-switch>
            </el-form-item>
            <el-form-item label="宝石类型" prop="stoneType" v-if="orderForm.hasStone">
              <el-select v-model="orderForm.stoneType" placeholder="请选择宝石类型" style="width: 100%">
                <el-option label="锆石" value="锆石"></el-option>
                <el-option label="水晶" value="水晶"></el-option>
                <el-option label="玛瑙" value="玛瑙"></el-option>
                <el-option label="翡翠" value="翡翠"></el-option>
                <el-option label="珍珠" value="珍珠"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="宝石数量" prop="stoneCount" v-if="orderForm.hasStone">
              <el-input-number v-model="orderForm.stoneCount" :min="1" :max="10" :step="1"></el-input-number>
            </el-form-item>

            <el-divider content-position="left">客户信息</el-divider>
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名" @input="validateField('customerName')"></el-input>
            </el-form-item>
            <el-form-item label="联系电话" prop="phone">
              <el-input v-model="orderForm.phone" placeholder="请输入联系电话" @input="validateField('phone')"></el-input>
            </el-form-item>
            <el-form-item label="备注说明" prop="remark">
              <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="其他定制要求说明"></el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" size="large" @click="submitOrder" style="width: 100%">提交订单</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-main>
    </div>
  `,
  data() {
    const processRanges = {
      length: { min: 20, max: 50 },
      width: { min: 15, max: 40 },
      thickness: { min: 1.5, max: 3 }
    };
    
    const validateLength = (rule, value, callback) => {
      if (value < 10 || value > 100) {
        callback(new Error('长度范围应在10-100mm之间'));
      } else {
        callback();
      }
    };
    const validateWidth = (rule, value, callback) => {
      if (value < 10 || value > 80) {
        callback(new Error('宽度范围应在10-80mm之间'));
      } else {
        callback();
      }
    };
    const validateThickness = (rule, value, callback) => {
      if (value < 1 || value > 10) {
        callback(new Error('厚度范围应在1-10mm之间'));
      } else {
        callback();
      }
    };
    
    return {
      processRanges,
      sizeWarnings: {},
      orderForm: {
        purity: '',
        style: '',
        pattern: [],
        length: 30,
        width: 20,
        thickness: 2,
        hasStone: false,
        stoneType: '',
        stoneCount: 1,
        customerName: '',
        phone: '',
        remark: ''
      },
      rules: {
        purity: [{ required: true, message: '请选择银胚纯度', trigger: 'change' }],
        style: [{ required: true, message: '请选择坠型款式', trigger: 'change' }],
        pattern: [{ type: 'array', required: true, message: '请至少选择一种花丝纹样', trigger: 'change' }],
        length: [
          { required: true, message: '请输入长度', trigger: 'change' },
          { validator: validateLength, trigger: 'change' }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'change' },
          { validator: validateWidth, trigger: 'change' }
        ],
        thickness: [
          { required: true, message: '请输入厚度', trigger: 'change' },
          { validator: validateThickness, trigger: 'change' }
        ],
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    };
  },
  mounted() {
    this.checkSizeRange('length');
    this.checkSizeRange('width');
    this.checkSizeRange('thickness');
  },
  methods: {
    checkSizeRange(field) {
      const value = this.orderForm[field];
      const range = this.processRanges[field];
      
      if (value < range.min) {
        this.sizeWarnings[field] = `⚠ 低于推荐值，花丝工艺难度增加`;
      } else if (value > range.max) {
        this.sizeWarnings[field] = `⚠ 高于推荐值，变形风险增加`;
      } else {
        this.sizeWarnings[field] = `✓ 在最佳工艺范围内`;
      }
    },
    getSizeTip(field) {
      return this.sizeWarnings[field] || '';
    },
    getSizeTipClass(field) {
      const tip = this.sizeWarnings[field] || '';
      if (tip.includes('✓')) return 'tip-success';
      if (tip.includes('⚠')) return 'tip-warning';
      return '';
    },
    validateField(field) {
      this.$refs.orderForm.validateField(field);
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const orders = JSON.parse(localStorage.getItem('orders') || '[]');
          const newOrderId = Date.now();
          const newOrder = {
            id: newOrderId,
            ...this.orderForm,
            status: 0,
            statusLocked: false,
            createTime: new Date().toLocaleString()
          };
          orders.unshift(newOrder);
          localStorage.setItem('orders', JSON.stringify(orders));
          
          this.$message({
            type: 'success',
            message: '订单提交成功！'
          });
          
          this.$refs.orderForm.resetFields();
          this.orderForm.hasStone = false;
          this.orderForm.length = 30;
          this.orderForm.width = 20;
          this.orderForm.thickness = 2;
          this.orderForm.stoneCount = 1;
          
          EventBus.$emit('orderCreated', newOrderId);
        }
      });
    },
    goToAdmin() {
      this.$router.push('/admin');
    }
  }
};

const AdminPanel = {
  template: `
    <div class="admin-container">
      <el-header class="page-header">
        <div class="header-content">
          <h1>订单管理系统</h1>
          <el-button @click="goToOrder">返回下单页</el-button>
        </div>
      </el-header>
      
      <el-main class="admin-main">
        <el-card class="stats-card" shadow="hover">
          <div slot="header">
            <span>生产统计</span>
          </div>
          <el-row :gutter="20">
            <el-col :span="3" v-for="(step, index) in steps" :key="index">
              <div class="stat-item">
                <div class="stat-number">{{ getStepCount(index) }}</div>
                <div class="stat-label">{{ step }}</div>
              </div>
            </el-col>
          </el-row>
        </el-card>

        <el-card class="orders-card" shadow="hover">
          <div slot="header">
            <span>订单列表</span>
            <el-button type="primary" size="small" @click="refreshOrders" style="float: right">刷新</el-button>
          </div>
          
          <el-table 
            :data="orders" 
            stripe 
            border 
            style="width: 100%" 
            v-loading="loading"
            :row-class-name="tableRowClassName"
            ref="orderTable"
          >
            <el-table-column prop="id" label="订单号" width="150" sortable>
              <template slot-scope="scope">
                <div class="order-id-cell">
                  <span>{{ scope.row.id }}</span>
                  <el-badge 
                    v-if="scope.row.id === newOrderId" 
                    :value="'NEW'" 
                    class="new-order-badge"
                    type="danger"
                    :hidden="false"
                  ></el-badge>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
            <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
            <el-table-column label="定制详情" min-width="200">
              <template slot-scope="scope">
                <div class="detail-item">
                  <span class="label">纯度：</span>{{ scope.row.purity }}
                </div>
                <div class="detail-item">
                  <span class="label">款式：</span>{{ scope.row.style }}
                </div>
                <div class="detail-item">
                  <span class="label">纹样：</span>{{ scope.row.pattern.join('、') }}
                </div>
                <div class="detail-item">
                  <span class="label">尺寸：</span>{{ scope.row.length }}×{{ scope.row.width }}×{{ scope.row.thickness }}mm
                </div>
                <div class="detail-item" v-if="scope.row.hasStone">
                  <span class="label">镶石：</span>{{ scope.row.stoneType }} × {{ scope.row.stoneCount }}
                </div>
              </template>
            </el-table-column>
            <el-table-column label="生产进度" width="320">
              <template slot-scope="scope">
                <el-steps :active="scope.row.status" finish-status="success" size="small" align-center>
                  <el-step v-for="(step, index) in steps" :key="index" :title="step"></el-step>
                </el-steps>
                <div class="step-actions">
                  <el-button 
                    v-if="scope.row.status < steps.length" 
                    size="mini" 
                    type="success" 
                    @click="nextStep(scope.row)"
                    :loading="scope.row.statusLocked"
                    :disabled="scope.row.statusLocked"
                  >
                    {{ scope.row.status === 0 ? '开始：' + steps[0] : '进入：' + steps[scope.row.status] }}
                  </el-button>
                  <span v-if="scope.row.status === steps.length" class="finished-tag">
                    <el-tag type="success">已完成</el-tag>
                  </span>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="操作记录" min-width="220">
              <template slot-scope="scope">
                <div v-if="scope.row.operationLog && scope.row.operationLog.length > 0" class="operation-log">
                  <div 
                    v-for="(log, index) in scope.row.operationLog.slice(-2).reverse()" 
                    :key="index"
                    class="log-item"
                  >
                    <el-tag size="mini" type="info" class="log-step">{{ log.step }}</el-tag>
                    <span class="log-info">{{ log.operator }} | {{ log.ip }}</span>
                    <span class="log-time">{{ log.time }}</span>
                  </div>
                </div>
                <el-tag v-else size="mini" type="warning">暂无工序记录</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="170" sortable></el-table-column>
            <el-table-column label="操作" width="100">
              <template slot-scope="scope">
                <el-button size="mini" type="danger" @click="deleteOrder(scope.row.id)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>
        </el-card>
      </el-main>
    </div>
  `,
  data() {
    return {
      orders: [],
      loading: false,
      newOrderId: null,
      steps: ['拉丝', '掐丝', '填丝', '焊接', '酸洗', '镶石', '抛光', '成品']
    };
  },
  mounted() {
    this.loadOrders();
    EventBus.$on('orderCreated', (orderId) => {
      this.newOrderId = orderId;
      this.refreshOrders();
      this.$nextTick(() => {
        this.scrollToNewOrder();
      });
    });
  },
  methods: {
    tableRowClassName({ row }) {
      return row.id === this.newOrderId ? 'new-order-row' : '';
    },
    scrollToNewOrder() {
      if (this.newOrderId && this.$refs.orderTable) {
        const table = this.$refs.orderTable;
        const rows = table.$el.querySelectorAll('.el-table__row');
        const newOrderIndex = this.orders.findIndex(o => o.id === this.newOrderId);
        if (newOrderIndex !== -1 && rows[newOrderIndex]) {
          rows[newOrderIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
          setTimeout(() => {
            this.newOrderId = null;
          }, 3000);
        }
      }
    },
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('orders') || '[]').map(order => ({
        ...order,
        statusLocked: false
      }));
    },
    refreshOrders() {
      this.loading = true;
      setTimeout(() => {
        this.loadOrders();
        this.loading = false;
        this.$message.success('刷新成功');
      }, 500);
    },
    getOperatorInfo() {
      const operators = ['张三', '李四', '王五', '赵六', '陈师傅'];
      const randomOperator = operators[Math.floor(Math.random() * operators.length)];
      const ipSegments = [192, 168, Math.floor(Math.random() * 255), Math.floor(Math.random() * 255)];
      const ip = ipSegments.join('.');
      
      return { operator: randomOperator, ip };
    },
    nextStep(order) {
      if (order.statusLocked) {
        this.$message.warning('状态更新中，请稍候...');
        return;
      }
      
      if (order.status >= this.steps.length) {
        this.$message.info('订单已完成全部工序');
        return;
      }
      
      const nextStatus = order.status + 1;
      const { operator, ip } = this.getOperatorInfo();
      
      order.statusLocked = true;
      
      setTimeout(() => {
        order.status = nextStatus;
        
        if (!order.operationLog) {
          order.operationLog = [];
        }
        
        order.operationLog.push({
          step: this.steps[nextStatus - 1],
          operator: operator,
          ip: ip,
          time: new Date().toLocaleString()
        });
        
        this.saveOrders();
        order.statusLocked = false;
        
        if (nextStatus === this.steps.length) {
          this.$message.success('恭喜！订单已完成全部工序！');
        } else {
          this.$message.success(`已进入：${this.steps[nextStatus - 1]}`);
        }
      }, 500);
    },
    deleteOrder(id) {
      this.$confirm('确定要删除该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orders = this.orders.filter(item => item.id !== id);
        this.saveOrders();
        this.$message.success('删除成功');
      }).catch(() => {});
    },
    saveOrders() {
      const ordersToSave = this.orders.map(({ statusLocked, ...rest }) => rest);
      localStorage.setItem('orders', JSON.stringify(ordersToSave));
    },
    getStepCount(status) {
      return this.orders.filter(item => item.status === status).length;
    },
    goToOrder() {
      this.$router.push('/');
    }
  }
};

const routes = [
  { path: '/', component: OrderForm },
  { path: '/admin', component: AdminPanel }
];

const router = new VueRouter({
  routes
});

new Vue({
  router,
  template: `
    <router-view></router-view>
  `
}).$mount('#app');

const style = document.createElement('style');
style.textContent = `
  .page-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0 20px;
    display: flex;
    align-items: center;
  }
  .header-content {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .header-content h1 {
    font-size: 24px;
    margin: 0;
  }
  .form-main, .admin-main {
    padding: 30px;
    max-width: 900px;
    margin: 0 auto;
  }
  .admin-main {
    max-width: 1600px;
  }
  .order-card, .orders-card, .stats-card {
    border-radius: 12px;
  }
  .card-header {
    font-size: 18px;
    font-weight: bold;
    color: #333;
  }
  .stats-card {
    margin-bottom: 20px;
  }
  .stat-item {
    text-align: center;
    padding: 15px;
    background: #f5f7fa;
    border-radius: 8px;
  }
  .stat-number {
    font-size: 28px;
    font-weight: bold;
    color: #667eea;
  }
  .stat-label {
    font-size: 14px;
    color: #666;
    margin-top: 5px;
  }
  .detail-item {
    margin-bottom: 4px;
    font-size: 13px;
  }
  .detail-item .label {
    color: #909399;
  }
  .step-actions {
    margin-top: 10px;
    text-align: center;
  }
  .el-divider__text {
    font-weight: bold;
    color: #667eea;
  }
  .size-tip {
    display: inline-block;
    margin-left: 8px;
    font-size: 12px;
    padding: 2px 6px;
    border-radius: 3px;
  }
  .tip-success {
    color: #67c23a;
    background-color: #f0f9eb;
  }
  .tip-warning {
    color: #e6a23c;
    background-color: #fdf6ec;
  }
  .new-order-row td {
    background-color: #fff7e6 !important;
    animation: pulse 2s ease-in-out infinite;
  }
  .new-order-row td:first-child {
    border-left: 3px solid #ff9900;
  }
  @keyframes pulse {
    0%, 100% {
      background-color: #fff7e6;
    }
    50% {
      background-color: #ffe7ba;
    }
  }
  .finished-tag {
    display: inline-block;
    margin-top: 5px;
  }
  .order-id-cell {
    position: relative;
    display: flex;
    align-items: center;
  }
  .new-order-badge {
    position: absolute;
    top: -8px;
    right: -10px;
    transform: scale(0.8);
  }
  .operation-log {
    max-height: 80px;
    overflow-y: auto;
  }
  .log-item {
    margin-bottom: 6px;
    font-size: 11px;
    line-height: 1.4;
  }
  .log-step {
    margin-right: 5px;
  }
  .log-info {
    color: #606266;
    display: block;
  }
  .log-time {
    color: #909399;
    font-size: 10px;
  }
`;
document.head.appendChild(style);
