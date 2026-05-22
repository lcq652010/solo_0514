<template>
  <div class="login-container">
    <div class="login-wrapper">
      <div class="login-header">
        <h1>宣纸笺定制管理系统</h1>
        <p>管理员登录</p>
        <div class="decoration"></div>
      </div>

      <el-form
        ref="loginForm"
        :model="formData"
        :rules="rules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="formData.username"
            placeholder="请输入用户名"
            prefix-icon="el-icon-user"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="formData.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-lock"
            size="large"
            @keyup.enter.native="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登 录
          </el-button>
        </el-form-item>

        <div class="login-tips">
          <p>默认账号：admin / admin123</p>
        </div>
      </el-form>

      <div class="back-home">
        <el-link type="info" @click="goHome">
          <i class="el-icon-arrow-left"></i> 返回首页
        </el-link>
      </div>
    </div>
  </div>
</template>

<script>
import { login } from '@/utils/storage.js'

export default {
  name: 'Login',
  data() {
    return {
      formData: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  methods: {
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          setTimeout(() => {
            const success = login(this.formData.username, this.formData.password)
            if (success) {
              this.$message.success('登录成功')
              this.$router.push('/admin/orders')
            } else {
              this.$message.error('用户名或密码错误')
            }
            this.loading = false
          }, 500)
        }
      })
    },
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #F5F0E6 0%, #EDE5D4 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(196, 30, 58, 0.08) 0%, transparent 70%);
    border-radius: 50%;
  }

  &::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(93, 78, 55, 0.08) 0%, transparent 70%);
    border-radius: 50%;
  }
}

.login-wrapper {
  width: 420px;
  background: rgba(255, 253, 249, 0.95);
  border-radius: 12px;
  padding: 50px 40px;
  box-shadow: 0 10px 40px rgba(93, 78, 55, 0.15);
  border: 1px solid rgba(196, 30, 58, 0.1);
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;

  h1 {
    font-family: "KaiTi", "楷体", serif;
    font-size: 28px;
    color: #1A1A1A;
    margin-bottom: 10px;
    letter-spacing: 3px;
  }

  p {
    color: #8B7355;
    font-size: 14px;
    letter-spacing: 2px;
  }

  .decoration {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #C41E3A, transparent);
    margin: 20px auto 0;
  }
}

.login-form {
  .el-form-item {
    margin-bottom: 25px;
  }

  >>> .el-input__inner {
    border-radius: 6px;
  }
}

.login-btn {
  width: 100%;
  border-radius: 6px;
  font-size: 16px;
  letter-spacing: 4px;
}

.login-tips {
  text-align: center;
  color: #909399;
  font-size: 13px;
  margin-top: 20px;

  p {
    margin: 0;
  }
}

.back-home {
  text-align: center;
  margin-top: 30px;
}
</style>
