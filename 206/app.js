Vue.use(VueRouter);
Vue.use(ELEMENT);

const currentUser = {
  account: localStorage.getItem('adminAccount') || 'admin',
  name: localStorage.getItem('adminName') || '系统管理员'
};

const orderStore = {
  state: {
    orders: JSON.parse(localStorage.getItem('bookmarkOrders') || '[]')
  },
  save() {
    localStorage.setItem('bookmarkOrders', JSON.stringify(this.state.orders));
  },
  addOrder(order) {
    this.state.orders.unshift(order);
    this.save();
  },
  updateOrder(orderId, updates) {
    const index = this.state.orders.findIndex(o => o.id === orderId);
    if (index !== -1) {
      this.state.orders[index] = { ...this.state.orders[index], ...updates };
      this.save();
    }
  },
  deleteOrder(orderId) {
    this.state.orders = this.state.orders.filter(o => o.id !== orderId);
    this.save();
  }
};

const materials = [
  { id: 'ebony', name: '黑檀木', color: '#3d2b1f', desc: '质地坚硬，纹理细腻，色泽深沉', basePrice: 58 },
  { id: 'sandalwood', name: '紫檀木', color: '#8b4513', desc: '香气淡雅，纹理美观，高贵典雅', basePrice: 88 },
  { id: 'boxwood', name: '黄杨木', color: '#deb887', desc: '质地温润，色泽柔和，适合精细雕刻', basePrice: 48 },
  { id: 'rosewood', name: '花梨木', color: '#cd853f', desc: '纹理清晰，香气独特，经久耐用', basePrice: 68 },
  { id: 'cherry', name: '樱桃木', color: '#a0522d', desc: '纹理细腻，色泽温暖，手感舒适', basePrice: 52 }
];

const patterns = [
  { id: 'bamboo', name: '翠竹', icon: '🎋' },
  { id: 'plum', name: '梅花', icon: '🌸' },
  { id: 'orchid', name: '兰花', icon: '🌺' },
  { id: 'chrysanthemum', name: '菊花', icon: '🌼' },
  { id: 'lotus', name: '荷花', icon: '🪷' },
  { id: 'dragon', name: '龙纹', icon: '🐉' },
  { id: 'phoenix', name: '凤纹', icon: '🦅' },
  { id: 'cloud', name: '祥云', icon: '☁️' },
  { id: 'mountain', name: '山水', icon: '⛰️' },
  { id: 'calligraphy', name: '书法', icon: '✍️' },
  { id: 'heart', name: '爱心', icon: '❤️' },
  { id: 'star', name: '星辰', icon: '⭐' }
];

const depths = [
  { value: 0.5, label: '浅雕 (0.5mm)', priceAdd: 0 },
  { value: 1, label: '中雕 (1mm)', priceAdd: 10 },
  { value: 1.5, label: '深雕 (1.5mm)', priceAdd: 20 },
  { value: 2, label: '浮雕 (2mm)', priceAdd: 35 }
];

const holeOptions = [
  { value: 'none', label: '无孔', priceAdd: 0 },
  { value: 'small', label: '小孔 (2mm)', priceAdd: 5 },
  { value: 'medium', label: '中孔 (3mm)', priceAdd: 8 },
  { value: 'large', label: '大孔 (4mm)', priceAdd: 10 }
];

const processSteps = [
  { id: 'select', name: '选料' },
  { id: 'cut', name: '开料' },
  { id: 'rough', name: '粗雕' },
  { id: 'fine', name: '细雕' },
  { id: 'polish', name: '打磨' },
  { id: 'oil', name: '上油' },
  { id: 'hole', name: '穿孔' },
  { id: 'finish', name: '完工' }
];

function generateOrderId() {
  return 'BM' + Date.now().toString(36).toUpperCase() + Math.random().toString(36).substr(2, 4).toUpperCase();
}

function getCurrentStepIndex(order) {
  if (order.status === 'completed') return processSteps.length - 1;
  if (order.status === 'cancelled') return -1;
  return order.currentStep || 0;
}

