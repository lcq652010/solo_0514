<template>
  <div class="layout-container">
    <el-container style="height: 100%">
      <el-aside width="200px" class="sidebar">
        <div class="logo">
          <i class="el-icon-s-organization"></i>
          <span>培训管理系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          class="sidebar-menu"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          router
        >
          <el-menu-item index="/courses">
            <i class="el-icon-notebook-2"></i>
            <span slot="title">课程列表</span>
          </el-menu-item>
          <el-menu-item index="/schedule">
            <i class="el-icon-date"></i>
            <span slot="title">班级排课</span>
          </el-menu-item>
          <el-menu-item index="/students">
            <i class="el-icon-user"></i>
            <span slot="title">学员花名册</span>
          </el-menu-item>
          <el-menu-item index="/attendance">
            <i class="el-icon-circle-check"></i>
            <span slot="title">考勤打卡</span>
          </el-menu-item>
          <el-menu-item index="/statistics">
            <i class="el-icon-data-line"></i>
            <span slot="title">考勤统计</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <span class="breadcrumb-title">{{ currentTitle }}</span>
          </div>
          <div class="header-right">
            <span class="user-info">
              <i class="el-icon-user-solid"></i>
              管理员
            </span>
          </div>
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'Layout',
  computed: {
    activeMenu() {
      return this.$route.path
    },
    currentTitle() {
      return this.$route.meta.title || '培训管理系统'
    }
  }
}
</script>

<style scoped lang="scss">
.layout-container {
  height: 100%;
}

.sidebar {
  background-color: #304156;
  overflow: hidden;
  
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: #263445;
    color: #fff;
    font-size: 16px;
    font-weight: 600;
    
    i {
      margin-right: 8px;
      font-size: 20px;
    }
  }
}

.sidebar-menu {
  border: none;
  
  .el-menu-item {
    height: 55px;
    line-height: 55px;
    
    &:hover {
      background-color: #263445 !important;
    }
  }
}

.header {
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  
  .header-left {
    .breadcrumb-title {
      font-size: 18px;
      font-weight: 600;
      color: #303133;
    }
  }
  
  .header-right {
    .user-info {
      color: #606266;
      display: flex;
      align-items: center;
      
      i {
        margin-right: 5px;
      }
    }
  }
}

.main-content {
  background-color: #f5f7fa;
  padding: 20px;
  overflow-y: auto;
}
</style>