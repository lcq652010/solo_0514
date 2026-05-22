<template>
  <div id="app">
    <el-container style="height: 100vh;">
      <el-header style="background: #409EFF; color: #fff; padding: 0 20px;">
        <div style="display: flex; align-items: center; height: 100%;">
          <h2 style="margin: 0; font-size: 20px;">考试报名系统</h2>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" style="background: #fff; border-right: 1px solid #e6e6e6;">
          <el-menu
            :default-active="$route.path"
            class="el-menu-vertical"
            router
            style="border-right: none;"
          >
            <el-menu-item index="/">
              <i class="el-icon-document"></i>
              <span>考试科目</span>
            </el-menu-item>
            <el-menu-item index="/apply">
              <i class="el-icon-edit"></i>
              <span>我要报名</span>
            </el-menu-item>
            <el-menu-item index="/review">
              <i class="el-icon-s-check"></i>
              <span>资格审核</span>
            </el-menu-item>
            <el-menu-item index="/ticket">
              <i class="el-icon-tickets"></i>
              <span>准考证</span>
            </el-menu-item>
            <el-menu-item index="/records">
              <i class="el-icon-s-data"></i>
              <span>报名记录</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main style="background: #f5f7fa; padding: 20px;">
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

<style>
.el-header {
  display: flex;
  align-items: center;
}

.el-menu-vertical {
  height: 100%;
}
</style>
