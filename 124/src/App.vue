<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee;">
      <el-aside width="200px" style="background-color: #2E3B4E;">
        <div class="logo">
          <h3 style="color: white; text-align: center; padding: 20px 0;">宠物店管理系统</h3>
        </div>
        <el-menu
          :default-active="$route.path"
          class="el-menu-vertical-demo"
          background-color="#2E3B4E"
          text-color="#fff"
          active-text-color="#ffd04b"
          router
        >
          <el-menu-item index="/services">
            <i class="el-icon-goods"></i>
            <span slot="title">洗护服务套餐</span>
          </el-menu-item>
          <el-menu-item index="/appointment">
            <i class="el-icon-edit"></i>
            <span slot="title">宠物预约表单</span>
          </el-menu-item>
          <el-menu-item index="/members">
            <i class="el-icon-user"></i>
            <span slot="title">会员信息管理</span>
          </el-menu-item>
          <el-menu-item index="/appointments">
            <i class="el-icon-date"></i>
            <span slot="title">预约记录列表</span>
          </el-menu-item>
          <el-menu-item index="/checkout">
            <i class="el-icon-s-order"></i>
            <span slot="title">结算收银</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="background-color: #fff; border-bottom: 1px solid #eee; display: flex; align-items: center; justify-content: flex-end; padding-right: 20px;">
          <el-dropdown>
            <span class="el-dropdown-link" style="cursor: pointer;">
              <i class="el-icon-user-solid"></i> 管理员
              <i class="el-icon-arrow-down el-icon--right"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-header>
        <el-main style="background-color: #f5f7fa;">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body, html {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

#app {
  height: 100%;
}

.el-menu-vertical-demo {
  border-right: none;
}

.el-dropdown-link {
  color: #606266;
}

.page-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #303133;
}

.card-wrapper {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}
</style>
