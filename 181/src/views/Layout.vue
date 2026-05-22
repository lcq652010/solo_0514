<template>
  <el-container style="height: 100vh;">
    <el-aside width="220px" style="background-color: #304156;">
      <div class="logo">
        <i class="el-icon-s-shop"></i>
        <span>快递驿站管理</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        class="el-menu-vertical"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        router
      >
        <el-menu-item index="/send-order">
          <i class="el-icon-edit-outline"></i>
          <span slot="title">寄件下单</span>
        </el-menu-item>
        <el-menu-item index="/pickup-verify">
          <i class="el-icon-check"></i>
          <span slot="title">取件核销</span>
        </el-menu-item>
        <el-menu-item index="/package-inbound">
          <i class="el-icon-download"></i>
          <span slot="title">包裹入库</span>
        </el-menu-item>
        <el-menu-item index="/package-list">
          <i class="el-icon-s-goods"></i>
          <span slot="title">包裹列表</span>
        </el-menu-item>
        <el-menu-item index="/member-manage">
          <i class="el-icon-user"></i>
          <span slot="title">会员管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background: #fff; border-bottom: 1px solid #e6e6e6; padding: 0 20px;">
        <div class="header-content">
          <div class="header-title">{{ pageTitle }}</div>
          <div class="header-user">
            <el-dropdown>
              <span class="el-dropdown-link">
                <i class="el-icon-user-solid"></i>
                管理员
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item>个人中心</el-dropdown-item>
                <el-dropdown-item>修改密码</el-dropdown-item>
                <el-dropdown-item divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
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
      return this.$route.meta.title || '快递驿站管理系统'
    }
  }
}
</script>

<style scoped>
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  border-bottom: 1px solid #1f2d3d;
}

.logo i {
  font-size: 24px;
  margin-right: 10px;
}

.el-menu-vertical {
  border: none;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.header-user {
  display: flex;
  align-items: center;
}

.el-dropdown-link {
  cursor: pointer;
  color: #303133;
  display: flex;
  align-items: center;
}

.el-dropdown-link i {
  margin: 0 5px;
}
</style>
