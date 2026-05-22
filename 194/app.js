const orderStore = {
  orders: [],
  processSteps: [
    { id: 1, name: '熔铜', icon: '🔥' },
    { id: 2, name: '铸坯', icon: '📦' },
    { id: 3, name: '打磨', icon: '✨' },
    { id: 4, name: '雕刻', icon: '🪚' },
    { id: 5, name: '做旧', icon: '🎨' },
    { id: 6, name: '抛光', icon: '💎' },
    { id: 7, name: '质检', icon: '✅' },
    { id: 8, name: '完工', icon: '🎉' }
  ],
  materials: [
    { id: 'h62', name: 'H62黄铜', desc: '含铜62%，色泽金黄，适合精雕', price: 0.8 },
    { id: 'h59', name: 'H59黄铜', desc: '含铜59%，硬度较高，性价比高', price: 0.65 },
    { id: 'c1100', name: '紫铜', desc: '含铜99.9%，色泽古朴典雅', price: 1.0 },
    { id: 'qsn65', name: '锡青铜', desc: '铜锡合金，耐磨抗腐蚀', price: 1.2 }
  ],
  patterns: [
    { id: 'cloud', name: '祥云纹', icon: '☁️' },
    { id: 'dragon', name: '龙纹', icon: '🐉' },
    { id: 'phoenix', name: '凤纹', icon: '🦅' },
    { id: 'lotus', name: '莲花纹', icon: '🪷' },
    { id: 'bamboo', name: '竹节纹', icon: '🎋' },
    { id: 'plum', name: '梅花纹', icon: '🌸' },
    { id: 'landscape', name: '山水纹', icon: '🏔️' },
    { id: 'custom', name: '自定义文字', icon: '✍️' }
  ],
  crafts: [
    { id: 'matte', name: '哑光处理', desc: '表面细腻，手感温润', price: 0 },
    { id: 'bright', name: '亮光抛光', desc: '光亮如镜，华贵典雅', price: 50 },
    { id: 'antique', name: '仿古做旧', desc: '古色古香，韵味悠长', price: 80 },
    { id: 'gilt', name: '鎏金工艺', desc: '金线勾勒，富丽堂皇', price: 150 }
  ]
};

