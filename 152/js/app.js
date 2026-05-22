Vue.use(VueRouter)
Vue.use(ELEMENT)

const eventBus = new Vue()

const OrderForm = {
  template: `
    <div class="order-container">
      <div class="order-card">
        <h2 style="text-align: center; margin-bottom: 30px; color: #8B4513;">🧵 苏绣手帕定制</h2>
        
        <el-form :model="orderForm" :rules="rules" ref="orderFormRef" label-width="100px">
          <div class="section-title">📦 底料面料选择</div>
          <el-form-item prop="fabric" :error="errors.fabric">
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="8" v-for="fabric in fabrics" :key="fabric.value">
                <div 
                  class="fabric-item" 
                  :class="{ active: orderForm.fabric === fabric.value, error: errors.fabric }"
                  @click="selectFabric(fabric.value)"
                  @blur="validateField('fabric')"
                  tabindex="0"
                >
                  <div class="fabric-icon">{{ fabric.icon }}</div>
                  <div>{{ fabric.label }}</div>
                </div>
              </el-col>
            </el-row>
          </el-form-item>

          <el-divider></el-divider>

          <div class="section-title">📐 手帕尺寸</div>
          <div class="size-tip">
            <i class="el-icon-info"></i>
            <span>规范尺寸：小方巾(20×20cm)、中方巾(30×30cm)、大方巾(45×45cm)、超大巾(60×60cm)</span>
          </div>
          <el-row :gutter="20" style="margin-bottom: 30px;">
            <el-col :span="12">
              <el-form-item label="宽度 (cm)" prop="width" :error="errors.width">
                <el-input-number 
                  v-model="orderForm.width" 
                  :min="20" 
                  :max="60" 
                  :step="5"
                  @change="validateField('width')"
                  @blur.native="validateField('width')"
                ></el-input-number>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="高度 (cm)" prop="height" :error="errors.height">
                <el-input-number 
                  v-model="orderForm.height" 
                  :min="20" 
                  :max="60" 
                  :step="5"
                  @change="validateField('height')"
                  @blur.native="validateField('height')"
                ></el-input-number>
              </el-form-item>
            </el-col>
          </el-row>

          <el-divider></el-divider>

          <div class="section-title">🪡 刺绣针法选择</div>
          <el-form-item prop="stitch" :error="errors.stitch">
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="6" v-for="stitch in stitches" :key="stitch.value">
                <div 
                  class="stitch-item" 
                  :class="{ active: orderForm.stitch === stitch.value, error: errors.stitch }"
                  @click="selectStitch(stitch.value)"
                  @blur="validateField('stitch')"
                  tabindex="0"
                >
                  <div style="font-size: 24px; margin-bottom: 5px;">✂️</div>
                  <div style="font-size: 13px;">{{ stitch.label }}</div>
                </div>
              </el-col>
            </el-row>
          </el-form-item>

          <el-divider></el-divider>

          <div class="section-title">🎨 绣线色系选择</div>
          <el-form-item prop="color" :error="errors.color">
            <el-row :gutter="20" style="margin-bottom: 10px;">
              <el-col :span="6" v-for="color in colors" :key="color.value">
                <div 
                  class="color-item" 
                  :class="{ active: orderForm.color === color.value, error: errors.color }"
                  @click="selectColor(color.value)"
                  @blur="validateField('color')"
                  tabindex="0"
                >
                  <div class="color-swatch" :style="{ background: color.hex }"></div>
                  <div style="font-size: 13px;">{{ color.label }}</div>
                </div>
              </el-col>
            </el-row>
          </el-form-item>

          <el-divider></el-divider>

          <div class="section-title">🖼️ 图案排版选择</div>
          <el-row :gutter="20" style="margin-bottom: 30px;">
            <el-col :span="8" v-for="layout in layouts" :key="layout.value">
              <div 
                class="layout-item" 
                :class="{ active: orderForm.layout === layout.value }"
                @click="orderForm.layout = layout.value"
              >
                <div class="layout-preview">
                  <span style="font-size: 30px;">{{ layout.icon }}</span>
                </div>
                <div>{{ layout.label }}</div>
              </div>
            </el-col>
          </el-row>

          <el-divider></el-divider>

          <div class="section-title">📝 联系信息</div>
          <el-form-item label="联系人" prop="contact">
            <el-input 
              v-model="orderForm.contact" 
              placeholder="请输入您的姓名"
              @blur="validateField('contact')"
            ></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input 
              v-model="orderForm.phone" 
              placeholder="请输入联系电话"
              @blur="validateField('phone')"
            ></el-input>
          </el-form-item>
          <el-form-item label="备注">
            <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="其他特殊要求"></el-input>
          </el-form-item>

          <el-button type="primary" class="submit-btn" @click="submitOrder" :loading="submitting">
            提交订单
          </el-button>
        </el-form>
      </div>
    </div>
  `,
  data() {
    return {
      submitting: false,
      orderForm: {
        fabric: '',
        width: 30,
        height: 30,
        stitch: '',
        color: '',
        layout: 'center',
        contact: '',
        phone: '',
        remark: ''
      },
      errors: {
        fabric: '',
        width: '',
        height: '',
        stitch: '',
        color: '',
        contact: '',
        phone: ''
      },
      rules: {
        fabric: [{ required: true, message: '请选择底料面料', trigger: 'blur' }],
        width: [{ required: true, message: '请输入宽度', trigger: 'blur' }],
        height: [{ required: true, message: '请输入高度', trigger: 'blur' }],
        stitch: [{ required: true, message: '请选择刺绣针法', trigger: 'blur' }],
        color: [{ required: true, message: '请选择绣线色系', trigger: 'blur' }]
      },
      fabrics: [
        { value: 'silk', label: '真丝面料', icon: '🧵' },
        { value: 'cotton', label: '纯棉面料', icon: '👕' },
        { value: 'linen', label: '亚麻面料', icon: '🌿' }
      ],
      stitches: [
        { value: 'pingzhen', label: '平针' },
        { value: 'taozhen', label: '套针' },
        { value: 'dazhen', label: '打籽针' },
        { value: 'luanzhen', label: '乱针' }
      ],
      colors: [
        { value: 'traditional', label: '传统色系', hex: '#8B0000' },
        { value: 'elegant', label: '淡雅色系', hex: '#FFB6C1' },
        { value: 'fresh', label: '清新色系', hex: '#98FB98' },
        { value: 'luxury', label: '华贵色系', hex: '#FFD700' }
      ],
      layouts: [
        { value: 'center', label: '居中图案', icon: '⭐' },
        { value: 'corner', label: '角隅图案', icon: '🔸' },
        { value: 'border', label: '边框图案', icon: '🔲' }
      ]
    }
  },
  methods: {
    selectFabric(value) {
      this.orderForm.fabric = value
      this.validateField('fabric')
    },
    selectStitch(value) {
      this.orderForm.stitch = value
      this.validateField('stitch')
    },
    selectColor(value) {
      this.orderForm.color = value
      this.validateField('color')
    },
    validateField(field) {
      this.$nextTick(() => {
        switch(field) {
          case 'fabric':
            if (!this.orderForm.fabric) {
              this.errors.fabric = '请选择底料面料'
            } else {
              this.errors.fabric = ''
            }
            break
          case 'width':
            if (!this.orderForm.width) {
              this.errors.width = '请输入宽度'
            } else if (this.orderForm.width < 20 || this.orderForm.width > 60) {
              this.errors.width = '宽度范围为20-60cm'
            } else {
              this.errors.width = ''
            }
            break
          case 'height':
            if (!this.orderForm.height) {
              this.errors.height = '请输入高度'
            } else if (this.orderForm.height < 20 || this.orderForm.height > 60) {
              this.errors.height = '高度范围为20-60cm'
            } else {
              this.errors.height = ''
            }
            break
          case 'stitch':
            if (!this.orderForm.stitch) {
              this.errors.stitch = '请选择刺绣针法'
            } else {
              this.errors.stitch = ''
            }
            break
          case 'color':
            if (!this.orderForm.color) {
              this.errors.color = '请选择绣线色系'
            } else {
              this.errors.color = ''
            }
            break
          case 'contact':
            if (!this.orderForm.contact) {
              this.$message.warning('请输入联系人姓名')
            }
            break
          case 'phone':
            if (!this.orderForm.phone) {
              this.$message.warning('请输入联系电话')
            } else if (!/^1[3-9]\d{9}$/.test(this.orderForm.phone)) {
              this.$message.warning('请输入正确的手机号码')
            }
            break
        }
      })
    },
    validateAll() {
      let isValid = true
      if (!this.orderForm.fabric) {
        this.errors.fabric = '请选择底料面料'
        isValid = false
      }
      if (!this.orderForm.width || this.orderForm.width < 20 || this.orderForm.width > 60) {
        this.errors.width = '请输入有效的宽度(20-60cm)'
        isValid = false
      }
      if (!this.orderForm.height || this.orderForm.height < 20 || this.orderForm.height > 60) {
        this.errors.height = '请输入有效的高度(20-60cm)'
        isValid = false
      }
      if (!this.orderForm.stitch) {
        this.errors.stitch = '请选择刺绣针法'
        isValid = false
      }
      if (!this.orderForm.color) {
        this.errors.color = '请选择绣线色系'
        isValid = false
      }
      if (!this.orderForm.contact) {
        this.$message.warning('请输入联系人姓名')
        isValid = false
      }
      if (!this.orderForm.phone) {
        this.$message.warning('请输入联系电话')
        isValid = false
      } else if (!/^1[3-9]\d{9}$/.test(this.orderForm.phone)) {
        this.$message.warning('请输入正确的手机号码')
        isValid = false
      }
      return isValid
    },
    submitOrder() {
      if (!this.validateAll()) {
        return
      }
      
      this.submitting = true
      setTimeout(() => {
        const newOrder = {
          id: 'ORD' + Date.now().toString().slice(-6),
          ...this.orderForm,
          status: 0,
          statusHistory: [
            {
              status: 0,
              stepName: '选料',
              time: new Date().toLocaleString(),
              remark: '订单创建'
            }
          ],
          createTime: new Date().toLocaleString()
        }
        
        const orders = JSON.parse(localStorage.getItem('suxiu_orders') || '[]')
        orders.unshift(newOrder)
        localStorage.setItem('suxiu_orders', JSON.stringify(orders))
        
        eventBus.$emit('order-created', newOrder.id)
        
        this.$message.success('订单提交成功！')
        this.submitting = false
        
        this.orderForm = {
          fabric: '',
          width: 30,
          height: 30,
          stitch: '',
          color: '',
          layout: 'center',
          contact: '',
          phone: '',
          remark: ''
        }
        this.errors = {
          fabric: '',
          width: '',
          height: '',
          stitch: '',
          color: '',
          contact: '',
          phone: ''
        }
        
        this.$router.push('/admin')
      }, 1000)
    }
  }
}

