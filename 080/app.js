Vue.use(VueRouter);
Vue.use(ELEMENT);

const STATUS_ORDER = ['选竹', '破篾', '编织', '定型', '浸油', '晾干', '完工'];

const orderStorage = {
  getOrders() {
    const orders = localStorage.getItem('bamboo_orders');
    return orders ? JSON.parse(orders) : [];
  },
  saveOrders(orders) {
    localStorage.setItem('bamboo_orders', JSON.stringify(orders));
  },
  addOrder(order) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const orders = this.getOrders();
        order.id = Date.now();
        order.createTime = new Date().toLocaleString();
        order.status = '选竹';
        orders.unshift(order);
        this.saveOrders(orders);
        resolve(orders);
      }, 500);
    });
  },
  updateOrder(id, data) {
    return new Promise((resolve) => {
      setTimeout(() => {
        const orders = this.getOrders();
        const index = orders.findIndex(o => o.id === id);
        if (index !== -1) {
          orders[index] = { ...orders[index], ...data };
          this.saveOrders(orders);
        }
        resolve(orders);
      }, 300);
    });
  },
  fetchOrders() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(this.getOrders());
      }, 200);
    });
  }
};

const CustomerOrder = {
  template: `
    <div class="customer-page">
      <el-header class="page-header">
        <div class="header-content">
          <h1><i class="el-icon-date"></i> 传统竹编茶滤定制</h1>
          <el-button type="primary" @click="$router.push('/admin')">管理员入口</el-button>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <el-row :gutter="20">
          <el-col :span="14">
            <el-card class="form-card" shadow="hover">
              <div slot="header" class="card-header">
                <span><i class="el-icon-edit"></i> 定制信息</span>
              </div>
              
              <el-form ref="orderForm" :model="orderForm" :rules="rules" label-width="100px" size="medium">
                <el-form-item label="客户姓名" prop="customerName">
                  <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名" clearable></el-input>
                </el-form-item>
                
                <el-form-item label="联系电话" prop="phone">
                  <el-input v-model="orderForm.phone" placeholder="请输入联系电话" clearable></el-input>
                </el-form-item>
                
                <el-form-item label="竹材选型" prop="bambooType">
                  <el-select v-model="orderForm.bambooType" placeholder="请选择竹材" style="width: 100%">
                    <el-option label="毛竹 - 坚韧耐用" value="毛竹"></el-option>
                    <el-option label="楠竹 - 纹理细腻" value="楠竹"></el-option>
                    <el-option label="水竹 - 柔软轻盈" value="水竹"></el-option>
                    <el-option label="紫竹 - 色泽典雅" value="紫竹"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="滤兜直径" prop="diameter">
                  <el-input-number 
                    v-model="orderForm.diameter" 
                    :min="5" 
                    :max="15" 
                    :step="0.5"
                    :precision="1"
                    style="width: 100%">
                  </el-input-number>
                  <div style="color: #909399; font-size: 12px; margin-top: 5px;">
                    <i class="el-icon-info"></i> 合理范围：5-15cm，建议标准尺寸为 8cm
                  </div>
                </el-form-item>
                
                <el-form-item label="手柄款式" prop="handleStyle">
                  <el-radio-group v-model="orderForm.handleStyle">
                    <el-radio label="无手柄">无手柄</el-radio>
                    <el-radio label="直柄">直柄</el-radio>
                    <el-radio label="弯柄">弯柄</el-radio>
                    <el-radio label="雕花柄">雕花柄</el-radio>
                  </el-radio-group>
                </el-form-item>
                
                <el-form-item label="编织纹路" prop="weavePattern">
                  <el-select v-model="orderForm.weavePattern" placeholder="请选择编织纹路" style="width: 100%">
                    <el-option label="十字纹 - 经典大方" value="十字纹"></el-option>
                    <el-option label="人字纹 - 疏密有致" value="人字纹"></el-option>
                    <el-option label="六角纹 - 精致细密" value="六角纹"></el-option>
                    <el-option label="回字纹 - 传统吉祥" value="回字纹"></el-option>
                    <el-option label="螺旋纹 - 现代简约" value="螺旋纹"></el-option>
                  </el-select>
                </el-form-item>
                
                <el-form-item label="定制数量" prop="quantity">
                  <el-input-number v-model="orderForm.quantity" :min="1" :max="100" style="width: 100%"></el-input-number>
                </el-form-item>
                
                <el-form-item label="备注留言" prop="remark">
                  <el-input
                    type="textarea"
                    :rows="4"
                    v-model="orderForm.remark"
                    placeholder="请输入特殊要求或备注信息..."
                    maxlength="200"
                    show-word-limit>
                  </el-input>
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" size="large" @click="submitOrder" :loading="submitting" :disabled="submitting" style="width: 100%">
                    <i class="el-icon-check"></i> {{ submitting ? '提交中...' : '提交订单' }}
                  </el-button>
                </el-form-item>
              </el-form>
            </el-card>
          </el-col>
          
          <el-col :span="10">
            <el-card class="preview-card" shadow="hover">
              <div slot="header" class="card-header">
                <span><i class="el-icon-picture"></i> 效果预览</span>
              </div>
              
              <div class="preview-content">
                <div class="tea-filter-preview">
                  <div class="filter-body" :class="[getBambooClass, getPatternClass]">
                    <div class="filter-rim top-rim"></div>
                    <div class="filter-mesh">
                      <div class="mesh-pattern"></div>
                    </div>
                    <div class="filter-rim bottom-rim"></div>
                  </div>
                  <div class="handle" v-if="orderForm.handleStyle !== '无手柄'" :class="getHandleClass"></div>
                </div>
                
                <el-divider></el-divider>
                
                <div class="order-summary">
                  <h3><i class="el-icon-document"></i> 订单摘要</h3>
                  <el-descriptions :column="1" border size="small">
                    <el-descriptions-item label="竹材类型">{{ orderForm.bambooType || '未选择' }}</el-descriptions-item>
                    <el-descriptions-item label="滤兜直径">{{ orderForm.diameter ? orderForm.diameter + 'cm' : '未选择' }}</el-descriptions-item>
                    <el-descriptions-item label="手柄款式">{{ orderForm.handleStyle || '未选择' }}</el-descriptions-item>
                    <el-descriptions-item label="编织纹路">{{ orderForm.weavePattern || '未选择' }}</el-descriptions-item>
                    <el-descriptions-item label="定制数量">{{ orderForm.quantity }} 个</el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </el-main>
    </div>
  `,
  data() {
    return {
      submitting: false,
      orderForm: {
        customerName: '',
        phone: '',
        bambooType: '',
        diameter: null,
        handleStyle: '',
        weavePattern: '',
        quantity: 1,
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        bambooType: [
          { required: true, message: '请选择竹材类型', trigger: 'change' }
        ],
        diameter: [
          { required: true, message: '请输入滤兜直径', trigger: 'blur' },
          { type: 'number', min: 5, max: 15, message: '直径需在 5-15cm 范围内', trigger: 'blur' }
        ],
        handleStyle: [
          { required: true, message: '请选择手柄款式', trigger: 'change' }
        ],
        weavePattern: [
          { required: true, message: '请选择编织纹路', trigger: 'change' }
        ]
      }
    };
  },
  computed: {
    getBambooClass() {
      const map = {
        '毛竹': 'bamboo-maozhu',
        '楠竹': 'bamboo-nanzhu',
        '水竹': 'bamboo-shuizhu',
        '紫竹': 'bamboo-zizhu'
      };
      return map[this.orderForm.bambooType] || 'bamboo-default';
    },
    getPatternClass() {
      const map = {
        '十字纹': 'pattern-cross',
        '人字纹': 'pattern-herringbone',
        '六角纹': 'pattern-hexagon',
        '回字纹': 'pattern-meander',
        '螺旋纹': 'pattern-spiral'
      };
      return map[this.orderForm.weavePattern] || '';
    },
    getHandleClass() {
      const map = {
        '直柄': 'handle-straight',
        '弯柄': 'handle-curved',
        '雕花柄': 'handle-engraved'
      };
      return map[this.orderForm.handleStyle] || '';
    }
  },
  methods: {
    async submitOrder() {
      this.$refs.orderForm.validate(async valid => {
        if (valid) {
          this.submitting = true;
          try {
            await orderStorage.addOrder({ ...this.orderForm });
            this.$message.success('订单提交成功！感谢您的定制！');
            this.$refs.orderForm.resetFields();
          } catch (error) {
            this.$message.error('订单提交失败，请重试！');
          } finally {
            this.submitting = false;
          }
        }
      });
    }
  }
};

