Vue.component('order-page', {
  template: `
    <div class="card">
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
        <div class="form-section">
          <h3>📌 基本信息</h3>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="客户姓名" prop="customerName">
                <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系电话" prop="phone">
                <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h3>🦴 牛角材质选择</h3>
          <el-form-item prop="material">
            <div 
              v-for="mat in materials" 
              :key="mat.value"
              :class="['material-option', { selected: orderForm.material === mat.value }]"
              @click="orderForm.material = mat.value"
            >
              <div class="material-color" :style="{ background: mat.color }"></div>
              <div>
                <strong>{{ mat.name }}</strong>
                <p style="color: #666; font-size: 12px; margin-top: 5px;">{{ mat.desc }}</p>
              </div>
              <div style="margin-left: auto; color: #D2691E; font-weight: bold;">+¥{{ mat.price }}</div>
            </div>
          </el-form-item>
        </div>

        <div class="form-section">
          <h3>📏 规格参数</h3>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="梳子长度" prop="length">
                <el-input-number 
                  v-model="orderForm.length" 
                  :min="12" 
                  :max="25" 
                  :step="1"
                  placeholder="cm"
                  style="width: 100%"
                ></el-input-number>
                <span style="margin-left: 10px; color: #666;">厘米（12-25cm）</span>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="齿距规格" prop="toothSpacing">
                <el-select v-model="orderForm.toothSpacing" placeholder="请选择齿距" style="width: 100%">
                  <el-option label="细密齿 (2mm)" value="fine"></el-option>
                  <el-option label="标准齿 (3mm)" value="normal"></el-option>
                  <el-option label="宽齿 (5mm)" value="wide"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="梳柄造型" prop="handleStyle">
                <el-select v-model="orderForm.handleStyle" placeholder="请选择梳柄" style="width: 100%">
                  <el-option label="直柄（经典款" value="straight"></el-option>
                  <el-option label="弯柄（手感款）" value="curved"></el-option>
                  <el-option label="雕花柄（艺术款）" value="carved"></el-option>
                  <el-option label="无柄（便携款）" value="none"></el-option>
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <h3>✍️ 个性刻字</h3>
          <el-form-item label="刻字内容" prop="engraving">
            <el-input 
              v-model="orderForm.engraving" 
              type="textarea" 
              :rows="3"
              maxlength="20"
              show-word-limit
              placeholder="请输入要刻的文字（最多20字）"
            ></el-input>
            <div style="color: #999; font-size: 12px; margin-top: 5px;">
              温馨提示：刻字内容将雕刻在梳柄位置，建议刻字内容不超过20字。
            </div>
          </el-form-item>
        </div>

        <div class="form-section">
          <h3>📝 订单备注</h3>
          <el-form-item label="备注信息">
            <el-input 
              v-model="orderForm.remark" 
              type="textarea" 
              :rows="2"
              placeholder="如有特殊要求请在此说明"
            ></el-input>
          </el-form-item>
        </div>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitOrder" style="width: 100%; background: linear-gradient(90deg, #8B4513, #D2691E); border: none;">
            🛒 提交定制订单
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  `,
  data() {
    return {
      orderForm: {
        customerName: '',
        phone: '',
        material: '',
        length: 18,
        toothSpacing: '',
        handleStyle: '',
        engraving: '',
        remark: ''
      },
      materials: [
        { value: 'black', name: '黑水牛角', color: '#2c2c2c', desc: '质地坚硬，色泽乌黑发亮', price: 0 },
        { value: 'white', name: '白水牛角', color: '#f5f5dc', desc: '温润如玉，品质上乘', price: 50 },
        { value: 'yellow', name: '黄牛角', color: '#d4a574', desc: '色泽金黄，性价比高', price: 30 },
        { value: 'mixed', name: '花色牛角', color: '#8B4513', desc: '纹理独特，每把皆孤品', price: 80 }
      ],
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        material: [
          { required: true, message: '请选择牛角材质', trigger: 'change' }
        ],
        length: [
          { required: true, message: '请输入梳子长度', trigger: 'change' },
          { type: 'number', min: 12, max: 25, message: '梳子长度应在12-25厘米之间', trigger: 'change' }
        ],
        toothSpacing: [
          { required: true, message: '请选择齿距规格', trigger: 'change' }
        ],
        handleStyle: [
          { required: true, message: '请选择梳柄造型', trigger: 'change' }
        ]
      }
    }
  },
  methods: {
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.$emit('submit', { ...this.orderForm });
          this.resetForm();
        }
      });
    },
    resetForm() {
      this.$refs.orderForm.resetFields();
      this.orderForm = {
        customerName: '',
        phone: '',
        material: '',
        length: 18,
        toothSpacing: '',
        handleStyle: '',
        engraving: '',
        remark: ''
      };
    }
  }
});

