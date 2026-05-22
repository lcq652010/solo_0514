<template>
  <div class="checkout-page">
    <div class="page-container">
      <div class="page-header">
        <h2 class="page-title">下单结算</h2>
        <el-button @click="$router.push('/dishes')">
          <i class="el-icon-arrow-left"></i> 继续选购
        </el-button>
      </div>

      <el-row :gutter="24">
        <el-col :span="16">
          <el-card class="mb-24">
            <div slot="header" class="card-header">
              <span><i class="el-icon-shopping-cart-2"></i> 购物车商品</span>
            </div>
            <div v-if="cart.length === 0" class="empty-state">
              <i class="el-icon-shopping-cart-empty"></i>
              <p>购物车是空的</p>
              <el-button type="primary" @click="$router.push('/dishes')">去选购</el-button>
            </div>
            <div v-else>
              <el-alert
                v-if="stockError"
                :title="stockError"
                type="error"
                :closable="false"
                show-icon
                class="mb-16"
              />
              <el-table :data="cart" border>
                <el-table-column label="菜品信息" min-width="200">
                  <template slot-scope="scope">
                    <div class="dish-item">
                      <img :src="scope.row.image" class="dish-thumb" />
                      <div class="dish-detail">
                        <div class="dish-name">{{ scope.row.name }}</div>
                        <div class="dish-price">¥ {{ scope.row.price }}</div>
                        <div
                          class="dish-stock"
                          :class="{ 'stock-error': getDishStock(scope.row.id) < scope.row.quantity, 'stock-warning': getDishStock(scope.row.id) > 0 && getDishStock(scope.row.id) <= 10 }"
                        >
                          <i class="el-icon-box"></i>
                          {{ getDishStock(scope.row.id) > 0 ? `库存 ${getDishStock(scope.row.id)}` : '已售罄' }}
                          {{ getDishStock(scope.row.id) < scope.row.quantity ? '（库存不足）' : '' }}
                        </div>
                      </div>
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="单价" width="100" align="center">
                  <template slot-scope="scope">
                    ¥ {{ scope.row.price }}
                  </template>
                </el-table-column>
                <el-table-column label="数量" width="160" align="center">
                  <template slot-scope="scope">
                    <div class="quantity-control">
                      <el-button
                        type="danger"
                        size="small"
                        icon="el-icon-minus"
                        circle
                        @click="decreaseQuantity(scope.row)"
                      />
                      <span class="quantity">{{ scope.row.quantity }}</span>
                      <el-button
                        type="primary"
                        size="small"
                        icon="el-icon-plus"
                        circle
                        :disabled="getDishStock(scope.row.id) <= scope.row.quantity"
                        @click="increaseQuantity(scope.row)"
                      />
                    </div>
                  </template>
                </el-table-column>
                <el-table-column label="小计" width="120" align="center">
                  <template slot-scope="scope">
                    <span class="subtotal">¥ {{ (scope.row.price * scope.row.quantity).toFixed(2) }}</span>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="80" align="center">
                  <template slot-scope="scope">
                    <el-button
                      type="text"
                      icon="el-icon-delete"
                      @click="removeItem(scope.row.id)"
                    >
                      删除
                    </el-button>
                  </template>
                </el-table-column>
              </el-table>
            </div>
          </el-card>

          <el-card>
            <div slot="header" class="card-header">
              <span><i class="el-icon-location"></i> 收货信息</span>
            </div>
            <el-form
              :model="form"
              :rules="rules"
              ref="orderForm"
              label-width="100px"
              class="order-form"
            >
              <el-row :gutter="24">
                <el-col :span="12">
                  <el-form-item label="收货人" prop="customerName">
                    <el-input v-model="form.customerName" placeholder="请输入收货人姓名" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="联系电话" prop="phone">
                    <el-input v-model="form.phone" placeholder="请输入联系电话" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="收货地址" prop="address">
                <el-input
                  v-model="form.address"
                  type="textarea"
                  :rows="3"
                  placeholder="请输入详细收货地址"
                />
              </el-form-item>
              <el-form-item label="备注">
                <el-input
                  v-model="form.remark"
                  type="textarea"
                  :rows="2"
                  placeholder="如有特殊要求请备注（选填）"
                />
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>

        <el-col :span="8">
          <el-card class="order-summary" v-if="cart.length > 0">
            <div slot="header" class="card-header">
              <span><i class="el-icon-document"></i> 订单汇总</span>
            </div>
            <div class="summary-item">
              <span>商品总数：</span>
              <span>{{ cartCount }} 件</span>
            </div>
            <div class="summary-item">
              <span>商品金额：</span>
              <span>¥ {{ cartTotal.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span>配送费：</span>
              <span>¥ {{ deliveryFee.toFixed(2) }}</span>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-total">
              <span>应付金额：</span>
              <span class="total-price">¥ {{ (cartTotal + deliveryFee).toFixed(2) }}</span>
            </div>
            <el-button
              type="primary"
              size="large"
              class="submit-btn"
              :disabled="cart.length === 0"
              @click="submitOrder"
            >
              提交订单
            </el-button>
            <el-button
              type="text"
              class="clear-btn"
              @click="clearCart"
            >
              清空购物车
            </el-button>
          </el-card>

          <el-card class="order-tips mt-24">
            <div slot="header" class="card-header">
              <span><i class="el-icon-info"></i> 温馨提示</span>
            </div>
            <ul class="tips-list">
              <li>配送时间：30-45分钟送达</li>
              <li>配送范围：市区内5公里</li>
              <li>满30元免配送费</li>
              <li>如有问题请联系客服：400-123-4567</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'Checkout',
  data() {
    return {
      form: {
        customerName: '',
        phone: '',
        address: '',
        remark: ''
      },
      rules: {
        customerName: [
          { required: true, message: '请输入收货人姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入收货地址', trigger: 'blur' },
          { min: 10, message: '地址信息不够详细', trigger: 'blur' }
        ]
      },
      deliveryFee: 5
    }
  },
  computed: {
    ...mapState(['cart', 'dishes']),
    ...mapGetters(['cartTotal', 'cartCount']),
    stockError() {
      const errors = []
      this.cart.forEach(item => {
        const stock = this.getDishStock(item.id)
        if (stock < item.quantity) {
          errors.push(`${item.name}（库存${stock}份）`)
        }
      })
      if (errors.length > 0) {
        return `以下商品库存不足：${errors.join('、')}，请调整购买数量或删除商品`
      }
      return ''
    }
  },
  methods: {
    ...mapActions(['addToCart', 'removeFromCart', 'updateCartItemQuantity', 'clearCart', 'placeOrder']),
    getDishStock(dishId) {
      const dish = this.dishes.find(d => d.id === dishId)
      return dish ? dish.stock : 0
    },
    increaseQuantity(item) {
      const stock = this.getDishStock(item.id)
      if (item.quantity >= stock) {
        this.$message.warning(`商品「${item.name}」库存不足，最多可购买 ${stock} 份`)
        return
      }
      this.addToCart(item)
    },
    decreaseQuantity(item) {
      this.removeFromCart(item.id)
    },
    removeItem(dishId) {
      this.updateCartItemQuantity({ dishId, quantity: 0 })
    },
    submitOrder() {
      if (this.stockError) {
        this.$message.error(this.stockError)
        return
      }
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          this.$confirm('确认提交订单吗？', '提示', {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }).then(async () => {
            const orderData = {
              ...this.form,
              dishes: this.cart.map(item => ({
                id: item.id,
                name: item.name,
                price: item.price,
                quantity: item.quantity
              })),
              totalPrice: this.cartTotal + this.deliveryFee
            }
            const result = await this.placeOrder(orderData)
            if (result.success) {
              this.$message.success('订单提交成功！')
              this.$router.push({
                path: '/orders'
              })
            } else {
              this.$message.error(result.message)
            }
          }).catch(() => {})
        } else {
          this.$message.error('请完善收货信息')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.card-header {
  font-weight: 600;
}
.dish-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
.dish-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
}
.dish-detail {
  flex: 1;
}
.dish-name {
  font-weight: 500;
  margin-bottom: 4px;
}
.dish-price {
  color: #f56c6c;
}
.dish-stock {
  font-size: 12px;
  color: #909399;
  margin-top: 2px;
}
.dish-stock.stock-warning {
  color: #e6a23c;
}
.dish-stock.stock-error {
  color: #f56c6c;
}
.dish-stock i {
  margin-right: 2px;
}
.quantity-control {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
.quantity {
  min-width: 30px;
  text-align: center;
  font-size: 14px;
}
.subtotal {
  color: #f56c6c;
  font-weight: 600;
}
.order-summary {
  position: sticky;
  top: 20px;
}
.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #606266;
}
.summary-divider {
  border-top: 1px solid #ebeef5;
  margin: 16px 0;
}
.summary-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.summary-total .total-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}
.submit-btn {
  width: 100%;
  font-size: 16px;
}
.clear-btn {
  width: 100%;
  margin-top: 12px;
}
.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.tips-list li {
  padding: 8px 0;
  color: #606266;
  font-size: 13px;
  padding-left: 16px;
  position: relative;
}
.tips-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #409eff;
}
.order-form {
  padding-right: 20px;
}
</style>
