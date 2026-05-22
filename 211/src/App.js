window.App = {
  template: `
    <div class="app-container">
      <el-container>
        <el-header class="header">
          <div class="logo">
            <i class="el-icon-camera"></i>
            <span>光影摄影预订系统</span>
          </div>
          <el-menu
            mode="horizontal"
            :default-active="$route.path"
            class="nav-menu"
            router>
            <el-menu-item index="/packages">摄影套餐</el-menu-item>
            <el-menu-item index="/booking">预订表单</el-menu-item>
            <el-menu-item index="/schedule">摄影师档期</el-menu-item>
            <el-menu-item index="/orders">订单列表</el-menu-item>
            <el-menu-item index="/customers">客户档案</el-menu-item>
          </el-menu>
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
        <el-footer class="footer">
          <p>© 2024 光影摄影工作室 版权所有</p>
        </el-footer>
      </el-container>
    </div>
  `,
  name: 'App'
};