Vue.component('admin-page', {
  props: ['orders'],
  template: `
    <div class="card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2 style="color: #8B4513;">📋 订单管理</h2>
        <el-tag type="info">共 {{ orders.length }} 个订单</el-tag>
      </div>
      
      <el-empty v-if="orders.length === 0" description="暂无订单"></el-empty>
      
      <div v-else>
        <div v-for="order in orders" :key="order.id" class="order-card">
          <div class="order-header">
            <span class="order-no">订单号: {{ order.id }}</span>
            <span :class="['order-status', order.currentStep >= 8 ? 'status-done' : 'status-doing']">
              {{ order.currentStep >= 8 ? '已完工' : '生产中' }}
            </span>
            <span style="color: #666; font-size: 12px;">{{ order.createTime }}</span>
          </div>
          
          <el-row :gutter="20">
            <el-col :span="6">
              <p><strong>客户：</strong>{{ order.customerName }}</p>
              <p><strong>电话：</strong>{{ order.phone }}</p>
            </el-col>
            <el-col :span="6">
              <p><strong>材质：</strong>{{ getMaterialName(order.material) }}</p>
              <p><strong>长度：</strong>{{ order.length }}cm</p>
            </el-col>
            <el-col :span="6">
              <p><strong>齿距：</strong>{{ getSpacingName(order.toothSpacing) }}</p>
              <p><strong>梳柄：</strong>{{ getHandleName(order.handleStyle) }}</p>
            </el-col>
            <el-col :span="6">
              <p><strong>刻字：</strong>{{ order.engraving || '无' }}</p>
              <p><strong>备注：</strong>{{ order.remark || '无' }}</p>
            </el-col>
          </el-row>
          
          <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #f0f0f0;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
              <strong style="color: #8B4513;">生产进度</strong>
              <el-button size="small" type="primary" @click="showStepDialog(order)" :disabled="order.currentStep >= 8">
                更新工序
              </el-button>
            </div>
            <div class="step-timeline">
              <div 
                v-for="(step, index) in steps" 
                :key="index"
                :class="['step-item', { 
                  completed: order.currentStep > index, 
                  current: order.currentStep === index + 1 
                }]"
              >
                <div class="step-circle">
                  <span v-if="order.currentStep > index">✓</span>
                  <span v-else>{{ index + 1 }}</span>
                </div>
                <div class="step-label">{{ step }}</div>
              </div>
            </div>
            <div v-if="order.stepHistory && order.stepHistory.length > 0" style="margin-top: 15px; padding-top: 15px; border-top: 1px dashed #e0e0e0;">
              <strong style="color: #666; font-size: 14px;">操作记录</strong>
              <div v-for="(record, idx) in order.stepHistory" :key="idx" style="margin-top: 8px; font-size: 12px; color: #888;">
                <span style="color: #8B4513;">{{ record.stepName }}</span>
                <span> - 操作人：{{ record.operator }}</span>
                <span style="margin-left: 10px;">{{ record.time }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <el-dialog title="更新生产工序" :visible.sync="dialogVisible" width="500px">
        <el-form label-width="100px">
          <el-form-item label="当前工序">
            <el-input :value="getStepName(currentOrder.currentStep)" disabled style="width: 100%"></el-input>
          </el-form-item>
          <el-form-item label="下一工序" v-if="currentOrder && currentOrder.currentStep < 8">
            <el-select v-model="selectedStep" style="width: 100%">
              <el-option 
                :label="getStepName(currentOrder.currentStep + 1)"
                :value="currentOrder.currentStep + 1"
              ></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="操作人" prop="operator" v-if="currentOrder && currentOrder.currentStep < 8">
            <el-input v-model="operator" placeholder="请输入操作人姓名" style="width: 100%"></el-input>
          </el-form-item>
          <el-form-item label="状态" v-else>
            <el-tag type="success">全部工序已完成</el-tag>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmUpdate" :disabled="currentOrder && currentOrder.currentStep >= 8">确定</el-button>
        </span>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      steps: ['选料', '切坯', '开齿', '打磨', '抛光', '刻字', '上油', '完工'],
      dialogVisible: false,
      currentOrder: null,
      selectedStep: 1,
      operator: ''
    }
  },
  methods: {
    getMaterialName(value) {
      const map = {
        black: '黑水牛角',
        white: '白水牛角',
        yellow: '黄牛角',
        mixed: '花色牛角'
      };
      return map[value] || value;
    },
    getSpacingName(value) {
      const map = {
        fine: '细密齿 (2mm)',
        normal: '标准齿 (3mm)',
        wide: '宽齿 (5mm)'
      };
      return map[value] || value;
    },
    getHandleName(value) {
      const map = {
        straight: '直柄（经典款）',
        curved: '弯柄（手感款）',
        carved: '雕花柄（艺术款）',
        none: '无柄（便携款）'
      };
      return map[value] || value;
    },
    getStepName(stepIndex) {
      return this.steps[stepIndex - 1] || '未知';
    },
    showStepDialog(order) {
      this.currentOrder = order;
      this.selectedStep = order.currentStep < 8 ? order.currentStep + 1 : order.currentStep;
      this.operator = '';
      this.dialogVisible = true;
    },
    confirmUpdate() {
      if (!this.operator || this.operator.trim() === '') {
        this.$message.error('请输入操作人姓名！');
        return;
      }
      if (this.selectedStep !== this.currentOrder.currentStep + 1) {
        this.$message.error('只能按顺序进入下一道工序，不可跳步！');
        return;
      }
      this.$emit('update-step', {
        orderId: this.currentOrder.id,
        step: this.selectedStep,
        operator: this.operator.trim()
      });
      this.dialogVisible = false;
      this.$message.success('工序更新成功！');
    }
  }
});

new Vue({
  el: '#app',
  data() {
    return {
      currentRoute: '/order',
      orders: []
    }
  },
  created() {
    this.handleHashChange();
    window.addEventListener('hashchange', this.handleHashChange);
    
    this.orders = [
      {
        id: 'HC20240516001',
        customerName: '张三',
        phone: '13800138000',
        material: 'black',
        length: 18,
        toothSpacing: 'normal',
        handleStyle: 'straight',
        engraving: '平安喜乐',
        remark: '请尽快发货',
        currentStep: 4,
        createTime: '2024-05-16 10:30'
      },
      {
        id: 'HC20240516002',
        customerName: '李四',
        phone: '13900139000',
        material: 'white',
        length: 20,
        toothSpacing: 'wide',
        handleStyle: 'carved',
        engraving: '',
        remark: '',
        currentStep: 8,
        createTime: '2024-05-15 14:20'
      }
    ];
  },
  beforeDestroy() {
    window.removeEventListener('hashchange', this.handleHashChange);
  },
  methods: {
    handleHashChange() {
      const hash = window.location.hash.slice(1) || '/order';
      this.currentRoute = hash;
    },
    handleOrderSubmit(orderData) {
      const newOrder = {
        id: 'HC' + this.generateOrderNo(),
        ...orderData,
        currentStep: 1,
        createTime: this.formatDate(new Date())
      };
      this.orders.unshift(newOrder);
      this.$message({
        message: '订单提交成功！',
        type: 'success',
        duration: 3000
      });
    },
    updateStep({ orderId, step, operator }) {
      const order = this.orders.find(o => o.id === orderId);
      if (order) {
        order.currentStep = step;
        if (!order.stepHistory) {
          order.stepHistory = [];
        }
        const stepNames = ['选料', '切坯', '开齿', '打磨', '抛光', '刻字', '上油', '完工'];
        order.stepHistory.push({
          stepName: stepNames[step - 1],
          operator: operator,
          time: this.formatDate(new Date())
        });
      }
    },
    generateOrderNo() {
      const now = new Date();
      const dateStr = now.getFullYear().toString() +
        (now.getMonth() + 1).toString().padStart(2, '0') +
        now.getDate().toString().padStart(2, '0');
      const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
      return dateStr + random;
    },
    formatDate(date) {
      const y = date.getFullYear();
      const m = (date.getMonth() + 1).toString().padStart(2, '0');
      const d = date.getDate().toString().padStart(2, '0');
      const h = date.getHours().toString().padStart(2, '0');
      const min = date.getMinutes().toString().padStart(2, '0');
      return `${y}-${m}-${d} ${h}:${min}`;
    }
  }
});
