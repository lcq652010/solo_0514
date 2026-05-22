<template>
  <div class="dishes-page">
    <div class="page-container">
      <div class="page-header">
        <h2 class="page-title">菜品列表</h2>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索菜品名称..."
          style="width: 240px"
          clearable
          prefix-icon="el-icon-search"
        />
      </div>

      <div class="dishes-content">
        <div class="category-sidebar">
          <div class="category-title">菜品分类</div>
          <el-menu
            :default-active="activeCategory"
            class="category-menu"
            @select="handleCategorySelect"
          >
            <el-menu-item
              v-for="cat in categories"
              :key="cat.id"
              :index="String(cat.id)"
            >
              {{ cat.name }}
            </el-menu-item>
          </el-menu>
        </div>

        <div class="dishes-grid">
          <div v-if="filteredDishes.length === 0" class="empty-state">
            <i class="el-icon-goods"></i>
            <p>暂无相关菜品</p>
          </div>
          <div
            v-for="dish in filteredDishes"
            :key="dish.id"
            class="dish-card"
            :class="{ 'sold-out': dish.stock <= 0 }"
          >
            <div class="dish-image">
              <img :src="dish.image" :alt="dish.name" />
              <div class="dish-rating">
                <i class="el-icon-star-on"></i>
                {{ dish.rating }}
              </div>
              <div v-if="dish.stock <= 0" class="sold-out-mask">
                <span>已售罄</span>
              </div>
            </div>
            <div class="dish-info">
              <div class="dish-name">{{ dish.name }}</div>
              <div class="dish-desc">{{ dish.description }}</div>
              <div class="dish-stats">
                <span>月售 {{ dish.sales }} 份</span>
                <span :class="{ 'stock-warning': dish.stock > 0 && dish.stock <= 10, 'stock-soldout': dish.stock <= 0 }">
                  <i class="el-icon-box"></i>
                  {{ dish.stock > 0 ? `库存 ${dish.stock}` : '已售罄' }}
                </span>
              </div>
              <div class="dish-footer">
                <div class="dish-price">
                  <span class="price-symbol">¥</span>
                  <span class="price-value">{{ dish.price }}</span>
                </div>
                <div class="dish-actions">
                  <template v-if="dish.stock <= 0">
                    <el-button
                      type="info"
                      size="small"
                      disabled
                    >
                      已售罄
                    </el-button>
                  </template>
                  <template v-else-if="getCartQuantity(dish.id) === 0">
                    <el-button
                      type="primary"
                      size="small"
                      icon="el-icon-plus"
                      circle
                      @click="handleAddToCart(dish)"
                    />
                  </template>
                  <div v-else class="quantity-control">
                    <el-button
                      type="danger"
                      size="small"
                      icon="el-icon-minus"
                      circle
                      @click="removeFromCart(dish.id)"
                    />
                    <span class="quantity">{{ getCartQuantity(dish.id) }}</span>
                    <el-button
                      type="primary"
                      size="small"
                      icon="el-icon-plus"
                      circle
                      :disabled="getCartQuantity(dish.id) >= dish.stock"
                      @click="handleAddToCart(dish)"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="cartTotal > 0" class="cart-bar">
        <div class="cart-info">
          <div class="cart-icon-wrapper">
            <i class="el-icon-shopping-cart-2"></i>
            <el-badge :value="cartCount" class="cart-badge" />
          </div>
          <div class="cart-total">
            <span class="total-label">合计：</span>
            <span class="total-price">¥ {{ cartTotal.toFixed(2) }}</span>
          </div>
        </div>
        <el-button type="primary" @click="goToCheckout">去结算</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { categories } from '@/mock/data'
import { mapState, mapGetters, mapActions } from 'vuex'

export default {
  name: 'Dishes',
  data() {
    return {
      categories,
      activeCategory: '1',
      searchKeyword: ''
    }
  },
  computed: {
    ...mapState(['dishes', 'cart']),
    ...mapGetters(['cartTotal', 'cartCount']),
    filteredDishes() {
      let result = this.dishes
      if (this.activeCategory !== '1') {
        result = result.filter(d => d.categoryId === Number(this.activeCategory))
      }
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        result = result.filter(d => d.name.toLowerCase().includes(keyword))
      }
      return result
    }
  },
  methods: {
    ...mapActions(['addToCart', 'removeFromCart']),
    handleCategorySelect(index) {
      this.activeCategory = index
    },
    getCartQuantity(dishId) {
      const item = this.cart.find(i => i.id === dishId)
      return item ? item.quantity : 0
    },
    handleAddToCart(dish) {
      const currentQty = this.getCartQuantity(dish.id)
      if (currentQty >= dish.stock) {
        this.$message.warning(`商品「${dish.name}」库存不足，最多可购买 ${dish.stock} 份`)
        return
      }
      this.addToCart(dish)
    },
    goToCheckout() {
      this.$router.push('/checkout')
    }
  }
}
</script>

<style scoped>
.dishes-content {
  display: flex;
  gap: 24px;
}
.category-sidebar {
  width: 160px;
  flex-shrink: 0;
}
.category-title {
  font-size: 16px;
  font-weight: 600;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 4px 4px 0 0;
}
.category-menu {
  border-right: none;
}
.dishes-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 20px;
}
.dish-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
.dish-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
.dish-image {
  position: relative;
  height: 140px;
  overflow: hidden;
}
.dish-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.dish-rating {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.6);
  color: #ffd700;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
}
.dish-info {
  padding: 12px;
}
.dish-name {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
  color: #303133;
}
.dish-desc {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
  line-height: 1.4;
  height: 32px;
  overflow: hidden;
}
.dish-sales {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
}
.dish-stats {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
}
.dish-stats .stock-warning {
  color: #e6a23c;
}
.dish-stats .stock-soldout {
  color: #f56c6c;
}
.dish-stats i {
  margin-right: 2px;
}
.sold-out {
  opacity: 0.7;
}
.sold-out .dish-image {
  position: relative;
}
.sold-out-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
}
.sold-out-mask span {
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  background: #f56c6c;
  padding: 4px 16px;
  border-radius: 4px;
  transform: rotate(-15deg);
}
.dish-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dish-price {
  display: flex;
  align-items: baseline;
}
.price-symbol {
  font-size: 12px;
  color: #f56c6c;
}
.price-value {
  font-size: 20px;
  font-weight: bold;
  color: #f56c6c;
}
.quantity-control {
  display: flex;
  align-items: center;
  gap: 8px;
}
.quantity {
  min-width: 20px;
  text-align: center;
  font-size: 14px;
}
.cart-bar {
  position: fixed;
  bottom: 24px;
  left: 264px;
  right: 24px;
  background: #fff;
  border-radius: 8px;
  padding: 12px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  z-index: 100;
}
.cart-info {
  display: flex;
  align-items: center;
  gap: 16px;
}
.cart-icon-wrapper {
  position: relative;
  font-size: 28px;
  color: #409eff;
}
.cart-badge {
  position: absolute;
  top: -8px;
  right: -8px;
}
.total-label {
  color: #606266;
}
.total-price {
  font-size: 22px;
  font-weight: bold;
  color: #f56c6c;
}
</style>