const AdminPanel = {
  template: `
    <div class="admin-container">
      <div class="admin-card">
        <h2 style="text-align: center; margin-bottom: 30px; color: #8B4513;">📋 订单管理系统</h2>
        
        <div style="margin-bottom: 20px;" class="admin-toolbar">
          <el-input 
            v-model="operatorName" 
            placeholder="请输入操作员姓名" 
            size="small" 
            style="width: 180px; margin-right: 10px;"
          ></el-input>
          <el-button type="primary" size="small" @click="addDemoOrders">添加演示订单</el-button>
          <el-button type="danger" size="small" @click="clearAllOrders">清空所有订单</el-button>
        </div>

        <el-table 
          :data="orders" 
          border 
          class="order-table" 
          v-loading="loading"
          ref="orderTable"
          row-key="id"
          :highlight-current-row="true"
          :row-class-name="getRowClassName"
        >
          <el-table-column label="订单号" width="160">
            <template slot-scope="scope">
              <span>{{ scope.row.id }}</span>
              <el-tag v-if="isNewOrder(scope.row)" type="danger" size="mini" class="new-order-tag">新订单</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="contact" label="联系人" width="100"></el-table-column>
          <el-table-column prop="phone" label="电话" width="120"></el-table-column>
          <el-table-column label="订单详情" width="280">
            <template slot-scope="scope">
              <div class="order-detail">
                <p>面料：{{ getFabricLabel(scope.row.fabric) }}</p>
                <p>尺寸：{{ scope.row.width }} × {{ scope.row.height }} cm</p>
                <p>针法：{{ getStitchLabel(scope.row.stitch) }}</p>
                <p>色系：{{ getColorLabel(scope.row.color) }}</p>
                <p>排版：{{ getLayoutLabel(scope.row.layout) }}</p>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="生产进度" min-width="400">
            <template slot-scope="scope">
              <div class="process-steps" style="padding: 10px 0; margin: 0;">
                <div 
                  v-for="(step, index) in processSteps" 
                  :key="index"
                  class="process-step"
                  :class="{ 
                    completed: scope.row.status > index, 
                    current: scope.row.status === index 
                  }"
                >
                  <div class="step-number">{{ index + 1 }}</div>
                  <div class="step-name">{{ step }}</div>
                </div>
              </div>
              <div v-if="scope.row.statusHistory && scope.row.statusHistory.length > 0" class="status-history">
                <el-popover
                  placement="top"
                  width="300"
                  trigger="hover"
                >
                  <div style="max-height: 250px; overflow-y: auto;">
                    <p v-for="(record, idx) in scope.row.statusHistory" :key="idx" style="margin: 8px 0; font-size: 12px; padding-bottom: 5px; border-bottom: 1px dashed #eee;">
                      <span style="color: #67C23A; font-weight: bold;">✓</span> 
                      <strong style="color: #8B4513;">{{ record.stepName }}</strong>
                      <br>
                      <span style="color: #999; margin-left: 18px;">时间：{{ record.time }}</span>
                      <span v-if="record.operator" style="color: #409EFF; margin-left: 18px; display: block;">操作员：{{ record.operator }}</span>
                      <span v-if="record.remark" style="color: #666; margin-left: 18px; display: block;">{{ record.remark }}</span>
                    </p>
                  </div>
                  <el-button slot="reference" type="text" size="mini" style="color: #8B4513;">查看历史记录</el-button>
                </el-popover>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" fixed="right">
            <template slot-scope="scope">
              <el-button 
                v-if="scope.row.status < processSteps.length"
                type="success" 
                size="mini" 
                @click="nextStep(scope.row)"
              >
                下一步
              </el-button>
              <el-tag v-else type="success" size="small">已完工</el-tag>
            </template>
          </el-table-column>
        </el-table>

        <el-empty v-if="orders.length === 0" description="暂无订单数据"></el-empty>
      </div>
    </div>
  `,
  data() {
    return {
      loading: false,
      orders: [],
      operatorName: '',
      processSteps: ['选料', '描图', '上绷', '刺绣', '清洗', '整烫', '锁边', '完工'],
      fabrics: [
        { value: 'silk', label: '真丝面料' },
        { value: 'cotton', label: '纯棉面料' },
        { value: 'linen', label: '亚麻面料' }
      ],
      stitches: [
        { value: 'pingzhen', label: '平针' },
        { value: 'taozhen', label: '套针' },
        { value: 'dazhen', label: '打籽针' },
        { value: 'luanzhen', label: '乱针' }
      ],
      colors: [
        { value: 'traditional', label: '传统色系' },
        { value: 'elegant', label: '淡雅色系' },
        { value: 'fresh', label: '清新色系' },
        { value: 'luxury', label: '华贵色系' }
      ],
      layouts: [
        { value: 'center', label: '居中图案' },
        { value: 'corner', label: '角隅图案' },
        { value: 'border', label: '边框图案' }
      ]
    }
  },
  created() {
    this.loadOrders()
    eventBus.$on('order-created', (orderId) => {
      this.loadOrders()
      this.$nextTick(() => {
        this.scrollToOrder(orderId)
      })
    })
  },
  beforeDestroy() {
    eventBus.$off('order-created')
  },
  methods: {
    loadOrders() {
      this.orders = JSON.parse(localStorage.getItem('suxiu_orders') || '[]')
    },
    getFabricLabel(value) {
      const item = this.fabrics.find(f => f.value === value)
      return item ? item.label : value
    },
    getStitchLabel(value) {
      const item = this.stitches.find(s => s.value === value)
      return item ? item.label : value
    },
    getColorLabel(value) {
      const item = this.colors.find(c => c.value === value)
      return item ? item.label : value
    },
    getLayoutLabel(value) {
      const item = this.layouts.find(l => l.value === value)
      return item ? item.label : value
    },
    nextStep(order) {
      if (!this.operatorName.trim()) {
        this.$message.warning('请先输入操作员姓名')
        return
      }
      
      if (order.status >= this.processSteps.length) {
        this.$message.warning('订单已完工，无法继续操作')
        return
      }
      
      const previousStatus = order.status
      const nextStatus = previousStatus + 1
      
      if (!order.statusHistory) {
        order.statusHistory = []
      }
      
      const historyRecord = {
        status: nextStatus,
        stepName: this.processSteps[nextStatus] || '完工',
        time: new Date().toLocaleString(),
        operator: this.operatorName,
        remark: `从「${this.processSteps[previousStatus]}」推进`
      }
      
      order.statusHistory.push(historyRecord)
      order.status = nextStatus
      
      localStorage.setItem('suxiu_orders', JSON.stringify(this.orders))
      this.$message.success(`已推进到「${historyRecord.stepName}」工序`)
    },
    isNewOrder(order) {
      if (!order.createTime) return false
      const orderTime = new Date(order.createTime)
      const now = new Date()
      const diffHours = (now - orderTime) / (1000 * 60 * 60)
      return diffHours < 24
    },
    getRowClassName({ row }) {
      return this.isNewOrder(row) ? 'new-order-row' : ''
    },
    scrollToOrder(orderId) {
      const table = this.$refs.orderTable
      if (table && table.$el) {
        const rows = table.$el.querySelectorAll('.el-table__row')
        for (let i = 0; i < rows.length; i++) {
          if (rows[i].textContent.includes(orderId)) {
            rows[i].scrollIntoView({ behavior: 'smooth', block: 'center' })
            rows[i].style.backgroundColor = '#FFF8DC'
            setTimeout(() => {
              rows[i].style.backgroundColor = ''
            }, 2000)
            break
          }
        }
      }
    },
    addDemoOrders() {
      const now = new Date()
      const nowStr = now.toLocaleString()
      const yesterdayStr = new Date(now - 24 * 60 * 60 * 1000).toLocaleString()
      
      const demoOrders = [
        {
          id: 'ORD001001',
          fabric: 'silk',
          width: 35,
          height: 35,
          stitch: 'pingzhen',
          color: 'traditional',
          layout: 'center',
          contact: '张三',
          phone: '13800138001',
          remark: '加急订单',
          status: 3,
          statusHistory: [
            { status: 0, stepName: '选料', time: yesterdayStr, remark: '订单创建', operator: '李主管' },
            { status: 1, stepName: '描图', time: yesterdayStr, remark: '从「选料」推进', operator: '王师傅' },
            { status: 2, stepName: '上绷', time: yesterdayStr, remark: '从「描图」推进', operator: '张师傅' },
            { status: 3, stepName: '刺绣', time: yesterdayStr, remark: '从「上绷」推进', operator: '刘师傅' }
          ],
          createTime: yesterdayStr
        },
        {
          id: 'ORD001002',
          fabric: 'cotton',
          width: 30,
          height: 30,
          stitch: 'taozhen',
          color: 'elegant',
          layout: 'corner',
          contact: '李四',
          phone: '13800138002',
          remark: '',
          status: 5,
          statusHistory: [
            { status: 0, stepName: '选料', time: yesterdayStr, remark: '订单创建', operator: '李主管' },
            { status: 1, stepName: '描图', time: yesterdayStr, remark: '从「选料」推进', operator: '王师傅' },
            { status: 2, stepName: '上绷', time: nowStr, remark: '从「描图」推进', operator: '张师傅' },
            { status: 3, stepName: '刺绣', time: nowStr, remark: '从「上绷」推进', operator: '刘师傅' },
            { status: 4, stepName: '清洗', time: nowStr, remark: '从「刺绣」推进', operator: '陈师傅' },
            { status: 5, stepName: '整烫', time: nowStr, remark: '从「清洗」推进', operator: '周师傅' }
          ],
          createTime: yesterdayStr
        },
        {
          id: 'ORD001005',
          fabric: 'silk',
          width: 30,
          height: 30,
          stitch: 'dazhen',
          color: 'luxury',
          layout: 'center',
          contact: '钱七',
          phone: '13800138005',
          remark: '定制礼品',
          status: 0,
          statusHistory: [
            { status: 0, stepName: '选料', time: nowStr, remark: '订单创建' }
          ],
          createTime: nowStr
        },
        {
          id: 'ORD001004',
          fabric: 'silk',
          width: 25,
          height: 25,
          stitch: 'luanzhen',
          color: 'luxury',
          layout: 'center',
          contact: '赵六',
          phone: '13800138004',
          remark: '',
          status: 8,
          statusHistory: [
            { status: 0, stepName: '选料', time: yesterdayStr, remark: '订单创建', operator: '李主管' },
            { status: 1, stepName: '描图', time: yesterdayStr, remark: '从「选料」推进', operator: '王师傅' },
            { status: 2, stepName: '上绷', time: yesterdayStr, remark: '从「描图」推进', operator: '张师傅' },
            { status: 3, stepName: '刺绣', time: yesterdayStr, remark: '从「上绷」推进', operator: '刘师傅' },
            { status: 4, stepName: '清洗', time: '2024-01-16 09:00:00', remark: '从「刺绣」推进' },
            { status: 5, stepName: '整烫', time: '2024-01-16 11:00:00', remark: '从「清洗」推进' },
            { status: 6, stepName: '锁边', time: '2024-01-16 15:00:00', remark: '从「整烫」推进' },
            { status: 7, stepName: '完工', time: '2024-01-16 17:00:00', remark: '从「锁边」推进' },
            { status: 8, stepName: '完工', time: '2024-01-16 17:00:00', remark: '订单完成' }
          ],
          createTime: '2024-01-14 16:45:00'
        }
      ]
      localStorage.setItem('suxiu_orders', JSON.stringify(demoOrders))
      this.loadOrders()
      this.$message.success('已添加演示订单')
    },
    clearAllOrders() {
      this.$confirm('确定要清空所有订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem('suxiu_orders')
        this.orders = []
        this.$message.success('已清空所有订单')
      }).catch(() => {})
    }
  }
}

const routes = [
  { path: '/', redirect: '/order' },
  { path: '/order', component: OrderForm },
  { path: '/admin', component: AdminPanel }
]

const router = new VueRouter({
  routes
})

new Vue({
  el: '#app',
  router,
  template: `
    <div>
      <div class="header">
        <h1>🌸 苏绣手帕定制系统 🌸</h1>
      </div>
      <div class="nav-tabs">
        <el-tabs v-model="activeTab" @tab-click="handleTabClick">
          <el-tab-pane label="用户下单" name="order"></el-tab-pane>
          <el-tab-pane label="管理员订单" name="admin"></el-tab-pane>
        </el-tabs>
      </div>
      <router-view></router-view>
    </div>
  `,
  data() {
    return {
      activeTab: 'order'
    }
  },
  created() {
    this.activeTab = this.$route.path.replace('/', '') || 'order'
  },
  methods: {
    handleTabClick(tab) {
      this.$router.push('/' + tab.name)
    }
  },
  watch: {
    $route(to) {
      this.activeTab = to.path.replace('/', '') || 'order'
    }
  }
})
