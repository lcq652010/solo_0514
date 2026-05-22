document.addEventListener('DOMContentLoaded', function() {
  Vue.use(VueRouter);
  Vue.use(ELEMENT);

const OrderForm = {
  template: `
    <div class="order-form-container">
      <el-card class="form-card" shadow="hover">
        <div slot="header" class="clearfix">
          <span style="font-size: 20px; font-weight: bold; color: #8B4513;">🦴 兽骨雕挂牌定制下单</span>
        </div>
        
        <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
          
          <el-divider content-position="left">骨料选材</el-divider>
          <el-form-item label="骨料类型" prop="boneType">
            <el-radio-group v-model="orderForm.boneType">
              <el-radio v-for="bone in boneTypes" :key="bone.value" :label="bone.value">
                {{ bone.label }} (+¥{{ bone.price }})
              </el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-divider content-position="left">挂牌尺寸</el-divider>
          <el-form-item label="长度 (mm)" prop="length">
            <el-input-number v-model="orderForm.length" :min="30" :max="100" :step="1"></el-input-number>
            <div class="size-hint">
              <span class="hint-label">标准范围：</span>
              <span class="hint-value recommended">生产推荐：45-65mm</span>
              <span class="hint-label">可接受范围：</span>
              <span class="hint-value">30-100mm</span>
            </div>
            <div v-if="!isLengthRecommended" class="warning-text">
              <i class="el-icon-warning"></i> 当前尺寸不在推荐生产范围内，可能影响生产效率
            </div>
          </el-form-item>
          <el-form-item label="宽度 (mm)" prop="width">
            <el-input-number v-model="orderForm.width" :min="20" :max="80" :step="1"></el-input-number>
            <div class="size-hint">
              <span class="hint-label">标准范围：</span>
              <span class="hint-value recommended">生产推荐：25-45mm</span>
              <span class="hint-label">可接受范围：</span>
              <span class="hint-value">20-80mm</span>
            </div>
            <div v-if="!isWidthRecommended" class="warning-text">
              <i class="el-icon-warning"></i> 当前尺寸不在推荐生产范围内，可能影响生产效率
            </div>
          </el-form-item>
          
          <el-divider content-position="left">纹饰图案</el-divider>
          <el-form-item label="图案选择" prop="pattern">
            <el-select v-model="orderForm.pattern" placeholder="请选择纹饰图案" style="width: 100%;">
              <el-option v-for="p in patterns" :key="p.value" :label="p.label" :value="p.value">
                <span style="float: left">{{ p.label }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">+¥{{ p.price }}</span>
              </el-option>
            </el-select>
          </el-form-item>
          
          <el-divider content-position="left">做旧工艺</el-divider>
          <el-form-item label="工艺类型" prop="agingProcess">
            <el-radio-group v-model="orderForm.agingProcess">
              <el-radio v-for="process in agingProcesses" :key="process.value" :label="process.value">
                {{ process.label }} (+¥{{ process.price }})
              </el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-divider content-position="left">挂孔位置</el-divider>
          <el-form-item label="挂孔位置" prop="holePosition">
            <el-radio-group v-model="orderForm.holePosition">
              <el-radio v-for="pos in holePositions" :key="pos.value" :label="pos.value">
                {{ pos.label }}
              </el-radio>
            </el-radio-group>
          </el-form-item>
          
          <el-divider></el-divider>
          
          <el-form-item label="客户姓名" prop="customerName">
            <el-input v-model="orderForm.customerName" placeholder="请输入姓名"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
          <el-form-item label="备注说明">
            <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="其他特殊要求"></el-input>
          </el-form-item>
          
          <el-form-item>
            <el-button type="primary" @click="submitOrder" style="width: 100%; height: 50px; font-size: 18px;" :loading="submitting">
              提交订单 (总计: ¥{{ totalPrice }})
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  `,
  data() {
    const validateLength = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入长度'));
      } else if (value < 30 || value > 100) {
        callback(new Error('长度必须在30-100mm之间'));
      } else if (!Number.isInteger(Number(value))) {
        callback(new Error('长度必须为整数'));
      } else {
        callback();
      }
    };
    
    const validateWidth = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入宽度'));
      } else if (value < 20 || value > 80) {
        callback(new Error('宽度必须在20-80mm之间'));
      } else if (!Number.isInteger(Number(value))) {
        callback(new Error('宽度必须为整数'));
      } else {
        callback();
      }
    };

    const validateBoneType = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择骨料类型'));
      } else {
        const validBoneTypes = this.boneTypes.map(b => b.value);
        if (!validBoneTypes.includes(value)) {
          callback(new Error('请选择有效的骨料类型'));
        } else {
          callback();
        }
      }
    };

    const validatePattern = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择纹饰图案'));
      } else {
        const validPatterns = this.patterns.map(p => p.value);
        if (!validPatterns.includes(value)) {
          callback(new Error('请选择有效的纹饰图案'));
        } else {
          callback();
        }
      }
    };

    return {
      submitting: false,
      orderForm: {
        boneType: '',
        length: 50,
        width: 30,
        pattern: '',
        agingProcess: '',
        holePosition: '',
        customerName: '',
        phone: '',
        remark: ''
      },
      rules: {
        boneType: [
          { required: true, validator: validateBoneType, trigger: 'change' }
        ],
        length: [
          { required: true, validator: validateLength, trigger: 'blur' }
        ],
        width: [
          { required: true, validator: validateWidth, trigger: 'blur' }
        ],
        pattern: [
          { required: true, validator: validatePattern, trigger: 'change' }
        ],
        agingProcess: [{ required: true, message: '请选择做旧工艺', trigger: 'change' }],
        holePosition: [{ required: true, message: '请选择挂孔位置', trigger: 'change' }],
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      boneTypes: [
        { label: '牛骨', value: 'cow', price: 100 },
        { label: '鹿角', value: 'deer', price: 200 },
        { label: '象牙果', value: 'ivory', price: 150 },
        { label: '骆驼骨', value: 'camel', price: 180 }
      ],
      patterns: [
        { label: '祥云纹', value: 'cloud', price: 50 },
        { label: '龙凤纹', value: 'dragon', price: 120 },
        { label: '回字纹', value: 'hui', price: 40 },
        { label: '饕餮纹', value: 'taotie', price: 100 },
        { label: '莲花纹', value: 'lotus', price: 60 },
        { label: '自定义图案', value: 'custom', price: 200 }
      ],
      agingProcesses: [
        { label: '古法烟熏', value: 'smoke', price: 80 },
        { label: '茶水煮', value: 'tea', price: 60 },
        { label: '太阳暴晒', value: 'sun', price: 40 },
        { label: '不做旧', value: 'none', price: 0 }
      ],
      holePositions: [
        { label: '顶部居中', value: 'top-center' },
        { label: '左上角', value: 'top-left' },
        { label: '右上角', value: 'top-right' },
        { label: '左右对称', value: 'both-sides' }
      ],
      recommendedLength: { min: 45, max: 65 },
      recommendedWidth: { min: 25, max: 45 }
    };
  },
  computed: {
    totalPrice() {
      let basePrice = 50;
      const bone = this.boneTypes.find(b => b.value === this.orderForm.boneType);
      if (bone) basePrice += bone.price;
      
      const pattern = this.patterns.find(p => p.value === this.orderForm.pattern);
      if (pattern) basePrice += pattern.price;
      
      const process = this.agingProcesses.find(p => p.value === this.orderForm.agingProcess);
      if (process) basePrice += process.price;
      
      return basePrice;
    },
    isLengthRecommended() {
      return this.orderForm.length >= this.recommendedLength.min && 
             this.orderForm.length <= this.recommendedLength.max;
    },
    isWidthRecommended() {
      return this.orderForm.width >= this.recommendedWidth.min && 
             this.orderForm.width <= this.recommendedWidth.max;
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true;
          setTimeout(() => {
            const newOrder = {
              id: 'ORD' + Date.now(),
              ...this.orderForm,
              status: 0,
              createTime: new Date().toLocaleString(),
              createTimestamp: Date.now(),
              totalPrice: this.totalPrice,
              isNew: true,
              statusHistory: [
                { 
                  status: 0, 
                  time: new Date().toLocaleString(), 
                  remark: '订单创建',
                  operator: '客户自助',
                  terminal: this.getTerminalInfo()
                }
              ]
            };
            
            const orders = JSON.parse(localStorage.getItem('boneOrders') || '[]');
            orders.unshift(newOrder);
            localStorage.setItem('boneOrders', JSON.stringify(orders));
            
            this.submitting = false;
            this.$message.success('订单提交成功！订单号：' + newOrder.id);
            this.$refs.orderForm.resetFields();
            this.orderForm.length = 50;
            this.orderForm.width = 30;
          }, 1000);
        } else {
          this.$message.error('请完善订单信息');
          return false;
        }
      });
    },
    getTerminalInfo() {
      const ua = navigator.userAgent;
      let browser = '未知浏览器';
      let os = '未知系统';
      
      if (ua.includes('Chrome')) browser = 'Chrome';
      else if (ua.includes('Firefox')) browser = 'Firefox';
      else if (ua.includes('Safari')) browser = 'Safari';
      else if (ua.includes('Edge')) browser = 'Edge';
      
      if (ua.includes('Windows')) os = 'Windows';
      else if (ua.includes('Mac')) os = 'MacOS';
      else if (ua.includes('Linux')) os = 'Linux';
      else if (ua.includes('Android')) os = 'Android';
      else if (ua.includes('iPhone')) os = 'iOS';
      
      return `${os} / ${browser}`;
    }
  }
};

