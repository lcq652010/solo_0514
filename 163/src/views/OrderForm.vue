<template>
  <div class="page-container">
    <h2 class="page-title">下单参团</h2>
    
    <div class="form-container">
      <el-form
        ref="orderForm"
        :model="orderForm"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="选择商品" prop="goodsId">
          <el-select
            v-model="orderForm.goodsId"
            placeholder="请选择拼团商品"
            style="width: 100%;"
            @change="onGoodsChange"
          >
            <el-option
              v-for="goods in availableGoods"
              :key="goods.id"
              :label="goods.name"
              :value="goods.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item v-if="selectedGoods" label="商品信息">
          <div style="display: flex; gap: 20px; padding: 15px; background: #f5f7fa; border-radius: 4px;">
            <img :src="selectedGoods.image" style="width: 120px; height: 90px; object-fit: cover; border-radius: 4px;">
            <div>
              <p style="font-weight: bold; margin-bottom: 8px;">{{ selectedGoods.name }}</p>
              <p style="color: #ff6b00; font-size: 20px; font-weight: bold;">¥{{ selectedGoods.groupPrice }}</p>
              <p style="font-size: 12px; color: #666; margin-top: 5px;">
                已参团 {{ selectedGoods.currentCount }}/{{ selectedGoods.needCount }} 人
              </p>
              <p style="font-size: 12px; margin-top: 5px;">
                <el-tag :type="selectedGoods.stock > 0 ? 'success' : 'danger'" size="small">
                  库存：{{ selectedGoods.stock }} 件
                </el-tag>
                <el-tag :type="getGroupStatusType(selectedGoods)" size="small" style="margin-left: 8px;">
                  {{ getGroupStatusText(selectedGoods) }}
                </el-tag>
              </p>
            </div>
          </div>
        </el-form-item>

        <el-form-item label="购买数量" prop="quantity">
          <el-input-number
            v-model="orderForm.quantity"
            :min="1"
            :max="selectedGoods ? Math.min(selectedGoods.limitBuy, selectedGoods.stock) : 10"
            @change="calculateTotal"
          ></el-input-number>
          <span style="margin-left: 10px; color: #666;">件</span>
          <span v-if="selectedGoods && selectedGoods.stock < orderForm.quantity" style="margin-left: 10px; color: #f56c6c;">
            库存不足！仅剩 {{ selectedGoods.stock }} 件
          </span>
          <span v-if="selectedGoods" style="margin-left: 10px; color: #409EFF;">
            每人限购 {{ selectedGoods.limitBuy }} 件
          </span>
        </el-form-item>

        <el-form-item label="收货人姓名" prop="buyerName">
          <el-input
            v-model="orderForm.buyerName"
            placeholder="请输入收货人姓名"
          ></el-input>
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input
            v-model="orderForm.phone"
            placeholder="请输入联系电话"
            maxlength="11"
          ></el-input>
        </el-form-item>

        <el-form-item label="提货地址" prop="address">
          <el-select
            v-model="orderForm.address"
            placeholder="请选择提货地址"
            style="width: 100%;"
          >
            <el-option label="幸福小区1号楼自提点" value="幸福小区1号楼自提点"></el-option>
            <el-option label="阳光花园3号楼自提点" value="阳光花园3号楼自提点"></el-option>
            <el-option label="和平小区5号楼自提点" value="和平小区5号楼自提点"></el-option>
            <el-option label="绿地小区2号楼自提点" value="绿地小区2号楼自提点"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="备注">
          <el-input
            type="textarea"
            v-model="orderForm.remark"
            placeholder="如有特殊要求请备注"
            :rows="3"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <div style="text-align: right; padding: 15px; background: #fff7e6; border-radius: 4px;">
            <span style="font-size: 16px;">订单总额：</span>
            <span style="font-size: 28px; color: #ff6b00; font-weight: bold;">¥{{ totalPrice }}</span>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" class="btn-block" @click="submitOrder">
            提交订单
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { goodsList } from '../data/mock.js'

