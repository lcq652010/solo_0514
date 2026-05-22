<template>
  <el-container style="height: 100%">
    <el-aside width="220px" style="background-color: #2f4050;">
      <div class="logo">
        <h2>培训机构管理</h2>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        background-color="#2f4050"
        text-color="#b8c7ce"
        active-text-color="#fff"
      >
        <el-menu-item index="/students">
          <i class="el-icon-user"></i>
          <span slot="title">学员列表</span>
        </el-menu-item>
        <el-menu-item index="/attendance">
          <i class="el-icon-time"></i>
          <span slot="title">考勤签到</span>
        </el-menu-item>
        <el-menu-item index="/deductions">
          <i class="el-icon-document"></i>
          <span slot="title">课时扣费记录</span>
        </el-menu-item>
        <el-menu-item index="/schedule">
          <i class="el-icon-date"></i>
          <span slot="title">班级课程表</span>
        </el-menu-item>
        <el-menu-item index="/recharge">
          <i class="el-icon-credit-card"></i>
          <span slot="title">续费充值</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="background-color: #fff; border-bottom: 1px solid #e6e6e6; padding: 0 20px;">
        <div class="header-content">
          <span class="page-title">{{ pageTitle }}</span>
          <span class="user-info">管理员</span>
        </div>
      </el-header>
      <el-main style="background-color: #f5f7fa; padding: 20px;">
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
      return this.$route.path;
    },
    pageTitle() {
      return this.$route.meta.title || '管理系统';
    }
  }
};
</script>

<style scoped>
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #243447;
}
.logo h2 {
  color: #fff;
  font-size: 18px;
  margin: 0;
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}
.header-content .page-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}
.header-content .user-info {
  color: #606266;
}
.el-menu-item {
  font-size: 14px;
}
</style>
