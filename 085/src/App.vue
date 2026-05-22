<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="title">
            <i class="el-icon-s-goods"></i>
            快递代收代寄系统
          </h1>
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
            :default-active="$route.path"
            class="menu"
            router
            background-color="#545c64"
            text-color="#fff"
            active-text-color="#ffd04b"
          >
            <el-menu-item index="/inbound">
              <i class="el-icon-download"></i>
              <span>快递入库</span>
            </el-menu-item>
            <el-menu-item index="/outbound">
              <i class="el-icon-upload"></i>
              <span>快递出库签收</span>
            </el-menu-item>
            <el-menu-item index="/send">
              <i class="el-icon-s-promotion"></i>
              <span>寄件登记</span>
            </el-menu-item>
            <el-menu-item index="/list">
              <i class="el-icon-search"></i>
              <span>快递查询</span>
            </el-menu-item>
            <el-menu-item index="/pickup">
              <i class="el-icon-tickets"></i>
              <span>取件码展示</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
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
  height: 100vh;
}

.el-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  padding: 0 20px;
  height: 60px !important;
}

.header-content .title {
  font-size: 22px;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 10px;
}

.el-aside {
  background-color: #545c64;
  height: calc(100vh - 60px);
}

.menu {
  border: none;
}

.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}

.page-card {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 20px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e4e7ed;
}
</style>
