<template>
  <div id="app">
    <el-container style="min-height: 100vh;">
      <el-header style="background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%); color: white; padding: 0 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; height: 100%;">
          <h2 style="margin: 0; display: flex; align-items: center;">
            <i class="el-icon-goods" style="margin-right: 10px; font-size: 24px;"></i>
            传统木雕书签定制系统
          </h2>
          <el-menu mode="horizontal" background-color="transparent" text-color="#fff" active-text-color="#FFD700" router>
            <el-menu-item index="/order">
              <i class="el-icon-edit"></i>
              客户下单
            </el-menu-item>
            <el-menu-item index="/admin">
              <i class="el-icon-s-order"></i>
              订单管理
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main style="background-color: #f5f5f5; padding: 30px;">
        <router-view></router-view>
      </el-main>
      <el-footer style="background: #8B4513; color: white; text-align: center; line-height: 60px;">
        © 2024 传统木雕工艺坊 - 匠心独运，精雕细琢
      </el-footer>
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

body {
  font-family: 'Microsoft YaHei', sans-serif;
}

#app {
  min-height: 100vh;
}
</style>
