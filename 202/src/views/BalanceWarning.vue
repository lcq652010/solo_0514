<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">余额预警</div>
      <div class="page-subtitle">实时监控宿舍水电余额，及时处理低余额预警</div>
    </div>

    <el-row :gutter="20" class="mb-20">
      <el-col :span="6">
        <div class="stat-card warning-card">
          <div class="icon-wrapper danger">
            <i class="el-icon-warning"></i>
          </div>
          <div class="info">
            <div class="label">紧急预警</div>
            <div class="value text-danger">{{ dangerCount }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card warning-card">
          <div class="icon-wrapper warning">
            <i class="el-icon-bell"></i>
          </div>
          <div class="info">
            <div class="label">一般预警</div>
            <div class="value text-warning">{{ warningCount }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card warning-card">
          <div class="icon-wrapper primary">
            <i class="el-icon-water-cup"></i>
          </div>
          <div class="info">
            <div class="label">水费预警</div>
            <div class="value text-primary">{{ waterWarningCount }}</div>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card warning-card">
          <div class="icon-wrapper success">
            <i class="el-icon-lightning"></i>
          </div>
          <div class="info">
            <div class="label">电费预警</div>
            <div class="value text-warning">{{ electricityWarningCount }}</div>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-alert
      title="预警说明"
      type="info"
      :closable="false"
      class="mb-20"
    >
      <template slot="default">
        <p>• 水费余额低于 30 元 触发预警提醒</p>
        <p>• 电费余额低于 50 元 触发预警提醒</p>
        <p>• 余额低于阈值的 50% 标记为紧急预警，需尽快充值</p>
      </template>
    </el-alert>

    <el-card>
      <div slot="header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>预警列表</span>
          <el-radio-group v-model="filterLevel" size="mini" @change="handleFilter">
            <el-radio-button label="all">全部</el-radio-button>
            <el-radio-button label="danger">紧急</el-radio-button>
            <el-radio-button label="warning">一般</el-radio-button>
          </el-radio-group>
        </div>
      </div>

      <el-table
        :data="filteredWarnings"
        border
        stripe
        style="width: 100%;"
        :row-class-name="tableRowClassName"
      >
        <el-table-column
          label="预警级别"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.level === 'danger' ? 'danger' : 'warning'"
              effect="dark"
              size="medium"
            >
              <i :class="scope.row.level === 'danger' ? 'el-icon-warning' : 'el-icon-bell'" style="margin-right: 3px;"></i>
              {{ scope.row.level === 'danger' ? '紧急' : '一般' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="dormitory"
          label="宿舍"
          width="120"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="type"
          label="类型"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.type === 'water'" class="text-primary">
              <i class="el-icon-water-cup"></i> 水费
            </span>
            <span v-else class="text-warning">
              <i class="el-icon-lightning"></i> 电费
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="balance"
          label="当前余额"
          width="150"
          align="right"
        >
          <template slot-scope="scope">
            <span class="text-danger" style="font-size: 18px; font-weight: 600;">
              {{ scope.row.balance.toFixed(2) }} 元
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="threshold"
          label="预警阈值"
          width="120"
          align="right"
        >
          <template slot-scope="scope">
            <span>{{ scope.row.threshold }} 元</span>
          </template>
        </el-table-column>
        <el-table-column
          label="差额"
          width="120"
          align="right"
        >
          <template slot-scope="scope">
            <span class="text-danger">
              -{{ (scope.row.threshold - scope.row.balance).toFixed(2) }} 元
            </span>
          </template>
        </el-table-column>
        <el-table-column
          label="建议充值"
          width="150"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag type="info" size="small">
              {{ getSuggestAmount(scope.row) }} 元
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="180"
          align="center"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="mini"
              @click="goRecharge(scope.row)"
            >
              <i class="el-icon-credit-pay"></i> 立即充值
            </el-button>
            <el-button
              type="text"
              size="mini"
              @click="ignoreWarning(scope.row)"
            >忽略</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="filteredWarnings.length === 0" class="empty-tip">
        <el-empty description="暂无预警信息，所有宿舍余额正常">
          <el-button type="primary">查看全部宿舍</el-button>
        </el-empty>
      </div>
    </el-card>

    <el-dialog
      title="快速充值"
      :visible.sync="rechargeDialogVisible"
      width="450px"
      @close="handleDialogClose"
    >
      <el-form :model="rechargeForm" :rules="rechargeRules" ref="rechargeForm" label-width="80px">
        <el-form-item label="宿舍">
          <el-input v-model="rechargeForm.dormitory" disabled></el-input>
        </el-form-item>
        <el-form-item label="类型">
          <el-input v-model="rechargeForm.typeName" disabled></el-input>
        </el-form-item>
        <el-form-item label="充值金额" prop="amount">
          <el-input-number
            v-model="rechargeForm.amount"
            :min="1"
            :max="maxAmount"
            :step="1"
            :precision="0"
            style="width: 100%;"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="支付方式" prop="payMethod">
          <el-radio-group v-model="rechargeForm.payMethod">
            <el-radio label="微信支付">微信</el-radio>
            <el-radio label="支付宝">支付宝</el-radio>
            <el-radio label="校园卡">校园卡</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="rechargeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmQuickRecharge" :loading="recharging">确认充值</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getWarningList, recharge, checkDuplicateRecharge } from '@/utils/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'BalanceWarning',
  data() {
    const maxAmount = 1000
    const validatePositiveInteger = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入充值金额'))
      } else if (!Number.isInteger(value) || value <= 0) {
        callback(new Error('充值金额必须为正整数'))
      } else if (value > maxAmount) {
        callback(new Error(`单笔充值金额不能超过${maxAmount}元`))
      } else {
        callback()
      }
    }
    return {
      maxAmount,
      warnings: [],
      filterLevel: 'all',
      rechargeDialogVisible: false,
      recharging: false,
      rechargeForm: {
        dormitory: '',
        type: '',
        typeName: '',
        amount: 50,
        payMethod: '微信支付'
      },
      rechargeRules: {
        amount: [
          { required: true, validator: validatePositiveInteger, trigger: 'blur' }
        ],
        payMethod: [
          { required: true, message: '请选择支付方式', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    filteredWarnings() {
      if (this.filterLevel === 'all') return this.warnings
      return this.warnings.filter(w => w.level === this.filterLevel)
    },
    dangerCount() {
      return this.warnings.filter(w => w.level === 'danger').length
    },
    warningCount() {
      return this.warnings.filter(w => w.level === 'warning').length
    },
    waterWarningCount() {
      return this.warnings.filter(w => w.type === 'water').length
    },
    electricityWarningCount() {
      return this.warnings.filter(w => w.type === 'electricity').length
    }
  },
  created() {
    this.loadWarnings()
    EventBus.$on('recharge-success', () => {
      this.loadWarnings()
    })
  },
  beforeDestroy() {
    EventBus.$off('recharge-success')
  },
  activated() {
    this.loadWarnings()
  },
  methods: {
    loadWarnings() {
      this.warnings = getWarningList()
    },
    handleFilter() {
    },
    tableRowClassName({ row }) {
      return row.level === 'danger' ? 'danger-row' : 'warning-row'
    },
    getSuggestAmount(row) {
      const deficit = row.threshold - row.balance
      return Math.ceil((deficit + 20) / 10) * 10
    },
    goRecharge(row) {
      this.rechargeForm = {
        dormitory: row.dormitory,
        type: row.type,
        typeName: row.type === 'water' ? '水费' : '电费',
        amount: this.getSuggestAmount(row),
        payMethod: '微信支付'
      }
      this.rechargeDialogVisible = true
    },
    ignoreWarning(row) {
      this.$confirm(`确定忽略 ${row.dormitory} 的${row.type === 'water' ? '水费' : '电费'}余额预警吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.warnings.findIndex(w => w.dormitory === row.dormitory && w.type === row.type)
        if (index > -1) {
          this.warnings.splice(index, 1)
        }
        this.$message.success('已忽略该预警')
      }).catch(() => {})
    },
    confirmQuickRecharge() {
      this.$refs.rechargeForm.validate((valid) => {
        if (valid) {
          const isDuplicate = checkDuplicateRecharge(
            this.rechargeForm.dormitory,
            this.rechargeForm.type,
            this.rechargeForm.amount
          )
          if (isDuplicate) {
            this.$confirm(
              '检测到该宿舍在5分钟内有相同金额的充值记录，是否确认继续充值？',
              '重复充值提醒',
              {
                confirmButtonText: '继续充值',
                cancelButtonText: '取消',
                type: 'warning'
              }
            ).then(() => {
              this.doQuickRecharge()
            }).catch(() => {})
            return
          }
          this.doQuickRecharge()
        }
      })
    },
    doQuickRecharge() {
      this.recharging = true
      setTimeout(() => {
        recharge(
          this.rechargeForm.dormitory,
          this.rechargeForm.type,
          this.rechargeForm.amount,
          this.rechargeForm.payMethod
        )
        this.recharging = false
        this.rechargeDialogVisible = false
        this.$message.success('充值成功！')
        EventBus.$emit('recharge-success', {
          dormitory: this.rechargeForm.dormitory,
          type: this.rechargeForm.type,
          amount: this.rechargeForm.amount
        })
        this.loadWarnings()
      }, 1000)
    },
    handleDialogClose() {
      this.$refs.rechargeForm.resetFields()
    }
  }
}
</script>

<style scoped>
.warning-card {
  display: flex;
  align-items: center;
  padding: 20px;
}

.warning-card .icon-wrapper {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  margin-right: 15px;
}

.warning-card .icon-wrapper.danger {
  background: #fef0f0;
  color: #F56C6C;
}

.warning-card .icon-wrapper.warning {
  background: #fdf6ec;
  color: #E6A23C;
}

.warning-card .icon-wrapper.primary {
  background: #ecf5ff;
  color: #409EFF;
}

.warning-card .icon-wrapper.success {
  background: #f0f9eb;
  color: #67C23A;
}

.warning-card .info .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 5px;
}

.warning-card .info .value {
  font-size: 28px;
  font-weight: 600;
}

.danger-row {
  background: #fef0f0 !important;
}

.warning-row {
  background: #fdf6ec !important;
}

.empty-tip {
  padding: 40px 0;
}

::v-deep .el-table .danger-row:hover > td {
  background-color: #fde2e2 !important;
}

::v-deep .el-table .warning-row:hover > td {
  background-color: #faecd8 !important;
}
</style>
