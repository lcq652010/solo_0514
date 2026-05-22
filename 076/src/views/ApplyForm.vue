<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">
        <i class="el-icon-edit-outline" style="margin-right: 10px; color: #409eff;"></i>
        领用申请
      </h2>
    </div>

    <el-card class="form-card">
      <el-form
        ref="applyForm"
        :model="applyForm"
        :rules="rules"
        label-width="120px"
        class="form-container"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="物资名称" prop="materialId">
              <el-select
                v-model="applyForm.materialId"
                placeholder="请选择物资"
                style="width: 100%"
                filterable
                @change="handleMaterialChange"
              >
                <el-option
                  v-for="item in availableMaterials"
                  :key="item.id"
                  :label="item.name + ' (' + item.specification + ')'"
                  :value="item.id"
                ></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="领用数量" prop="quantity">
              <el-input-number
                v-model="applyForm.quantity"
                :min="1"
                :max="maxQuantity"
                style="width: 100%"
              ></el-input-number>
              <span v-if="selectedMaterial" style="margin-left: 10px; color: #909399; font-size: 12px;">
                可用：{{ selectedMaterial.available }} {{ selectedMaterial.unit }}
              </span>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="申请人" prop="applicant">
              <el-input v-model="applyForm.applicant" placeholder="请输入申请人姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="所属部门" prop="department">
              <el-select v-model="applyForm.department" placeholder="请选择部门" style="width: 100%">
                <el-option label="研发部" value="研发部"></el-option>
                <el-option label="市场部" value="市场部"></el-option>
                <el-option label="销售部" value="销售部"></el-option>
                <el-option label="人事部" value="人事部"></el-option>
                <el-option label="财务部" value="财务部"></el-option>
                <el-option label="行政部" value="行政部"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="申请日期" prop="applyDate">
              <el-date-picker
                v-model="applyForm.applyDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
              ></el-date-picker>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="预计归还日期" prop="expectReturnDate">
              <el-date-picker
                v-model="applyForm.expectReturnDate"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd"
                :picker-options="pickerOptions"
              ></el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="领用用途" prop="purpose">
          <el-input
            v-model="applyForm.purpose"
            type="textarea"
            :rows="4"
            placeholder="请详细说明领用用途"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitForm" :loading="submitting">
            <i class="el-icon-check"></i>
            提交申请
          </el-button>
          <el-button size="large" @click="resetForm">
            <i class="el-icon-refresh-left"></i>
            重置表单
          </el-button>
          <el-button size="large" @click="goToList">
            <i class="el-icon-document"></i>
            查看记录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-divider content-position="left">领用须知</el-divider>
    <el-alert
      title="注意事项"
      type="info"
      :closable="false"
      show-icon
    >
      <ul style="margin: 10px 0; padding-left: 20px;">
        <li style="margin: 5px 0;">请提前1-2个工作日提交领用申请，以便安排物资准备</li>
        <li style="margin: 5px 0;">贵重物品需部门负责人审批后方可领用</li>
        <li style="margin: 5px 0;">请在预计归还日期前归还物资，如需续借请提前申请</li>
        <li style="margin: 5px 0;">归还时请确保物资完好无损，如有损坏需照价赔偿</li>
      </ul>
    </el-alert>
  </div>
</template>

<script>
import { materials } from '@/mock/data.js'

export default {
  name: 'ApplyForm',
  data() {
    return {
      materialsList: materials,
      applyForm: {
        materialId: '',
        quantity: 1,
        applicant: '',
        department: '',
        applyDate: '',
        expectReturnDate: '',
        purpose: ''
      },
      rules: {
        materialId: [
          { required: true, message: '请选择物资', trigger: 'change' }
        ],
        quantity: [
          { required: true, message: '请输入领用数量', trigger: 'blur' },
          { type: 'number', message: '请输入数字', trigger: 'blur' },
          { validator: this.checkStock, trigger: 'blur' }
        ],
        applicant: [
          { required: true, message: '请输入申请人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        department: [
          { required: true, message: '请选择所属部门', trigger: 'change' }
        ],
        applyDate: [
          { required: true, message: '请选择申请日期', trigger: 'change' }
        ],
        expectReturnDate: [
          { required: true, message: '请选择预计归还日期', trigger: 'change' }
        ],
        purpose: [
          { required: true, message: '请输入领用用途', trigger: 'blur' },
          { min: 5, message: '请至少输入5个字符', trigger: 'blur' }
        ]
      },
      submitting: false,
      pickerOptions: {
        disabledDate(time) {
          return time.getTime() < Date.now() - 8.64e7
        }
      }
    }
  },
  computed: {
    availableMaterials() {
      return this.materialsList.filter(item => item.available > 0)
    },
    selectedMaterial() {
      if (!this.applyForm.materialId) return null
      return this.materialsList.find(item => item.id === this.applyForm.materialId)
    },
    maxQuantity() {
      if (!this.selectedMaterial) return 999
      return this.selectedMaterial.available
    }
  },
  mounted() {
    const materialId = this.$route.query.materialId
    if (materialId) {
      this.applyForm.materialId = parseInt(materialId)
    }
    const today = new Date().toISOString().split('T')[0]
    this.applyForm.applyDate = today
  },
  methods: {
    checkStock(rule, value, callback) {
      if (!this.applyForm.materialId) {
        callback(new Error('请先选择物资'))
        return
      }
      if (value > this.maxQuantity) {
        callback(new Error(`领用数量不能超过库存 ${this.maxQuantity}`))
      } else {
        callback()
      }
    },
    handleMaterialChange() {
      this.applyForm.quantity = 1
      this.$refs.applyForm.clearValidate(['quantity'])
    },
    submitForm() {
      this.$refs.applyForm.validate((valid) => {
        if (valid) {
          if (this.applyForm.quantity > this.maxQuantity) {
            this.$message.error(`领用数量不能超过库存 ${this.maxQuantity}！`)
            return
          }
          this.submitting = true
          setTimeout(() => {
            this.submitting = false
            this.$message.success('领用申请提交成功，等待审批！')
            console.log('申请数据：', this.applyForm)
          }, 1000)
        } else {
          this.$message.error('请完善表单信息！')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.applyForm.resetFields()
      const today = new Date().toISOString().split('T')[0]
      this.applyForm.applyDate = today
    },
    goToList() {
      this.$router.push('/records')
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

:deep(.el-input__inner),
:deep(.el-textarea__inner),
:deep(.el-select .el-input__inner) {
  border-radius: 4px;
}

:deep(.el-button) {
  border-radius: 4px;
}
</style>
