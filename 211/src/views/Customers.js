window.Customers = {
  template: `
    <div class="customers-page">
      <h2 class="page-title">
        <i class="el-icon-user"></i>
        客户档案
      </h2>

      <el-card class="card-shadow mb-20">
        <div class="toolbar">
          <el-form :inline="true" :model="searchForm" class="search-form">
            <el-form-item label="客户姓名">
              <el-input
                v-model="searchForm.name"
                placeholder="请输入客户姓名"
                clearable />
            </el-form-item>
            <el-form-item label="手机号码">
              <el-input
                v-model="searchForm.phone"
                placeholder="请输入手机号码"
                clearable />
            </el-form-item>
            <el-form-item label="会员等级">
              <el-select
                v-model="searchForm.level"
                placeholder="全部"
                clearable>
                <el-option label="普通会员" value="普通会员" />
                <el-option label="VIP会员" value="VIP会员" />
                <el-option label="钻石会员" value="钻石会员" />
                <el-option label="企业客户" value="企业客户" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="searchCustomers">
                <i class="el-icon-search"></i> 搜索
              </el-button>
              <el-button @click="resetSearch">
                <i class="el-icon-refresh"></i> 重置
              </el-button>
            </el-form-item>
          </el-form>
          <el-button type="primary" icon="el-icon-plus" @click="addCustomer">
            新增客户
          </el-button>
        </div>
      </el-card>

      <el-card class="card-shadow">
        <el-table
          :data="filteredCustomers"
          border
          class="customers-table"
          stripe>
          <el-table-column label="客户信息" width="220">
            <template slot-scope="scope">
              <div class="customer-info">
                <div class="avatar">
                  {{ scope.row.name.charAt(0) }}
                </div>
                <div class="info">
                  <div class="name">
                    {{ scope.row.name }}
                    <el-tag size="mini" :type="getLevelType(scope.row.level)">
                      {{ scope.row.level }}
                    </el-tag>
                  </div>
                  <div class="phone">{{ scope.row.phone }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="基本信息">
            <template slot-scope="scope">
              <div>性别：{{ scope.row.gender }}</div>
              <div>年龄：{{ scope.row.age }}岁</div>
              <div>邮箱：{{ scope.row.email }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="address" label="地址" min-width="180" />
          <el-table-column label="消费统计" width="150">
            <template slot-scope="scope">
              <div>订单数：{{ scope.row.totalOrders }}单</div>
              <div class="amount">消费额：¥{{ scope.row.totalAmount }}</div>
            </template>
          </el-table-column>
          <el-table-column label="注册信息" width="180">
            <template slot-scope="scope">
              <div>注册：{{ scope.row.createTime }}</div>
              <div>最近：{{ scope.row.lastVisit }}</div>
            </template>
          </el-table-column>
          <el-table-column prop="remark" label="备注" width="150" />
          <el-table-column label="操作" width="200" fixed="right">
            <template slot-scope="scope">
              <el-button
                type="text"
                size="small"
                @click="viewCustomer(scope.row)">
                详情
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="editCustomer(scope.row)">
                编辑
              </el-button>
              <el-button
                type="text"
                size="small"
                style="color: #f56c6c"
                @click="deleteCustomer(scope.row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination">
          <el-pagination
            background
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pagination.currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="filteredCustomers.length">
          </el-pagination>
        </div>
      </el-card>

      <el-dialog
        :visible.sync="formVisible"
        :title="isEdit ? '编辑客户' : '新增客户'"
        width="600px">
        <el-form
          ref="customerForm"
          :model="customerForm"
          :rules="rules"
          label-width="100px">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="客户姓名" prop="name">
                <el-input v-model="customerForm.name" placeholder="请输入姓名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="手机号码" prop="phone">
                <el-input v-model="customerForm.phone" placeholder="请输入手机号码" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="性别" prop="gender">
                <el-radio-group v-model="customerForm.gender">
                  <el-radio label="男">男</el-radio>
                  <el-radio label="女">女</el-radio>
                </el-radio-group>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="年龄" prop="age">
                <el-input-number
                  v-model="customerForm.age"
                  :min="1"
                  :max="120"
                  style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮箱">
                <el-input v-model="customerForm.email" placeholder="请输入邮箱" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="会员等级" prop="level">
                <el-select v-model="customerForm.level" style="width: 100%">
                  <el-option label="普通会员" value="普通会员" />
                  <el-option label="VIP会员" value="VIP会员" />
                  <el-option label="钻石会员" value="钻石会员" />
                  <el-option label="企业客户" value="企业客户" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="地址">
                <el-input v-model="customerForm.address" placeholder="请输入地址" />
              </el-form-item>
            </el-col>
            <el-col :span="24">
              <el-form-item label="备注">
                <el-input
                  v-model="customerForm.remark"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入备注信息" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="formVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCustomer">保存</el-button>
        </span>
      </el-dialog>

      <el-dialog
        :visible.sync="detailVisible"
        title="客户详情"
        width="700px">
        <el-descriptions v-if="currentCustomer" :column="2" border>
          <el-descriptions-item label="客户姓名">
            {{ currentCustomer.name }}
            <el-tag size="mini" :type="getLevelType(currentCustomer.level)" style="margin-left: 10px;">
              {{ currentCustomer.level }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="手机号码">
            {{ currentCustomer.phone }}
          </el-descriptions-item>
          <el-descriptions-item label="性别">
            {{ currentCustomer.gender }}
          </el-descriptions-item>
          <el-descriptions-item label="年龄">
            {{ currentCustomer.age }}岁
          </el-descriptions-item>
          <el-descriptions-item label="邮箱">
            {{ currentCustomer.email || '未填写' }}
          </el-descriptions-item>
          <el-descriptions-item label="注册时间">
            {{ currentCustomer.createTime }}
          </el-descriptions-item>
          <el-descriptions-item label="最近到访">
            {{ currentCustomer.lastVisit }}
          </el-descriptions-item>
          <el-descriptions-item label="地址" :span="2">
            {{ currentCustomer.address || '未填写' }}
          </el-descriptions-item>
          <el-descriptions-item label="累计订单">
            {{ currentCustomer.totalOrders }}单
          </el-descriptions-item>
          <el-descriptions-item label="累计消费">
            <span class="price">¥{{ currentCustomer.totalAmount }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="备注" :span="2">
            {{ currentCustomer.remark || '无' }}
          </el-descriptions-item>
        </el-descriptions>

        <div class="customer-orders" v-if="currentCustomer">
          <h4>历史订单</h4>
          <el-table :data="customerOrders" border size="small">
            <el-table-column prop="id" label="订单号" width="160" />
            <el-table-column prop="packageName" label="套餐" />
            <el-table-column prop="shootDate" label="拍摄日期" width="120" />
            <el-table-column label="金额" width="100">
              <template slot-scope="scope">
                <span class="price">¥{{ scope.row.price }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag size="mini" :type="getStatusType(scope.row.status)">
                  {{ scope.row.status }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          <el-empty v-if="customerOrders.length === 0" description="暂无订单" />
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="detailVisible = false">关闭</el-button>
        </span>
      </el-dialog>
    </div>
  `,
  data() {
    const validatePhone = (rule, value, callback) => {
      const reg = /^1[3-9]\d{9}$/;
      if (!value) {
        callback(new Error('请输入手机号码'));
      } else if (!reg.test(value)) {
        callback(new Error('请输入正确的手机号码'));
      } else {
        callback();
      }
    };

    return {
      searchForm: {
        name: '',
        phone: '',
        level: ''
      },
      pagination: {
        currentPage: 1,
        pageSize: 10
      },
      formVisible: false,
      detailVisible: false,
      isEdit: false,
      currentCustomer: null,
      customerForm: {
        id: '',
        name: '',
        phone: '',
        gender: '男',
        age: 25,
        email: '',
        level: '普通会员',
        address: '',
        remark: ''
      },
      rules: {
        name: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        gender: [
          { required: true, message: '请选择性别', trigger: 'change' }
        ],
        age: [
          { required: true, message: '请输入年龄', trigger: 'blur' }
        ],
        level: [
          { required: true, message: '请选择会员等级', trigger: 'change' }
        ]
      }
    };
  },
  computed: {
    customers() {
      return this.$store.state.customers;
    },
    orders() {
      return this.$store.state.orders;
    },
    filteredCustomers() {
      let result = [...this.customers];
      
      if (this.searchForm.name) {
        result = result.filter(c => c.name.includes(this.searchForm.name));
      }
      
      if (this.searchForm.phone) {
        result = result.filter(c => c.phone.includes(this.searchForm.phone));
      }
      
      if (this.searchForm.level) {
        result = result.filter(c => c.level === this.searchForm.level);
      }
      
      return result;
    },
    customerOrders() {
      if (!this.currentCustomer) return [];
      return this.orders.filter(o => o.customerId === this.currentCustomer.id);
    }
  },
  methods: {
    getLevelType(level) {
      const types = {
        '普通会员': 'info',
        'VIP会员': 'warning',
        '钻石会员': 'danger',
        '企业客户': 'primary'
      };
      return types[level] || 'info';
    },
    getStatusType(status) {
      const types = {
        '待支付': 'warning',
        '已支付': 'primary',
        '拍摄中': 'success',
        '已完成': 'success',
        '已取消': 'info'
      };
      return types[status] || 'info';
    },
    searchCustomers() {
      this.pagination.currentPage = 1;
    },
    resetSearch() {
      this.searchForm = {
        name: '',
        phone: '',
        level: ''
      };
      this.pagination.currentPage = 1;
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val;
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val;
    },
    addCustomer() {
      this.isEdit = false;
      this.customerForm = {
        id: Date.now(),
        name: '',
        phone: '',
        gender: '男',
        age: 25,
        email: '',
        level: '普通会员',
        address: '',
        remark: ''
      };
      this.formVisible = true;
    },
    editCustomer(customer) {
      this.isEdit = true;
      this.customerForm = { ...customer };
      this.formVisible = true;
    },
    viewCustomer(customer) {
      this.currentCustomer = customer;
      this.detailVisible = true;
    },
    submitCustomer() {
      this.$refs.customerForm.validate(valid => {
        if (valid) {
          if (this.isEdit) {
            this.$store.dispatch('updateCustomer', { ...this.customerForm });
            this.$message.success('客户信息更新成功！');
          } else {
            const newCustomer = {
              ...this.customerForm,
              totalOrders: 0,
              totalAmount: 0,
              lastVisit: new Date().toISOString().split('T')[0],
              createTime: new Date().toISOString().split('T')[0]
            };
            this.$store.dispatch('addCustomer', newCustomer);
            this.$message.success('客户添加成功！');
          }
          this.formVisible = false;
        }
      });
    },
    deleteCustomer(customer) {
      this.$confirm('确认删除客户 "' + customer.name + '" 吗？此操作不可恢复。', '删除确认', {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'error'
      }).then(() => {
        this.$store.dispatch('deleteCustomer', customer.id);
        this.$message.success('删除成功！');
      }).catch(() => {});
    }
  }
};
