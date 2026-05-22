<template>
  <div class="page-container">
    <el-card class="card-box">
      <div slot="header" class="clearfix">
        <span>包裹入库登记</span>
      </div>
      <el-form :model="inboundForm" :rules="rules" ref="inboundForm" label-width="120px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="快递单号" prop="trackingNo">
              <el-input 
                v-model="inboundForm.trackingNo" 
                placeholder="请输入快递单号"
                @blur="checkTrackingNoDuplicate"
                :class="{'duplicate-warning': isTrackingDuplicate}"
              ></el-input>
              <div v-if="isTrackingDuplicate" class="duplicate-tip">
                <i class="el-icon-warning"></i>
                <span>该运单号已入库，请勿重复登记</span>
              </div>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="快递公司" prop="expressCompany">
              <el-select v-model="inboundForm.expressCompany" placeholder="请选择快递公司" style="width: 100%;">
                <el-option label="顺丰速运" value="顺丰速运"></el-option>
                <el-option label="圆通速递" value="圆通速递"></el-option>
                <el-option label="中通快递" value="中通快递"></el-option>
                <el-option label="韵达快递" value="韵达快递"></el-option>
                <el-option label="申通快递" value="申通快递"></el-option>
                <el-option label="邮政EMS" value="邮政EMS"></el-option>
                <el-option label="京东物流" value="京东物流"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">收件人信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="收件人姓名" prop="receiverName">
              <el-input v-model="inboundForm.receiverName" placeholder="请输入姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="联系电话" prop="receiverPhone">
              <el-input v-model="inboundForm.receiverPhone" placeholder="请输入手机号"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="是否会员">
              <el-switch v-model="inboundForm.isMember" active-text="是" inactive-text="否"></el-switch>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">存放信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="存放区域" prop="storageArea">
              <el-select v-model="inboundForm.storageArea" placeholder="请选择区域" style="width: 100%;">
                <el-option label="A区" value="A区"></el-option>
                <el-option label="B区" value="B区"></el-option>
                <el-option label="C区" value="C区"></el-option>
                <el-option label="D区" value="D区"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="货架编号" prop="shelfNo">
              <el-input v-model="inboundForm.shelfNo" placeholder="如：03-15"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="取件码" prop="pickupCode">
              <el-input v-model="inboundForm.pickupCode" placeholder="系统自动生成" disabled>
                <el-button slot="append" icon="el-icon-refresh" @click="generatePickupCode">生成</el-button>
              </el-input>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-divider content-position="left">包裹信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="物品类型" prop="goodsType">
              <el-select v-model="inboundForm.goodsType" placeholder="请选择类型" style="width: 100%;">
                <el-option label="文件资料" value="文件资料"></el-option>
                <el-option label="电子产品" value="电子产品"></el-option>
                <el-option label="服装鞋帽" value="服装鞋帽"></el-option>
                <el-option label="食品生鲜" value="食品生鲜"></el-option>
                <el-option label="日常用品" value="日常用品"></el-option>
                <el-option label="其他" value="其他"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="包裹重量(kg)" prop="weight">
              <el-input-number v-model="inboundForm.weight" :min="0.1" :step="0.1" style="width: 100%;"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="包裹状态" prop="status">
              <el-select v-model="inboundForm.status" placeholder="请选择状态" style="width: 100%;">
                <el-option label="完好" value="完好"></el-option>
                <el-option label="轻微破损" value="轻微破损"></el-option>
                <el-option label="严重破损" value="严重破损"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="备注信息">
          <el-input type="textarea" v-model="inboundForm.remark" :rows="2" placeholder="请输入备注信息（选填）"></el-input>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitInbound" size="large">确认入库</el-button>
          <el-button @click="resetForm" size="large">重置表单</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <el-card class="card-box" style="margin-top: 20px;">
      <div slot="header" class="clearfix">
        <span>今日入库记录</span>
      </div>
      <el-table :data="todayInbound" stripe style="width: 100%;">
        <el-table-column prop="trackingNo" label="快递单号" width="180"></el-table-column>
        <el-table-column prop="expressCompany" label="快递公司" width="120"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
        <el-table-column prop="receiverPhone" label="联系电话" width="130"></el-table-column>
        <el-table-column prop="pickupCode" label="取件码" width="100"></el-table-column>
        <el-table-column prop="location" label="存放位置" width="120"></el-table-column>
        <el-table-column prop="inboundTime" label="入库时间" width="180"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag type="success" size="small">已入库</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { packageStorage } from '@/utils/storage.js'
import { eventBus } from '@/utils/eventBus.js'

