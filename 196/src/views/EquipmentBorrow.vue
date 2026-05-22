<template>
  <div class="equipment-borrow">
    <div class="page-header">
      <h2>设备借用登记</h2>
    </div>

    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="可借设备" name="equipment">
        <div class="equipment-grid">
          <el-card
            v-for="item in equipmentList"
            :key="item.id"
            class="equipment-card"
            :class="{ 'disabled': item.status !== 'available' }"
          >
            <div class="card-header">
              <div class="equipment-icon">
                <i :class="getEquipmentIcon(item.name)"></i>
              </div>
              <el-tag
                :type="equipmentStatusMap[item.status].type"
                size="small"
              >
                {{ equipmentStatusMap[item.status].label }}
              </el-tag>
            </div>
            <div class="card-body">
              <h4 class="equipment-name">{{ item.name }}</h4>
              <p class="equipment-model">型号：{{ item.model }}</p>
              <div v-if="item.status === 'borrowed'" class="borrow-info">
                <p>借用人：{{ item.borrower }}</p>
                <p>借用日期：{{ item.borrowDate }}</p>
                <p>预计归还：{{ item.expectedReturn }}</p>
              </div>
            </div>
            <div class="card-footer">
              <el-button
                type="primary"
                size="small"
                :disabled="item.status !== 'available'"
                icon="el-icon-s-order"
                @click="openBorrowForm(item)"
              >
                申请借用
              </el-button>
              <el-button
                v-if="item.status === 'borrowed'"
                type="success"
                size="small"
                icon="el-icon-check"
                @click="returnEquipment(item)"
              >
                归还
              </el-button>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="借用记录" name="records">
        <div class="filter-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索设备名称或借用人"
            clearable
            style="width: 250px; margin-right: 16px;"
          >
            <i slot="prefix" class="el-input__icon el-icon-search"></i>
          </el-input>
          <el-select
            v-model="recordStatusFilter"
            placeholder="状态筛选"
            clearable
            style="width: 150px;"
          >
            <el-option label="借用中" value="borrowing"></el-option>
            <el-option label="已归还" value="returned"></el-option>
          </el-select>
        </div>
        <el-table
          :data="filteredRecords"
          border
          stripe
          style="width: 100%;"
        >
          <el-table-column
            prop="equipmentName"
            label="设备名称"
            min-width="150"
          ></el-table-column>
          <el-table-column
            prop="model"
            label="型号"
            min-width="150"
          ></el-table-column>
          <el-table-column
            prop="borrower"
            label="借用人"
            width="100"
          ></el-table-column>
          <el-table-column
            prop="borrowDate"
            label="借用日期"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="expectedReturn"
            label="预计归还"
            width="120"
          ></el-table-column>
          <el-table-column
            prop="actualReturn"
            label="实际归还"
            width="120"
          >
            <template slot-scope="scope">
              <span v-if="scope.row.actualReturn">{{ scope.row.actualReturn }}</span>
              <span v-else class="text-muted">-</span>
            </template>
          </el-table-column>
          <el-table-column
            label="状态"
            width="100"
            align="center"
          >
            <template slot-scope="scope">
              <el-tag
                :type="scope.row.status === 'borrowing' ? 'warning' : 'success'"
                size="small"
              >
                {{ scope.row.status === 'borrowing' ? '借用中' : '已归还' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </el-tab-pane>
    </el-tabs>

    <el-dialog
      title="设备借用申请"
      :visible.sync="borrowFormVisible"
      width="500px"
      @close="resetBorrowForm"
    >
      <el-form
        ref="borrowForm"
        :model="borrowForm"
        :rules="borrowRules"
        label-width="100px"
      >
        <el-form-item label="设备名称">
          <span>{{ selectedEquipment ? selectedEquipment.name : '' }}</span>
        </el-form-item>
        <el-form-item label="设备型号">
          <span>{{ selectedEquipment ? selectedEquipment.model : '' }}</span>
        </el-form-item>
        <el-form-item label="借用人" prop="borrower">
          <el-select
            v-model="borrowForm.borrower"
            placeholder="请选择借用人"
            style="width: 100%;"
            filterable
          >
            <el-option
              v-for="emp in employees"
              :key="emp.id"
              :label="emp.name"
              :value="emp.name"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="借用日期" prop="borrowDate">
          <el-date-picker
            v-model="borrowForm.borrowDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
            :picker-options="borrowDatePickerOptions"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="预计归还" prop="expectedReturn">
          <el-date-picker
            v-model="borrowForm.expectedReturn"
            type="date"
            placeholder="选择日期"
            style="width: 100%;"
            :picker-options="returnDatePickerOptions"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="借用原因">
          <el-input
            v-model="borrowForm.reason"
            type="textarea"
            :rows="3"
            placeholder="请输入借用原因（可选）"
            maxlength="200"
            show-word-limit
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="borrowFormVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBorrow" :loading="submitting">提交申请</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { equipment, equipmentStatusMap, borrowRecords } from '@/mock/equipment'
import { employees } from '@/mock/employees'

export default {
  name: 'EquipmentBorrow',
  data() {
    const validateReturnDate = (rule, value, callback) => {
      if (this.borrowForm.borrowDate && value) {
        if (value < this.borrowForm.borrowDate) {
          callback(new Error('归还日期不能早于借用日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }

    return {
      activeTab: 'equipment',
      submitting: false,
      searchKeyword: '',
      recordStatusFilter: '',
      equipmentList: equipment,
      equipmentStatusMap,
      borrowRecords,
      employees,
      selectedEquipment: null,
      borrowFormVisible: false,
      borrowForm: {
        borrower: '',
        borrowDate: '',
        expectedReturn: '',
        reason: ''
      },
      borrowRules: {
        borrower: [
          { required: true, message: '请选择借用人', trigger: 'change' }
        ],
        borrowDate: [
          { required: true, message: '请选择借用日期', trigger: 'change' }
        ],
        expectedReturn: [
          { required: true, message: '请选择预计归还日期', trigger: 'change' },
          { validator: validateReturnDate, trigger: 'change' }
        ]
      },
      borrowDatePickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      }
    }
  },
  computed: {
    returnDatePickerOptions() {
      const minDate = this.borrowForm.borrowDate
      return {
        disabledDate(time) {
          return time.getTime() < (minDate ? new Date(minDate).getTime() : Date.now() - 8.64e7)
        }
      }
    },
    filteredRecords() {
      return this.borrowRecords.filter(record => {
        const matchKeyword = !this.searchKeyword ||
          record.equipmentName.includes(this.searchKeyword) ||
          record.borrower.includes(this.searchKeyword)
        const matchStatus = !this.recordStatusFilter || record.status === this.recordStatusFilter
        return matchKeyword && matchStatus
      })
    }
  },
  methods: {
    handleTabClick() {},
    getEquipmentIcon(name) {
      if (name.includes('投影')) return 'el-icon-video-camera'
      if (name.includes('麦克风')) return 'el-icon-microphone'
      if (name.includes('电脑') || name.includes('笔记本')) return 'el-icon-cpu'
      if (name.includes('白板')) return 'el-icon-edit-outline'
      if (name.includes('摄像头')) return 'el-icon-video-camera-solid'
      if (name.includes('音响')) return 'el-icon-bell'
      if (name.includes('翻页笔')) return 'el-icon-pointer'
      return 'el-icon-monitor'
    },
    openBorrowForm(item) {
      this.selectedEquipment = item
      this.borrowFormVisible = true
    },
    resetBorrowForm() {
      this.$refs.borrowForm && this.$refs.borrowForm.resetFields()
      this.selectedEquipment = null
    },
    submitBorrow() {
      this.$refs.borrowForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.selectedEquipment.status = 'borrowed'
            this.selectedEquipment.borrower = this.borrowForm.borrower
            this.selectedEquipment.borrowDate = this.borrowForm.borrowDate
            this.selectedEquipment.expectedReturn = this.borrowForm.expectedReturn

            this.borrowRecords.unshift({
              id: Date.now(),
              equipmentName: this.selectedEquipment.name,
              model: this.selectedEquipment.model,
              borrower: this.borrowForm.borrower,
              borrowDate: this.borrowForm.borrowDate,
              expectedReturn: this.borrowForm.expectedReturn,
              actualReturn: '',
              status: 'borrowing'
            })

            this.submitting = false
            this.borrowFormVisible = false
            this.$message.success('借用申请提交成功！')
          }, 800)
        } else {
          return false
        }
      })
    },
    returnEquipment(item) {
      this.$confirm('确定要归还此设备吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const today = this.formatDate(new Date())
        item.status = 'available'
        item.borrower = ''
        item.borrowDate = ''
        item.expectedReturn = ''

        const record = this.borrowRecords.find(r =>
          r.equipmentName === item.name && r.status === 'borrowing'
        )
        if (record) {
          record.status = 'returned'
          record.actualReturn = today
        }

        this.$message.success('设备归还成功！')
      }).catch(() => {})
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    }
  }
}
</script>

<style lang="scss" scoped>
.equipment-borrow {
  padding: 20px;

  .page-header {
    margin-bottom: 20px;

    h2 {
      margin: 0;
      color: #303133;
    }
  }

  .filter-bar {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
  }

  .equipment-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
  }

  .equipment-card {
    transition: all 0.3s;

    &:hover:not(.disabled) {
      transform: translateY(-4px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    }

    &.disabled {
      opacity: 0.7;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;

      .equipment-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 24px;
      }
    }

    .card-body {
      .equipment-name {
        margin: 0 0 8px 0;
        color: #303133;
        font-size: 16px;
      }

      .equipment-model {
        margin: 0 0 12px 0;
        color: #909399;
        font-size: 14px;
      }

      .borrow-info {
        padding: 12px;
        background: #f5f7fa;
        border-radius: 4px;
        font-size: 13px;
        color: #606266;

        p {
          margin: 4px 0;
        }
      }
    }

    .card-footer {
      margin-top: 16px;
      display: flex;
      gap: 8px;
    }
  }

  .text-muted {
    color: #c0c4cc;
  }
}
</style>
