<template>
  <div class="page-card">
    <el-row :gutter="20" style="margin-bottom: 25px">
      <el-col :span="8">
        <div class="verify-card">
          <div class="verify-icon">
            <i class="el-icon-scanning"></i>
          </div>
          <div class="verify-content">
            <h3>扫码核销</h3>
            <p>使用设备扫描会员预约二维码快速核销</p>
            <el-button type="primary" size="large" @click="handleScan">
              <i class="el-icon-camera"></i> 开始扫码
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="verify-card">
          <div class="verify-icon code">
            <i class="el-icon-document-checked"></i>
          </div>
          <div class="verify-content">
            <h3>预约码核销</h3>
            <p>输入会员提供的6位预约码进行核销</p>
            <el-input
              v-model="verifyCode"
              placeholder="请输入预约码"
              size="large"
              style="width: 200px; margin-bottom: 10px"
              maxlength="6"
            ></el-input>
            <el-button type="success" size="large" @click="handleVerifyCode" :loading="verifyLoading">
              <i class="el-icon-check"></i> 确认核销
            </el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="8">
        <div class="verify-card">
          <div class="verify-icon phone">
            <i class="el-icon-phone"></i>
          </div>
          <div class="verify-content">
            <h3>手机号查询</h3>
            <p>通过会员手机号查询预约记录并核销</p>
            <el-input
              v-model="searchPhone"
              placeholder="请输入手机号"
              size="large"
              style="width: 200px; margin-bottom: 10px"
            ></el-input>
            <el-button type="warning" size="large" @click="handleSearchByPhone">
              <i class="el-icon-search"></i> 查询预约
            </el-button>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-divider content-position="left">待核销预约列表</el-divider>

    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索会员姓名、教练或课程名称"
        style="width: 300px"
        clearable
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      <el-date-picker
        v-model="filterDate"
        type="date"
        placeholder="选择日期"
        style="width: 200px"
      ></el-date-picker>
      <el-button type="primary" @click="handleSearch">
        <i class="el-icon-search"></i> 搜索
      </el-button>
      <el-button @click="handleReset">
        <i class="el-icon-refresh"></i> 重置
      </el-button>
    </div>

    <div class="table-container">
      <el-table
        :data="filteredList"
        border
        style="width: 100%"
        :row-class-name="tableRowClassName"
      >
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="bookingCode" label="预约码" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="primary" size="small">{{ scope.row.bookingCode }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="memberName" label="会员姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="memberPhone" label="会员手机号" width="120" align="center"></el-table-column>
        <el-table-column prop="trainerName" label="教练" width="100" align="center"></el-table-column>
        <el-table-column prop="courseName" label="课程名称" min-width="150"></el-table-column>
        <el-table-column prop="date" label="上课日期" width="120" align="center"></el-table-column>
        <el-table-column prop="time" label="上课时间" width="120" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="课时余额" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getMemberBalance(scope.row.memberName) && getMemberBalance(scope.row.memberName).balance > 0 ? 'success' : 'danger'" size="small">
              {{ getMemberBalance(scope.row.memberName) ? getMemberBalance(scope.row.memberName).balance : 0 }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button
              v-if="scope.row.status === 'confirmed'"
              type="success"
              size="mini"
              icon="el-icon-check"
              @click="handleVerify(scope.row)"
            >
              核销
            </el-button>
            <el-button
              v-else
              type="info"
              size="mini"
              icon="el-icon-view"
              @click="handleView(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[5, 10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </div>

    <el-dialog title="核销确认" :visible.sync="verifyDialogVisible" width="450px">
      <div v-if="currentVerify" style="padding: 10px 0">
        <div style="text-align: center; margin-bottom: 20px">
          <i class="el-icon-question" style="font-size: 50px; color: #e6a23c"></i>
          <h3 style="margin-top: 15px">确认核销此课程？</h3>
        </div>
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="预约码">
            <el-tag type="primary">{{ currentVerify.bookingCode }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="会员">{{ currentVerify.memberName }}</el-descriptions-item>
          <el-descriptions-item label="教练">{{ currentVerify.trainerName }}</el-descriptions-item>
          <el-descriptions-item label="课程">{{ currentVerify.courseName }}</el-descriptions-item>
          <el-descriptions-item label="时间">{{ currentVerify.date }} {{ currentVerify.time }}</el-descriptions-item>
          <el-descriptions-item label="当前课时余额">
            <el-tag :type="currentMemberBalance && currentMemberBalance.balance > 0 ? 'success' : 'danger'" size="medium">
              {{ currentMemberBalance ? currentMemberBalance.balance : 0 }} 课时
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        <div v-if="currentMemberBalance && currentMemberBalance.balance <= 0" style="margin-top: 15px; padding: 10px; background: #fef0f0; border-radius: 4px; color: #f56c6c;">
          <i class="el-icon-warning"></i> 该会员课时余额不足，无法核销！请先充值。
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="verifyDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmVerify" :loading="confirmLoading">确认核销</el-button>
      </span>
    </el-dialog>

    <el-dialog title="核销成功" :visible.sync="successVisible" width="400px" :close-on-click-modal="false">
      <div style="text-align: center; padding: 20px">
        <i class="el-icon-circle-check" style="font-size: 60px; color: #67c23a"></i>
        <h3 style="margin: 20px 0; color: #67c23a">课时核销成功！</h3>
        <el-descriptions :column="1" border size="small">
          <el-descriptions-item label="核销时间">{{ verifySuccessTime }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="successVisible = false">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockMemberBalances } from '@/mock/data'

export default {
  name: 'VerifyLesson',
  data() {
    return {
      verifyList: [
        {
          id: 1,
          bookingCode: 'A10001',
          memberName: '张三',
          memberPhone: '138****1234',
          trainerName: '张教练',
          courseName: '增肌训练课',
          date: '2024-05-17',
          time: '10:00-11:00',
          status: 'confirmed'
        },
        {
          id: 2,
          bookingCode: 'A10002',
          memberName: '李四',
          memberPhone: '139****5678',
          trainerName: '李教练',
          courseName: '瑜伽基础课',
          date: '2024-05-17',
          time: '14:00-15:00',
          status: 'confirmed'
        },
        {
          id: 3,
          bookingCode: 'A10003',
          memberName: '王五',
          memberPhone: '137****9012',
          trainerName: '王教练',
          courseName: 'HIIT减脂课',
          date: '2024-05-17',
          time: '19:00-20:00',
          status: 'verified'
        },
        {
          id: 4,
          bookingCode: 'A10004',
          memberName: '赵六',
          memberPhone: '136****3456',
          trainerName: '陈教练',
          courseName: '拳击入门课',
          date: '2024-05-18',
          time: '15:00-16:00',
          status: 'confirmed'
        }
      ],
      memberBalances: [...mockMemberBalances],
      searchKeyword: '',
      filterDate: '',
      verifyCode: '',
      searchPhone: '',
      verifyLoading: false,
      confirmLoading: false,
      verifyDialogVisible: false,
      successVisible: false,
      currentVerify: null,
      currentMemberBalance: null,
      verifySuccessTime: '',
      pagination: {
        page: 1,
        pageSize: 10,
        total: 4
      }
    }
  },
  computed: {
    filteredList() {
      let list = this.verifyList
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        list = list.filter(
          item =>
            item.memberName.toLowerCase().includes(keyword) ||
            item.trainerName.toLowerCase().includes(keyword) ||
            item.courseName.toLowerCase().includes(keyword)
        )
      }
      if (this.filterDate) {
        const dateStr = this.formatDate(this.filterDate)
        list = list.filter(item => item.date === dateStr)
      }
      this.pagination.total = list.length
      const start = (this.pagination.page - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return list.slice(start, end)
    }
  },
  methods: {
    formatDate(date) {
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    getStatusType(status) {
      const map = {
        confirmed: 'primary',
        verified: 'success'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        confirmed: '待核销',
        verified: '已核销'
      }
      return map[status] || '未知'
    },
    tableRowClassName({ row }) {
      return row.status === 'verified' ? 'verified-row' : ''
    },
    handleSearch() {
      this.pagination.page = 1
    },
    handleReset() {
      this.searchKeyword = ''
      this.filterDate = ''
      this.pagination.page = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.page = val
    },
    handleScan() {
      this.$message.info('扫码功能需要硬件支持，请连接扫码设备')
    },
    handleVerifyCode() {
      if (!this.verifyCode || this.verifyCode.length !== 6) {
        this.$message.warning('请输入6位预约码')
        return
      }
      this.verifyLoading = true
      setTimeout(() => {
        const found = this.verifyList.find(
          item => item.bookingCode === this.verifyCode && item.status === 'confirmed'
        )
        this.verifyLoading = false
        if (found) {
          this.currentVerify = found
          this.currentMemberBalance = this.getMemberBalance(found.memberName)
          this.verifyDialogVisible = true
        } else {
          this.$message.error('未找到有效的预约记录，请检查预约码是否正确')
        }
      }, 800)
    },
    handleSearchByPhone() {
      if (!this.searchPhone) {
        this.$message.warning('请输入手机号')
        return
      }
      this.searchKeyword = this.searchPhone
      this.handleSearch()
    },
    getMemberBalance(memberName) {
      return this.memberBalances.find(m => m.memberName === memberName) || null
    },
    checkBalanceSufficient(memberName) {
      const balance = this.getMemberBalance(memberName)
      if (!balance || balance.balance <= 0) {
        return false
      }
      return true
    },
    handleVerify(row) {
      this.currentVerify = row
      this.currentMemberBalance = this.getMemberBalance(row.memberName)
      this.verifyDialogVisible = true
    },
    handleView(row) {
      this.$message.info('查看详情功能开发中...')
    },
    confirmVerify() {
      if (!this.checkBalanceSufficient(this.currentVerify.memberName)) {
        this.$message.error(`会员【${this.currentVerify.memberName}】课时余额不足，无法核销！当前剩余：${this.currentMemberBalance ? this.currentMemberBalance.balance : 0} 课时`)
        return
      }
      
      this.confirmLoading = true
      setTimeout(() => {
        const index = this.verifyList.findIndex(item => item.id === this.currentVerify.id)
        if (index > -1) {
          this.verifyList[index].status = 'verified'
          
          const balanceIndex = this.memberBalances.findIndex(
            m => m.memberName === this.currentVerify.memberName
          )
          if (balanceIndex > -1) {
            this.memberBalances[balanceIndex].balance -= 1
            this.memberBalances[balanceIndex].usedHours += 1
          }
        }
        this.confirmLoading = false
        this.verifyDialogVisible = false
        this.verifyCode = ''
        this.verifySuccessTime = new Date().toLocaleString()
        this.successVisible = true
      }, 1000)
    }
  }
}
</script>

<style scoped>
.verified-row {
  background-color: #f0f9eb !important;
}

.verify-card {
  display: flex;
  align-items: flex-start;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
  border-radius: 8px;
  min-height: 180px;
}

.verify-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #fff;
  margin-right: 15px;
  flex-shrink: 0;

  &.code {
    background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
  }

  &.phone {
    background: linear-gradient(135deg, #e6a23c 0%, #ebb563 100%);
  }
}

.verify-content {
  flex: 1;

  h3 {
    margin: 0 0 8px;
    font-size: 18px;
    color: #303133;
  }

  p {
    margin: 0 0 15px;
    font-size: 13px;
    color: #909399;
    line-height: 1.5;
  }
}
</style>
