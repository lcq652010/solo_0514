<template>
  <div id="app">
    <el-container>
      <el-header class="app-header">
        <div class="header-content">
          <div class="logo">
            <i class="el-icon-present"></i>
            <span>藤编果篮定制系统</span>
          </div>
          <el-menu
            mode="horizontal"
            :default-active="activeMenu"
            class="header-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="/">
              <i class="el-icon-edit"></i>
              <span>我要定制</span>
            </el-menu-item>
            <el-menu-item index="/admin">
              <i class="el-icon-setting"></i>
              <span>管理后台</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-header>
      <el-main class="app-main">
        <router-view />
      </el-main>
      <el-footer class="app-footer">
        <p>© 2024 藤编工艺坊 - 匠心传承，精工细作</p>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    activeMenu() {
      return this.$route.path
    }
  },
  methods: {
    handleMenuSelect(index) {
      this.$router.push(index)
    }
  }
}
</script>

<style lang="scss">
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #8B4513 0%, #A0522D 100%);
  padding: 0;
  height: 70px;
  line-height: 70px;
  box-shadow: 0 2px 8px rgba(139, 69, 19, 0.3);

  .header-content {
    max-width: 1400px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
  }

  .logo {
    display: flex;
    align-items: center;
    color: #FFF8DC;
    font-size: 22px;
    font-weight: 600;
    font-family: 'Noto Serif SC', serif;

    i {
      font-size: 28px;
      margin-right: 12px;
    }
  }

  .header-menu {
    background: transparent;
    border-bottom: none;

    .el-menu-item {
      color: #FFF8DC;
      border-bottom: 2px solid transparent;
      transition: all 0.3s;

      &:hover {
        color: #FFE4B5;
        background: rgba(255, 255, 255, 0.1);
      }

      &.is-active {
        color: #FFE4B5;
        border-bottom: 2px solid #FFE4B5;
      }
    }
  }
}

.app-main {
  flex: 1;
  background: linear-gradient(180deg, #FDF5E6 0%, #FAEBD7 100%);
  padding: 32px 24px;
}

.app-footer {
  background: #5D4037;
  color: #D7CCC8;
  text-align: center;
  padding: 20px 0;
  font-size: 14px;
}
</style>
