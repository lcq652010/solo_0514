<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">会员详情</h2>
      <div>
        <el-button @click="goBack">
          <i class="el-icon-back"></i> 返回列表
        </el-button>
      </div>
    </div>

    <el-card v-loading="loading" class="detail-card">
      <div slot="header">
        <span>基本信息</span>
      </div>
      <el-descriptions :column="3" border>
        <el-descriptions-item label="会员编号">{{ member.memberNo }}</el-descriptions-item>
        <el-descriptions-item label="会员姓名">{{ member.name }}</el-descriptions-item>
        <el-descriptions-item label="会员等级">
          <el-tag v-if="member.level === '钻石会员'" type="danger" size="small">{{ member.level }}</el-tag>
          <el-tag v-else-if="member.level === '金卡会员'" type="warning" size="small">{{ member.level }}</el-tag>
          <el-tag v-else-if="member.level === '银卡会员'" type="success" size="small">{{ member.level }}</el-tag>
          <el-tag v-else size="small">{{ member.level }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="手机号码">{{ member.phone }}</el-descriptions-item>
        <el-descriptions-item label="电子邮箱">{{ member.email }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ member.gender === 1 ? '男' : '女' }}</el-descriptions-item>
        <el-descriptions-item label="出生日期">{{ member.birthday }}</el-descriptions-item>
        <el-descriptions-item label="账户余额">
          <span style="color: #e6a23c; font-weight: bold; font-size: 18px;">¥{{ member.balance | formatMoney }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="会员积分">{{ member.point }}</el-descriptions-item>
        <el-descriptions-item label="会员状态">
          <el-tag :class="member.status === 1 ? 'status-tag active' : 'status-tag inactive'" size="small">
            {{ member.status === 1 ? '正常' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="累计充值">¥{{ member.totalRecharge | formatMoney }}</el-descriptions-item>
        <el-descriptions-item label="累计消费">¥{{ member.totalConsume | formatMoney }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ member.registerTime }}</el-descriptions-item>
        <el-descriptions-item label="最后消费">{{ member.lastConsumeTime }}</el-descriptions-item>
        <el-descriptions-item label="联系地址" :span="2">{{ member.address }}</el-descriptions-item>
        <el-descriptions-item label="备注" :span="3">{{ member.remark || '无' }}</el-descriptions-item>
      </el-descriptions>

      <div style="margin-top: 20px;">
        <el-button type="primary" @click="handleRecharge">
          <i class="el-icon-plus"></i> 会员充值
        </el-button>
        <el-button type="success" @click="handleConsume">
          <i class="el-icon-shopping-cart-2"></i> 消费扣款
        </el-button>
        <el-button type="warning" @click="handleEdit">
          <i class="el-icon-edit"></i> 编辑信息
        </el-button>
      </div>
    </el-card>

    <el-card style="margin-top: 20px;">
      <div slot="header">
        <span>最近交易记录</span>
      </div>
      <el-table :data="recentTransactions" border stripe style="width: 100%">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="orderNo" label="交易单号" width="180" align="center"></el-table-column>
        <el-table-column prop="type" label="交易类型" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 1 ? 'success' : 'danger'" size="small">
              {{ scope.row.type === 1 ? '充值' : '消费' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="交易金额" width="120" align="center">
          <template slot-scope="scope">
            <span :style="{ color: scope.row.type === 1 ? '#67c23a' : '#f56c6c' }">
              {{ scope.row.type === 1 ? '+' : '-' }}¥{{ scope.row.amount | formatMoney }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="afterBalance" label="交易后余额" width="120" align="center">
          <template slot-scope="scope">
            ¥{{ scope.row.afterBalance | formatMoney }}
          </template>
        </el-table-column>
        <el-table-column prop="paymentMethod" label="支付方式" width="120" align="center"></el-table-column>
        <el-table-column prop="remark" label="备注" align="center"></el-table-column>
        <el-table-column prop="createTime" label="交易时间" width="170" align="center"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { getMemberById, getTransactionsByMemberId } from '@/mock/data'

export default {
  name: 'MemberDetail',
  data() {
    return {
      loading: false,
      member: {},
      recentTransactions: []
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        const memberId = this.$route.params.id
        this.member = getMemberById(memberId) || {}
        this.recentTransactions = getTransactionsByMemberId(memberId).slice(0, 10)
        this.loading = false
      }, 300)
    },
    goBack() {
      this.$router.back()
    },
    handleRecharge() {
      this.$router.push(`/recharge/${this.member.id}`)
    },
    handleConsume() {
      this.$router.push(`/consume/${this.member.id}`)
    },
    handleEdit() {
      this.$message.info('编辑会员功能待实现')
    }
  }
}
</script>