const OrderPage = {
  template: `
    <div class="page-container">
      <h2 class="page-title">客户下单</h2>
      <el-form :model="form" :rules="rules" ref="orderForm" class="order-form" label-width="100px">
        <div class="form-section">
          <h3 class="section-title">一、选择铜材类型</h3>
          <el-row :gutter="20">
            <el-col :span="12" v-for="mat in materials" :key="mat.id">
              <div :class="['material-card', { selected: form.material === mat.id }]" @click="form.material = mat.id">
                <el-card shadow="hover">
                  <div slot="header">
                    <strong>{{ mat.name }}</strong>
                  </div>
                  <p style="color: #666; font-size: 13px;">{{ mat.desc }}</p>
                  <p style="color: #ff6600; margin-top: 8px;">¥{{ mat.price }} 元/克</p>
                </el-card>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h3 class="section-title">二、镇纸尺寸规格</h3>
          <div class="dimension-inputs">
            <div class="dimension-item">
              <el-form-item label="长度" prop="length">
                <el-input-number v-model="form.length" :min="80" :max="300" :step="10" style="width: 100%;"></el-input-number>
                <span style="margin-left: 10px;">毫米</span>
              </el-form-item>
              <div :class="['process-tip', getLengthTipClass()]">
                <i class="el-icon-info"></i>
                {{ getLengthTip() }}
              </div>
            </div>
            <div class="dimension-item">
              <el-form-item label="宽度" prop="width">
                <el-input-number v-model="form.width" :min="20" :max="80" :step="5" style="width: 100%;"></el-input-number>
                <span style="margin-left: 10px;">毫米</span>
              </el-form-item>
              <div :class="['process-tip', getWidthTipClass()]">
                <i class="el-icon-info"></i>
                {{ getWidthTip() }}
              </div>
            </div>
          </div>
          <div class="dimension-inputs">
            <div class="dimension-item">
              <el-form-item label="厚度" prop="thickness">
                <el-input-number v-model="form.thickness" :min="5" :max="20" :step="1" style="width: 100%;"></el-input-number>
                <span style="margin-left: 10px;">毫米</span>
              </el-form-item>
            </div>
            <div class="dimension-item">
              <el-form-item label="数量" prop="quantity">
                <el-input-number v-model="form.quantity" :min="1" :max="10" style="width: 100%;"></el-input-number>
                <span style="margin-left: 10px;">件</span>
              </el-form-item>
            </div>
          </div>
        </div>

        <div class="form-section">
          <h3 class="section-title">三、纹饰雕刻</h3>
          <div class="pattern-grid">
            <div 
              v-for="pt in patterns" 
              :key="pt.id"
              :class="['pattern-item', { selected: form.pattern === pt.id }]"
              @click="form.pattern = pt.id"
            >
              <div class="pattern-icon">{{ pt.icon }}</div>
              <div class="pattern-name">{{ pt.name }}</div>
            </div>
          </div>
          <el-form-item label="雕刻文字" v-if="form.pattern === 'custom'" style="margin-top: 15px;">
            <el-input v-model="form.customText" placeholder="请输入需要雕刻的文字（限20字以内）" maxlength="20"></el-input>
          </el-form-item>
        </div>

        <div class="form-section">
          <h3 class="section-title">四、表面处理工艺</h3>
          <el-form-item prop="craft">
            <el-radio-group v-model="form.craft">
              <el-radio v-for="c in crafts" :key="c.id" :label="c.id" class="craft-radio" border>
                <div style="display: flex; justify-content: space-between; width: 100%;">
                  <span>{{ c.name }}</span>
                  <span style="color: #ff6600;">{{ c.price > 0 ? '+' + c.price + '元' : '免费' }}</span>
                </div>
                <div style="color: #999; font-size: 12px; margin-top: 5px;">{{ c.desc }}</div>
              </el-radio>
            </el-radio-group>
          </el-form-item>
        </div>

        <div class="form-section">
          <h3 class="section-title">五、客户信息</h3>
          <el-form-item label="客户姓名" prop="customerName">
            <el-input v-model="form.customerName" placeholder="请输入您的姓名"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="customerPhone">
            <el-input v-model="form.customerPhone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="form.remark" placeholder="其他特殊要求" :rows="3"></el-input>
          </el-form-item>
        </div>

        <div class="preview-card">
          <div class="preview-demo">
            镇纸预览效果
          </div>
          <p style="font-size: 13px;">长度: {{ form.length }}mm × 宽度: {{ form.width }}mm × 厚度: {{ form.thickness }}mm</p>
          <p style="font-size: 13px; margin-top: 5px;">
            铜材: {{ getMaterialName(form.material) }} | 纹饰: {{ getPatternName(form.pattern) }}
          </p>
        </div>

        <div class="price-info">
          <p style="margin-bottom: 10px; color: #666;">预估总价</p>
          <p class="price-value">¥{{ totalPrice }}</p>
          <p style="font-size: 12px; color: #999; margin-top: 8px;">
            (铜材约{{ estimatedWeight }}克 × 单价 + 工艺费)
          </p>
        </div>

        <el-button type="primary" class="submit-btn" @click="submitOrder">提交订单</el-button>
      </el-form>
    </div>
  `,
  data() {
    return {
      materials: orderStore.materials,
      patterns: orderStore.patterns,
      crafts: orderStore.crafts,
      form: {
        material: 'h62',
        length: 150,
        width: 40,
        thickness: 10,
        quantity: 1,
        pattern: 'cloud',
        craft: 'matte',
        customText: '',
        customerName: '',
        customerPhone: '',
        remark: ''
      },
      rules: {
        material: [{ required: true, message: '请选择铜材类型', trigger: 'change' }],
        length: [
          { required: true, message: '请输入长度', trigger: 'blur' },
          { type: 'number', message: '长度必须为数字', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value === '' || value === null || isNaN(value)) {
                callback(new Error('请输入有效的数字'));
              } else if (value < 80 || value > 300) {
                callback(new Error('长度范围为80-300毫米'));
              } else if (value % 10 !== 0) {
                callback(new Error('长度必须为10的整数倍'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        width: [
          { required: true, message: '请输入宽度', trigger: 'blur' },
          { type: 'number', message: '宽度必须为数字', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (value === '' || value === null || isNaN(value)) {
                callback(new Error('请输入有效的数字'));
              } else if (value < 20 || value > 80) {
                callback(new Error('宽度范围为20-80毫米'));
              } else if (value % 5 !== 0) {
                callback(new Error('宽度必须为5的整数倍'));
              } else {
                callback();
              }
            },
            trigger: 'blur'
          }
        ],
        thickness: [{ required: true, message: '请输入厚度', trigger: 'blur' }],
        pattern: [{ required: true, message: '请选择纹饰', trigger: 'change' }],
        craft: [{ required: true, message: '请选择表面处理工艺', trigger: 'change' }],
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        customerPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    estimatedWeight() {
      const volume = this.form.length * this.form.width * this.form.thickness;
      const density = 8.5;
      return Math.round(volume * density / 1000 * this.form.quantity);
    },
    materialPrice() {
      const mat = this.materials.find(m => m.id === this.form.material);
      return mat ? mat.price : 0;
    },
    craftPrice() {
      const craft = this.crafts.find(c => c.id === this.form.craft);
      return craft ? craft.price : 0;
    },
    totalPrice() {
      return Math.round(this.estimatedWeight * this.materialPrice + this.craftPrice);
    }
  },
  methods: {
    getMaterialName(id) {
      const mat = this.materials.find(m => m.id === id);
      return mat ? mat.name : '';
    },
    getPatternName(id) {
      const pt = this.patterns.find(p => p.id === id);
      return pt ? pt.name : '';
    },
    getLengthTip() {
      const len = this.form.length;
      if (len >= 80 && len < 120) {
        return '小巧精致款：适合随身携带、书签用途';
      } else if (len >= 120 && len < 200) {
        return '标准通用款：适合日常书画、压纸使用';
      } else if (len >= 200 && len <= 300) {
        return '大气厚重款：适合大幅作品、镇尺使用';
      }
      return '';
    },
    getLengthTipClass() {
      const len = this.form.length;
      if (len >= 120 && len < 200) {
        return 'tip-recommend';
      }
      return 'tip-normal';
    },
    getWidthTip() {
      const width = this.form.width;
      if (width >= 20 && width < 35) {
        return '纤细款：适合轻型纸张';
      } else if (width >= 35 && width < 55) {
        return '标准款：稳定性好，适合大多数场景';
      } else if (width >= 55 && width <= 80) {
        return '宽版款：稳重厚实，适合厚重书籍';
      }
      return '';
    },
    getWidthTipClass() {
      const width = this.form.width;
      if (width >= 35 && width < 55) {
        return 'tip-recommend';
      }
      return 'tip-normal';
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          const order = {
            id: 'ORD' + Date.now(),
            ...this.form,
            weight: this.estimatedWeight,
            totalPrice: this.totalPrice,
            status: 'pending',
            currentStep: 0,
            createTime: new Date().toLocaleString('zh-CN'),
            materialName: this.getMaterialName(this.form.material),
            patternName: this.getPatternName(this.form.pattern),
            craftName: this.crafts.find(c => c.id === this.form.craft)?.name || '',
            isNew: true,
            expanded: true
          };
          orderStore.orders.forEach(o => o.isNew = false);
          orderStore.orders.unshift(order);
          this.$message.success('订单提交成功！');
          this.resetForm();
          this.$root.activeMenu = 'admin';
        }
      });
    },
    resetForm() {
      this.$refs.orderForm.clearValidate();
      this.form.material = 'h62';
      this.form.length = 150;
      this.form.width = 40;
      this.form.thickness = 10;
      this.form.quantity = 1;
      this.form.pattern = 'cloud';
      this.form.craft = 'matte';
      this.form.customText = '';
      this.form.customerName = '';
      this.form.customerPhone = '';
      this.form.remark = '';
      this.$nextTick(() => {
        this.$refs.orderForm.resetFields();
      });
    }
  }
};

const AdminPage = {
  template: `
    <div class="page-container">
      <h2 class="page-title">订单管理</h2>
      <el-row :gutter="20" style="margin-bottom: 20px;">
        <el-col :span="6">
          <el-card :class="{ 'stat-card-active': statusFilter === 'pending' }" @click.native="setFilter('pending')" style="cursor: pointer;">
            <div style="text-align: center;">
              <div style="font-size: 28px; color: #e6a23c;">{{ pendingCount }}</div>
              <div style="color: #666; margin-top: 5px;">待处理</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :class="{ 'stat-card-active': statusFilter === 'processing' }" @click.native="setFilter('processing')" style="cursor: pointer;">
            <div style="text-align: center;">
              <div style="font-size: 28px; color: #409eff;">{{ processingCount }}</div>
              <div style="color: #666; margin-top: 5px;">生产中</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :class="{ 'stat-card-active': statusFilter === 'completed' }" @click.native="setFilter('completed')" style="cursor: pointer;">
            <div style="text-align: center;">
              <div style="font-size: 28px; color: #67c23a;">{{ completedCount }}</div>
              <div style="color: #666; margin-top: 5px;">已完成</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card :class="{ 'stat-card-active': statusFilter === 'all' }" @click.native="setFilter('all')" style="cursor: pointer;">
            <div style="text-align: center;">
              <div style="font-size: 28px; color: #909399;">{{ totalAmount }}</div>
              <div style="color: #666; margin-top: 5px;">总金额(元)</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <div style="margin-bottom: 20px;">
        <el-button-group>
          <el-button :type="statusFilter === 'all' ? 'primary' : ''" @click="setFilter('all')">全部订单</el-button>
          <el-button :type="statusFilter === 'pending' ? 'warning' : ''" @click="setFilter('pending')">待生产</el-button>
          <el-button :type="statusFilter === 'processing' ? 'primary' : ''" @click="setFilter('processing')">生产中</el-button>
          <el-button :type="statusFilter === 'completed' ? 'success' : ''" @click="setFilter('completed')">已完工</el-button>
        </el-button-group>
        <span style="margin-left: 20px; color: #666;">共 {{ filteredOrders.length }} 条订单</span>
      </div>

      <div v-if="filteredOrders.length === 0" class="empty-state">
        <el-empty description="暂无符合条件的订单"></el-empty>
      </div>

      <div v-else>
        <div v-for="order in filteredOrders" :key="order.id" :class="['order-card', { 'order-new': order.isNew }]">
          <div class="order-card-header" @click="toggleExpand(order)" style="cursor: pointer;">
            <div>
              <strong style="font-size: 16px;">订单号: {{ order.id }}</strong>
              <span v-if="order.isNew" class="new-badge">新订单</span>
              <span style="margin-left: 20px; color: #666;">下单时间: {{ order.createTime }}</span>
            </div>
            <div>
              <span :class="['status-badge', getStatusClass(order.status)]">{{ getStatusText(order.status) }}</span>
              <i :class="['el-icon-arrow-right', 'expand-icon', { 'expanded': order.expanded }]" style="margin-left: 15px;"></i>
            </div>
          </div>
          <el-collapse-transition>
            <div v-show="order.expanded">
              <div class="order-card-body">
                <el-row :gutter="20">
                  <el-col :span="10">
                    <div class="order-detail">
                      <div class="detail-row">
                        <span class="detail-label">客户姓名:</span>
                        <span class="detail-value">{{ order.customerName }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">联系电话:</span>
                        <span class="detail-value">{{ order.customerPhone }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">铜材类型:</span>
                        <span class="detail-value">{{ order.materialName }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">尺寸规格:</span>
                        <span class="detail-value">{{ order.length }}×{{ order.width }}×{{ order.thickness }}mm × {{ order.quantity }}件</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">纹饰雕刻:</span>
                        <span class="detail-value">{{ order.patternName }}</span>
                      </div>
                      <div class="detail-row" v-if="order.customText">
                        <span class="detail-label">自定义文字:</span>
                        <span class="detail-value">{{ order.customText }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">表面处理:</span>
                        <span class="detail-value">{{ order.craftName }}</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">预估重量:</span>
                        <span class="detail-value">{{ order.weight }}克</span>
                      </div>
                      <div class="detail-row">
                        <span class="detail-label">订单金额:</span>
                        <span class="detail-value" style="color: #ff6600; font-size: 16px;">¥{{ order.totalPrice }}</span>
                      </div>
                      <div class="detail-row" v-if="order.remark">
                        <span class="detail-label">备注:</span>
                        <span class="detail-value">{{ order.remark }}</span>
                      </div>
                    </div>
                  </el-col>
                  <el-col :span="14">
                    <h4 style="margin-bottom: 15px; color: #8b4513;">生产工序进度</h4>
                    <el-steps :active="order.currentStep" finish-status="success" align-center>
                      <el-step 
                        v-for="step in processSteps" 
                        :key="step.id" 
                        :title="step.name"
                        :icon="step.icon"
                      ></el-step>
                    </el-steps>
                    <div style="margin-top: 20px; text-align: center;">
                      <el-button 
                        type="primary" 
                        size="small"
                        :disabled="order.status === 'completed'"
                        @click.stop="nextStep(order)"
                      >
                        {{ order.status === 'completed' ? '已完成' : '进入下一道工序' }}
                      </el-button>
                      <el-button 
                        type="danger" 
                        size="small"
                        :disabled="order.currentStep === 0"
                        @click.stop="prevStep(order)"
                        style="margin-left: 10px;"
                      >
                        上一步
                      </el-button>
                      <el-button 
                        type="success" 
                        size="small"
                        :disabled="order.status !== 'pending'"
                        @click.stop="startProduction(order)"
                        style="margin-left: 10px;"
                      >
                        开始生产
                      </el-button>
                    </div>
                  </el-col>
                </el-row>
              </div>
            </div>
          </el-collapse-transition>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      processSteps: orderStore.processSteps,
      statusFilter: 'all'
    };
  },
  computed: {
    orders() {
      return orderStore.orders;
    },
    filteredOrders() {
      if (this.statusFilter === 'all') {
        return this.orders;
      }
      return this.orders.filter(o => o.status === this.statusFilter);
    },
    pendingCount() {
      return this.orders.filter(o => o.status === 'pending').length;
    },
    processingCount() {
      return this.orders.filter(o => o.status === 'processing').length;
    },
    completedCount() {
      return this.orders.filter(o => o.status === 'completed').length;
    },
    totalAmount() {
      return this.orders.reduce((sum, o) => sum + o.totalPrice, 0);
    }
  },
  methods: {
    setFilter(status) {
      this.statusFilter = status;
    },
    toggleExpand(order) {
      order.expanded = !order.expanded;
      if (order.isNew) {
        order.isNew = false;
      }
    },
    getStatusClass(status) {
      const map = {
        pending: 'status-pending',
        processing: 'status-processing',
        completed: 'status-completed'
      };
      return map[status] || '';
    },
    getStatusText(status) {
      const map = {
        pending: '待生产',
        processing: '生产中',
        completed: '已完工'
      };
      return map[status] || status;
    },
    startProduction(order) {
      this.$confirm('确认开始生产此订单？将进入第一道工序：熔铜', '开始生产确认', {
        confirmButtonText: '确认开始',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        order.status = 'processing';
        order.currentStep = 1;
        this.$message.success(`订单 ${order.id} 开始生产，当前工序：熔铜`);
      }).catch(() => {
        this.$message.info('已取消操作');
      });
    },
    nextStep(order) {
      const nextStepIndex = order.currentStep;
      const nextStepName = nextStepIndex < this.processSteps.length 
        ? this.processSteps[nextStepIndex].name 
        : '完工';
      const isComplete = nextStepIndex >= this.processSteps.length;
      
      const message = isComplete 
        ? '确认将此订单标记为全部完工？' 
        : `确认将订单推进到下一道工序：${nextStepName}？`;
      
      this.$confirm(message, '工序推进确认', {
        confirmButtonText: '确认',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (order.currentStep >= this.processSteps.length) {
          order.status = 'completed';
          this.$message.success(`订单 ${order.id} 已全部完工！`);
          return;
        }
        order.currentStep++;
        if (order.currentStep >= this.processSteps.length) {
          order.status = 'completed';
          this.$message.success(`订单 ${order.id} 已全部完工！`);
        } else {
          const stepName = this.processSteps[order.currentStep - 1].name;
          this.$message.info(`订单 ${order.id} 进入工序：${stepName}`);
        }
      }).catch(() => {
        this.$message.info('已取消操作');
      });
    },
    prevStep(order) {
      if (order.currentStep > 0) {
        const prevStepIndex = order.currentStep - 2;
        const prevStepName = prevStepIndex >= 0 
          ? this.processSteps[prevStepIndex].name 
          : '待生产';
        
        this.$confirm(`确认回退到上一道工序：${prevStepName}？`, '工序回退确认', {
          confirmButtonText: '确认回退',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          order.currentStep--;
          if (order.status === 'completed') {
            order.status = 'processing';
          }
          const stepName = this.processSteps[Math.max(0, order.currentStep - 1)]?.name || '待生产';
          this.$message.info(`订单 ${order.id} 回退到工序：${stepName}`);
        }).catch(() => {
          this.$message.info('已取消操作');
        });
      }
    }
  }
};

new Vue({
  el: '#app',
  components: {
    OrderPage,
    AdminPage
  },
  data() {
    return {
      activeMenu: 'order'
    };
  },
  computed: {
    currentPage() {
      return this.activeMenu === 'order' ? 'OrderPage' : 'AdminPage';
    }
  },
  methods: {
    handleMenuSelect(index) {
      this.activeMenu = index;
    }
  }
});
