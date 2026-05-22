<template>
  <el-container style="height: 100%">
    <el-aside width="200px" style="background-color: #304156;">
      <div class="logo">
        <h2 style="color: #fff; text-align: center; padding: 20px 0; font-size: 18px;">酒店预订系统</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical-demo"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
        router
      >
        <el-menu-item index="/room-types">
          <i class="el-icon-house"></i>
          <span slot="title">房型展示</span>
        </el-menu-item>
        <el-menu-item index="/booking">
          <i class="el-icon-edit-outline"></i>
          <span slot="title">预订登记</span>
        </el-menu-item>
        <el-menu-item index="/check-in">
          <i class="el-icon-s-check"></i>
          <span slot="title">入住登记</span>
        </el-menu-item>
        <el-menu-item index="/orders">
          <i class="el-icon-document"></i>
          <span slot="title">订单列表</span>
        </el-menu-item>
        <el-menu-item index="/room-status">
          <i class="el-icon-menu"></i>
          <span slot="title">房态管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background-color: #fff; border-bottom: 1px solid #e4e7ed; display: flex; align-items: center; justify-content: space-between; padding: 0 20px;">
        <div style="font-size: 18px; font-weight: 500;">{{ pageTitle }}</div>
        <div style="display: flex; align-items: center;">
          <el-dropdown>
            <span class="el-dropdown-link" style="cursor: pointer;">
              <i class="el-icon-user" style="margin-right: 5px;"></i>管理员
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人信息</el-dropdown-item>
              <el-dropdown-item>修改密码</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>
      <el-main style="background-color: #f5f7fa; padding: 20px; margin: 0;">
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
    pageTitle() {
      const titleMap = {
        '/room-types': '房型展示',
        '/booking': '预订登记',
        '/check-in': '入住登记',
        '/orders': '订单列表',
        '/room-status': '房态管理'
      }
      return titleMap[this.$route.path] || '酒店预订系统'
    }
  }
}
</script>

<style scoped>
.el-aside {
  overflow: hidden;
}

.logo {
  border-bottom: 1px solid #1f2d3d;
}

.el-menu {
  border-right: none;
}
</style>
