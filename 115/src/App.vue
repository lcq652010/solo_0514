<template>
  <div id="app">
    <el-container style="height: 100vh">
      <el-header style="background: #409EFF; color: white; padding: 0 20px;">
        <div style="display: flex; align-items: center; height: 100%;">
          <h2 style="margin: 0; font-size: 20px;">📚 图书馆座位预约系统</h2>
          <div style="flex: 1;"></div>
          <span style="margin-right: 20px;">欢迎，{{ userName }}</span>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" style="background: #f5f5f5;">
          <el-menu
            :default-active="$route.path"
            class="el-menu-vertical"
            router
            style="border-right: none;"
          >
            <el-menu-item index="/">
              <i class="el-icon-location"></i>
              <span>座位分布图</span>
            </el-menu-item>
            <el-menu-item index="/reservation">
              <i class="el-icon-edit"></i>
              <span>在线预约</span>
            </el-menu-item>
            <el-menu-item index="/my-reservations">
              <i class="el-icon-document"></i>
              <span>我的预约</span>
            </el-menu-item>
            <el-menu-item index="/check-in">
              <i class="el-icon-success"></i>
              <span>签到确认</span>
            </el-menu-item>
            <el-menu-item index="/violations">
              <i class="el-icon-warning"></i>
              <span>违规记录</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main style="background: #fff; padding: 20px;">
          <router-view></router-view>
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
      userName: '张三'
    };
  }
};
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

#app {
  height: 100%;
}

.el-header {
  display: flex;
  align-items: center;
}

.el-menu-vertical {
  height: 100%;
}
</style>
