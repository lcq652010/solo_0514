<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <el-menu router default-active="1" class="el-menu-vertical-demo">
          <el-menu-item index="/statistics">
            <i class="el-icon-s-data"></i>
            <span slot="title">营业额统计</span>
          </el-menu-item>
          <el-menu-item index="/categories">
            <i class="el-icon-menu"></i>
            <span slot="title">菜品分类管理</span>
          </el-menu-item>
          <el-menu-item index="/dishes">
            <i class="el-icon-goods"></i>
            <span slot="title">菜品管理</span>
          </el-menu-item>
          <el-menu-item index="/orders">
            <i class="el-icon-s-order"></i>
            <span slot="title">订单列表</span>
          </el-menu-item>
          <el-menu-item index="/order-operations">
            <i class="el-icon-s-claim"></i>
            <span slot="title">接单出餐操作</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>商家管理员</span>
        </el-header>
        <el-main>
          <router-view />
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

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>