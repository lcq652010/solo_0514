<template>
  <el-container style="height: 100%">
    <el-aside width="200px" style="background-color: #2f4050">
      <div class="logo">
        <h3>超市库存管理</h3>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        background-color="#2f4050"
        text-color="#a7b1c2"
        active-text-color="#fff"
        router
      >
        <el-menu-item index="/stock-in">
          <i class="el-icon-plus"></i>
          <span slot="title">商品入库</span>
        </el-menu-item>
        <el-menu-item index="/product-list">
          <i class="el-icon-goods"></i>
          <span slot="title">商品列表</span>
        </el-menu-item>
        <el-menu-item index="/stock-query">
          <i class="el-icon-search"></i>
          <span slot="title">库存查询</span>
        </el-menu-item>
        <el-menu-item index="/stock-warning">
          <i class="el-icon-warning"></i>
          <span slot="title">库存预警</span>
        </el-menu-item>
        <el-menu-item index="/inventory-records">
          <i class="el-icon-document"></i>
          <span slot="title">出入库记录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background-color: #fff; border-bottom: 1px solid #e6e6e6; padding: 0 20px">
        <div class="header-content">
          <span class="breadcrumb">{{ currentPageTitle }}</span>
          <div class="user-info">
            <span>管理员</span>
          </div>
        </div>
      </el-header>
      <el-main style="background-color: #f5f7fa; padding: 20px">
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
    currentPageTitle() {
      return this.$route.meta.title || '首页'
    }
  }
}
</script>

<style scoped>
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #243443;
}

.logo h3 {
  color: #fff;
  font-size: 16px;
  font-weight: 500;
}

.el-menu-vertical-demo {
  border-right: none;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.breadcrumb {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.user-info {
  color: #606266;
}
</style>
