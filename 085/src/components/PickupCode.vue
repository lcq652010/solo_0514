<template>
  <div class="page-card">
    <h2 class="page-title">
      <i class="el-icon-tickets"></i>
      我的取件码
    </h2>

    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="手机号码" required>
        <el-input
          v-model="searchForm.phone"
          placeholder="请输入收件人手机号"
          clearable
          style="width: 250px"
          maxlength="11"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchPickupCodes" :loading="loading">
          <i class="el-icon-search"></i>
          查询我的取件码
        </el-button>
      </el-form-item>
    </el-form>

    <div v-if="searched" class="result-section">
      <div v-if="pendingList.length > 0" class="code-list">
        <h3 class="list-title">
          <i class="el-icon-time"></i>
          待取件 ({{ pendingList.length }} 件)
        </h3>
        <el-row :gutter="20">
          <el-col :span="8" v-for="(item, index) in pendingList" :key="item.id">
            <el-card class="code-card" shadow="hover">
              <div class="code-header">
                <span class="company-badge">{{ item.company }}</span>
                <el-tag type="warning" size="small">待取件</el-tag>
              </div>
              <div class="pickup-code-display">
                <span class="code-label">取件码</span>
                <div class="code-value">{{ item.pickupCode }}</div>
              </div>
              <div class="express-info">
                <p><span class="info-label">快递单号：</span>{{ item.expressNo }}</p>
                <p><span class="info-label">收件人：</span>{{ item.receiverName }}</p>
                <p><span class="info-label">快递类型：</span>{{ item.type }}</p>
                <p><span class="info-label">重量：</span>{{ item.weight }} kg</p>
                <p><span class="info-label">入库时间：</span>{{ item.inboundTime }}</p>
              </div>
              <div class="card-footer">
                <el-button type="success" size="small" icon="el-icon-check" @click="signRemind">
                  已取件，通知我
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <div v-else-if="signedList.length > 0 && pendingList.length === 0" class="empty-state">
        <el-empty description="暂无待取件，您的快递都已签收啦！">
          <el-button type="primary" size="small" @click="goInbound">去入库登记</el-button>
        </el-empty>
      </div>

      <div v-if="signedList.length > 0" class="history-section">
        <h3 class="list-title">
          <i class="el-icon-document-checked"></i>
          已签收记录 ({{ signedList.length }} 件)
        </h3>
        <el-table :data="signedList" border stripe style="width: 100%">
          <el-table-column prop="pickupCode" label="取件码" width="120" align="center">
            <template slot-scope="scope">
              <el-tag type="info" size="small">{{ scope.row.pickupCode }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="expressNo" label="快递单号" width="180"></el-table-column>
          <el-table-column prop="company" label="快递公司" width="120"></el-table-column>
          <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
          <el-table-column prop="inboundTime" label="入库时间" width="180"></el-table-column>
          <el-table-column prop="signerName" label="签收人" width="100"></el-table-column>
          <el-table-column prop="signTime" label="签收时间" width="180"></el-table-column>
        </el-table>
      </div>

      <div v-if="pendingList.length === 0 && signedList.length === 0 && searched" class="empty-state">
        <el-empty description="未找到该手机号对应的快递信息">
          <el-button type="primary" size="small" @click="goInbound">去入库登记</el-button>
        </el-empty>
      </div>
    </div>

    <div v-else class="welcome-section">
      <el-empty description="请输入收件人手机号查询您的取件码">
        <div class="quick-tips">
          <h4>
            <i class="el-icon-info"></i>
            温馨提示
          </h4>
          <ul>
            <li>请输入快递登记时填写的收件人手机号</li>
            <li>取件码是您取件的唯一凭证，请妥善保管</li>
            <li>如有疑问，请联系快递站点工作人员</li>
          </ul>
        </div>
      </el-empty>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PickupCode',
  data() {
    return {
      loading: false,
      searched: false,
      searchForm: {
        phone: ''
      },
      pendingList: [],
      signedList: []
    };
  },
  methods: {
    searchPickupCodes() {
      if (!this.searchForm.phone) {
        this.$message.warning('请输入收件人手机号');
        return;
      }
      if (!/^1[3-9]\d{9}$/.test(this.searchForm.phone)) {
        this.$message.error('请输入正确的手机号格式');
        return;
      }

      this.loading = true;
      setTimeout(() => {
        const list = JSON.parse(localStorage.getItem('expressList') || '[]');
        const userExpress = list.filter(item => item.receiverPhone === this.searchForm.phone);
        
        this.pendingList = userExpress.filter(item => item.status === '待取件');
        this.signedList = userExpress.filter(item => item.status === '已签收');
        this.searched = true;
        this.loading = false;

        if (userExpress.length > 0) {
          this.$message.success(`找到 ${userExpress.length} 条快递记录`);
        } else {
          this.$message.info('未找到该手机号对应的快递信息');
        }
      }, 500);
    },
    signRemind() {
      this.$message({
        message: '感谢您的反馈！系统将尽快更新状态',
        type: 'success'
      });
    },
    goInbound() {
      this.$router.push('/inbound');
    }
  }
};
</script>

<style scoped>
.search-form {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 30px;
  text-align: center;
}

.result-section {
  min-height: 300px;
}

.code-list {
  margin-bottom: 40px;
}

.list-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e4e7ed;
  display: flex;
  align-items: center;
  gap: 8px;
}

.code-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.code-card:hover {
  transform: translateY(-5px);
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px dashed #e4e7ed;
}

.company-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 14px;
}

.pickup-code-display {
  text-align: center;
  padding: 20px 0;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-radius: 8px;
  margin-bottom: 15px;
}

.code-label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.code-value {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
  letter-spacing: 8px;
  font-family: 'Courier New', monospace;
}

.express-info {
  padding: 10px 0;
}

.express-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}

.info-label {
  color: #909399;
}

.card-footer {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e4e7ed;
  text-align: center;
}

.history-section {
  margin-top: 30px;
}

.empty-state {
  padding: 40px 0;
}

.welcome-section {
  padding: 40px 0;
}

.quick-tips {
  text-align: left;
  max-width: 500px;
  margin: 20px auto 0;
  padding: 20px;
  background: #ecf5ff;
  border-radius: 8px;
  border: 1px solid #b3d8ff;
}

.quick-tips h4 {
  color: #409eff;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.quick-tips ul {
  padding-left: 20px;
}

.quick-tips li {
  margin: 8px 0;
  color: #606266;
  font-size: 14px;
}
</style>