const AdminPanel = {
  template: `
    <div class="admin-panel-container" id="admin-panel">
      <el-card class="admin-card" shadow="hover">
        <div slot="header" class="clearfix">
          <span style="font-size: 20px; font-weight: bold; color: #8B4513;">📋 管理员订单管理</span>
          <el-button style="float: right; padding: 3px 0" type="text" @click="loadOrders">刷新</el-button>
        </div>
        
        <el-table :data="orders" style="width: 100%" border v-loading="loading" ref="orderTable" :row-class-name="getRowClassName">
          <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
          <el-table-column prop="id" label="订单号" width="170">
            <template slot-scope="scope">
              <span style="position: relative;">
                {{ scope.row.id }}
                <el-tag v-if="isNewOrder(scope.row)" type="danger" size="mini" class="new-order-badge">新</el-tag>
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="customerName" label="客户" width="100"></el-table-column>
          <el-table-column prop="boneType" label="骨料" width="100">
            <template slot-scope="scope">
              {{ getBoneLabel(scope.row.boneType) }}
            </template>
          </el-table-column>
          <el-table-column label="尺寸" width="100">
            <template slot-scope="scope">
              <span :class="{'size-warning': !isSizeRecommended(scope.row)}">
                {{ scope.row.length }}×{{ scope.row.width }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="pattern" label="纹饰" width="100">
            <template slot-scope="scope">
              {{ getPatternLabel(scope.row.pattern) }}
            </template>
          </el-table-column>
          <el-table-column prop="totalPrice" label="价格" width="80">
            <template slot-scope="scope">
              ¥{{ scope.row.totalPrice }}
            </template>
          </el-table-column>
          <el-table-column label="生产进度" width="500">
            <template slot-scope="scope">
              <el-steps :active="scope.row.status" finish-status="success" align-center size="small">
                <el-step v-for="(step, idx) in steps" :key="idx" :title="step"></el-step>
              </el-steps>
              <div class="status-history" v-if="scope.row.statusHistory && scope.row.statusHistory.length > 0">
                <el-tag size="mini" type="info" class="history-tag" v-for="(h, idx) in scope.row.statusHistory.slice(-2)" :key="idx">
                  {{ steps[h.status] || '未知' }}: {{ h.time }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="220">
            <template slot-scope="scope">
              <el-button 
                size="mini" 
                type="primary" 
                @click="nextStep(scope.row, scope.$index)"
                :disabled="scope.row.status >= 8"
              >
                下一步
              </el-button>
              <el-popover
                placement="top"
                width="400"
                v-model="scope.row.showHistory"
                trigger="click">
                <div style="max-height: 250px; overflow-y: auto;">
                  <p v-for="(h, idx) in (scope.row.statusHistory || [])" :key="idx" style="margin: 8px 0; font-size: 12px; padding: 5px; background: #f5f7fa; border-radius: 4px;">
                    <el-tag size="mini" type="success" style="margin-right: 8px;">{{ steps[h.status] || '未知' }}</el-tag>
                    <span style="color: #666;">{{ h.time }}</span>
                    <br>
                    <span v-if="h.operator" style="color: #999; font-size: 11px;">操作人: {{ h.operator }}</span>
                    <span v-if="h.terminal" style="color: #999; font-size: 11px; margin-left: 10px;">终端: {{ h.terminal }}</span>
                    <span v-if="h.remark" style="color: #999; margin-left: 10px; font-size: 11px;">{{ h.remark }}</span>
                  </p>
                </div>
                <el-button size="mini" slot="reference" type="success">历史</el-button>
              </el-popover>
              <el-button size="mini" type="danger" @click="deleteOrder(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>
      </el-card>
    </div>
  `,
  data() {
    return {
      loading: false,
      orders: [],
      operatorName: '管理员',
      boneTypes: [
        { label: '牛骨', value: 'cow' },
        { label: '鹿角', value: 'deer' },
        { label: '象牙果', value: 'ivory' },
        { label: '骆驼骨', value: 'camel' }
      ],
      patterns: [
        { label: '祥云纹', value: 'cloud' },
        { label: '龙凤纹', value: 'dragon' },
        { label: '回字纹', value: 'hui' },
        { label: '饕餮纹', value: 'taotie' },
        { label: '莲花纹', value: 'lotus' },
        { label: '自定义图案', value: 'custom' }
      ],
      steps: ['选料', '切胚', '整形', '雕刻', '做旧', '打孔', '抛光', '完工'],
      recommendedLength: { min: 45, max: 65 },
      recommendedWidth: { min: 25, max: 45 },
      newOrderDuration: 5 * 60 * 1000
    };
  },
  mounted() {
    this.loadOrders();
    this.checkNewOrders();
    this.promptOperatorName();
  },
  methods: {
    promptOperatorName() {
      const savedName = localStorage.getItem('operatorName');
      if (savedName) {
        this.operatorName = savedName;
      }
    },
    loadOrders() {
      this.loading = true;
      setTimeout(() => {
        const oldOrders = this.orders;
        this.orders = JSON.parse(localStorage.getItem('boneOrders') || '[]');
        
        this.orders.forEach(order => {
          if (!order.statusHistory) {
            order.statusHistory = [
              { status: order.status, time: order.createTime, remark: '历史订单', operator: '系统', terminal: '未知' }
            ];
          }
        });
        
        if (this.orders.length > oldOrders.length) {
          this.$nextTick(() => {
            this.scrollToNewOrder();
          });
        }
        
        this.loading = false;
      }, 500);
    },
    checkNewOrders() {
      setInterval(() => {
        const currentOrders = JSON.parse(localStorage.getItem('boneOrders') || '[]');
        if (currentOrders.length > this.orders.length) {
          this.$message.info('检测到新订单，正在刷新列表...');
          this.loadOrders();
        }
      }, 3000);
    },
    scrollToNewOrder() {
      const tableWrapper = document.querySelector('.el-table__body-wrapper');
      if (tableWrapper) {
        tableWrapper.scrollTop = 0;
      }
    },
    getRowClassName({ row }) {
      if (this.isNewOrder(row)) {
        return 'new-order-row';
      }
      return '';
    },
    isNewOrder(order) {
      if (!order.createTimestamp) return false;
      const age = Date.now() - order.createTimestamp;
      return age < this.newOrderDuration;
    },
    isSizeRecommended(order) {
      return order.length >= this.recommendedLength.min && 
             order.length <= this.recommendedLength.max &&
             order.width >= this.recommendedWidth.min && 
             order.width <= this.recommendedWidth.max;
    },
    getBoneLabel(value) {
      const bone = this.boneTypes.find(b => b.value === value);
      return bone ? bone.label : value;
    },
    getPatternLabel(value) {
      const pattern = this.patterns.find(p => p.value === value);
      return pattern ? pattern.label : value;
    },
    getTerminalInfo() {
      const ua = navigator.userAgent;
      let browser = '未知浏览器';
      let os = '未知系统';
      
      if (ua.includes('Chrome')) browser = 'Chrome';
      else if (ua.includes('Firefox')) browser = 'Firefox';
      else if (ua.includes('Safari')) browser = 'Safari';
      else if (ua.includes('Edge')) browser = 'Edge';
      
      if (ua.includes('Windows')) os = 'Windows';
      else if (ua.includes('Mac')) os = 'MacOS';
      else if (ua.includes('Linux')) os = 'Linux';
      else if (ua.includes('Android')) os = 'Android';
      else if (ua.includes('iPhone')) os = 'iOS';
      
      return `${os} / ${browser}`;
    },
    nextStep(order, index) {
      const currentStatus = order.status;
      
      if (currentStatus >= 8) {
        this.$message.warning('订单已完成，无法继续推进');
        return;
      }
      
      if (currentStatus < 0) {
        this.$message.error('无效的订单状态');
        return;
      }
      
      const nextStatus = currentStatus + 1;
      order.status = nextStatus;
      
      if (!order.statusHistory) {
        order.statusHistory = [];
      }
      
      order.statusHistory.push({
        status: nextStatus,
        time: new Date().toLocaleString(),
        remark: '工序推进',
        operator: this.operatorName,
        terminal: this.getTerminalInfo()
      });
      
      localStorage.setItem('boneOrders', JSON.stringify(this.orders));
      
      if (nextStatus >= 8) {
        this.$message.success('订单已完成！');
      } else {
        this.$message.success('已推进到：' + this.steps[nextStatus - 1]);
      }
    },
    deleteOrder(index) {
      this.$confirm('确定删除该订单吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orders.splice(index, 1);
        localStorage.setItem('boneOrders', JSON.stringify(this.orders));
        this.$message.success('删除成功');
      }).catch(() => {});
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
    <div class="app-container">
      <el-menu 
        :default-active="activeRoute" 
        mode="horizontal" 
        background-color="#8B4513"
        text-color="#fff"
        active-text-color="#ffd04b"
        style="margin-bottom: 20px;"
      >
        <el-menu-item index="/" @click="goTo('/')">
          <i class="el-icon-edit"></i>
          <span>客户下单</span>
        </el-menu-item>
        <el-menu-item index="/admin" @click="goTo('/admin')">
          <i class="el-icon-s-management"></i>
          <span>管理后台</span>
        </el-menu-item>
      </el-menu>
      
      <div class="content-wrapper">
        <router-view></router-view>
      </div>
      
      <div class="footer">
        <p>© 2024 兽骨雕挂牌定制系统 - 传统工艺，匠心独运</p>
      </div>
    </div>
  `,
  computed: {
    activeRoute() {
      return this.$route.path;
    }
  },
  methods: {
    goTo(path) {
      this.$router.push(path);
    }
  }
}).$mount('#app');

const style = document.createElement('style');
style.textContent = `
  .app-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px 20px;
  }
  .content-wrapper {
    min-height: calc(100vh - 120px);
  }
  .form-card, .admin-card {
    max-width: 800px;
    margin: 0 auto;
  }
  .admin-card {
    max-width: 1400px;
  }
  .el-divider--horizontal {
    margin: 20px 0;
  }
  .footer {
    text-align: center;
    padding: 20px;
    color: #666;
    margin-top: 40px;
  }
  .el-step__title {
    font-size: 12px;
  }
  .status-history {
    margin-top: 10px;
    text-align: center;
  }
  .history-tag {
    margin: 2px;
  }
  .el-table__body-wrapper {
    overflow-y: auto;
  }
  .size-hint {
    margin-top: 8px;
    font-size: 12px;
    line-height: 1.6;
  }
  .hint-label {
    color: #909399;
    margin-right: 5px;
  }
  .hint-value {
    color: #606266;
    margin-right: 15px;
  }
  .hint-value.recommended {
    color: #67C23A;
    font-weight: bold;
  }
  .warning-text {
    margin-top: 5px;
    font-size: 12px;
    color: #E6A23C;
  }
  .new-order-row {
    background: linear-gradient(90deg, #fef0f0 0%, #fff 50%, #fef0f0 100%) !important;
  }
  .new-order-badge {
    position: absolute;
    top: -8px;
    right: -30px;
    animation: pulse 1.5s infinite;
  }
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.8; }
    100% { transform: scale(1); opacity: 1; }
  }
  .size-warning {
    color: #E6A23C;
    font-weight: bold;
  }
`;
document.head.appendChild(style);
});