const OrderForm = {
  template: `
    <div class="card-wrapper">
      <el-card class="form-card">
        <h2 class="form-title">🌿 木雕书签定制</h2>
        
        <el-form :model="form" :rules="rules" ref="orderForm" label-position="top">
          
          <div class="form-section">
            <h3 class="section-title">📦 选择木料材质</h3>
            <div 
              v-for="m in materials" 
              :key="m.id"
              class="material-option"
              :class="{ selected: form.materialId === m.id }"
              @click="form.materialId = m.id"
            >
              <div class="material-color" :style="{ backgroundColor: m.color }"></div>
              <div class="material-info">
                <div class="material-name">{{ m.name }}</div>
                <div class="material-desc">{{ m.desc }}</div>
              </div>
              <div class="material-price">¥{{ m.basePrice }}</div>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">📏 书签尺寸</h3>
            <el-form-item label="常用尺寸一键选择">
              <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
                <el-button 
                  v-for="size in quickSizes" 
                  :key="size.value"
                  size="small"
                  :type="form.length === size.value ? 'primary' : ''"
                  @click="selectQuickSize(size.value)"
                >
                  {{ size.label }}
                </el-button>
              </div>
            </el-form-item>
            <el-form-item label="书签长度 (mm)" prop="length">
              <el-slider 
                v-model="form.length" 
                :min="100" 
                :max="200" 
                :step="10"
                show-input
                :input-size="'small'"
              ></el-slider>
              <div style="text-align: center; color: #909399; font-size: 12px; margin-top: 5px;">
                标准尺寸：120-160mm，宽度固定为 30mm
              </div>
            </el-form-item>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">🎨 图案样式</h3>
            <div class="pattern-grid">
              <div 
                v-for="p in patterns" 
                :key="p.id"
                class="pattern-item"
                :class="{ selected: form.patternId === p.id }"
                @click="form.patternId = p.id"
              >
                <div class="pattern-icon">{{ p.icon }}</div>
                <div class="pattern-name">{{ p.name }}</div>
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">🗡️ 雕刻深度</h3>
            <el-form-item prop="depth">
              <el-radio-group v-model="form.depth">
                <el-radio 
                  v-for="d in depths" 
                  :key="d.value" 
                  :label="d.value"
                  style="display: block; margin-bottom: 10px;"
                >
                  {{ d.label }}
                  <span v-if="d.priceAdd > 0" style="color: #f56c6c;">+¥{{ d.priceAdd }}</span>
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">🔗 挂绳孔配置</h3>
            <el-form-item prop="holeOption">
              <el-radio-group v-model="form.holeOption">
                <el-radio 
                  v-for="h in holeOptions" 
                  :key="h.value" 
                  :label="h.value"
                  style="margin-right: 20px;"
                >
                  {{ h.label }}
                  <span v-if="h.priceAdd > 0" style="color: #f56c6c;">+¥{{ h.priceAdd }}</span>
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">📝 备注信息</h3>
            <el-form-item prop="remark">
              <el-input 
                type="textarea" 
                v-model="form.remark" 
                :rows="3"
                placeholder="如有特殊要求请在此说明..."
              ></el-input>
            </el-form-item>
          </div>
          
          <div class="form-section">
            <h3 class="section-title">👤 联系信息</h3>
            <el-form-item label="客户姓名" prop="customerName">
              <el-input v-model="form.customerName" placeholder="请输入您的姓名"></el-input>
            </el-form-item>
            <el-form-item label="联系电话" prop="customerPhone">
              <el-input v-model="form.customerPhone" placeholder="请输入您的联系电话"></el-input>
            </el-form-item>
          </div>
          
          <div class="order-summary">
            <div class="summary-title">💰 订单明细</div>
            <div class="summary-item">
              <span>木料材质</span>
              <span>{{ selectedMaterial ? selectedMaterial.name + ' - ¥' + selectedMaterial.basePrice : '未选择' }}</span>
            </div>
            <div class="summary-item">
              <span>书签长度</span>
              <span>{{ form.length }}mm</span>
            </div>
            <div class="summary-item">
              <span>图案样式</span>
              <span>{{ selectedPattern ? selectedPattern.name : '未选择' }}</span>
            </div>
            <div class="summary-item">
              <span>雕刻深度</span>
              <span>{{ selectedDepth ? selectedDepth.label : '未选择' }}</span>
            </div>
            <div class="summary-item">
              <span>挂绳孔</span>
              <span>{{ selectedHole ? selectedHole.label : '未选择' }}</span>
            </div>
            <div class="summary-total">
              <span>合计金额</span>
              <span>¥{{ totalPrice }}</span>
            </div>
          </div>
          
          <el-button 
            type="primary" 
            size="large" 
            class="btn-submit"
            @click="submitOrder"
            :loading="submitting"
          >
            提交订单
          </el-button>
          
        </el-form>
      </el-card>
    </div>
  `,
  data() {
    return {
      submitting: false,
      materials,
      patterns,
      depths,
      holeOptions,
      quickSizes: [
        { value: 120, label: '小巧 120mm' },
        { value: 140, label: '标准 140mm' },
        { value: 150, label: '经典 150mm' },
        { value: 160, label: '长款 160mm' },
        { value: 180, label: '加长 180mm' }
      ],
      form: {
        materialId: '',
        length: 150,
        patternId: '',
        depth: 1,
        holeOption: 'none',
        remark: '',
        customerName: '',
        customerPhone: ''
      },
      rules: {
        materialId: [{ required: true, message: '请选择木料材质', trigger: 'change' }],
        patternId: [{ required: true, message: '请选择图案样式', trigger: 'change' }],
        depth: [{ required: true, message: '请选择雕刻深度', trigger: 'change' }],
        holeOption: [{ required: true, message: '请选择挂绳孔配置', trigger: 'change' }],
        length: [
          { required: true, message: '请输入书签长度', trigger: 'change' },
          { type: 'number', message: '长度必须为数字', trigger: 'change' },
          { 
            validator: (rule, value, callback) => {
              if (value <= 0) {
                callback(new Error('长度必须为正数'));
              } else if (value < 100 || value > 200) {
                callback(new Error('长度必须在 100-200mm 之间'));
              } else {
                callback();
              }
            }, 
            trigger: 'change' 
          }
        ],
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        customerPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      }
    };
  },
  computed: {
    selectedMaterial() {
      return materials.find(m => m.id === this.form.materialId);
    },
    selectedPattern() {
      return patterns.find(p => p.id === this.form.patternId);
    },
    selectedDepth() {
      return depths.find(d => d.value === this.form.depth);
    },
    selectedHole() {
      return holeOptions.find(h => h.value === this.form.holeOption);
    },
    totalPrice() {
      let price = 0;
      if (this.selectedMaterial) price += this.selectedMaterial.basePrice;
      if (this.selectedDepth) price += this.selectedDepth.priceAdd;
      if (this.selectedHole) price += this.selectedHole.priceAdd;
      if (this.form.length > 160) price += Math.ceil((this.form.length - 160) / 10) * 5;
      return price;
    }
  },
  methods: {
    selectQuickSize(value) {
      this.form.length = value;
    },
    resetForm() {
      this.form = {
        materialId: '',
        length: 150,
        patternId: '',
        depth: 1,
        holeOption: 'none',
        remark: '',
        customerName: '',
        customerPhone: ''
      };
      this.$nextTick(() => {
        this.$refs.orderForm.clearValidate();
      });
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          this.submitting = true;
          const order = {
            id: generateOrderId(),
            materialId: this.form.materialId,
            materialName: this.selectedMaterial.name,
            materialColor: this.selectedMaterial.color,
            length: this.form.length,
            patternId: this.form.patternId,
            patternName: this.selectedPattern.name,
            patternIcon: this.selectedPattern.icon,
            depth: this.form.depth,
            depthLabel: this.selectedDepth.label,
            holeOption: this.form.holeOption,
            holeLabel: this.selectedHole.label,
            remark: this.form.remark,
            customerName: this.form.customerName,
            customerPhone: this.form.customerPhone,
            totalPrice: this.totalPrice,
            status: 'processing',
            currentStep: 0,
            stepTimes: [new Date().toISOString()],
            stepOperators: [{ account: currentUser.account, name: currentUser.name }],
            isNew: true,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString()
          };
          
          setTimeout(() => {
            orderStore.addOrder(order);
            this.submitting = false;
            this.$message.success('订单提交成功！订单号：' + order.id);
            this.resetForm();
            this.$router.push('/admin');
          }, 1000);
        } else {
          this.$message.error('请完善订单信息');
          return false;
        }
      });
    }
  }
};

