<template>
  <div class="page-card">
    <h2 class="page-title">
      <i class="el-icon-upload"></i>
      快递出库签收
    </h2>

    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="搜索方式">
        <el-select v-model="searchType" style="width: 150px">
          <el-option label="取件码" value="pickupCode"></el-option>
          <el-option label="快递单号" value="expressNo"></el-option>
          <el-option label="手机号" value="phone"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-input
          v-model="searchForm.keyword"
          :placeholder="searchPlaceholder"
          style="width: 250px"
          clearable
          @keyup.enter.native="searchExpress"
        ></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="searchExpress" :loading="searchLoading">
          <i class="el-icon-search"></i>
          查询
        </el-button>
      </el-form-item>
    </el-form>

    <div v-if="expressInfo" class="express-detail">
      <el-divider content-position="left">快递信息</el-divider>
      
      <el-descriptions :column="2" border class="detail-table">
        <el-descriptions-item label="快递单号">{{ expressInfo.expressNo }}</el-descriptions-item>
        <el-descriptions-item label="快递公司">{{ expressInfo.company }}</el-descriptions-item>
        <el-descriptions-item label="收件人">{{ expressInfo.receiverName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ expressInfo.receiverPhone }}</el-descriptions-item>
        <el-descriptions-item label="收件地址" :span="2">{{ expressInfo.receiverAddress }}</el-descriptions-item>
        <el-descriptions-item label="取件码">
          <el-tag type="success" size="medium" style="font-size: 18px; padding: 8px 16px;">
            {{ expressInfo.pickupCode }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="入库时间">{{ expressInfo.inboundTime }}</el-descriptions-item>
        <el-descriptions-item label="快递重量">{{ expressInfo.weight }} kg</el-descriptions-item>
        <el-descriptions-item label="快递类型">{{ expressInfo.type }}</el-descriptions-item>
        <el-descriptions-item label="当前状态">
          <el-tag :type="expressInfo.status === '待取件' ? 'warning' : 'success'" size="medium">
            {{ expressInfo.status }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div v-if="expressInfo.status === '待取件'" class="sign-section">
        <el-divider content-position="left">签收确认</el-divider>
        
        <el-form :model="signForm" :rules="signRules" ref="signForm" label-width="100px">
          <el-form-item label="签收人" prop="signerName">
            <el-input v-model="signForm.signerName" placeholder="请输入签收人姓名" style="width: 300px"></el-input>
          </el-form-item>
          <el-form-item label="签收人电话" prop="signerPhone">
            <el-input v-model="signForm.signerPhone" placeholder="请输入签收人手机号" style="width: 300px"></el-input>
          </el-form-item>
          <el-form-item label="证件类型">
            <el-select v-model="signForm.idType" style="width: 300px">
              <el-option label="身份证" value="身份证"></el-option>
              <el-option label="学生证" value="学生证"></el-option>
              <el-option label="工作证" value="工作证"></el-option>
              <el-option label="其他" value="其他"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="success" size="large" @click="confirmSign" :loading="signLoading">
              <i class="el-icon-check"></i>
              确认签收出库
            </el-button>
            <el-button size="large" @click="clearSearch">
              <i class="el-icon-close"></i>
              取消
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-else class="already-signed">
        <el-alert
          title="该快递已签收"
          type="success"
          :closable="false"
          show-icon
        >
          <div slot="description">
            <p>签收人：{{ expressInfo.signerName }}</p>
            <p>签收时间：{{ expressInfo.signTime }}</p>
          </div>
        </el-alert>
      </div>
    </div>

    <div v-else-if="searchDone && !expressInfo" class="no-result">
      <el-empty description="未找到相关快递信息，请检查输入是否正确"></el-empty>
    </div>

    <div class="today-outbound">
      <el-divider content-position="left">今日出库记录</el-divider>
      <el-table :data="todayList" border stripe style="width: 100%">
        <el-table-column prop="expressNo" label="快递单号" width="180"></el-table-column>
        <el-table-column prop="company" label="快递公司" width="120"></el-table-column>
        <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
        <el-table-column prop="pickupCode" label="取件码" width="100" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="small">{{ scope.row.pickupCode }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="signerName" label="签收人" width="100"></el-table-column>
        <el-table-column prop="signTime" label="签收时间" width="180"></el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'OutboundSign',
  data() {
    return {
      searchType: 'pickupCode',
      searchForm: {
        keyword: ''
      },
      searchLoading: false,
      searchDone: false,
      expressInfo: null,
      signLoading: false,
      signForm: {
        signerName: '',
        signerPhone: '',
        idType: '身份证'
      },
      signRules: {
        signerName: [
          { required: true, message: '请输入签收人姓名', trigger: 'blur' }
        ],
        signerPhone: [
          { required: true, message: '请输入签收人手机号', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      },
      todayList: []
    };
  },
  computed: {
    searchPlaceholder() {
      const map = {
        pickupCode: '请输入取件码',
        expressNo: '请输入快递单号',
        phone: '请输入收件人手机号'
      };
      return map[this.searchType];
    }
  },
  methods: {
    searchExpress() {
      if (!this.searchForm.keyword) {
        this.$message.warning('请输入搜索关键词');
        return;
      }

      this.searchLoading = true;
      setTimeout(() => {
        const list = JSON.parse(localStorage.getItem('expressList') || '[]');
        const keyword = this.searchForm.keyword.trim();
        
        let found = null;
        if (this.searchType === 'pickupCode') {
          found = list.find(item => item.pickupCode === keyword);
        } else if (this.searchType === 'expressNo') {
          found = list.find(item => item.expressNo === keyword);
        } else if (this.searchType === 'phone') {
          found = list.find(item => item.receiverPhone === keyword);
        }

        this.expressInfo = found || null;
        this.searchDone = true;
        this.searchLoading = false;

        if (found) {
          this.$message.success('找到快递信息');
        } else {
          this.$message.warning('未找到相关快递');
        }
      }, 500);
    },
    confirmSign() {
      this.$refs.signForm.validate((valid) => {
        if (valid) {
          this.signLoading = true;
          setTimeout(() => {
            const list = JSON.parse(localStorage.getItem('expressList') || '[]');
            const index = list.findIndex(item => item.id === this.expressInfo.id);
            
            if (index !== -1) {
              list[index].status = '已签收';
              list[index].signerName = this.signForm.signerName;
              list[index].signerPhone = this.signForm.signerPhone;
              list[index].idType = this.signForm.idType;
              list[index].signTime = moment().format('YYYY-MM-DD HH:mm:ss');
              localStorage.setItem('expressList', JSON.stringify(list));
              
              this.expressInfo = list[index];
              this.loadTodayList();
              
              this.$message({
                type: 'success',
                message: '签收出库成功！'
              });
            }
            
            this.signLoading = false;
          }, 1000);
        }
      });
    },
    clearSearch() {
      this.searchForm.keyword = '';
      this.expressInfo = null;
      this.searchDone = false;
      this.$refs.signForm.resetFields();
    },
    loadTodayList() {
      const list = JSON.parse(localStorage.getItem('expressList') || '[]');
      const today = moment().format('YYYY-MM-DD');
      this.todayList = list.filter(item => {
        return item.status === '已签收' && item.signTime && item.signTime.startsWith(today);
      });
    }
  },
  mounted() {
    this.loadTodayList();
  }
};
</script>

<style scoped>
.search-form {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.express-detail {
  margin-bottom: 30px;
}

.detail-table {
  margin-bottom: 20px;
}

.sign-section {
  margin-top: 20px;
}

.already-signed {
  margin-top: 20px;
}

.no-result {
  padding: 40px 0;
}

.today-outbound {
  margin-top: 30px;
}
</style>
