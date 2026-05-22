Vue.use(VueRouter);
Vue.use(ELEMENT);

const eventBus = new Vue();

const OrderForm = {
  template: `
    <div class="order-form-container">
      <el-card class="form-card" shadow="hover">
        <div slot="header" class="card-header">
          <span>牛角梳定制</span>
          <span class="subtitle">匠心打造，独一无二</span>
        </div>
        
        <el-form :model="form" :rules="rules" ref="form" label-width="120px" class="order-form">
          <el-form-item label="牛角材质" prop="material">
            <el-select 
              v-model="form.material" 
              placeholder="请选择牛角材质" 
              style="width: 100%"
              @change="validateField('material')"
              :class="{ 'field-valid': fieldStatus.material.valid, 'field-invalid': !fieldStatus.material.valid && fieldStatus.material.touched }">
              <el-option label="白水牛角 - 温润如玉" value="white"></el-option>
              <el-option label="黑水牛角 - 厚重典雅" value="black"></el-option>
              <el-option label="黄牛角 - 古朴自然" value="yellow"></el-option>
              <el-option label="牦牛角 - 珍稀名贵" value="yak"></el-option>
            </el-select>
            <div v-if="fieldStatus.material.touched" class="field-feedback">
              <i v-if="fieldStatus.material.valid" class="el-icon-circle-check valid-icon"></i>
              <i v-else class="el-icon-circle-close invalid-icon"></i>
              <span v-if="!fieldStatus.material.valid" class="error-text">{{ fieldStatus.material.message }}</span>
            </div>
          </el-form-item>
          
          <el-form-item label="梳齿密度" prop="density">
            <el-radio-group 
              v-model="form.density"
              @change="validateField('density')"
              :class="{ 'field-valid': fieldStatus.density.valid }">
              <el-radio label="sparse">稀疏（适合长发）</el-radio>
              <el-radio label="medium">适中（通用型）</el-radio>
              <el-radio label="dense">密集（适合短发）</el-radio>
            </el-radio-group>
            <div class="field-feedback">
              <i v-if="fieldStatus.density.valid" class="el-icon-circle-check valid-icon"></i>
            </div>
          </el-form-item>
          
          <el-form-item label="梳子长度" prop="length">
            <div class="length-slider-wrapper">
              <el-slider 
                v-model="form.length" 
                :min="10" 
                :max="25" 
                :step="0.5" 
                show-input
                @input="validateField('length')"
                :class="{ 'field-valid': fieldStatus.length.valid }">
              </el-slider>
              <span class="length-unit">厘米</span>
            </div>
            <div class="field-feedback">
              <i v-if="fieldStatus.length.valid" class="el-icon-circle-check valid-icon"></i>
              <span class="hint-text">范围: 10-25cm</span>
            </div>
            <div class="process-adaptation">
              <div class="adaptation-title">工艺适配参考：</div>
              <div class="adaptation-ranges">
                <span 
                  v-for="range in lengthRanges" 
                  :key="range.label"
                  class="range-tag"
                  :class="{ active: isLengthInRange(range) }">
                  {{ range.label }}
                </span>
              </div>
              <div class="adaptation-tip" :class="lengthTip.type">
                <i :class="lengthTip.icon"></i>
                <span>{{ lengthTip.text }}</span>
              </div>
            </div>
          </el-form-item>
          
          <el-form-item label="手柄造型" prop="handle">
            <el-select 
              v-model="form.handle" 
              placeholder="请选手柄造型" 
              style="width: 100%"
              @change="validateField('handle')"
              :class="{ 'field-valid': fieldStatus.handle.valid, 'field-invalid': !fieldStatus.handle.valid && fieldStatus.handle.touched }">
              <el-option label="直柄 - 经典简约" value="straight"></el-option>
              <el-option label="弯柄 - 贴合手掌" value="curved"></el-option>
              <el-option label="雕花 - 精致工艺" value="carved"></el-option>
              <el-option label="无柄 - 便携小巧" value="none"></el-option>
            </el-select>
            <div v-if="fieldStatus.handle.touched" class="field-feedback">
              <i v-if="fieldStatus.handle.valid" class="el-icon-circle-check valid-icon"></i>
              <i v-else class="el-icon-circle-close invalid-icon"></i>
              <span v-if="!fieldStatus.handle.valid" class="error-text">{{ fieldStatus.handle.message }}</span>
            </div>
          </el-form-item>
          
          <el-form-item label="刻字内容" prop="engraving">
            <el-input 
              v-model="form.engraving" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入刻字内容（最多20字）"
              maxlength="20"
              show-word-limit>
            </el-input>
          </el-form-item>
          
          <el-form-item label="客户姓名" prop="customerName">
            <el-input v-model="form.customerName" placeholder="请输入您的姓名"></el-input>
          </el-form-item>
          
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="form.phone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitOrder" :loading="submitting" size="large" class="submit-btn">
              提交订单
            </el-button>
            <el-button @click="resetForm" size="large">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  `,
  data() {
    return {
      submitting: false,
      form: {
        material: '',
        density: 'medium',
        length: 18,
        handle: '',
        engraving: '',
        customerName: '',
        phone: ''
      },
      fieldStatus: {
        material: { valid: false, touched: false, message: '请选择牛角材质' },
        density: { valid: true, touched: true, message: '' },
        length: { valid: true, touched: true, message: '' },
        handle: { valid: false, touched: false, message: '请选手柄造型' }
      },
      lengthRanges: [
        { label: '10-13cm 便携款', min: 10, max: 13, type: 'short' },
        { label: '14-18cm 标准款', min: 14, max: 18, type: 'standard' },
        { label: '19-22cm 长发款', min: 19, max: 22, type: 'long' },
        { label: '23-25cm 特殊款', min: 23, max: 25, type: 'special' }
      ],
      rules: {
        material: [
          { required: true, message: '请选择牛角材质', trigger: 'change' }
        ],
        handle: [
          { required: true, message: '请选手柄造型', trigger: 'change' }
        ],
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    lengthTip() {
      const length = this.form.length;
      if (length >= 10 && length <= 13) {
        return {
          type: 'info',
          icon: 'el-icon-info',
          text: '便携款适合随身携带，工艺难度适中，适合日常使用。'
        };
      } else if (length >= 14 && length <= 18) {
        return {
          type: 'success',
          icon: 'el-icon-success',
          text: '标准款为推荐尺寸，工艺成熟，适合绝大多数用户。'
        };
      } else if (length >= 19 && length <= 22) {
        return {
          type: 'warning',
          icon: 'el-icon-warning',
          text: '长发款适合浓密长发，选材要求较高，制作周期延长1天。'
        };
      } else if (length >= 23 && length <= 25) {
        return {
          type: 'danger',
          icon: 'el-icon-circle-close',
          text: '特殊款需定制材料，工艺复杂度高，制作周期延长2-3天。'
        };
      }
      return {
        type: 'info',
        icon: 'el-icon-info',
        text: '请选择合适的梳子长度。'
      };
    }
  },
  created() {
    this.validateField('density');
    this.validateField('length');
  },
  methods: {
    isLengthInRange(range) {
      return this.form.length >= range.min && this.form.length <= range.max;
    },
    validateField(field) {
      const status = this.fieldStatus[field];
      if (!status) return;
      
      status.touched = true;
      
      switch(field) {
        case 'material':
          status.valid = !!this.form.material;
          status.message = status.valid ? '' : '请选择牛角材质';
          break;
        case 'density':
          status.valid = ['sparse', 'medium', 'dense'].includes(this.form.density);
          break;
        case 'length':
          status.valid = this.form.length >= 10 && this.form.length <= 25;
          status.message = status.valid ? '' : '长度必须在10-25厘米之间';
          break;
        case 'handle':
          status.valid = !!this.form.handle;
          status.message = status.valid ? '' : '请选手柄造型';
          break;
      }
    },
    submitOrder() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          this.submitting = true;
          setTimeout(() => {
            const order = {
              id: 'ORD' + Date.now(),
              ...this.form,
              status: 0,
              statusHistory: [{
                status: 0,
                stepName: '选料',
                operator: '系统',
                operatorId: 'SYS_001',
                operationTime: new Date().toLocaleString(),
                operationTimestamp: Date.now(),
                ipAddress: '127.0.0.1',
                note: '订单创建'
              }],
              createTime: new Date().toLocaleString(),
              isNew: true
            };
            const orders = JSON.parse(localStorage.getItem('combOrders') || '[]');
            orders.unshift(order);
            localStorage.setItem('combOrders', JSON.stringify(orders));
            
            this.submitting = false;
            this.$message.success('订单提交成功！');
            
            eventBus.$emit('newOrderCreated', order.id);
            
            this.$router.push('/admin');
          }, 1000);
        }
      });
    },
    resetForm() {
      this.$refs.form.resetFields();
      this.fieldStatus.material = { valid: false, touched: false, message: '请选择牛角材质' };
      this.fieldStatus.handle = { valid: false, touched: false, message: '请选手柄造型' };
      this.validateField('density');
      this.validateField('length');
    }
  }
};

