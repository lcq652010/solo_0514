<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-header style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 30px;">
        <div style="display: flex; align-items: center;">
          <i class="el-icon-box" style="font-size: 28px; margin-right: 15px;"></i>
          <h1 style="font-size: 22px; font-weight: 600; margin: 0;">物资领用管理系统</h1>
        </div>
        <div style="display: flex; align-items: center;">
          <span style="margin-right: 20px;">
            <i class="el-icon-user-solid"></i>
            管理员
          </span>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" style="background-color: #fff; border-right: 1px solid #e6e6e6;">
          <el-menu
            :default-active="$route.path"
            class="el-menu-vertical"
            router
            background-color="#fff"
            text-color="#303133"
            active-text-color="#409eff"
            style="border-right: none;"
          >
            <el-menu-item index="/materials">
              <i class="el-icon-goods"></i>
              <span slot="title">物资列表</span>
            </el-menu-item>
            <el-menu-item index="/apply">
              <i class="el-icon-edit-outline"></i>
              <span slot="title">领用申请</span>
            </el-menu-item>
            <el-menu-item index="/return">
              <i class="el-icon-refresh-left"></i>
              <span slot="title">归还登记</span>
            </el-menu-item>
            <el-menu-item index="/records">
              <i class="el-icon-document"></i>
              <span slot="title">领用记录</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main style="background-color: #f5f7fa; padding: 20px;">
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

<style lang="scss" scoped>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.el-menu-item {
  &:hover {
    background-color: #ecf5ff !important;
  }
}

.el-menu-item.is-active {
  background-color: #ecf5ff !important;
  border-right: 3px solid #409eff;
}
</style>
