<template>
  <el-container class="app-container">
    <el-aside :width="isCollapse ? '64px' : '220px'">
      <div class="logo">
        <i class="el-icon-date"></i>
        <span v-show="!isCollapse">会议管理系统</span>
      </div>
      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#ffffff"
      >
        <el-menu-item index="/rooms">
          <i class="el-icon-office-building"></i>
          <span slot="title">会议室列表</span>
        </el-menu-item>
        <el-menu-item index="/booking">
          <i class="el-icon-edit-outline"></i>
          <span slot="title">会议预定</span>
        </el-menu-item>
        <el-menu-item index="/records">
          <i class="el-icon-document"></i>
          <span slot="title">会议记录</span>
        </el-menu-item>
        <el-menu-item index="/equipment">
          <i class="el-icon-cpu"></i>
          <span slot="title">设备借用</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <div class="header-left">
          <i
            class="el-icon-s-fold toggle-btn"
            :class="{ 'el-icon-s-unfold': isCollapse }"
            @click="toggleCollapse"
          ></i>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/rooms' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="user-info">
          <el-dropdown>
            <span class="user-dropdown">
              <el-avatar
                :size="32"
                src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
              ></el-avatar>
              <span class="user-name">管理员</span>
              <i class="el-icon-caret-bottom"></i>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>个人中心</el-dropdown-item>
              <el-dropdown-item divided>退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </div>
      </el-header>

      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isCollapse: false
    }
  },
  computed: {
    activeMenu() {
      return this.$route.path
    },
    currentPageName() {
      const nameMap = {
        '/rooms': '会议室列表',
        '/booking': '会议预定',
        '/records': '会议记录',
        '/equipment': '设备借用'
      }
      return nameMap[this.$route.path] || '首页'
    }
  },
  methods: {
    toggleCollapse() {
      this.isCollapse = !this.isCollapse
    }
  }
}
</script>

<style lang="scss" scoped>
.app-container {
  .toggle-btn {
    font-size: 20px;
    cursor: pointer;
    margin-right: 20px;
    color: #606266;
    transition: all 0.3s;

    &:hover {
      color: #409eff;
    }
  }

  .header-left {
    display: flex;
    align-items: center;
  }

  .user-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 0 10px;
    height: 60px;

    &:hover {
      background-color: #f5f7fa;
    }

    .user-name {
      color: #606266;
      font-size: 14px;
    }
  }
}
</style>
