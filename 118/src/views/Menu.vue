<template>
  <div class="menu-page">
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card class="menu-card">
          <div slot="header" class="clearfix">
            <span class="card-title">商品分类</span>
          </div>
          <el-tabs v-model="activeCategory" type="card">
            <el-tab-pane
              v-for="category in categories"
              :key="category.id"
              :label="category.name"
              :name="category.id"
            >
              <el-row :gutter="15">
                <el-col
                  v-for="product in category.products"
                  :key="product.id"
                  :span="8"
                  class="product-col"
                >
                  <el-card
                    class="product-card"
                    :class="{ 'out-of-stock': product.stock <= 0 }"
                    shadow="hover"
                    @click.native="selectProduct(product)"
                  >
                    <div class="product-image-wrapper">
                      <img :src="product.image" class="product-image" />
                      <div v-if="product.stock <= 0" class="out-of-stock-mask">
                        <span>已售罄</span>
                      </div>
                    </div>
                    <div class="product-info">
                      <div class="product-name">{{ product.name }}</div>
                      <div class="product-price">¥{{ product.price }}</div>
                      <div class="product-stock" :class="{ 'stock-low': product.stock <= 5 && product.stock > 0 }">
                        库存：{{ product.stock }} 杯
                      </div>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="cart-card">
          <div slot="header" class="clearfix">
            <span class="card-title">购物车</span>
            <el-button
              type="danger"
              size="mini"
              style="float: right"
              @click="clearCart"
            >
              清空
            </el-button>
          </div>
          <div class="cart-list" v-if="cartItems.length > 0">
            <div
              v-for="(item, index) in cartItems"
              :key="index"
              class="cart-item"
            >
              <div class="cart-item-info">
                <div class="cart-item-name">{{ item.name }}</div>
                <div class="cart-item-specs">{{ item.specsText }}</div>
              </div>
              <div class="cart-item-right">
                <div class="cart-item-price">¥{{ item.totalPrice }}</div>
                <el-input-number
                  v-model="item.quantity"
                  size="mini"
                  :min="1"
                  :max="99"
                  @change="updateTotal"
                ></el-input-number>
                <el-button
                  type="text"
                  icon="el-icon-delete"
                  class="delete-btn"
                  @click="removeCartItem(index)"
                ></el-button>
              </div>
            </div>
          </div>
          <el-empty v-else description="购物车为空"></el-empty>
          <div class="cart-footer">
            <div class="total-section">
              <span>合计：</span>
              <span class="total-price">¥{{ totalPrice }}</span>
            </div>
            <el-button
              type="primary"
              size="large"
              class="checkout-btn"
              :disabled="cartItems.length === 0"
              @click="showCheckoutDialog"
            >
              去结算
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-dialog
      title="选择商品规格"
      :visible.sync="specDialogVisible"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="currentProduct" label-width="80px">
        <el-form-item label="商品名称">
          <span>{{ selectedProduct.name }}</span>
        </el-form-item>
        <el-form-item label="规格" required>
          <el-select
            v-model="currentProduct.size"
            placeholder="请选择杯型"
            style="width: 100%"
          >
            <el-option
              v-for="size in sizes"
              :key="size.value"
              :label="size.label + (size.price > 0 ? ' +¥' + size.price : '')"
              :value="size.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="温度" required>
          <el-radio-group v-model="currentProduct.temperature">
            <el-radio
              v-for="temp in temperatures"
              :key="temp.value"
              :label="temp.value"
            >
              {{ temp.label }}{{ temp.price > 0 ? ' +¥' + temp.price : '' }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="糖度" required>
          <el-radio-group v-model="currentProduct.sugar">
            <el-radio
              v-for="sugar in sugars"
              :key="sugar.value"
              :label="sugar.value"
            >
              {{ sugar.label }}{{ sugar.price > 0 ? ' +¥' + sugar.price : '' }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="加料">
          <el-checkbox-group v-model="currentProduct.toppings">
            <el-checkbox
              v-for="topping in toppings"
              :key="topping.value"
              :label="topping.value"
            >
              {{ topping.label }} +¥{{ topping.price }}
            </el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="数量">
          <el-input-number 
            v-model="currentProduct.quantity" 
            :min="1" 
            :max="Math.min(selectedProduct.stock, 99)"
          ></el-input-number>
        </el-form-item>
        <el-form-item label="价格计算">
          <div class="price-calculation">
            <div class="price-row">
              <span>基础价格：</span>
              <span>¥{{ selectedProduct.price || 0 }}</span>
            </div>
            <div class="price-row">
              <span>规格差价：</span>
              <span>¥{{ sizePriceDiff }}</span>
            </div>
            <div class="price-row">
              <span>加料总价：</span>
              <span>¥{{ toppingsTotalPrice }}</span>
            </div>
            <div class="price-row total-row">
              <span>单价：</span>
              <span class="unit-price">¥{{ currentUnitPrice }}</span>
            </div>
            <div class="price-row total-row">
              <span>小计 (x{{ currentProduct.quantity }})：</span>
              <span class="total-price">¥{{ currentTotalPrice }}</span>
            </div>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="specDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addToCart">加入购物车</el-button>
      </span>
    </el-dialog>

    <el-dialog
      title="订单结算"
      :visible.sync="checkoutDialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="orderForm" :rules="orderRules" ref="orderForm" label-width="100px">
        <el-form-item label="顾客姓名" prop="customerName">
          <el-input v-model="orderForm.customerName" placeholder="请输入顾客姓名"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="取餐方式" prop="takeType">
          <el-radio-group v-model="orderForm.takeType">
            <el-radio label="堂食">堂食</el-radio>
            <el-radio label="打包">打包</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input
            type="textarea"
            v-model="orderForm.remark"
            placeholder="特殊要求请备注"
            :rows="3"
          ></el-input>
        </el-form-item>
        <el-form-item label="订单明细">
          <el-table :data="cartItems" size="small" border>
            <el-table-column prop="name" label="商品" width="120"></el-table-column>
            <el-table-column prop="specsText" label="规格" width="150"></el-table-column>
            <el-table-column prop="quantity" label="数量" width="80"></el-table-column>
            <el-table-column prop="unitPrice" label="单价" width="80"></el-table-column>
            <el-table-column prop="totalPrice" label="小计" width="80"></el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="订单金额">
          <span class="order-total">¥{{ totalPrice }}</span>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="checkoutDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitOrder">确认下单</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { EventBus } from '@/utils/eventBus'
export default {
  name: 'Menu',
  data() {
    return {
      activeCategory: '1',
      categories: [
        {
          id: '1',
          name: '人气推荐',
          products: [
            { id: 1, name: '珍珠奶茶', price: 15, stock: 20, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=bubble%20milk%20tea%20drink%20product%20photo&image_size=square' },
            { id: 2, name: '杨枝甘露', price: 22, stock: 15, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=mango%20pomelo%20sago%20drink%20product%20photo&image_size=square' },
            { id: 3, name: '芝士奶盖茶', price: 18, stock: 5, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cheese%20foam%20tea%20drink%20product%20photo&image_size=square' }
          ]
        },
        {
          id: '2',
          name: '经典奶茶',
          products: [
            { id: 4, name: '原味奶茶', price: 12, stock: 30, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=original%20milk%20tea%20drink%20product%20photo&image_size=square' },
            { id: 5, name: '红豆奶茶', price: 14, stock: 0, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=red%20bean%20milk%20tea%20drink%20product%20photo&image_size=square' },
            { id: 6, name: '芋泥奶茶', price: 16, stock: 25, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=taro%20milk%20tea%20drink%20product%20photo&image_size=square' }
          ]
        },
        {
          id: '3',
          name: '鲜果茶',
          products: [
            { id: 7, name: '柠檬茶', price: 13, stock: 18, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=lemon%20tea%20drink%20product%20photo&image_size=square' },
            { id: 8, name: '满杯水果茶', price: 20, stock: 3, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=fruit%20tea%20drink%20product%20photo&image_size=square' },
            { id: 9, name: '百香果茶', price: 17, stock: 12, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=passion%20fruit%20tea%20drink%20product%20photo&image_size=square' }
          ]
        },
        {
          id: '4',
          name: '咖啡系列',
          products: [
            { id: 10, name: '拿铁咖啡', price: 20, stock: 22, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=latte%20coffee%20drink%20product%20photo&image_size=square' },
            { id: 11, name: '美式咖啡', price: 15, stock: 28, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=americano%20coffee%20drink%20product%20photo&image_size=square' },
            { id: 12, name: '卡布奇诺', price: 22, stock: 10, image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=cappuccino%20coffee%20drink%20product%20photo&image_size=square' }
          ]
        }
      ],
      sizes: [
        { label: '中杯', value: '中杯', price: 0 },
        { label: '大杯', value: '大杯', price: 3 }
      ],
      temperatures: [
        { label: '正常冰', value: '正常冰', price: 0 },
        { label: '少冰', value: '少冰', price: 0 },
        { label: '去冰', value: '去冰', price: 0 },
        { label: '温热', value: '温热', price: 0 },
        { label: '热饮', value: '热饮', price: 0 }
      ],
      sugars: [
        { label: '正常糖', value: '正常糖', price: 0 },
        { label: '七分糖', value: '七分糖', price: 0 },
        { label: '五分糖', value: '五分糖', price: 0 },
        { label: '三分糖', value: '三分糖', price: 0 },
        { label: '无糖', value: '无糖', price: 0 }
      ],
      toppings: [
        { label: '珍珠', value: '珍珠', price: 2 },
        { label: '椰果', value: '椰果', price: 2 },
        { label: '芋圆', value: '芋圆', price: 3 },
        { label: '奶盖', value: '奶盖', price: 5 }
      ],
      specDialogVisible: false,
      checkoutDialogVisible: false,
      selectedProduct: {},
      currentProduct: {
        size: '',
        temperature: '',
        sugar: '',
        toppings: [],
        quantity: 1
      },
      cartItems: [],
      orderForm: {
        customerName: '',
        phone: '',
        takeType: '堂食',
        remark: ''
      },
      orderRules: {
        customerName: [
          { required: true, message: '请输入顾客姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        takeType: [
          { required: true, message: '请选择取餐方式', trigger: 'change' }
        ]
      }
    }
  },
  created() {
    this.loadProductStocks()
  },
  computed: {
    sizePriceDiff() {
      const size = this.sizes.find(s => s.value === this.currentProduct.size)
      return size ? size.price : 0
    },
    toppingsTotalPrice() {
      return this.currentProduct.toppings.reduce((total, toppingValue) => {
        const topping = this.toppings.find(t => t.value === toppingValue)
        return total + (topping ? topping.price : 0)
      }, 0)
    },
    currentUnitPrice() {
      return (this.selectedProduct.price || 0) + this.sizePriceDiff + this.toppingsTotalPrice
    },
    currentTotalPrice() {
      return this.currentUnitPrice * this.currentProduct.quantity
    },
    totalPrice() {
      return this.cartItems.reduce((total, item) => total + item.totalPrice * item.quantity, 0)
    }
  },
  methods: {
    selectProduct(product) {
      if (product.stock <= 0) {
        this.$message.error(`${product.name} 已售罄，暂时无法选择`)
        return
      }
      this.selectedProduct = product
      this.currentProduct = {
        size: '中杯',
        temperature: '正常冰',
        sugar: '正常糖',
        toppings: [],
        quantity: 1
      }
      this.specDialogVisible = true
    },
    addToCart() {
      if (this.selectedProduct.stock <= 0) {
        this.$message.error(`${this.selectedProduct.name} 库存不足`)
        return
      }
      if (this.currentProduct.quantity > this.selectedProduct.stock) {
        this.$message.error(`${this.selectedProduct.name} 库存仅剩 ${this.selectedProduct.stock} 杯`)
        return
      }
      if (!this.currentProduct.size || !this.currentProduct.temperature || !this.currentProduct.sugar) {
        this.$message.warning('请选择完整的商品规格')
        return
      }
      const toppingsText = this.currentProduct.toppings.length > 0 
        ? ` +${this.currentProduct.toppings.join('/')}` 
        : ''
      const cartItem = {
        productId: this.selectedProduct.id,
        name: this.selectedProduct.name,
        specsText: `${this.currentProduct.size}/${this.currentProduct.temperature}/${this.currentProduct.sugar}${toppingsText}`,
        unitPrice: this.currentUnitPrice,
        totalPrice: this.currentTotalPrice,
        quantity: this.currentProduct.quantity,
        specs: { ...this.currentProduct }
      }
      this.cartItems.push(cartItem)
      this.specDialogVisible = false
      this.$message.success('已加入购物车')
    },
    removeCartItem(index) {
      this.cartItems.splice(index, 1)
    },
    clearCart() {
      this.$confirm('确定要清空购物车吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.cartItems = []
        this.$message.success('购物车已清空')
      }).catch(() => {})
    },
    updateTotal() {
      this.cartItems.forEach(item => {
        item.totalPrice = item.unitPrice * item.quantity
      })
    },
    showCheckoutDialog() {
      this.checkoutDialogVisible = true
      this.$nextTick(() => {
        this.$refs.orderForm.clearValidate()
      })
    },
    submitOrder() {
      this.$refs.orderForm.validate(valid => {
        if (valid) {
          for (const item of this.cartItems) {
            const category = this.categories.find(cat => 
              cat.products.some(p => p.id === item.productId)
            )
            if (category) {
              const product = category.products.find(p => p.id === item.productId)
              if (product && product.stock < item.quantity) {
                this.$message.error(`${product.name} 库存不足，仅剩 ${product.stock} 杯`)
                return
              }
            }
          }
          for (const item of this.cartItems) {
            const category = this.categories.find(cat => 
              cat.products.some(p => p.id === item.productId)
            )
            if (category) {
              const product = category.products.find(p => p.id === item.productId)
              if (product) {
                product.stock -= item.quantity
              }
            }
          }
          this.saveProductStocks()
          const order = {
            id: Date.now(),
            orderNo: 'ORD' + Date.now(),
            customerName: this.orderForm.customerName,
            phone: this.orderForm.phone,
            takeType: this.orderForm.takeType,
            remark: this.orderForm.remark,
            items: [...this.cartItems],
            totalAmount: this.totalPrice,
            status: 'pending',
            paymentStatus: 'paid',
            createTime: new Date().toLocaleString(),
            timestamp: Date.now()
          }
          let orders = JSON.parse(localStorage.getItem('milkTeaOrders') || '[]')
          orders.unshift(order)
          localStorage.setItem('milkTeaOrders', JSON.stringify(orders))
          this.checkoutDialogVisible = false
          this.cartItems = []
          this.orderForm = {
            customerName: '',
            phone: '',
            takeType: '堂食',
            remark: ''
          }
          EventBus.$emit('orderStatusChanged')
          EventBus.$emit('newOrder', order)
          this.$message.success(`下单成功！订单号：${order.orderNo}`)
          this.$router.push('/orders')
        }
      })
    },
    saveProductStocks() {
      const stockData = {}
      this.categories.forEach(category => {
        category.products.forEach(product => {
          stockData[product.id] = product.stock
        })
      })
      localStorage.setItem('milkTeaProductStocks', JSON.stringify(stockData))
    },
    loadProductStocks() {
      const stockData = JSON.parse(localStorage.getItem('milkTeaProductStocks') || '{}')
      this.categories.forEach(category => {
        category.products.forEach(product => {
          if (stockData[product.id] !== undefined) {
            product.stock = stockData[product.id]
          }
        })
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.menu-page {
  .menu-card {
    height: calc(100vh - 100px);
    ::v-deep .el-card__body {
      height: calc(100% - 57px);
      overflow-y: auto;
    }
    .product-col {
      margin-bottom: 15px;
      .product-card {
        cursor: pointer;
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        &.out-of-stock {
          cursor: not-allowed;
          opacity: 0.7;
          &:hover {
            transform: none;
            box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
          }
        }
        .product-image-wrapper {
          position: relative;
          .product-image {
            width: 100%;
            height: 120px;
            object-fit: cover;
            border-radius: 4px;
          }
          .out-of-stock-mask {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.6);
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            span {
              color: #fff;
              font-size: 16px;
              font-weight: bold;
            }
          }
        }
        .product-info {
          margin-top: 10px;
          .product-name {
            font-size: 14px;
            color: #303133;
            margin-bottom: 5px;
          }
          .product-price {
            font-size: 16px;
            font-weight: bold;
            color: #f56c6c;
            display: inline-block;
            margin-right: 10px;
          }
          .product-stock {
            font-size: 12px;
            color: #909399;
            &.stock-low {
              color: #e6a23c;
              font-weight: bold;
            }
          }
        }
      }
    }
  }
  .cart-card {
    height: calc(100vh - 100px);
    display: flex;
    flex-direction: column;
    ::v-deep .el-card__body {
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .cart-list {
      flex: 1;
      overflow-y: auto;
      padding-right: 5px;
      .cart-item {
        padding: 12px 0;
        border-bottom: 1px solid #ebeef5;
        display: flex;
        justify-content: space-between;
        align-items: center;
        &:last-child {
          border-bottom: none;
        }
        .cart-item-info {
          flex: 1;
          .cart-item-name {
            font-size: 14px;
            color: #303133;
            margin-bottom: 4px;
          }
          .cart-item-specs {
            font-size: 12px;
            color: #909399;
          }
        }
        .cart-item-right {
          display: flex;
          align-items: center;
          .cart-item-price {
            font-size: 14px;
            color: #f56c6c;
            font-weight: bold;
            margin-right: 10px;
            min-width: 50px;
            text-align: right;
          }
          .delete-btn {
            margin-left: 5px;
            color: #909399;
            &:hover {
              color: #f56c6c;
            }
          }
        }
      }
    }
    .cart-footer {
      border-top: 1px solid #ebeef5;
      padding-top: 15px;
      margin-top: 10px;
      .total-section {
        margin-bottom: 15px;
        font-size: 14px;
        .total-price {
          font-size: 24px;
          font-weight: bold;
          color: #f56c6c;
        }
      }
      .checkout-btn {
        width: 100%;
      }
    }
  }
}
.order-total {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}
.price-calculation {
  background: #f5f7fa;
  border-radius: 4px;
  padding: 10px 15px;
  .price-row {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
    font-size: 14px;
    color: #606266;
    &:last-child {
      margin-bottom: 0;
    }
    &.total-row {
      font-weight: bold;
      color: #303133;
      padding-top: 8px;
      border-top: 1px solid #ebeef5;
      .unit-price,
      .total-price {
        color: #f56c6c;
        font-size: 16px;
      }
    }
  }
}
</style>
