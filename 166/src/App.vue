<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <i class="el-icon-reading"></i>
          <span>二手书系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          router
        >
          <el-menu-item index="/book-entry">
            <i class="el-icon-edit-outline"></i>
            <span slot="title">书籍录入</span>
          </el-menu-item>
          <el-menu-item index="/pricing">
            <i class="el-icon-price-tag"></i>
            <span slot="title">回收定价</span>
          </el-menu-item>
          <el-menu-item index="/book-list">
            <i class="el-icon-s-goods"></i>
            <span slot="title">书籍上架</span>
          </el-menu-item>
          <el-menu-item index="/order">
            <i class="el-icon-s-order"></i>
            <span slot="title">订单购买</span>
          </el-menu-item>
          <el-menu-item index="/recycle-records">
            <i class="el-icon-document"></i>
            <span slot="title">回收记录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-title">{{ pageTitle }}</div>
        </el-header>
        <el-main class="main-content">
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
    },
    pageTitle() {
      const titleMap = {
        '/book-entry': '书籍录入',
        '/pricing': '回收定价',
        '/book-list': '书籍上架列表',
        '/order': '订单购买',
        '/recycle-records': '回收记录列表'
      }
      return titleMap[this.$route.path] || '二手书回收售卖系统'
    }
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
</style>
