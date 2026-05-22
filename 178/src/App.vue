<template>
  <div id="app">
    <el-container style="height: 100%">
      <el-aside width="200px" style="background-color: #2f4050">
        <div class="logo">
          <h3>图书管理系统</h3>
        </div>
        <el-menu
          default-active="$route.path"
          class="el-menu-vertical"
          router
          background-color="#2f4050"
          text-color="#fff"
          active-text-color="#1890ff"
        >
          <el-menu-item index="/books">
            <i class="el-icon-document"></i>
            <span slot="title">图书列表</span>
          </el-menu-item>
          <el-menu-item index="/borrow/apply">
            <i class="el-icon-edit"></i>
            <span slot="title">借阅申请</span>
          </el-menu-item>
          <el-menu-item index="/borrow/records">
            <i class="el-icon-s-order"></i>
            <span slot="title">借阅记录</span>
          </el-menu-item>
          <el-menu-item index="/return">
            <i class="el-icon-refresh"></i>
            <span slot="title">图书归还</span>
          </el-menu-item>
          <el-menu-item index="/overdue">
            <i class="el-icon-warning"></i>
            <span slot="title">逾期提醒</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="background: #fff; border-bottom: 1px solid #e6e6e6; padding: 0 20px; display: flex; align-items: center; justify-content: flex-end;">
          <span>欢迎使用图书管理系统</span>
        </el-header>
        <el-main style="background-color: #f5f7fa; padding: 0;">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid #1f2d3d;
}

.el-menu-vertical {
  border: none;
}
</style>