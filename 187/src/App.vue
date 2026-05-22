<template>
  <div id="app">
    <el-container class="layout-container">
      <el-header class="layout-header">
        <div class="header-title">
          <i class="el-icon-s-shop"></i>
          建材订单管理系统
        </div>
      </el-header>
      <el-container>
        <el-aside width="200px" class="layout-aside">
          <el-menu
            :default-active="$route.path"
            class="aside-menu"
            router
            background-color="#304156"
            text-color="#bfcbd9"
            active-text-color="#409EFF"
          >
            <el-menu-item index="/products">
              <i class="el-icon-goods"></i>
              <span slot="title">商品列表</span>
            </el-menu-item>
            <el-menu-item index="/order-create">
              <i class="el-icon-edit"></i>
              <span slot="title">订单下单</span>
            </el-menu-item>
            <el-menu-item index="/delivery">
              <i class="el-icon-truck"></i>
              <span slot="title">发货登记</span>
            </el-menu-item>
            <el-menu-item index="/orders">
              <i class="el-icon-document"></i>
              <span slot="title">订单记录</span>
            </el-menu-item>
            <el-menu-item index="/stock-warning">
              <i class="el-icon-warning"></i>
              <span slot="title">库存预警</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        <el-main class="layout-main">
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

<style lang="less">
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100vh;
}

.layout-container {
  height: 100%;
  
  .layout-header {
    background: #fff;
    box-shadow: 0 1px 4px rgba(0,21,41,.08);
    display: flex;
    align-items: center;
    padding: 0 20px;
    
    .header-title {
      font-size: 20px;
      font-weight: 600;
      color: #303133;
      
      i {
        margin-right: 10px;
        color: #409EFF;
      }
    }
  }
  
  .layout-aside {
    background: #304156;
    
    .aside-menu {
      border: none;
      
      .el-menu-item {
        &:hover {
          background-color: #263445 !important;
        }
        
        &.is-active {
          background-color: #409EFF !important;
          color: #fff !important;
        }
      }
    }
  }
  
  .layout-main {
    background: #f0f2f5;
    padding: 20px;
  }
}
</style>
