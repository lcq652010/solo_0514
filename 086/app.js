Vue.use(ELEMENT);

const OrderForm = {
  template: `
    <div>
      <h1 class="page-title">传统瓷质茶盏定制 - 客户下单</h1>
      <el-card class="form-card" shadow="hover">
        <el-form 
          :model="orderForm" 
          :rules="rules" 
          ref="orderForm" 
          label-width="120px"
          label-position="right"
        >
          <el-form-item label="泥料类型" prop="clayType">
            <el-radio-group v-model="orderForm.clayType" @change="validateField('clayType')">
              <el-radio label="紫砂泥">紫砂泥</el-radio>
              <el-radio label="青瓷泥">青瓷泥</el-radio>
              <el-radio label="白瓷泥">白瓷泥</el-radio>
              <el-radio label="黑瓷泥">黑瓷泥</el-radio>
              <el-radio label="青花瓷泥">青花瓷泥</el-radio>
            </el-radio-group>
          </el-form-item>

          <el-form-item label="盏口直径 (cm)" prop="diameter">
            <el-input-number 
              v-model="orderForm.diameter" 
              :min="3" 
              :max="15" 
              :step="0.5"
              :precision="1"
              controls-position="right"
              style="width: 200px"
              @change="validateField('diameter')"
            ></el-input-number>
            <span style="margin-left: 10px; color: #909399; font-size: 12px;">范围：3cm - 15cm（品茗杯3-5cm，主人杯6-8cm，公道杯8-15cm）</span>
          </el-form-item>

          <el-form-item label="釉色选择" prop="glazeColor">
            <el-select v-model="orderForm.glazeColor" placeholder="请选择釉色" style="width: 300px" @change="validateField('glazeColor')" clearable>
              <el-option label="天青色" value="天青色"></el-option>
              <el-option label="月白色" value="月白色"></el-option>
              <el-option label="粉青色" value="粉青色"></el-option>
              <el-option label="翠绿色" value="翠绿色"></el-option>
              <el-option label="酱褐色" value="酱褐色"></el-option>
              <el-option label="象牙白" value="象牙白"></el-option>
              <el-option label="宝石蓝" value="宝石蓝"></el-option>
              <el-option label="鸡血红" value="鸡血红"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="花纹图案" prop="pattern">
            <el-select v-model="orderForm.pattern" placeholder="请选择花纹图案" style="width: 300px" @change="validateField('pattern')" clearable>
              <el-option label="素面无纹" value="素面无纹"></el-option>
              <el-option label="山水图案" value="山水图案"></el-option>
              <el-option label="花鸟图案" value="花鸟图案"></el-option>
              <el-option label="龙凤图案" value="龙凤图案"></el-option>
              <el-option label="诗词书法" value="诗词书法"></el-option>
              <el-option label="梅兰竹菊" value="梅兰竹菊"></el-option>
              <el-option label="祥云图案" value="祥云图案"></el-option>
              <el-option label="莲花图案" value="莲花图案"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="订单备注" prop="remark">
            <el-input
              type="textarea"
              :rows="4"
              v-model="orderForm.remark"
              placeholder="请输入特殊要求或备注信息..."
              style="width: 500px"
            ></el-input>
          </el-form-item>

          <el-form-item>
            <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
              提交订单
            </el-button>
            <el-button size="large" @click="resetForm">重置表单</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  `,
  data() {
    return {
      submitting: false,
      orderForm: {
        clayType: '',
        diameter: 6,
        glazeColor: '',
        pattern: '',
        remark: ''
      },
      rules: {
        clayType: [
          { required: true, message: '请选择泥料类型', trigger: 'change' }
        ],
        diameter: [
          { required: true, message: '请输入盏口直径', trigger: 'blur' },
          { type: 'number', min: 3, max: 15, message: '直径范围应为 3-15cm', trigger: 'change' }
        ],
        glazeColor: [
          { required: true, message: '请选择釉色', trigger: 'change' }
        ],
        pattern: [
          { required: true, message: '请选择花纹图案', trigger: 'change' }
        ]
      }
    };
  },
  methods: {
    validateField(field) {
      this.$refs.orderForm.validateField(field);
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true;
          setTimeout(() => {
            const now = new Date().toLocaleString('zh-CN');
            const order = {
              id: Date.now(),
              ...this.orderForm,
              status: 0,
              createTime: now,
              statusHistory: [
                { status: 0, time: now, action: '订单创建' }
              ]
            };
            this.$emit('order-submitted', order);
            this.$message.success('订单提交成功！');
            this.resetForm();
            this.submitting = false;
          }, 1000);
        } else {
          this.$message.error('请完善必填项信息');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.orderForm.resetFields();
    }
  }
};

