Vue.component('order-form', {
  template: `
    <div>
      <div class="card">
        <h2 class="section-title">📝 定制信息填写</h2>
        
        <div class="form-section">
          <div class="section-label">
            <span class="icon">1</span>
            选择纸张材质
            <span v-if="!isMaterialValid && validationTouched.material" style="color: #f56c6c; margin-left: 10px; font-size: 14px;">
              <i class="el-icon-warning"></i> 请选择纸张材质
            </span>
          </div>
          <el-row :gutter="20">
            <el-col :xs="12" :sm="8" :md="6" v-for="material in materials" :key="material.id">
              <div 
                class="material-card" 
                :class="{ active: formData.material === material.id, 'error-border': !isMaterialValid && validationTouched.material }"
                @click="selectMaterial(material.id)"
              >
                <div style="font-size: 24px; margin-bottom: 8px;">{{ material.icon }}</div>
                <div style="font-weight: 600;">{{ material.name }}</div>
                <div style="font-size: 12px; color: #666;">{{ material.desc }}</div>
                <div class="price">¥{{ material.price }}/张</div>
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="section-label">
            <span class="icon">2</span>
            窗花尺寸
            <span v-if="!isSizeValid && (validationTouched.width || validationTouched.height)" style="color: #f56c6c; margin-left: 10px; font-size: 14px;">
              <i class="el-icon-warning"></i> 尺寸需在15-60cm之间，且为5的倍数
            </span>
          </div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-input-number 
                v-model="formData.width" 
                :min="15" 
                :max="60" 
                :step="5"
                size="large"
                style="width: 100%;"
                :class="{ 'error-input': !isWidthValid && validationTouched.width }"
                @change="validateWidth"
                @blur="validateWidth"
              >
                <template slot="append">cm</template>
              </el-input-number>
              <div style="font-size: 12px; color: #666; margin-top: 8px;">宽度</div>
              <div style="font-size: 11px; color: #909399; margin-top: 4px;">
                <i class="el-icon-info"></i> 参考范围：小窗花15-25cm，中窗花30-40cm，大窗花45-60cm
              </div>
            </el-col>
            <el-col :span="12">
              <el-input-number 
                v-model="formData.height" 
                :min="15" 
                :max="60" 
                :step="5"
                size="large"
                style="width: 100%;"
                :class="{ 'error-input': !isHeightValid && validationTouched.height }"
                @change="validateHeight"
                @blur="validateHeight"
              >
                <template slot="append">cm</template>
              </el-input-number>
              <div style="font-size: 12px; color: #666; margin-top: 8px;">高度</div>
              <div style="font-size: 11px; color: #909399; margin-top: 4px;">
                <i class="el-icon-info"></i> 参考范围：小窗花15-25cm，中窗花30-40cm，大窗花45-60cm
              </div>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="section-label">
            <span class="icon">3</span>
            图案主题
            <span v-if="!isThemeValid && validationTouched.theme" style="color: #f56c6c; margin-left: 10px; font-size: 14px;">
              <i class="el-icon-warning"></i> 请选择图案主题
            </span>
          </div>
          <el-select 
            v-model="formData.theme" 
            placeholder="请选择图案主题" 
            size="large" 
            style="width: 100%;"
            :class="{ 'error-select': !isThemeValid && validationTouched.theme }"
            @change="validateTheme"
            @blur="validateTheme"
          >
            <el-option label="春节福字" value="spring_festival"></el-option>
            <el-option label="花鸟鱼虫" value="flowers_birds"></el-option>
            <el-option label="人物故事" value="characters"></el-option>
            <el-option label="吉祥图案" value="auspicious"></el-option>
            <el-option label="生肖属相" value="zodiac"></el-option>
            <el-option label="山水风景" value="landscape"></el-option>
            <el-option label="自定义图案" value="custom"></el-option>
          </el-select>
        </div>

        <div class="form-section">
          <div class="section-label">
            <span class="icon">4</span>
            镂空复杂度
          </div>
          <div class="complexity-slider">
            <el-slider 
              v-model="formData.complexity" 
              :marks="complexityMarks"
              :min="1"
              :max="5"
              show-input
              input-size="small"
            ></el-slider>
          </div>
        </div>

        <div class="form-section">
          <div class="section-label">
            <span class="icon">5</span>
            装裱方式
          </div>
          <el-radio-group v-model="formData.framing" size="large">
            <el-radio-button label="none">无需装裱</el-radio-button>
            <el-radio-button label="simple">简易装裱</el-radio-button>
            <el-radio-button label="standard">标准装裱</el-radio-button>
            <el-radio-button label="premium">精品装裱</el-radio-button>
          </el-radio-group>
        </div>

        <div class="form-section">
          <div class="section-label">
            <span class="icon">6</span>
            联系方式
          </div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-input v-model="formData.customerName" placeholder="请输入您的姓名" size="large"></el-input>
            </el-col>
            <el-col :span="12">
              <el-input v-model="formData.customerPhone" placeholder="请输入联系电话" size="large"></el-input>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <el-input
            type="textarea"
            :rows="3"
            v-model="formData.remark"
            placeholder="其他要求或备注信息..."
            size="large"
          ></el-input>
        </div>

        <div class="price-summary">
          <el-row type="flex" justify="space-between" align="middle">
            <el-col>
              <div style="color: #666; margin-bottom: 5px;">预估总价</div>
              <div class="total-price">¥{{ totalPrice }}</div>
            </el-col>
            <el-col>
              <el-button 
                type="primary" 
                size="large" 
                class="submit-btn"
                @click="submitOrder"
                :disabled="!canSubmit"
              >
                提交订单
              </el-button>
            </el-col>
          </el-row>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      formData: {
        material: '',
        width: 30,
        height: 30,
        theme: '',
        complexity: 3,
        framing: 'none',
        customerName: '',
        customerPhone: '',
        remark: ''
      },
      validationTouched: {
        material: false,
        width: false,
        height: false,
        theme: false
      },
      materials: [
        { id: 'xuan', name: '宣纸', icon: '📜', desc: '传统手工宣纸', price: 20 },
        { id: 'red', name: '红纸', icon: '🔴', desc: '大红喜庆专用纸', price: 15 },
        { id: 'gold', name: '金箔纸', icon: '✨', desc: '高档金箔装饰纸', price: 50 },
        { id: 'silk', name: '丝绸纸', icon: '🎀', desc: '精品丝绸材质纸', price: 80 }
      ],
      complexityMarks: {
        1: '简单',
        2: '较易',
        3: '中等',
        4: '复杂',
        5: '极复杂'
      },
      framingPrices: {
        none: 0,
        simple: 30,
        standard: 80,
        premium: 200
      }
    }
  },
  computed: {
    isMaterialValid() {
      return this.formData.material && this.formData.material !== '';
    },
    isWidthValid() {
      const w = this.formData.width;
      return w >= 15 && w <= 60 && w % 5 === 0;
    },
    isHeightValid() {
      const h = this.formData.height;
      return h >= 15 && h <= 60 && h % 5 === 0;
    },
    isSizeValid() {
      return this.isWidthValid && this.isHeightValid;
    },
    isThemeValid() {
      return this.formData.theme && this.formData.theme !== '';
    },
    canSubmit() {
      return this.isMaterialValid && 
             this.isSizeValid && 
             this.isThemeValid && 
             this.formData.customerName && 
             this.formData.customerPhone;
    },
    totalPrice() {
      const material = this.materials.find(m => m.id === this.formData.material);
      const materialPrice = material ? material.price : 0;
      const sizeFactor = (this.formData.width * this.formData.height) / 900;
      const complexityFactor = 1 + (this.formData.complexity - 1) * 0.3;
      const framingPrice = this.framingPrices[this.formData.framing];
      const basePrice = 50;
      
      const total = Math.round((basePrice + materialPrice) * sizeFactor * complexityFactor + framingPrice);
      return total;
    }
  },
  methods: {
    selectMaterial(id) {
      this.formData.material = id;
      this.validationTouched.material = true;
    },
    validateWidth() {
      this.validationTouched.width = true;
      if (this.formData.width % 5 !== 0) {
        this.formData.width = Math.round(this.formData.width / 5) * 5;
        this.formData.width = Math.max(15, Math.min(60, this.formData.width));
      }
    },
    validateHeight() {
      this.validationTouched.height = true;
      if (this.formData.height % 5 !== 0) {
        this.formData.height = Math.round(this.formData.height / 5) * 5;
        this.formData.height = Math.max(15, Math.min(60, this.formData.height));
      }
    },
    validateTheme() {
      this.validationTouched.theme = true;
    },
    submitOrder() {
      this.validationTouched = {
        material: true,
        width: true,
        height: true,
        theme: true
      };
      
      if (!this.canSubmit) {
        this.$message({
          message: '请检查并完善必填信息',
          type: 'warning'
        });
        return;
      }
      
      this.$emit('submit', {
        ...this.formData,
        price: this.totalPrice,
        orderTime: new Date().toLocaleString('zh-CN')
      });
      
      this.formData = {
        material: '',
        width: 30,
        height: 30,
        theme: '',
        complexity: 3,
        framing: 'none',
        customerName: '',
        customerPhone: '',
        remark: ''
      };
      this.validationTouched = {
        material: false,
        width: false,
        height: false,
        theme: false
      };
    }
  }
});

Vue.component('admin-panel', {
  props: ['orders', 'newOrderId'],
  template: `
    <div>
      <div class="card">
        <h2 class="section-title">📋 订单管理</h2>
        
        <el-row :gutter="20" style="margin-bottom: 20px;">
          <el-col :span="6">
            <el-input 
              v-model="searchKeyword" 
              placeholder="搜索订单号/客户名"
              clearable
              size="small"
            ></el-input>
          </el-col>
          <el-col :span="6">
            <el-select v-model="filterStatus" placeholder="筛选状态" clearable size="small" style="width: 100%;">
              <el-option label="待处理" value="pending"></el-option>
              <el-option label="生产中" value="processing"></el-option>
              <el-option label="已完成" value="completed"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="currentOperator" placeholder="选择操作人" size="small" style="width: 100%;">
              <el-option label="张师傅" value="张师傅"></el-option>
              <el-option label="李师傅" value="李师傅"></el-option>
              <el-option label="王师傅" value="王师傅"></el-option>
              <el-option label="赵师傅" value="赵师傅"></el-option>
              <el-option label="管理员" value="管理员"></el-option>
            </el-select>
          </el-col>
          <el-col :span="6" style="text-align: right;">
            <span style="color: #666;">共 {{ filteredOrders.length }} 个订单</span>
          </el-col>
        </el-row>

        <div v-if="filteredOrders.length === 0" style="text-align: center; padding: 40px; color: #999;">
          暂无订单数据
        </div>

        <div v-for="order in filteredOrders" :key="order.id" class="order-card" :id="'order-' + order.id" :class="{ 'new-order-highlight': order.id === newOrderId, 'pending-order': order.status === 'pending' }">
          <div class="order-header">
            <span class="order-id">
              订单号：{{ order.id }}
              <el-tag v-if="order.id === newOrderId" type="success" size="mini" style="margin-left: 10px;">
                <i class="el-icon-star-on"></i> 新订单
              </el-tag>
            </span>
            <span>
              <span class="order-status" :style="getStatusStyle(order.status)">
                {{ getStatusText(order.status) }}
              </span>
              <span style="margin-left: 15px; font-weight: 600; color: #c0392b;">¥{{ order.price }}</span>
            </span>
          </div>
          
          <el-row :gutter="20">
            <el-col :md="12">
              <div style="margin-bottom: 10px;">
                <strong>客户信息：</strong>{{ order.customerName }} - {{ order.customerPhone }}
              </div>
              <div style="margin-bottom: 10px;">
                <strong>定制规格：</strong>{{ getMaterialText(order.material) }} · {{ order.width }}×{{ order.height }}cm
              </div>
              <div style="margin-bottom: 10px;">
                <strong>图案主题：</strong>{{ getThemeText(order.theme) }}
              </div>
              <div style="margin-bottom: 10px;">
                <strong>装裱方式：</strong>{{ getFramingText(order.framing) }}
              </div>
            </el-col>
            <el-col :md="12">
              <div style="margin-bottom: 10px;">
                <strong>下单时间：</strong>{{ order.orderTime }}
              </div>
              <div v-if="order.statusHistory && order.statusHistory.length > 0" style="margin-bottom: 10px;">
                <strong>状态变更记录：</strong>
                <div style="margin-top: 5px; padding-left: 15px;">
                  <div v-for="(h, idx) in order.statusHistory" :key="idx" style="font-size: 12px; color: #666; margin-bottom: 3px;">
                    {{ h.time }} - {{ h.statusText }} <span v-if="h.operator" style="color: #409eff;">(操作人: {{ h.operator }})</span>
                  </div>
                </div>
              </div>
              <div v-if="order.remark" style="margin-bottom: 10px;">
                <strong>备注：</strong>{{ order.remark }}
              </div>
            </el-col>
          </el-row>

          <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid #f0f0f0;">
            <div style="margin-bottom: 10px; font-weight: 600;">生产流程进度</div>
            <el-steps :active="getStepIndex(order.status)" size="small" finish-status="success">
              <el-step title="选纸"></el-step>
              <el-step title="画稿"></el-step>
              <el-step title="刻制"></el-step>
              <el-step title="修整"></el-step>
              <el-step title="除尘"></el-step>
              <el-step title="装裱"></el-step>
              <el-step title="质检"></el-step>
              <el-step title="完工"></el-step>
            </el-steps>
            
            <div style="margin-top: 20px; text-align: right;">
              <el-dropdown @command="(status) => handleUpdateStatus(order.id, status)" v-if="order.status !== 'completed'">
                <el-button type="primary" size="small">
                  更新状态<i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="step_1">1. 选纸完成</el-dropdown-item>
                  <el-dropdown-item command="step_2">2. 画稿完成</el-dropdown-item>
                  <el-dropdown-item command="step_3">3. 刻制完成</el-dropdown-item>
                  <el-dropdown-item command="step_4">4. 修整完成</el-dropdown-item>
                  <el-dropdown-item command="step_5">5. 除尘完成</el-dropdown-item>
                  <el-dropdown-item command="step_6">6. 装裱完成</el-dropdown-item>
                  <el-dropdown-item command="step_7">7. 质检完成</el-dropdown-item>
                  <el-dropdown-item command="completed">8. 订单完工</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown>
              <el-tag type="success" v-else size="small">订单已完成</el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  data() {
    return {
      searchKeyword: '',
      filterStatus: '',
      currentOperator: ''
    }
  },
  computed: {
    filteredOrders() {
      return this.orders.filter(order => {
        const matchSearch = !this.searchKeyword || 
          order.id.includes(this.searchKeyword) || 
          order.customerName.includes(this.searchKeyword);
        const matchStatus = !this.filterStatus || order.status === this.filterStatus;
        return matchSearch && matchStatus;
      }).sort((a, b) => new Date(b.orderTime) - new Date(a.orderTime));
    }
  },
  watch: {
    newOrderId(newId) {
      if (newId) {
        this.$nextTick(() => {
          const element = document.getElementById('order-' + newId);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      }
    }
  },
  methods: {
    getStatusStyle(status) {
      const styles = {
        pending: { background: '#fef0f0', color: '#f56c6c' },
        step_1: { background: '#ecf5ff', color: '#409eff' },
        step_2: { background: '#ecf5ff', color: '#409eff' },
        step_3: { background: '#ecf5ff', color: '#409eff' },
        step_4: { background: '#ecf5ff', color: '#409eff' },
        step_5: { background: '#ecf5ff', color: '#409eff' },
        step_6: { background: '#ecf5ff', color: '#409eff' },
        step_7: { background: '#ecf5ff', color: '#409eff' },
        completed: { background: '#f0f9eb', color: '#67c23a' }
      };
      return styles[status] || styles.pending;
    },
    getStatusText(status) {
      const texts = {
        pending: '待处理',
        step_1: '选纸中',
        step_2: '画稿中',
        step_3: '刻制中',
        step_4: '修整中',
        step_5: '除尘中',
        step_6: '装裱中',
        step_7: '质检中',
        completed: '已完成'
      };
      return texts[status] || '未知';
    },
    getStepIndex(status) {
      const indexes = {
        pending: -1,
        step_1: 0,
        step_2: 1,
        step_3: 2,
        step_4: 3,
        step_5: 4,
        step_6: 5,
        step_7: 6,
        completed: 7
      };
      return indexes[status] || -1;
    },
    getMaterialText(material) {
      const texts = {
        xuan: '宣纸',
        red: '红纸',
        gold: '金箔纸',
        silk: '丝绸纸'
      };
      return texts[material] || material;
    },
    getThemeText(theme) {
      const texts = {
        spring_festival: '春节福字',
        flowers_birds: '花鸟鱼虫',
        characters: '人物故事',
        auspicious: '吉祥图案',
        zodiac: '生肖属相',
        landscape: '山水风景',
        custom: '自定义图案'
      };
      return texts[theme] || theme;
    },
    getFramingText(framing) {
      const texts = {
        none: '无需装裱',
        simple: '简易装裱',
        standard: '标准装裱',
        premium: '精品装裱'
      };
      return texts[framing] || framing;
    },
    handleUpdateStatus(orderId, status) {
      if (!this.currentOperator) {
        this.$message({
          message: '请先选择操作人',
          type: 'warning'
        });
        return;
      }
      this.$emit('update-status', orderId, status, this.currentOperator);
    }
  }
});

new Vue({
  el: '#app',
  data() {
    return {
      activeTab: 'order',
      orders: [],
      newOrderId: ''
    }
  },
  created() {
    this.loadOrders();
  },
  methods: {
    handleTabClick(tab) {
      this.activeTab = tab.name;
    },
    handleOrderSubmit(orderData) {
      const newOrder = {
        id: 'PC' + Date.now().toString().slice(-8),
        ...orderData,
        status: 'pending',
        statusHistory: [
          {
            status: 'pending',
            statusText: '订单创建（待处理）',
            time: new Date().toLocaleString('zh-CN'),
            operator: '系统'
          }
        ]
      };
      this.orders.push(newOrder);
      this.saveOrders();
      
      this.activeTab = 'admin';
      this.newOrderId = newOrder.id;
      
      this.$message({
        message: '订单提交成功！订单号：' + newOrder.id,
        type: 'success',
        duration: 3000
      });
      
      setTimeout(() => {
        this.newOrderId = '';
      }, 10000);
    },
    updateOrderStatus(orderId, status, operator) {
      const order = this.orders.find(o => o.id === orderId);
      if (order) {
        order.status = status;
        if (!order.statusHistory) {
          order.statusHistory = [];
        }
        order.statusHistory.push({
          status: status,
          statusText: this.getStatusText(status),
          time: new Date().toLocaleString('zh-CN'),
          operator: operator
        });
        this.saveOrders();
        this.$message({
          message: '订单状态已更新',
          type: 'success'
        });
      }
    },
    getStatusText(status) {
      const texts = {
        pending: '待处理',
        step_1: '进入选纸工序',
        step_2: '进入画稿工序',
        step_3: '进入刻制工序',
        step_4: '进入修整工序',
        step_5: '进入除尘工序',
        step_6: '进入装裱工序',
        step_7: '进入质检工序',
        completed: '订单已完工'
      };
      return texts[status] || '未知状态';
    },
    saveOrders() {
      localStorage.setItem('paperCuttingOrders', JSON.stringify(this.orders));
    },
    loadOrders() {
      const saved = localStorage.getItem('paperCuttingOrders');
      if (saved) {
        this.orders = JSON.parse(saved);
      }
    }
  }
});