export default {
  name: 'OrderForm',
  data() {
    return {
      goodsList: goodsList,
      orderForm: {
        goodsId: '',
        quantity: 1,
        buyerName: '',
        phone: '',
        address: '',
        remark: ''
      },
      rules: {
        goodsId: [
          { required: true, message: '请选择商品', trigger: 'change' }
        ],
        quantity: [
          { required: true, message: '请输入购买数量', trigger: 'blur' }
        ],
        buyerName: [
          { required: true, message: '请输入收货人姓名', trigger: 'blur' },
          { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请选择提货地址', trigger: 'change' }
        ]
      }
    }
  },
  computed: {
    availableGoods() {
      return this.goodsList.filter(item => item.status === 'going')
    },
    selectedGoods() {
      return this.goodsList.find(item => item.id === this.orderForm.goodsId)
    },
    totalPrice() {
      if (!this.selectedGoods) return '0.00'
      return (this.selectedGoods.groupPrice * this.orderForm.quantity).toFixed(2)
    }
  },
  mounted() {
    const goodsId = this.$route.query.goodsId
    if (goodsId) {
      this.orderForm.goodsId = parseInt(goodsId)
    }
  },
  methods: {
    onGoodsChange() {
      this.orderForm.quantity = 1
    },
    calculateTotal() {
    },
    getGroupStatusText(goods) {
      if (goods.currentCount >= goods.needCount) {
        return '已成团'
      }
      return '待成团'
    },
    getGroupStatusType(goods) {
      if (goods.currentCount >= goods.needCount) {
        return 'success'
      }
      return 'warning'
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          if (this.selectedGoods.stock <= 0) {
            this.$message.error('该商品库存不足，无法下单')
            return
          }
          if (this.orderForm.quantity > this.selectedGoods.stock) {
            this.$message.error(`购买数量超过库存，仅剩 ${this.selectedGoods.stock} 件`)
            return
          }
          if (this.orderForm.quantity > this.selectedGoods.limitBuy) {
            this.$message.error(`超过限购数量，每人限购 ${this.selectedGoods.limitBuy} 件`)
            return
          }
          if (this.selectedGoods.currentCount >= this.selectedGoods.needCount) {
            this.$message.warning('该拼团已成团，无需再参团')
            return
          }
          
          const wasSuccessBefore = this.selectedGoods.currentCount >= this.selectedGoods.needCount
          
          this.selectedGoods.stock -= this.orderForm.quantity
          this.selectedGoods.currentCount += 1
          
          const isSuccessNow = this.selectedGoods.currentCount >= this.selectedGoods.needCount
          
          if (isSuccessNow && !wasSuccessBefore) {
            this.selectedGoods.status = 'success'
            this.$message.success('恭喜！拼团已达成！')
          }
          
          const newOrder = {
            id: 'ORD' + Date.now(),
            goodsName: this.selectedGoods.name,
            category: this.selectedGoods.category,
            groupStatus: this.selectedGoods.status,
            buyerName: this.orderForm.buyerName,
            phone: this.orderForm.phone,
            quantity: this.orderForm.quantity,
            totalPrice: this.totalPrice,
            orderTime: new Date().toLocaleString().replace(/\//g, '-'),
            pickUpDate: new Date(Date.now() + 86400000 * 2).toISOString().split('T')[0],
            status: 'paid',
            pickUpCode: Math.random().toString(36).substring(2, 6).toUpperCase() + Math.floor(Math.random() * 10000)
          }
          
          this.$root.$emit('newOrder', newOrder)
          
          this.$alert(`
            <p>订单提交成功！</p>
            <p>商品：${this.selectedGoods.name}</p>
            <p>数量：${this.orderForm.quantity} 件</p>
            <p>总额：¥${this.totalPrice}</p>
            <p>收货人：${this.orderForm.buyerName}</p>
            <p>电话：${this.orderForm.phone}</p>
            <p>提货码：${newOrder.pickUpCode}</p>
            <p style="color: #52c41a; margin-top: 10px;">拼团状态：${this.getGroupStatusText(this.selectedGoods)}</p>
          `, '成功', {
            dangerouslyUseHTMLString: true,
            confirmButtonText: '确定'
          }).then(() => {
            this.$refs.orderForm.resetFields()
          })
        } else {
          return false
        }
      })
    }
  }
}
</script>