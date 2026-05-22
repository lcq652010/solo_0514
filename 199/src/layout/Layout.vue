<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="sidebar">
      <div class="logo">
        <i class="el-icon-food"></i>
        <span>外卖管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item
          v-for="route in menuRoutes"
          :key="route.path"
          :index="'/' + route.path"
        >
          <i :class="route.meta.icon"></i>
          <span slot="title">{{ route.meta.title }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <span class="page-title">{{ currentPageTitle }}</span>
        </div>
        <div class="header-right">
          <el-badge :value="cartCount" class="cart-badge" v-if="cartCount > 0">
            <el-button type="text" @click="$router.push('/checkout')">
              <i class="el-icon-shopping-cart-2"></i> 购物车
            </el-button>
          </el-badge>
          <span class="user-info">
            <i class="el-icon-user-solid"></i> 管理员
          </span>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'Layout',
  computed: {
    activeMenu() {
      return this.$route.path
    },
    menuRoutes() {
      return this.$router.options.routes[0].children
    },
    currentPageTitle() {
      return this.$route.meta.title || ''
    },
    cartCount() {
      return this.$store.state.cart.reduce((sum, item) => sum + item.quantity, 0)
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.sidebar {
  background-color: #304156;
  overflow: hidden;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background-color: #2b2f3a;
}
.logo i {
  font-size: 24px;
  margin-right: 8px;
}
.sidebar-menu {
  border-right: none;
}
.header {
  background-color: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}
.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}
.user-info {
  color: #606266;
}
.user-info i {
  margin-right: 5px;
}
.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
.cart-badge {
  margin-right: 10px;
}
</style>
