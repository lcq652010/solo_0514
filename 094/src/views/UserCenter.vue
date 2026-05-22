<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-user"></i>
      个人中心
    </h2>
    
    <el-row :gutter="20">
      <el-col :xs="24" :sm="8">
        <el-card class="profile-card">
          <div class="user-avatar">
            <img :src="userInfo.avatar" :alt="userInfo.nickname">
          </div>
          <div class="user-info">
            <h3>{{ userInfo.nickname }}</h3>
            <el-tag type="success" size="small">{{ userInfo.level }}</el-tag>
          </div>
          <div class="user-stats">
            <div class="stat-item">
              <span class="stat-value">{{ userInfo.totalOrders }}</span>
              <span class="stat-label">订单数</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">¥{{ userInfo.totalSpent }}</span>
              <span class="stat-label">消费总额</span>
            </div>
          </div>
        </el-card>
        
        <el-card class="menu-card" style="margin-top: 20px;">
          <el-menu
            :default-active="activeMenu"
            class="user-menu"
            @select="handleMenuSelect"
          >
            <el-menu-item index="profile">
              <i class="el-icon-setting"></i>
              <span>个人信息</span>
            </el-menu-item>
            <el-menu-item index="orders">
              <i class="el-icon-s-order"></i>
              <span>我的订单</span>
            </el-menu-item>
            <el-menu-item index="coupon">
              <i class="el-icon-ticket"></i>
              <span>优惠券</span>
            </el-menu-item>
            <el-menu-item index="favorite">
              <i class="el-icon-star-off"></i>
              <span>我的收藏</span>
            </el-menu-item>
            <el-menu-item index="security">
              <i class="el-icon-lock"></i>
              <span>安全设置</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>
      
      <el-col :xs="24" :sm="16">
        <el-card v-if="activeMenu === 'profile'" class="content-card">
          <div slot="header">
            <span>个人信息</span>
            <el-button type="text" style="float: right;" @click="editProfile = true">编辑</el-button>
          </div>
          
          <el-descriptions :column="1" border>
            <el-descriptions-item label="用户名">{{ userInfo.username }}</el-descriptions-item>
            <el-descriptions-item label="昵称">{{ userInfo.nickname }}</el-descriptions-item>
            <el-descriptions-item label="手机号码">{{ userInfo.phone }}</el-descriptions-item>
            <el-descriptions-item label="邮箱">{{ userInfo.email }}</el-descriptions-item>
            <el-descriptions-item label="注册时间">{{ userInfo.registerTime }}</el-descriptions-item>
          </el-descriptions>
        </el-card>
        
        <el-card v-else-if="activeMenu === 'orders'" class="content-card">
          <div slot="header">我的订单</div>
          
          <el-table :data="userOrders" style="width: 100%">
            <el-table-column prop="id" label="订单号" width="180"></el-table-column>
            <el-table-column prop="ticketName" label="门票类型"></el-table-column>
            <el-table-column prop="totalPrice" label="金额" width="100">
              <template slot-scope="scope">
                <span style="color: #f56c6c;">¥{{ scope.row.totalPrice }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="visitDate" label="入园日期" width="120"></el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template slot-scope="scope">
                <el-tag :type="statusMap[scope.row.status].type" size="small">
                  {{ statusMap[scope.row.status].label }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
        
        <el-card v-else-if="activeMenu === 'coupon'" class="content-card">
          <div slot="header">我的优惠券</div>
          
          <el-empty description="暂无优惠券">
            <el-button type="primary">去领取</el-button>
          </el-empty>
        </el-card>
        
        <el-card v-else-if="activeMenu === 'favorite'" class="content-card">
          <div slot="header">我的收藏</div>
          
          <el-empty description="暂无收藏">
            <el-button type="primary">去逛逛</el-button>
          </el-empty>
        </el-card>
        
        <el-card v-else-if="activeMenu === 'security'" class="content-card">
          <div slot="header">安全设置</div>
          
          <el-list>
            <el-list-item class="security-item">
              <div class="item-label">
                <i class="el-icon-mobile-phone"></i>
                <span>绑定手机</span>
              </div>
              <div class="item-content">{{ userInfo.phone }}</div>
              <el-button type="text">更换</el-button>
            </el-list-item>
            <el-list-item class="security-item">
              <div class="item-label">
                <i class="el-icon-message"></i>
                <span>邮箱绑定</span>
              </div>
              <div class="item-content">{{ userInfo.email }}</div>
              <el-button type="text">更换</el-button>
            </el-list-item>
            <el-list-item class="security-item">
              <div class="item-label">
                <i class="el-icon-key"></i>
                <span>登录密码</span>
              </div>
              <div class="item-content">已设置</div>
              <el-button type="text">修改</el-button>
            </el-list-item>
            <el-list-item class="security-item">
              <div class="item-label">
                <i class="el-icon-set-up"></i>
                <span>支付密码</span>
              </div>
              <div class="item-content">未设置</div>
              <el-button type="text">设置</el-button>
            </el-list-item>
          </el-list>
        </el-card>
      </el-col>
    </el-row>
    
    <el-dialog title="编辑个人信息" :visible.sync="editProfile" width="500px">
      <el-form :model="editForm" label-width="80px" class="edit-form">
        <el-form-item label="昵称">
          <el-input v-model="editForm.nickname"></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="editProfile = false">取 消</el-button>
        <el-button type="primary" @click="saveProfile">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { userInfo, orders, statusMap } from '@/data/mockData'

export default {
  name: 'UserCenter',
  data() {
    return {
      userInfo: userInfo,
      statusMap: statusMap,
      userOrders: orders,
      activeMenu: 'profile',
      editProfile: false,
      editForm: {
        nickname: '',
        email: ''
      }
    }
  },
  methods: {
    handleMenuSelect(index) {
      this.activeMenu = index
    },
    saveProfile() {
      this.userInfo.nickname = this.editForm.nickname
      this.userInfo.email = this.editForm.email
      this.editProfile = false
      this.$message.success('保存成功')
    }
  },
  mounted() {
    this.editForm.nickname = this.userInfo.nickname
    this.editForm.email = this.userInfo.email
  }
}
</script>

<style scoped>
.profile-card {
  text-align: center;
}

.user-avatar {
  margin-bottom: 15px;
}

.user-avatar img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: 3px solid #409eff;
}

.user-info h3 {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #303133;
}

.user-stats {
  display: flex;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #ebeef5;
}

.stat-item {
  flex: 1;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.stat-label {
  font-size: 12px;
  color: #909399;
}

.menu-card {
  padding: 0;
}

.user-menu {
  border: none;
}

.content-card {
  min-height: 400px;
}

.security-item {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #ebeef5;
}

.security-item:last-child {
  border-bottom: none;
}

.item-label {
  width: 120px;
  display: flex;
  align-items: center;
}

.item-label i {
  margin-right: 8px;
  font-size: 18px;
  color: #409eff;
}

.item-content {
  flex: 1;
  color: #606266;
}

.edit-form {
  padding: 10px 0;
}
</style>