export default {
  name: 'PackageInbound',
  data() {
    const validatePhone = (rule, value, callback) => {
      const reg = /^1[3-9]\d{9}$/
      if (!value) {
        callback(new Error('请输入手机号码'))
      } else if (!reg.test(value)) {
        callback(new Error('请输入正确的手机号码格式'))
      } else {
        callback()
      }
    }
    const validateTrackingNo = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入快递单号'))
      } else if (packageStorage.exists(value)) {
        callback(new Error('该运单号已入库，请勿重复登记'))
      } else {
        callback()
      }
    }
    return {
      isTrackingDuplicate: false,
      inboundForm: {
        trackingNo: '',
        expressCompany: '',
        receiverName: '',
        receiverPhone: '',
        isMember: false,
        storageArea: '',
        shelfNo: '',
        pickupCode: '',
        goodsType: '',
        weight: 1,
        status: '完好',
        remark: ''
      },
      rules: {
        trackingNo: [
          { required: true, validator: validateTrackingNo, trigger: 'blur' }
        ],
        expressCompany: [
          { required: true, message: '请选择快递公司', trigger: 'change' }
        ],
        receiverName: [
          { required: true, message: '请输入收件人姓名', trigger: 'blur' }
        ],
        receiverPhone: [
          { required: true, validator: validatePhone, trigger: 'blur' }
        ],
        storageArea: [
          { required: true, message: '请选择存放区域', trigger: 'change' }
        ],
        shelfNo: [
          { required: true, message: '请输入货架编号', trigger: 'blur' }
        ],
        pickupCode: [
          { required: true, message: '请生成取件码', trigger: 'blur' }
        ],
        goodsType: [
          { required: true, message: '请选择物品类型', trigger: 'change' }
        ]
      },
      todayInbound: [
        {
          trackingNo: 'SF1234567890123',
          expressCompany: '顺丰速运',
          receiverName: '张三',
          receiverPhone: '138****1234',
          pickupCode: '123456',
          location: 'A区-03-15',
          inboundTime: '2024-01-15 08:30:00'
        },
        {
          trackingNo: 'YT9876543210987',
          expressCompany: '圆通速递',
          receiverName: '李四',
          receiverPhone: '139****5678',
          pickupCode: '654321',
          location: 'B区-02-08',
          inboundTime: '2024-01-15 09:15:00'
        }
      ]
    }
  },
  methods: {
    checkTrackingNoDuplicate() {
      if (this.inboundForm.trackingNo) {
        this.isTrackingDuplicate = packageStorage.exists(this.inboundForm.trackingNo)
      } else {
        this.isTrackingDuplicate = false
      }
    },
    generatePickupCode() {
      this.inboundForm.pickupCode = Math.floor(100000 + Math.random() * 900000).toString()
      this.$message.success('取件码已生成')
    },
    submitInbound() {
      this.$refs.inboundForm.validate((valid) => {
        if (valid) {
          if (packageStorage.exists(this.inboundForm.trackingNo)) {
            this.$message.error('该运单号已入库，请勿重复登记！')
            return false
          }
          
          const packageData = {
            trackingNo: this.inboundForm.trackingNo,
            expressCompany: this.inboundForm.expressCompany,
            receiverName: this.inboundForm.receiverName,
            receiverPhone: this.inboundForm.receiverPhone,
            storageArea: this.inboundForm.storageArea,
            shelfNo: this.inboundForm.shelfNo,
            pickupCode: this.inboundForm.pickupCode,
            location: this.inboundForm.storageArea + '-' + this.inboundForm.shelfNo,
            goodsType: this.inboundForm.goodsType,
            weight: this.inboundForm.weight,
            packageStatus: this.inboundForm.status,
            isMember: this.inboundForm.isMember,
            remark: this.inboundForm.remark
          }
          
          packageStorage.addPackage(packageData)
          
          const newRecord = {
            trackingNo: this.inboundForm.trackingNo,
            expressCompany: this.inboundForm.expressCompany,
            receiverName: this.inboundForm.receiverName,
            receiverPhone: this.inboundForm.receiverPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2'),
            pickupCode: this.inboundForm.pickupCode,
            location: this.inboundForm.storageArea + '-' + this.inboundForm.shelfNo,
            inboundTime: new Date().toLocaleString()
          }
          this.todayInbound.unshift(newRecord)
          eventBus.$emit('packageStatusUpdated')
          this.$message.success('入库登记成功！')
          console.log('入库信息：', this.inboundForm)
          this.resetForm()
        } else {
          this.$message.error('请检查表单信息是否填写正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.inboundForm.resetFields()
      this.inboundForm.weight = 1
      this.inboundForm.status = '完好'
      this.inboundForm.isMember = false
    }
  }
}
</script>

<style scoped>
.el-card {
  max-width: 1000px;
  margin: 0 auto;
}

.el-divider {
  margin: 20px 0;
}

.el-divider__text {
  font-weight: 500;
  color: #409EFF;
}

.duplicate-warning .el-input__inner {
  border-color: #f56c6c;
}

.duplicate-tip {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
  display: flex;
  align-items: center;
  gap: 5px;
}
</style>
