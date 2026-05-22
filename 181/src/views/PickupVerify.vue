<template>
  <div class="page-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="card-box">
          <div slot="header" class="clearfix">
            <span>取件核销</span>
          </div>
          <el-form :model="verifyForm" label-width="100px">
            <el-form-item label="取件码">
              <el-input v-model="verifyForm.pickupCode" placeholder="请输入取件码" size="large" maxlength="6">
                <el-button slot="append" type="primary" @click="searchPackage" size="large">查询</el-button>
              </el-input>
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="verifyForm.phone" placeholder="请输入收件人手机号后4位" maxlength="4"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="success" @click="verifyPickup" size="large" :disabled="!packageInfo">确认取件</el-button>
              <el-button @click="resetVerify" size="large">重置</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="card-box" v-loading="loading">
          <div slot="header" class="clearfix">
            <span>包裹信息</span>
          </div>
          <div v-if="packageInfo" class="package-info">
            <div class="info-item">
              <span class="label">快递单号：</span>
              <span class="value">{{ packageInfo.trackingNo }}</span>
            </div>
            <div class="info-item">
              <span class="label">收件人：</span>
              <span class="value">{{ packageInfo.receiverName }}</span>
            </div>
            <div class="info-item">
              <span class="label">联系电话：</span>
              <span class="value">{{ packageInfo.receiverPhone }}</span>
            </div>
            <div class="info-item">
              <span class="label">存放位置：</span>
              <span class="value">{{ packageInfo.location }}</span>
            </div>
            <div class="info-item">
              <span class="label">入库时间：</span>
              <span class="value">{{ packageInfo.inboundTime }}</span>
            </div>
            <div class="info-item">
              <span class="label">物品类型：</span>
              <span class="value">{{ packageInfo.goodsType }}</span>
            </div>
            <div class="info-item status">
              <span class="label">状态：</span>
              <el-tag :type="packageInfo.status === '待取件' ? 'warning' : 'success'">
                {{ packageInfo.status }}
              </el-tag>
            </div>
          </div>
          <div v-else class="empty-state">
            <i class="el-icon-search"></i>
            <p>请输入取件码查询包裹信息</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card class="card-box" style="margin-top: 20px;">
      <div slot="header" class="clearfix">
        <span>今日取件记录</span>
      </div>
      <el-table :data="todayRecords" stripe style="width: 100%;">
        <el-table-column prop="trackingNo" label="快递单号" width="180"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="120"></el-table-column>
        <el-table-column prop="receiverPhone" label="联系电话" width="130"></el-table-column>
        <el-table-column prop="pickupCode" label="取件码" width="100"></el-table-column>
        <el-table-column prop="pickupTime" label="取件时间" width="180"></el-table-column>
        <el-table-column prop="operator" label="操作员" width="100"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag type="success" size="small">已取件</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { packageStorage, pickupRecordStorage } from '@/utils/storage.js'
import { eventBus } from '@/utils/eventBus.js'

export default {
  name: 'PickupVerify',
  data() {
    return {
      loading: false,
      verifyForm: {
        pickupCode: '',
        phone: ''
      },
      packageInfo: null,
      todayRecords: []
    }
  },
  methods: {
    searchPackage() {
      if (!this.verifyForm.pickupCode) {
        this.$message.warning('请输入取件码')
        return
      }
      this.loading = true
      setTimeout(() => {
        const pkg = packageStorage.getPackageByPickupCode(this.verifyForm.pickupCode)
        
        if (!pkg) {
          this.$message.error('未找到该取件码对应的包裹信息')
          this.packageInfo = null
          this.loading = false
          return
        }
        
        if (pkg.status === '已取件') {
          this.$message.warning('该包裹已取件，请勿重复扫码！')
          this.packageInfo = {
            ...pkg,
            receiverPhone: pkg.receiverPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
          }
          this.loading = false
          return
        }
        
        this.packageInfo = {
          ...pkg,
          receiverPhone: pkg.receiverPhone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
        }
        this.loading = false
        this.$message.success('查询成功')
      }, 300)
    },
    verifyPickup() {
      if (!this.verifyForm.phone) {
        this.$message.warning('请输入手机号后4位')
        return
      }
      
      if (this.packageInfo.status === '已取件') {
        this.$message.warning('该包裹已取件，请勿重复操作！')
        return
      }
      
      const phoneLast4 = this.packageInfo.receiverPhone.slice(-4)
      if (this.verifyForm.phone !== phoneLast4) {
        this.$message.error('手机号后4位验证失败，请核对')
        return
      }
      
      this.$confirm('确认该包裹已被领取？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        packageStorage.updatePackageStatus(this.packageInfo.trackingNo, '已取件')
        
        const newRecord = {
          trackingNo: this.packageInfo.trackingNo,
          receiverName: this.packageInfo.receiverName,
          receiverPhone: this.packageInfo.receiverPhone,
          pickupCode: this.verifyForm.pickupCode,
          pickupTime: new Date().toLocaleString(),
          operator: '管理员'
        }
        pickupRecordStorage.addRecord(newRecord)
        
        this.todayRecords.unshift(newRecord)
        this.packageInfo.status = '已取件'
        eventBus.$emit('packageStatusUpdated')
        this.$message.success('核销成功！')
        setTimeout(() => {
          this.resetVerify()
        }, 1000)
      }).catch(() => {})
    },
    resetVerify() {
      this.verifyForm.pickupCode = ''
      this.verifyForm.phone = ''
      this.packageInfo = null
    }
  },
  mounted() {
    this.todayRecords = pickupRecordStorage.getTodayRecords()
  }
}
</script>

<style scoped>
.package-info {
  padding: 10px 0;
}

.info-item {
  display: flex;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.info-item .label {
  width: 100px;
  color: #909399;
}

.info-item .value {
  flex: 1;
  color: #303133;
}

.empty-state {
  text-align: center;
  padding: 60px 0;
  color: #909399;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 15px;
  display: block;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}
</style>