const AdminManage = {
  template: `
    <div class="admin-page">
      <el-header class="page-header">
        <div class="header-content">
          <h1><i class="el-icon-s-management"></i> 订单管理系统</h1>
          <el-button @click="$router.push('/')">返回下单页</el-button>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <el-card class="list-card" shadow="hover">
          <div slot="header" class="card-header">
            <span><i class="el-icon-s-order"></i> 订单列表</span>
            <el-tag type="info" size="medium">共 {{ orders.length }} 条订单</el-tag>
          </div>
          
          <el-table :data="orders" stripe border style="width: 100%" v-loading="loading">
            <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
            <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
            <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
            <el-table-column label="定制信息" min-width="200">
              <template slot-scope="scope">
                <div class="order-info">
                  <p><span>竹材：</span>{{ scope.row.bambooType }}</p>
                  <p><span>直径：</span>{{ scope.row.diameter }}cm</p>
                  <p><span>手柄：</span>{{ scope.row.handleStyle }}</p>
                  <p><span>纹路：</span>{{ scope.row.weavePattern }}</p>
                  <p><span>数量：</span>{{ scope.row.quantity }} 个</p>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="createTime" label="下单时间" width="160" align="center"></el-table-column>
            <el-table-column label="生产状态" width="140" align="center">
              <template slot-scope="scope">
                <el-tag :type="getStatusType(scope.row.status)" size="small">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="240" align="center" fixed="right">
              <template slot-scope="scope">
                <el-button type="primary" size="mini" icon="el-icon-edit" @click="editOrder(scope.row)">编辑</el-button>
                <el-button-group>
                  <el-button 
                    size="mini" 
                    type="warning" 
                    icon="el-icon-arrow-left"
                    :disabled="isFirstStatus(scope.row.status)"
                    @click="prevStatus(scope.row)">
                    上一步
                  </el-button>
                  <el-button 
                    size="mini" 
                    type="success" 
                    :disabled="isLastStatus(scope.row.status)"
                    @click="nextStatus(scope.row)">
                    下一步<i class="el-icon-arrow-right el-icon--right"></i>
                  </el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-main>
      
      <el-dialog title="编辑订单" :visible.sync="editDialogVisible" width="600px" @close="closeEditDialog">
        <el-form ref="editForm" :model="editForm" :rules="editRules" label-width="100px" size="medium">
          <el-form-item label="客户姓名" prop="customerName">
            <el-input v-model="editForm.customerName"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="editForm.phone"></el-input>
          </el-form-item>
          <el-form-item label="竹材选型" prop="bambooType">
            <el-select v-model="editForm.bambooType" style="width: 100%">
              <el-option label="毛竹" value="毛竹"></el-option>
              <el-option label="楠竹" value="楠竹"></el-option>
              <el-option label="水竹" value="水竹"></el-option>
              <el-option label="紫竹" value="紫竹"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="滤兜直径" prop="diameter">
            <el-input-number 
              v-model="editForm.diameter" 
              :min="5" 
              :max="15" 
              :step="0.5"
              :precision="1"
              style="width: 100%">
            </el-input-number>
            <div style="color: #909399; font-size: 12px; margin-top: 5px;">
              <i class="el-icon-info"></i> 合理范围：5-15cm，建议标准尺寸为 8cm
            </div>
          </el-form-item>
          <el-form-item label="手柄款式" prop="handleStyle">
            <el-radio-group v-model="editForm.handleStyle">
              <el-radio label="无手柄">无手柄</el-radio>
              <el-radio label="直柄">直柄</el-radio>
              <el-radio label="弯柄">弯柄</el-radio>
              <el-radio label="雕花柄">雕花柄</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="编织纹路" prop="weavePattern">
            <el-select v-model="editForm.weavePattern" style="width: 100%">
              <el-option label="十字纹" value="十字纹"></el-option>
              <el-option label="人字纹" value="人字纹"></el-option>
              <el-option label="六角纹" value="六角纹"></el-option>
              <el-option label="回字纹" value="回字纹"></el-option>
              <el-option label="螺旋纹" value="螺旋纹"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="定制数量" prop="quantity">
            <el-input-number v-model="editForm.quantity" :min="1" :max="100"></el-input-number>
          </el-form-item>
          <el-form-item label="备注留言" prop="remark">
            <el-input type="textarea" :rows="3" v-model="editForm.remark"></el-input>
          </el-form-item>
        </el-form>
        <div slot="footer" class="dialog-footer">
          <el-button @click="editDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="saveEdit" :loading="saving">确 定</el-button>
        </div>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      loading: false,
      saving: false,
      orders: [],
      statusList: STATUS_ORDER,
      editDialogVisible: false,
      currentEditId: null,
      editForm: {
        customerName: '',
        phone: '',
        bambooType: '',
        diameter: null,
        handleStyle: '',
        weavePattern: '',
        quantity: 1,
        remark: ''
      },
      editRules: {
        customerName: [{ required: true, message: '请输入客户姓名', trigger: 'blur' }],
        phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
        bambooType: [{ required: true, message: '请选择竹材类型', trigger: 'change' }],
        diameter: [
          { required: true, message: '请输入滤兜直径', trigger: 'blur' },
          { type: 'number', min: 5, max: 15, message: '直径需在 5-15cm 范围内', trigger: 'blur' }
        ],
        handleStyle: [{ required: true, message: '请选择手柄款式', trigger: 'change' }],
        weavePattern: [{ required: true, message: '请选择编织纹路', trigger: 'change' }]
      }
    };
  },
  created() {
    this.loadOrders();
  },
  methods: {
    async loadOrders() {
      this.loading = true;
      try {
        this.orders = await orderStorage.fetchOrders();
      } catch (error) {
        this.$message.error('加载订单失败');
      } finally {
        this.loading = false;
      }
    },
    getStatusType(status) {
      const types = {
        '选竹': 'info',
        '破篾': 'warning',
        '编织': 'primary',
        '定型': '',
        '浸油': 'warning',
        '晾干': 'info',
        '完工': 'success'
      };
      return types[status] || '';
    },
    getStatusIndex(status) {
      return this.statusList.indexOf(status);
    },
    isFirstStatus(status) {
      return this.getStatusIndex(status) === 0;
    },
    isLastStatus(status) {
      return this.getStatusIndex(status) === this.statusList.length - 1;
    },
    editOrder(row) {
      this.currentEditId = row.id;
      this.editForm = {
        customerName: row.customerName,
        phone: row.phone,
        bambooType: row.bambooType,
        diameter: row.diameter,
        handleStyle: row.handleStyle,
        weavePattern: row.weavePattern,
        quantity: row.quantity,
        remark: row.remark || ''
      };
      this.editDialogVisible = true;
    },
    closeEditDialog() {
      this.$refs.editForm && this.$refs.editForm.resetFields();
    },
    async saveEdit() {
      this.$refs.editForm.validate(async valid => {
        if (valid) {
          this.saving = true;
          try {
            this.orders = await orderStorage.updateOrder(this.currentEditId, this.editForm);
            this.editDialogVisible = false;
            this.$message.success('订单更新成功！');
          } catch (error) {
            this.$message.error('订单更新失败！');
          } finally {
            this.saving = false;
          }
        }
      });
    },
    async prevStatus(row) {
      const currentIndex = this.getStatusIndex(row.status);
      if (currentIndex > 0) {
        const prevStatus = this.statusList[currentIndex - 1];
        this.$confirm(`确认将订单状态从「${row.status}」回退到「${prevStatus}」吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          this.orders = await orderStorage.updateOrder(row.id, { status: prevStatus });
          this.$message.success(`状态已更新为「${prevStatus}」！`);
        }).catch(() => {});
      }
    },
    async nextStatus(row) {
      const currentIndex = this.getStatusIndex(row.status);
      if (currentIndex < this.statusList.length - 1) {
        const nextStatus = this.statusList[currentIndex + 1];
        this.$confirm(`确认将订单状态从「${row.status}」推进到「${nextStatus}」吗？`, '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          this.orders = await orderStorage.updateOrder(row.id, { status: nextStatus });
          this.$message.success(`状态已更新为「${nextStatus}」！`);
        }).catch(() => {});
      }
    }
  }
};

const routes = [
  { path: '/', component: CustomerOrder },
  { path: '/admin', component: AdminManage }
];

const router = new VueRouter({ routes });

new Vue({
  router,
  el: '#app',
  template: `
    <router-view />
  `
});