const AdminPanel = {
  template: `
    <div class="admin-container">
      <el-card shadow="hover">
        <div slot="header" class="card-header">
          <span>订单管理</span>
          <el-badge :value="pendingCount" class="item">
            <span style="font-size: 14px; color: #606266;">待处理</span>
          </el-badge>
        </div>
        
        <el-table 
          :data="orders" 
          border 
          style="width: 100%" 
          class="order-table"
          ref="orderTable"
          row-key="id"
          :row-class-name="tableRowClassName">
          <el-table-column label="订单标识" width="180">
            <template slot-scope="scope">
              <div class="order-id-wrapper">
                <el-tag 
                  v-if="scope.row.isNew" 
                  type="success" 
                  size="mini" 
                  effect="dark"
                  class="new-order-tag">
                  新订单
                </el-tag>
                <span class="order-id-text">{{ scope.row.id }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
          <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
          <el-table-column label="定制信息" width="280">
            <template slot-scope="scope">
              <div class="order-info">
                <p><span class="label">材质：</span>{{ getMaterialText(scope.row.material) }}</p>
                <p><span class="label">密度：</span>{{ getDensityText(scope.row.density) }}</p>
                <p><span class="label">长度：</span>{{ scope.row.length }}cm {{ getLengthRange(scope.row.length) }}</p>
                <p><span class="label">手柄：</span>{{ getHandleText(scope.row.handle) }}</p>
                <p v-if="scope.row.engraving"><span class="label">刻字：</span>{{ scope.row.engraving }}</p>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="生产进度" min-width="400">
            <template slot-scope="scope">
              <div class="process-container">
                <div class="process-steps">
                  <div 
                    v-for="(step, index) in processSteps" 
                    :key="index"
                    class="process-step"
                    :class="{ active: scope.row.status >= index, current: scope.row.status === index }"
                    @click="showStepHistory(scope.row, index)"
                    title="点击查看操作记录">
                    <div class="step-icon">
                      <i v-if="scope.row.status > index" class="el-icon-check"></i>
                      <span v-else>{{ index + 1 }}</span>
                    </div>
                    <div class="step-name">{{ step }}</div>
                  </div>
                </div>
                <div class="process-actions">
                  <el-button 
                    v-if="scope.row.status < processSteps.length"
                    type="success" 
                    size="mini" 
                    @click="nextStep(scope.$index, scope.row)">
                    完成当前工序
                  </el-button>
                  <el-tag v-else type="success" size="small">已完工</el-tag>
                  <el-button 
                    type="info" 
                    size="mini" 
                    @click="showStatusHistory(scope.row)">
                    查看记录
                  </el-button>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="下单时间" width="170"></el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template slot-scope="scope">
              <el-button type="danger" size="mini" @click="deleteOrder(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-if="orders.length === 0" description="暂无订单"></el-empty>
      </el-card>
    </div>
  `,
  data() {
    return {
      processSteps: ['选料', '开坯', '整形', '开齿', '打磨', '抛光', '刻字', '完工'],
      orders: [],
      newOrderId: null,
      currentOperator: {
        name: '张师傅',
        id: 'OP_' + Math.floor(Math.random() * 1000),
        role: '高级工艺师'
      }
    };
  },
  computed: {
    pendingCount() {
      return this.orders.filter(o => o.status < this.processSteps.length).length;
    }
  },
  created() {
    this.loadOrders();
    eventBus.$on('newOrderCreated', (orderId) => {
      this.newOrderId = orderId;
      this.loadOrders();
      this.$nextTick(() => {
        this.scrollToNewOrder(orderId);
      });
    });
  },
  mounted() {
    if (this.newOrderId) {
      this.$nextTick(() => {
        this.scrollToNewOrder(this.newOrderId);
      });
    }
  },
  beforeDestroy() {
    eventBus.$off('newOrderCreated');
  },
  methods: {
    getLengthRange(length) {
      if (length >= 10 && length <= 13) return '（便携款）';
      if (length >= 14 && length <= 18) return '（标准款）';
      if (length >= 19 && length <= 22) return '（长发款）';
      if (length >= 23 && length <= 25) return '（特殊款）';
      return '';
    },
    tableRowClassName({ row }) {
      if (row.isNew) {
        setTimeout(() => {
          const order = this.orders.find(o => o.id === row.id);
          if (order) {
            order.isNew = false;
          }
        }, 10000);
        return 'new-order-row';
      }
      return '';
    },
    scrollToNewOrder(orderId) {
      const table = this.$refs.orderTable;
      if (table) {
        const rows = table.$el.querySelectorAll('.el-table__row');
        const index = this.orders.findIndex(o => o.id === orderId);
        if (index !== -1 && rows[index]) {
          rows[index].scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    },
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('combOrders') || '[]');
    },
    getMaterialText(val) {
      const map = {
        white: '白水牛角',
        black: '黑水牛角',
        yellow: '黄牛角',
        yak: '牦牛角'
      };
      return map[val] || val;
    },
    getDensityText(val) {
      const map = {
        sparse: '稀疏',
        medium: '适中',
        dense: '密集'
      };
      return map[val] || val;
    },
    getHandleText(val) {
      const map = {
        straight: '直柄',
        curved: '弯柄',
        carved: '雕花',
        none: '无柄'
      };
      return map[val] || val;
    },
    nextStep(index, row) {
      const currentStepName = this.processSteps[row.status];
      this.$confirm(`确认完成「${currentStepName}」工序吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const nextStatus = row.status + 1;
        const nextStepName = nextStatus < this.processSteps.length ? this.processSteps[nextStatus] : '全部完工';
        
        if (!row.statusHistory) {
          row.statusHistory = [];
        }
        
        row.statusHistory.push({
          status: nextStatus,
          stepName: nextStepName,
          operator: this.currentOperator.name,
          operatorId: this.currentOperator.id,
          operatorRole: this.currentOperator.role,
          operationTime: new Date().toLocaleString(),
          operationTimestamp: Date.now(),
          ipAddress: '192.168.1.' + Math.floor(Math.random() * 255),
          note: `完成「${currentStepName}」工序`
        });
        
        row.status = nextStatus;
        
        localStorage.setItem('combOrders', JSON.stringify(this.orders));
        
        this.$message({
          type: 'success',
          message: `「${currentStepName}」工序已完成！操作已记录（${this.currentOperator.name}）`
        });
      }).catch(() => {});
    },
    showStepHistory(row, stepIndex) {
      if (!row.statusHistory) return;
      
      const history = row.statusHistory.filter(h => h.status >= stepIndex);
      if (history.length === 0) return;
      
      this.$alert(
        history.map(h => `
          <div style="margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px solid #eee;">
            <div><strong>工序：</strong>${h.stepName}</div>
            <div><strong>操作人：</strong>${h.operator}（${h.operatorRole || '未知角色'}）</div>
            <div><strong>操作ID：</strong>${h.operatorId}</div>
            <div><strong>时间：</strong>${h.operationTime}</div>
            <div><strong>IP地址：</strong>${h.ipAddress || '未知'}</div>
            <div><strong>备注：</strong>${h.note}</div>
          </div>
        `).join(''),
        `${row.id} - 工序操作记录`,
        {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '关闭'
        }
      );
    },
    showStatusHistory(row) {
      if (!row.statusHistory || row.statusHistory.length === 0) {
        this.$message.info('暂无操作记录');
        return;
      }
      
      this.$alert(
        row.statusHistory.map(h => `
          <div style="margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid #eee;">
            <div><strong>状态：</strong>${h.stepName}</div>
            <div><strong>操作人：</strong>${h.operator}（${h.operatorRole || '未知角色'}）</div>
            <div><strong>操作ID：</strong>${h.operatorId}</div>
            <div><strong>时间：</strong>${h.operationTime}</div>
            <div><strong>IP地址：</strong>${h.ipAddress || '未知'}</div>
            <div><strong>备注：</strong>${h.note}</div>
          </div>
        `).join(''),
        `${row.id} - 完整操作记录`,
        {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '关闭'
        }
      );
    },
    deleteOrder(index) {
      this.$confirm('确认删除该订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orders.splice(index, 1);
        localStorage.setItem('combOrders', JSON.stringify(this.orders));
        this.$message({
          type: 'success',
          message: '删除成功！'
        });
      }).catch(() => {});
    }
  }
};

const routes = [
  { path: '/', component: OrderForm },
  { path: '/admin', component: AdminPanel }
];

const router = new VueRouter({ routes });

new Vue({
  router,
  template: `
    <div class="app-container">
      <el-header class="app-header">
        <div class="header-content">
          <h1 class="app-title">牛角梳定制系统</h1>
          <el-menu 
            mode="horizontal" 
            :router="true" 
            :default-active="$route.path"
            class="nav-menu"
            background-color="transparent"
            text-color="#fff"
            active-text-color="#ffd04b">
            <el-menu-item index="/">客户下单</el-menu-item>
            <el-menu-item index="/admin">订单管理</el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view></router-view>
      </el-main>
      <el-footer class="app-footer">
        <p>© 2024 牛角梳定制系统 - 匠心打造，独一无二</p>
      </el-footer>
    </div>
  `
}).$mount('#app');