const OrderList = {
  template: `
    <div class="card-wrapper">
      <el-card class="admin-card">
        <div class="admin-header">
          <h2 class="admin-title">📋 订单管理</h2>
          <div style="display: flex; align-items: center; gap: 15px; flex-wrap: wrap;">
            <el-tag type="primary">
              <i class="el-icon-user-solid"></i> 当前操作人: {{ currentUser.name }} ({{ currentUser.account }})
            </el-tag>
            <el-select v-model="filterStatus" placeholder="订单状态" style="width: 130px;" clearable>
              <el-option label="全部" value=""></el-option>
              <el-option label="生产中" value="processing"></el-option>
              <el-option label="已完成" value="completed"></el-option>
              <el-option label="已取消" value="cancelled"></el-option>
            </el-select>
            <el-select v-model="filterStep" placeholder="生产工序" style="width: 130px;" clearable>
              <el-option label="全部工序" value=""></el-option>
              <el-option 
                v-for="(step, index) in processSteps" 
                :key="step.id" 
                :label="step.name" 
                :value="index"
              ></el-option>
            </el-select>
            <el-button size="small" @click="clearFilters">
              <i class="el-icon-refresh"></i> 重置筛选
            </el-button>
            <el-button 
              size="small" 
              type="warning" 
              @click="clearAllNewMarks"
              :disabled="newOrderCount === 0"
            >
              <i class="el-icon-check"></i> 清除新标记 ({{ newOrderCount }})
            </el-button>
          </div>
        </div>
        
        <div class="stats-bar">
          <div class="stat-item">
            <div class="stat-value">{{ orderStore.state.orders.length }}</div>
            <div class="stat-label">总订单数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value" style="color: #e6a23c;">{{ processingCount }}</div>
            <div class="stat-label">生产中</div>
          </div>
          <div class="stat-item">
            <div class="stat-value" style="color: #67c23a;">{{ completedCount }}</div>
            <div class="stat-label">已完成</div>
          </div>
          <div class="stat-item">
            <div class="stat-value" style="color: #909399;">¥{{ totalRevenue }}</div>
            <div class="stat-label">总收入</div>
          </div>
        </div>
        
        <el-table 
          :data="filteredOrders" 
          style="width: 100%"
          empty-text="暂无订单"
          v-loading="loading"
          :row-class-name="tableRowClassName"
          @row-click="markAsViewed"
        >
          <el-table-column label="订单号" width="200">
            <template slot-scope="scope">
              <span style="display: flex; align-items: center; gap: 8px;">
                <span>{{ scope.row.id }}</span>
                <el-tag 
                  v-if="scope.row.isNew" 
                  type="danger" 
                  size="mini"
                  style="animation: blink 1.5s infinite;"
                >
                  新
                </el-tag>
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="customerName" label="客户" width="100"></el-table-column>
          <el-table-column label="产品信息" width="200">
            <template slot-scope="scope">
              <div style="display: flex; align-items: center;">
                <div 
                  style="width: 24px; height: 24px; border-radius: 4px; margin-right: 8px; border: 1px solid #dcdfe6;"
                  :style="{ backgroundColor: scope.row.materialColor }"
                ></div>
                <span>{{ scope.row.materialName }} · {{ scope.row.patternIcon }} {{ scope.row.patternName }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="totalPrice" label="金额" width="100">
            <template slot-scope="scope">
              <span style="color: #f56c6c; font-weight: 600;">¥{{ scope.row.totalPrice }}</span>
            </template>
          </el-table-column>
          <el-table-column label="状态" width="100">
            <template slot-scope="scope">
              <el-tag v-if="scope.row.status === 'processing'" type="warning">生产中</el-tag>
              <el-tag v-else-if="scope.row.status === 'completed'" type="success">已完成</el-tag>
              <el-tag v-else type="info">已取消</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createdAt" label="下单时间" width="160">
            <template slot-scope="scope">
              {{ formatDate(scope.row.createdAt) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" fixed="right">
            <template slot-scope="scope">
              <el-button 
                type="text" 
                size="small" 
                @click="viewDetail(scope.row)"
              >
                详情
              </el-button>
              <el-button 
                v-if="scope.row.status === 'processing'"
                type="text" 
                size="small" 
                @click="nextStep(scope.row)"
              >
                推进工序
              </el-button>
              <el-button 
                v-if="scope.row.status === 'processing'"
                type="text" 
                size="small" 
                style="color: #f56c6c;"
                @click="cancelOrder(scope.row)"
              >
                取消
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      
      <el-dialog 
        title="订单详情" 
        :visible.sync="detailVisible" 
        width="600px"
      >
        <div v-if="currentOrder">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="订单号">{{ currentOrder.id }}</el-descriptions-item>
            <el-descriptions-item label="下单时间">{{ formatDate(currentOrder.createdAt) }}</el-descriptions-item>
            <el-descriptions-item label="客户姓名">{{ currentOrder.customerName }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ currentOrder.customerPhone }}</el-descriptions-item>
            <el-descriptions-item label="木料材质">
              <span style="display: flex; align-items: center;">
                <div 
                  style="width: 16px; height: 16px; border-radius: 3px; margin-right: 6px; border: 1px solid #dcdfe6;"
                  :style="{ backgroundColor: currentOrder.materialColor }"
                ></div>
                {{ currentOrder.materialName }}
              </span>
            </el-descriptions-item>
            <el-descriptions-item label="书签尺寸">{{ currentOrder.length }} × 30 mm</el-descriptions-item>
            <el-descriptions-item label="图案样式">{{ currentOrder.patternIcon }} {{ currentOrder.patternName }}</el-descriptions-item>
            <el-descriptions-item label="雕刻深度">{{ currentOrder.depthLabel }}</el-descriptions-item>
            <el-descriptions-item label="挂绳孔">{{ currentOrder.holeLabel }}</el-descriptions-item>
            <el-descriptions-item label="订单金额">
              <span style="color: #f56c6c; font-weight: 600;">¥{{ currentOrder.totalPrice }}</span>
            </el-descriptions-item>
          </el-descriptions>
          
          <div style="margin-top: 20px;">
            <h4 style="margin-bottom: 10px; color: #606266;">📝 备注</h4>
            <p style="background: #f5f7fa; padding: 12px; border-radius: 6px; color: #606266;">
              {{ currentOrder.remark || '无' }}
            </p>
          </div>
          
          <div class="process-steps">
            <h4 style="margin-bottom: 15px; color: #606266;">🏭 生产进度</h4>
            <div 
              v-for="(step, index) in processSteps" 
              :key="step.id"
              class="process-step"
              :class="{ completed: index < currentStepIndex, current: index === currentStepIndex }"
            >
              <div 
                class="step-indicator"
                :class="{ 
                  completed: index < currentStepIndex, 
                  current: index === currentStepIndex 
                }"
              >
                <i v-if="index < currentStepIndex" class="el-icon-check"></i>
                <span v-else>{{ index + 1 }}</span>
              </div>
              <div class="step-content">
                <div 
                  class="step-name"
                  :class="{ 
                    completed: index < currentStepIndex, 
                    current: index === currentStepIndex 
                  }"
                >
                  {{ step.name }}
                </div>
                <div class="step-time" v-if="currentOrder.stepTimes && currentOrder.stepTimes[index]">
                  {{ formatDate(currentOrder.stepTimes[index]) }}
                  <span v-if="currentOrder.stepOperators && currentOrder.stepOperators[index]" style="margin-left: 10px;">
                    操作人: {{ currentOrder.stepOperators[index].name }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <span slot="footer" class="dialog-footer">
          <el-button v-if="currentOrder && currentOrder.status === 'processing'" type="primary" @click="nextStep(currentOrder)">
            推进到下一工序
          </el-button>
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      loading: false,
      filterStatus: '',
      filterStep: '',
      detailVisible: false,
      currentOrder: null,
      orderStore,
      processSteps,
      currentUser
    };
  },
  computed: {
    filteredOrders() {
      let orders = orderStore.state.orders;
      if (this.filterStatus) {
        orders = orders.filter(o => o.status === this.filterStatus);
      }
      if (this.filterStep !== '' && this.filterStep !== null) {
        orders = orders.filter(o => {
          const stepIndex = getCurrentStepIndex(o);
          return stepIndex === Number(this.filterStep);
        });
      }
      return orders;
    },
    processingCount() {
      return orderStore.state.orders.filter(o => o.status === 'processing').length;
    },
    completedCount() {
      return orderStore.state.orders.filter(o => o.status === 'completed').length;
    },
    totalRevenue() {
      return orderStore.state.orders
        .filter(o => o.status === 'completed')
        .reduce((sum, o) => sum + o.totalPrice, 0);
    },
    newOrderCount() {
      return orderStore.state.orders.filter(o => o.isNew).length;
    },
    currentStepIndex() {
      if (!this.currentOrder) return -1;
      return getCurrentStepIndex(this.currentOrder);
    }
  },
  methods: {
    clearFilters() {
      this.filterStatus = '';
      this.filterStep = '';
    },
    clearAllNewMarks() {
      this.$confirm('确认清除所有新订单标记？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        orderStore.state.orders.forEach(order => {
          if (order.isNew) {
            orderStore.updateOrder(order.id, { isNew: false, updatedAt: new Date().toISOString() });
          }
        });
        this.$message.success('已清除所有新订单标记');
      }).catch(() => {});
    },
    tableRowClassName({ row }) {
      if (row.isNew) {
        return 'new-order-row';
      }
      return '';
    },
    markAsViewed(order) {
      if (order.isNew) {
        orderStore.updateOrder(order.id, { isNew: false, updatedAt: new Date().toISOString() });
        if (this.currentOrder && this.currentOrder.id === order.id) {
          this.currentOrder.isNew = false;
        }
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr);
      return date.toLocaleString('zh-CN', {
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
      });
    },
    viewDetail(order) {
      this.currentOrder = { ...order };
      this.detailVisible = true;
      this.markAsViewed(order);
    },
    nextStep(order) {
      const currentIndex = getCurrentStepIndex(order);
      if (currentIndex >= processSteps.length - 1) {
        this.$message.info('订单已完成所有工序');
        return;
      }
      
      this.$confirm(`确认推进到「${processSteps[currentIndex + 1].name}」工序？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const nextIndex = currentIndex + 1;
        const updates = {
          currentStep: nextIndex,
          updatedAt: new Date().toISOString(),
          stepTimes: [...(order.stepTimes || []), new Date().toISOString()],
          stepOperators: [...(order.stepOperators || []), { account: currentUser.account, name: currentUser.name }]
        };
        
        if (nextIndex === processSteps.length - 1) {
          updates.status = 'completed';
        }
        
        orderStore.updateOrder(order.id, updates);
        this.$message.success(`已推进到「${processSteps[nextIndex].name}」工序`);
        
        if (this.currentOrder && this.currentOrder.id === order.id) {
          this.currentOrder = { ...this.currentOrder, ...updates };
        }
      }).catch(() => {});
    },
    cancelOrder(order) {
      this.$confirm('确认取消该订单？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        orderStore.updateOrder(order.id, {
          status: 'cancelled',
          updatedAt: new Date().toISOString()
        });
        this.$message.success('订单已取消');
      }).catch(() => {});
    }
  }
};

const App = {
  template: `
    <div class="app-container">
      <div class="header">
        <h1>🪵 木雕书签定制系统</h1>
        <div class="subtitle">匠心工艺 · 专属定制</div>
      </div>
      
      <el-tabs v-model="activeTab" class="nav-tabs" @tab-change="handleTabChange">
        <el-tab-pane label="🛒 客户下单" name="order"></el-tab-pane>
        <el-tab-pane label="📋 订单管理" name="admin"></el-tab-pane>
      </el-tabs>
      
      <router-view></router-view>
    </div>
  `,
  data() {
    return {
      activeTab: this.$route.path === '/admin' ? 'admin' : 'order'
    };
  },
  methods: {
    handleTabChange(tab) {
      this.$router.push(tab === 'admin' ? '/admin' : '/');
    }
  }
};

const router = new VueRouter({
  routes: [
    { path: '/', component: OrderForm },
    { path: '/admin', component: OrderList }
  ]
});

new Vue({
  router,
  render: h => h(App)
}).$mount('#app');
