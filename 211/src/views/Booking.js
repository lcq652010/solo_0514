window.Booking = {
  template: `
    <div class="booking-page">
      <h2 class="page-title">
        <i class="el-icon-edit-outline"></i>
        在线预订
      </h2>

      <el-row :gutter="24">
        <el-col :md="16">
          <el-card class="card-shadow">
            <el-form
              ref="bookingForm"
              :model="form"
              :rules="rules"
              label-width="120px"
              class="booking-form">
              <el-form-item label="选择套餐" prop="packageId">
                <el-select
                  v-model="form.packageId"
                  placeholder="请选择摄影套餐"
                  style="width: 100%"
                  @change="onPackageChange">
                  <el-option
                    v-for="pkg in packages"
                    :key="pkg.id"
                    :label="pkg.name"
                    :value="pkg.id">
                    <span>{{ pkg.name }}</span>
                    <span style="float: right; color: #e94560;">¥{{ pkg.price }}</span>
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="客户姓名" prop="customerName">
                <el-input
                  v-model="form.customerName"
                  placeholder="请输入您的姓名" />
              </el-form-item>

              <el-form-item label="联系电话" prop="phone">
                <el-input
                  v-model="form.phone"
                  placeholder="请输入手机号码" />
              </el-form-item>

              <el-form-item label="拍摄日期" prop="shootDate">
                <el-date-picker
                  v-model="form.shootDate"
                  type="date"
                  :picker-options="pickerOptions"
                  placeholder="选择拍摄日期"
                  style="width: 100%" />
              </el-form-item>

              <el-form-item label="拍摄时段" prop="shootTime">
                <el-select
                  v-model="form.shootTime"
                  placeholder="请选择拍摄时段"
                  style="width: 100%">
                  <el-option label="上午 08:00-12:00" value="08:00-12:00" />
                  <el-option label="下午 13:00-17:00" value="13:00-17:00" />
                  <el-option label="全天 08:00-18:00" value="08:00-18:00" />
                  <el-option label="夜景 18:00-21:00" value="18:00-21:00" />
                </el-select>
              </el-form-item>

              <el-form-item label="拍摄地点" prop="location">
                <el-radio-group v-model="form.location">
                  <el-radio label="室内棚拍">室内棚拍</el-radio>
                  <el-radio label="室外公园">室外公园</el-radio>
                  <el-radio label="海边">海边</el-radio>
                  <el-radio label="城市街景">城市街景</el-radio>
                  <el-radio label="上门拍摄">上门拍摄</el-radio>
                </el-radio-group>
              </el-form-item>

              <el-form-item label="选择摄影师" prop="photographerId">
                <el-select
                  v-model="form.photographerId"
                  placeholder="请选择摄影师"
                  style="width: 100%">
                  <el-option
                    v-for="p in photographers"
                    :key="p.id"
                    :label="p.name"
                    :value="p.id">
                    <span>{{ p.name }} - {{ p.level }}</span>
                  </el-option>
                </el-select>
              </el-form-item>

              <el-form-item label="备注信息">
                <el-input
                  v-model="form.remark"
                  type="textarea"
                  :rows="4"
                  placeholder="请填写您的特殊需求或拍摄风格偏好等" />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" size="large" @click="submitForm" :loading="submitting">
                  提交预订
                </el-button>
                <el-button size="large" @click="resetForm">重置</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :md="8">
          <el-card class="card-shadow order-summary">
            <h3 class="summary-title">
              <i class="el-icon-tickets"></i>
              订单摘要
            </h3>
            <div class="summary-content" v-if="selectedPackage">
              <img :src="selectedPackage.image" class="package-img" />
              <h4 class="package-name">{{ selectedPackage.name }}</h4>
              <div class="package-price">
                <span class="price">¥{{ selectedPackage.price }}</span>
                <span class="original" v-if="selectedPackage.originalPrice > selectedPackage.price">
                  ¥{{ selectedPackage.originalPrice }}
                </span>
              </div>
              <div class="package-detail">
                <p><i class="el-icon-time"></i> 拍摄时长：{{ selectedPackage.duration }}</p>
                <p><i class="el-icon-picture"></i> 拍摄张数：{{ selectedPackage.photos }}张</p>
                <p><i class="el-icon-magic-stick"></i> 精修张数：{{ selectedPackage.retouched }}张</p>
              </div>
              <div class="divider"></div>
              <div class="total-row">
                <span>预订日期</span>
                <span>{{ form.shootDate || '请选择' }}</span>
              </div>
              <div class="total-row">
                <span>拍摄时段</span>
                <span>{{ form.shootTime || '请选择' }}</span>
              </div>
              <div class="divider"></div>
              <div class="total-row total-price">
                <span>订单总价</span>
                <span class="price">¥{{ selectedPackage.price }}</span>
              </div>
            </div>
            <el-empty v-else description="请先选择套餐" />
          </el-card>

          <el-card class="card-shadow tips">
            <h3 class="tips-title">
              <i class="el-icon-info"></i>
              预订须知
            </h3>
            <ul>
              <li>请提前3天预约，方便我们为您安排摄影师</li>
              <li>预订成功后请在24小时内支付定金</li>
              <li>如需改期，请提前24小时联系客服</li>
              <li>拍摄前一天请注意休息，保持良好状态</li>
              <li>我们提供免费服装和化妆服务</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
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
      submitting: false,
      form: {
        packageId: '',
        customerName: '',
        phone: '',
        shootDate: '',
        shootTime: '',
        location: '室内棚拍',
        photographerId: '',
        remark: ''
      },
      rules: {
        packageId: [
          { required: true, message: '请选择套餐', trigger: 'change' }
        ],
        customerName: [
          { required: true, message: '请输入客户姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '姓名长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        shootDate: [
          { required: true, message: '请选择拍摄日期', trigger: 'change' }
        ],
        shootTime: [
          { required: true, message: '请选择拍摄时段', trigger: 'change' }
        ],
        photographerId: [
          { required: true, message: '请选择摄影师', trigger: 'change' }
        ]
      },
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7;
        }
      }
    };
  },
  computed: {
    packages() {
      return this.$store.state.packages;
    },
    photographers() {
      return this.$store.state.photographers;
    },
    selectedPackage() {
      if (!this.form.packageId) {
        return null;
      }
      return this.packages.find(p => p.id === this.form.packageId);
    }
  },
  mounted() {
    const packageId = this.$route.query.packageId;
    if (packageId) {
      this.form.packageId = parseInt(packageId);
    }
  },
  methods: {
    onPackageChange() {
    },
    checkScheduleConflict() {
      const shootDate = moment(this.form.shootDate).format('YYYY-MM-DD');
      const orders = this.$store.state.orders;
      const conflictOrder = orders.find(o => 
        o.photographerId === this.form.photographerId &&
        o.shootDate === shootDate &&
        o.status !== '已取消' &&
        this.isTimeOverlap(o.shootTime, this.form.shootTime)
      );
      return conflictOrder;
    },
    isTimeOverlap(time1, time2) {
      if (time1 === '全天' || time2 === '全天') return true;
      if (time1 === '定制' || time2 === '定制') return true;
      const getMinutes = (timeStr) => {
        const [hours, minutes] = timeStr.split(':').map(Number);
        return hours * 60 + minutes;
      };
      const [start1, end1] = time1.split('-').map(getMinutes);
      const [start2, end2] = time2.split('-').map(getMinutes);
      return !(end1 <= start2 || end2 <= start1);
    },
    checkPriceValid() {
      return this.selectedPackage && this.selectedPackage.price > 0;
    },
    submitForm() {
      this.$refs.bookingForm.validate(valid => {
        if (valid) {
          if (!this.checkPriceValid()) {
            this.$message.error('套餐金额必须为正数，无法提交订单');
            return;
          }
          const conflictOrder = this.checkScheduleConflict();
          if (conflictOrder) {
            this.$message.error(`档期冲突！该摄影师在 ${conflictOrder.shootDate} ${conflictOrder.shootTime} 已有预订（订单号：${conflictOrder.id}）`);
            return;
          }
          this.submitting = true;
          setTimeout(() => {
            const photographer = this.photographers.find(p => p.id === this.form.photographerId);
            const order = {
              id: 'ORD' + new Date().getTime(),
              packageId: this.form.packageId,
              packageName: this.selectedPackage.name,
              customerName: this.form.customerName,
              photographerId: this.form.photographerId,
              photographerName: photographer ? photographer.name : '',
              price: this.selectedPackage.price,
              status: '待支付',
              bookingDate: new Date().toISOString().split('T')[0],
              shootDate: moment(this.form.shootDate).format('YYYY-MM-DD'),
              shootTime: this.form.shootTime,
              location: this.form.location,
              createTime: new Date().toLocaleString(),
              remark: this.form.remark
            };
            this.$store.dispatch('addOrder', order);
            this.submitting = false;
            this.$message.success('预订成功！我们将尽快与您联系确认订单详情');
            this.$router.push('/orders');
          }, 1000);
        }
      });
    },
    resetForm() {
      this.$refs.bookingForm.resetFields();
      this.form.location = '室内棚拍';
    }
  }
};
