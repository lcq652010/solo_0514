<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">
        <i class="el-icon-refresh-left" style="margin-right: 10px; color: #409eff;"></i>
        归还登记
      </h2>
    </div>

    <el-card class="form-card">
      <el-form
        ref="returnForm"
        :model="returnForm"
        :rules="rules"
        label-width="120px"
        class="form-container"
      >
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="选择领用记录" prop="recordId">
              <el-select
                v-model="returnForm.recordId"
                placeholder="请选择要归还的领用记录"
                style="width: 100%"
                filterable
                @change="handleRecordChange"
              >
                <el-option
                  v-for="item in approvedRecords"
                  :key="item.id"
                  :label="item.materialName + ' - ' + item.applicant + ' (' + item.applyDate + ')'"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider v-if="selectedRecord" content-position="left">领用信息</el-divider>

        <el-row v-if="selectedRecord" :gutter="20">
          <el-col :span="12">
            <el-form-item label="物资名称">
              <el-input :value="selectedRecord.materialName" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="规格型号">
              <el-input :value="selectedRecord.specification" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row v-if="selectedRecord" :gutter="20">
          <el-col :span="12">
            <el-form-item label="申请人">
              <el-input :value="selectedRecord.applicant" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属部门">
              <el-input :value="selectedRecord.department" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row v-if="selectedRecord" :gutter="20">
          <el-col :span="12">
            <el-form-item label="领用数量">
              <el-input :value="selectedRecord.applyQuantity" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="领用日期">
              <el-input :value="selectedRecord.applyDate" disabled></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row v-if="selectedRecord" :gutter="20">
          <el-col :span="12">
            <el-form-item label="预计归还日期">
              <el-input :value="selectedRecord.expectReturnDate" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态">
              <el-tag type="success">已批准</el-tag>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider v-if="selectedRecord" content-position="left">归还信息</el-divider>

        <el-row v-if="selectedRecord" :gutter="20">
          <el-col :span="12">
            <el-form-item label="实际归还日期" prop="actualReturnDate">
              <el-date-picker
                v-model="returnForm.actualReturnDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="归还数量" prop="returnQuantity">
              <el-input-number
                v-model="returnForm.returnQuantity"
                :min="1"
                :max="selectedRecord.applyQuantity"
                style="width: 100%"
              ></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item v-if="selectedRecord" label="物资状态" prop="condition">
          <el-radio-group v-model="returnForm.condition">
            <el-radio label="good">完好无损</el-radio>
            <el-radio label="minor">轻微磨损</el-radio>
            <el-radio label="damaged">损坏</el-radio>
            <el-radio label="lost">丢失</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="selectedRecord" label="备注说明" prop="remarks">
          <el-input
            v-model="returnForm.remarks"
            type="textarea"
            :rows="3"
            placeholder="请输入归还备注，如物资损坏情况等"
          ></el-input>
        </el-form-item>

        <el-form-item v-if="selectedRecord">
          <el-button type="success" size="large" @click="submitReturn" :loading="submitting">
            <i class="el-icon-check"></i>
            确认归还
          </el-button>
          <el-button size="large" @click="resetForm">
            <i class="el-icon-refresh-left"></i>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-empty v-if="approvedRecords.length === 0" description="暂无待归还的领用记录">
      <el-button type="primary" @click="$router.push('/apply')">去领用物资</el-button>
    </el-empty>
  </div>
</template>

<script>
import { applyRecords } from '@/mock/data.js'

export default {
  name: 'ReturnForm',
  data() {
    return {
      recordsList: applyRecords,
      returnForm: {
        recordId: '',
        actualReturnDate: '',
        returnQuantity: 1,
        condition: 'good',
        remarks: ''
      },
      rules: {
        recordId: [
          { required: true, message: '请选择领用记录', trigger: 'change' }
        ],
        actualReturnDate: [
          { required: true, message: '请选择实际归还日期', trigger: 'change' }
        ],
        returnQuantity: [
          { required: true, message: '请输入归还数量', trigger: 'blur' },
          { type: 'number', message: '请输入数字', trigger: 'blur' }
        ],
        condition: [
          { required: true, message: '请选择物资状态', trigger: 'change' }
        ]
      },
      submitting: false
    }
  },
  computed: {
    approvedRecords() {
      return this.recordsList.filter(item => item.status === 'approved')
    },
    selectedRecord() {
      if (!this.returnForm.recordId) return null
      return this.recordsList.find(item => item.id === this.returnForm.recordId)
    }
  },
  mounted() {
    const today = new Date().toISOString().split('T')[0]
    this.returnForm.actualReturnDate = today
  },
  methods: {
    handleRecordChange() {
      if (this.selectedRecord) {
        this.returnForm.returnQuantity = this.selectedRecord.applyQuantity
      }
    },
    submitReturn() {
      this.$refs.returnForm.validate((valid) => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            this.submitting = false
            
            if (this.returnForm.condition === 'damaged' || this.returnForm.condition === 'lost') {
              this.$message.warning({
                message: '物资有损坏或丢失，请按规定进行赔偿处理',
                duration: 3000
              })
            } else {
              this.$message.success('归还登记成功！')
            }
            
            console.log('归还数据：', this.returnForm)
          }, 1000)
        } else {
          this.$message.error('请完善归还信息！')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.returnForm.resetFields()
      const today = new Date().toISOString().split('T')[0]
      this.returnForm.actualReturnDate = today
      this.returnForm.condition = 'good'
    }
  }
}
</script>

<style lang="scss" scoped>
.form-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #303133;
}

:deep(.el-input__inner) {
  border-radius: 4px;
}

:deep(.el-button) {
  border-radius: 4px;
}

.el-empty {
  padding: 40px 0;
}
</style>
