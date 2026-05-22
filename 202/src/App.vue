<template>
  <el-container style="height: 100vh;">
    <el-header>
      <div class="logo">💧⚡ 校园水电管理系统</div>
      <el-menu
        theme="dark"
        mode="horizontal"
        :router="true"
        :default-active="$route.path"
        background-color="#409EFF"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="/dormitory">宿舍选择</el-menu-item>
        <el-menu-item index="/recharge">水电充值</el-menu-item>
        <el-menu-item index="/statistics">用量统计</el-menu-item>
        <el-menu-item index="/records">充值记录</el-menu-item>
        <el-menu-item index="/warning">余额预警</el-menu-item>
      </el-menu>
      <div style="margin-left: auto;">
        <span>当前宿舍：{{ currentDormitory || '未选择' }}</span>
      </div>
    </el-header>
    <el-container>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'App',
  computed: {
    currentDormitory() {
      return this.$store && this.$store.state.currentDormitory
        ? this.$store.state.currentDormitory
        : localStorage.getItem('currentDormitory') || ''
    }
  }
}
</script>

<style scoped>
.el-header {
  background-color: #409EFF;
  color: #fff;
  display: flex;
  align-items: center;
}

.logo {
  font-size: 20px;
  font-weight: 600;
  margin-right: 50px;
}

.el-menu--horizontal {
  border-bottom: none;
}
</style>
