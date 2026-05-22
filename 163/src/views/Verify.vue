<template>
  <div class="page-container">
    <h2 class="page-title">提货核销</h2>

    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <div slot="header" style="text-align: center; font-size: 18px; font-weight: bold;">
            输入提货码
          </div>
          
          <div style="text-align: center; padding: 30px 0;">
            <el-input
              v-model="pickUpCode"
              placeholder="请输入提货码"
              size="large"
              style="width: 80%;"
              maxlength="10"
              @keyup.enter.native="verifyCode"
            ></el-input>
            <el-button
              type="primary"
              size="large"
              style="margin-top: 20px; width: 80%;"
              @click="verifyCode"
              :loading="verifying"
            >
              确认核销
            </el-button>
          </div>
        </el-card>
      </el-col>

      <el-col :span="12">
        <el-card shadow="hover" v-if="orderInfo">
          <div slot="header" style="text-align: center; font-size: 18px; font-weight: bold; color: #52c41a;">
            订单信息
          </div>
          
          <div style="padding: 20px;">
            <el-descriptions :column="1" border>
              <el-descriptions-item label="订单号">
                {{ orderInfo.id }}
              </el-descriptions-item>
              <el-descriptions-item label="商品名称">
                {{ orderInfo.goodsName }}
              </el-descriptions-item>
              <el-descriptions-item label="收货人">
                {{ orderInfo.buyerName }}
              </el-descriptions-item>
              <el-descriptions-item label="联系电话">
                {{ orderInfo.phone }}
              </el-descriptions-item>
              <el-descriptions-item label="购买数量">
                {{ orderInfo.quantity }} 件
              </el-descriptions-item>
              <el-descriptions-item label="订单金额">
                <span style="color: #ff6b00; font-weight: bold;">¥{{ orderInfo.totalPrice }}</span>
              </el-descriptions-item>
              <el-descriptions-item label="下单时间">
                {{ orderInfo.orderTime }}
              </el-descriptions-item>
              <el-descriptions-item label="订单状态">
                <el-tag :type="getStatusType(orderInfo.status)">
                  {{ getStatusText(orderInfo.status) }}
                </el-tag>
              </el-descriptions-item>
            </el-descriptions>

            <div v-if="orderInfo.status === 'shipped'" style="margin-top: 20px; text-align: center;">
              <el-button
                type="success"
                size="large"
                @click="confirmPickUp"
              >
                确认提货
              </el-button>
            </div>
            <div v-else-if="orderInfo.status === 'picked' || orderInfo.status === 'completed'" style="margin-top: 20px; text-align: center; padding: 20px; background: #f6ffed; border-radius: 8px;">
              <i class="el-icon-success" style="font-size: 48px; color: #52c41a;"></i>
              <p style="margin-top: 10px; font-size: 16px; color: #52c41a;">该订单已完成提货</p>
            </div>
          </div>
        </el-card>

        <el-card shadow="hover" v-else style="min-height: 400px;">
          <el-empty description="请输入提货码查询订单"></el-empty>
        </el-card>
      </el-col>
    </el-row>

    <div style="margin-top: 30px;">
      <h3 style="margin-bottom: 15px; font-size: 18px;">最近核销记录</h3>
      <el-table
        :data="recentRecords"
        border
        style="width: 100%;"
      >
        <el-table-column prop="id" label="订单号" width="180"></el-table-column>
        <el-table-column prop="goodsName" label="商品名称"></el-table-column>
        <el-table-column prop="buyerName" label="收货人" width="100"></el-table-column>
        <el-table-column prop="pickUpCode" label="提货码" width="100">
          <template slot-scope="scope">
            <el-tag size="small" type="warning">{{ scope.row.pickUpCode }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="verifyTime" label="核销时间" width="180"></el-table-column>
        <el-table-column label="状态" width="100">
          <template slot-scope="scope">
            <el-tag size="small" type="success">已核销</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import { ordersList } from '../data/mock.js'

export default {
  name: 'Verify',
  data() {
    return {
      ordersList: ordersList,
      pickUpCode: '',
      orderInfo: null,
      verifying: false,
      recentRecords: [
        {
          id: 'ORD20240116004',
          goodsName: '散养土鸡蛋 30枚',
          buyerName: '赵六',
          pickUpCode: 'D12348',
          verifyTime: '2024-01-16 15:30:00'
        }
      ]
    }
  },
  methods: {
    verifyCode() {
      if (!this.pickUpCode.trim()) {
        this.$message.warning('请输入提货码')
        return
      }

      this.verifying = true
      
      setTimeout(() => {
        const order = this.ordersList.find(item => item.pickUpCode === this.pickUpCode.toUpperCase())
        if (order) {
          this.orderInfo = { ...order }
          this.$message.success('查询成功')
        } else {
          this.orderInfo = null
          this.$message.error('未找到对应订单，请检查提货码是否正确')
        }
        this.verifying = false
      }, 500)
    },
    confirmPickUp() {
      this.$confirm('确认已收到商品？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orderInfo.status = 'picked'
        const orderInList = this.ordersList.find(item => item.id === this.orderInfo.id)
        if (orderInList) {
          orderInList.status = 'picked'
        }
        this.$root.$emit('orderPicked', this.orderInfo.id)
        this.recentRecords.unshift({
          id: this.orderInfo.id,
          goodsName: this.orderInfo.goodsName,
          buyerName: this.orderInfo.buyerName,
          pickUpCode: this.orderInfo.pickUpCode,
          verifyTime: new Date().toLocaleString()
        })
        this.$message.success('提货成功！订单状态已更新')
      }).catch(() => {
      })
    },
    getStatusText(status) {
      const map = {
        pending: '待付款',
        paid: '已付款',
        shipped: '已发货',
        picked: '已提货',
        completed: '已完成'
      }
      return map[status]
    },
    getStatusType(status) {
      const map = {
        pending: 'info',
        paid: 'warning',
        shipped: 'primary',
        picked: 'success',
        completed: 'success'
      }
      return map[status]
    }
  }
}
</script>