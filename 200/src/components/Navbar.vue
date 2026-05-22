<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand">
        <span class="brand-icon">砚</span>
        <span class="brand-text">石砚定制系统</span>
      </div>
      <div class="navbar-menu">
        <router-link 
          :to="{ name: 'OrderForm' }" 
          :class="['nav-item', { active: $route.name === 'OrderForm' }]"
        >
          <i class="el-icon-user"></i>
          <span>客户下单</span>
        </router-link>
        <router-link 
          :to="{ name: 'OrderList' }" 
          :class="['nav-item', { active: $route.name === 'OrderList' }]"
        >
          <i class="el-icon-s-tools"></i>
          <span>管理员订单</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'Navbar'
}
</script>

<style scoped>
.navbar {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  color: #fff;
  height: 60px;
  line-height: 60px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  font-size: 32px;
  font-weight: bold;
  color: #F5F5DC;
}

.brand-text {
  font-size: 18px;
  font-weight: 600;
}

.navbar-menu {
  display: flex;
  gap: 20px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 0 15px;
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.nav-item.active {
  background-color: rgba(255, 255, 255, 0.2);
  color: #fff;
}

.nav-item i {
  font-size: 16px;
}
</style>