const AdminPanel = {
  template: `
    <div>
      <h1 class="page-title">管理员订单管理</h1>
      
      <div v-if="isLoading" style="text-align: center; padding: 60px; background: white; border-radius: 12px;">
        <i class="el-icon-loading" style="font-size: 42px; color: #409EFF;"></i>
        <p style="margin-top: 15px; color: #909399;">订单列表加载中...</p>
      </div>

      <div v-else-if="orders.length === 0" style="text-align: center; padding: 60px; background: white; border-radius: 12px;">
        <el-empty description="暂无订单"></el-empty>
      </div>

      <div v-else>
        <div style="margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
          <span style="color: #606266;">共 <strong style="color: #409EFF;">{{ orders.length }}</strong> 个订单</span>
          <el-button size="small" icon="el-icon-refresh" @click="refreshOrders">刷新列表</el-button>
        </div>
        <div v-for="order in orders" :key="order.id" class="order-card">
          <el-card shadow="hover">
            <div slot="header" style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-weight: 600; font-size: 16px;">
                订单号：{{ order.id }}
              </span>
              <el-tag :type="getStatusType(order.status)" size="medium">
                {{ getStatusText(order.status) }}
              </el-tag>
            </div>

            <div class="order-info">
              <div class="info-item">
                <div class="info-label">泥料类型</div>
                <div class="info-value">{{ order.clayType }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">盏口直径</div>
                <div class="info-value">{{ order.diameter }} cm</div>
              </div>
              <div class="info-item">
                <div class="info-label">釉色</div>
                <div class="info-value">{{ order.glazeColor }}</div>
              </div>
              <div class="info-item">
                <div class="info-label">花纹图案</div>
                <div class="info-value">{{ order.pattern }}</div>
              </div>
            </div>

            <div class="status-step">
              <div 
                v-for="(step, index) in steps" 
                :key="index"
                :class="['step-item', { completed: index < order.status, active: index === order.status }]"
              >
                <div class="step-circle">{{ index + 1 }}</div>
                <div class="step-label">{{ step }}</div>
              </div>
            </div>

            <div v-if="order.remark" style="padding: 0 20px 20px;">
              <el-alert
                :title="'备注：' + order.remark"
                type="info"
                :closable="false"
                show-icon
              ></el-alert>
            </div>

            <div style="padding: 0 20px 20px;">
              <el-collapse>
                <el-collapse-item title="操作历史记录">
                  <el-timeline>
                    <el-timeline-item
                      v-for="(record, index) in order.statusHistory"
                      :key="index"
                      :timestamp="record.time"
                      placement="top"
                    >
                      <el-tag size="small">{{ record.action }}</el-tag>
                    </el-timeline-item>
                  </el-timeline>
                </el-collapse-item>
              </el-collapse>
            </div>

            <div style="padding: 0 20px 20px; display: flex; justify-content: space-between; align-items: center;">
              <span style="color: #909399; font-size: 12px;">下单时间：{{ order.createTime }}</span>
              <div>
                <el-button 
                  v-if="order.status > 0" 
                  size="small" 
                  @click="prevStep(order)"
                >
                  上一步
                </el-button>
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="nextStep(order)"
                  :disabled="order.status >= steps.length - 1"
                >
                  下一步
                </el-button>
                <span v-if="order.status >= steps.length - 1" style="color: #67c23a; font-weight: 600; margin-left: 10px;">
                  ✓ 已完工
                </span>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>
  `,
  props: {
    orders: {
      type: Array,
      default: () => []
    },
    loading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      localLoading: false,
      steps: ['揉泥', '拉坯', '利坯', '施釉', '烧制', '上彩', '完工']
    };
  },
  computed: {
    isLoading() {
      return this.loading || this.localLoading;
    }
  },
  methods: {
    getStatusText(status) {
      return this.steps[status] || '未知';
    },
    getStatusType(status) {
      if (status >= this.steps.length - 1) return 'success';
      if (status >= 4) return 'warning';
      return 'info';
    },
    nextStep(order) {
      if (order.status >= this.steps.length - 1) {
        this.$message.warning('订单已完成，无法继续前进');
        return;
      }
      const newStatus = order.status + 1;
      order.status = newStatus;
      if (!order.statusHistory) {
        order.statusHistory = [];
      }
      order.statusHistory.push({
        status: newStatus,
        time: new Date().toLocaleString('zh-CN'),
        action: '推进至：' + this.steps[newStatus]
      });
      this.$message.success(`生产流程已推进：${this.steps[newStatus]}`);
    },
    prevStep(order) {
      if (order.status <= 0) {
        this.$message.warning('已在初始状态，无法回退');
        return;
      }
      const newStatus = order.status - 1;
      order.status = newStatus;
      if (!order.statusHistory) {
        order.statusHistory = [];
      }
      order.statusHistory.push({
        status: newStatus,
        time: new Date().toLocaleString('zh-CN'),
        action: '回退至：' + this.steps[newStatus]
      });
      this.$message.info(`生产流程已回退至：${this.steps[newStatus]}`);
    },
    refreshOrders() {
      this.localLoading = true;
      setTimeout(() => {
        this.localLoading = false;
        this.$message.success('订单列表已刷新');
      }, 800);
    }
  }
};

new Vue({
  el: '#app',
  components: {
    OrderForm,
    AdminPanel
  },
  data() {
    return {
      activeRoute: 'order',
      orders: [],
      orderListLoading: false
    };
  },
  computed: {
    currentComponent() {
      return this.activeRoute === 'order' ? 'OrderForm' : 'AdminPanel';
    }
  },
  methods: {
    handleRouteChange(index) {
      this.activeRoute = index;
      if (index === 'admin') {
        this.orderListLoading = true;
        setTimeout(() => {
          this.orderListLoading = false;
        }, 500);
      }
    },
    handleOrderSubmitted(order) {
      this.orderListLoading = true;
      setTimeout(() => {
        this.orders.unshift(order);
        this.orderListLoading = false;
        this.$message.success('订单已同步至管理列表');
      }, 600);
    }
  }
});
