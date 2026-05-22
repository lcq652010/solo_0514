<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-header class="header">
        <h1 class="title">餐饮后厨管理系统</h1>
        <div class="header-time">{{ currentTime }}</div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="sidebar">
          <el-menu
            :default-active="$route.path"
            class="menu"
            router
            background-color="#304156"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
          >
            <el-menu-item index="/order-list">
              <i class="el-icon-notebook-2"></i>
              <span>订单菜品列表</span>
            </el-menu-item>
            <el-menu-item index="/kitchen-schedule">
              <i class="el-icon-s-order"></i>
              <span>后厨排菜</span>
            </el-menu-item>
            <el-menu-item index="/serve-confirm">
              <i class="el-icon-check-circle"></i>
              <span>出餐确认</span>
            </el-menu-item>
            <el-menu-item index="/cooking-status">
              <i class="el-icon-time"></i>
              <span>制作状态</span>
            </el-menu-item>
            <el-menu-item index="/urgent-reminder">
              <i class="el-icon-warning"></i>
              <span slot="title">催单提醒</span>
              <el-badge :value="urgentCount" class="item" v-if="urgentCount > 0"></el-badge>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      currentTime: '',
      timer: null
    }
  },
  computed: {
    urgentCount() {
      const orders = this.$router.app.$children.find(c => c.$options.name === 'OrderList')?.orders || []
      return orders.filter(o => o.urgency && o.status !== 'done').length
    }
  },
  mounted() {
    this.updateTime()
    this.timer = setInterval(this.updateTime, 1000)
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer)
    }
  },
  methods: {
    updateTime() {
      const now = new Date()
      this.currentTime = now.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}
</style>
