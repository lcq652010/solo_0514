<template>
  <div id="app">
    <el-container style="height: 100vh; border: 1px solid #eee">
      <el-aside width="200px" style="background-color: rgb(238, 241, 246)">
        <div class="logo">
          <h3>加班审批系统</h3>
        </div>
        <el-menu router :default-active="$route.path" class="el-menu-vertical-demo">
          <el-menu-item index="/apply">
            <i class="el-icon-edit"></i>
            <span slot="title">加班申请</span>
          </el-menu-item>
          <el-menu-item index="/my-records">
            <i class="el-icon-document"></i>
            <span slot="title">我的加班记录</span>
          </el-menu-item>
          <el-menu-item index="/approval-list">
            <i class="el-icon-s-check"></i>
            <span slot="title">部门审批列表</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <i class="el-icon-data-line"></i>
            <span slot="title">加班时长统计</span>
          </el-menu-item>
          <el-menu-item index="/ledger">
            <i class="el-icon-s-data"></i>
            <span slot="title">个人加班台账</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人信息</el-dropdown-item>
              <el-dropdown-item>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
          <span>张三</span>
        </el-header>
        <el-main>
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
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  background-color: #409EFF;
  color: white;
  font-size: 16px;
  font-weight: bold;
}

.el-menu {
  border-right: none;
}
</style>
