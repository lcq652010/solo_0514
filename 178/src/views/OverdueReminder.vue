<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">逾期提醒</h2>
    </div>
    <div class="card-wrapper">
      <el-row :gutter="20" class="mb-20">
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background-color: #f56c6c;">
                <i class="el-icon-warning"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ overdueTotal }}</div>
                <div class="stat-label">逾期总数量</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background-color: #e6a23c;">
                <i class="el-icon-time"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ overduePersons }}</div>
                <div class="stat-label">逾期人数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background-color: #67c23a;">
                <i class="el-icon-document"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ avgOverdueDays }}</div>
                <div class="stat-label">平均逾期天数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon" style="background-color: #409eff;">
                <i class="el-icon-s-custom"></i>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ maxOverdueDays }}</div>
                <div class="stat-label">最长逾期天数</div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="借阅人">
            <el-input v-model="searchForm.borrower" placeholder="请输入借阅人" clearable></el-input>
          </el-form-item>
          <el-form-item label="逾期天数">
            <el-select v-model="searchForm.overdueLevel" placeholder="请选择逾期等级" clearable>
              <el-option label="7天以内" value="7"></el-option>
              <el-option label="7-15天" value="15"></el-option>
              <el-option label="15-30天" value="30"></el-option>
              <el-option label="30天以上" value="more"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-wrapper">
        <el-table :data="filteredOverdueList" border stripe style="width: 100%">
          <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
          <el-table-column prop="bookName" label="图书名称" min-width="180"></el-table-column>
          <el-table-column prop="borrower" label="借阅人" width="100" align="center"></el-table-column>
          <el-table-column prop="borrowDate" label="借阅日期" width="120" align="center"></el-table-column>
          <el-table-column prop="dueDate" label="应还日期" width="120" align="center"></el-table-column>
          <el-table-column prop="overdueDays" label="逾期天数" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getOverdueTagType(scope.row.overdueDays)" size="small">
                {{ scope.row.overdueDays }}天
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="overdueLevel" label="逾期等级" width="100" align="center">
            <template slot-scope="scope">
              {{ getOverdueLevelText(scope.row.overdueDays) }}
            </template>
          </el-table-column>
          <el-table-column label="操作" width="200" align="center">
            <template slot-scope="scope">
              <el-button type="warning" size="mini" @click="handleSendReminder(scope.row)">发送提醒</el-button>
              <el-button type="success" size="mini" @click="handleReturn(scope.row)">立即归还</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="mt-20 text-right">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="currentPage"
            :page-sizes="[10, 20, 50, 100]"
            :page-size="pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="total">
          </el-pagination>
        </div>
      </div>
    </div>

    <el-dialog title="发送逾期提醒" :visible.sync="reminderDialogVisible" width="500px">
      <div v-if="currentReminder">
        <el-alert
          title="提醒信息预览"
          type="warning"
          :description="`${currentReminder.borrower}，您借阅的《${currentReminder.bookName}》已逾期${currentReminder.overdueDays}天，请尽快归还。`"
          show-icon>
        </el-alert>
        <el-form label-width="80px" style="margin-top: 20px;">
          <el-form-item label="提醒方式">
            <el-radio-group v-model="reminderType">
              <el-radio label="sms">短信</el-radio>
              <el-radio label="email">邮件</el-radio>
              <el-radio label="wechat">微信</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="备注信息">
            <el-input type="textarea" v-model="reminderRemark" :rows="3" placeholder="请输入备注信息（可选）"></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="reminderDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSendReminder">确认发送</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { borrowRecords } from '@/mock/data';

export default {
  name: 'OverdueReminder',
  data() {
    return {
      searchForm: {
        borrower: '',
        overdueLevel: ''
      },
      currentPage: 1,
      pageSize: 10,
      reminderDialogVisible: false,
      currentReminder: null,
      reminderType: 'sms',
      reminderRemark: ''
    };
  },
  computed: {
    overdueList() {
      return borrowRecords
        .filter(item => item.status !== 'returned')
        .map(item => ({
          ...item,
          overdueDays: this.calculateOverdueDays(item.dueDate)
        }))
        .filter(item => item.overdueDays > 0)
        .sort((a, b) => b.overdueDays - a.overdueDays);
    },
    filteredOverdueList() {
      let list = this.overdueList;
      if (this.searchForm.borrower) {
        list = list.filter(item => item.borrower.includes(this.searchForm.borrower));
      }
      if (this.searchForm.overdueLevel) {
        if (this.searchForm.overdueLevel === 'more') {
          list = list.filter(item => item.overdueDays > 30);
        } else {
          const level = parseInt(this.searchForm.overdueLevel);
          list = list.filter(item => item.overdueDays <= level);
        }
      }
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return list.slice(start, end);
    },
    total() {
      let list = this.overdueList;
      if (this.searchForm.borrower) {
        list = list.filter(item => item.borrower.includes(this.searchForm.borrower));
      }
      if (this.searchForm.overdueLevel) {
        if (this.searchForm.overdueLevel === 'more') {
          list = list.filter(item => item.overdueDays > 30);
        } else {
          const level = parseInt(this.searchForm.overdueLevel);
          list = list.filter(item => item.overdueDays <= level);
        }
      }
      return list.length;
    },
    overdueTotal() {
      return this.overdueList.length;
    },
    overduePersons() {
      const persons = new Set(this.overdueList.map(item => item.borrower));
      return persons.size;
    },
    avgOverdueDays() {
      if (this.overdueList.length === 0) return 0;
      const total = this.overdueList.reduce((sum, item) => sum + item.overdueDays, 0);
      return Math.round(total / this.overdueList.length);
    },
    maxOverdueDays() {
      if (this.overdueList.length === 0) return 0;
      return Math.max(...this.overdueList.map(item => item.overdueDays));
    }
  },
  methods: {
    calculateOverdueDays(dueDate) {
      const today = new Date();
      const due = new Date(dueDate);
      const diff = today - due;
      return diff > 0 ? Math.ceil(diff / (1000 * 60 * 60 * 24)) : 0;
    },
    getOverdueTagType(days) {
      if (days <= 7) return 'warning';
      if (days <= 15) return 'primary';
      if (days <= 30) return 'danger';
      return 'error';
    },
    getOverdueLevelText(days) {
      if (days <= 7) return '轻微';
      if (days <= 15) return '一般';
      if (days <= 30) return '严重';
      return '特别严重';
    },
    handleSearch() {
      this.currentPage = 1;
      this.$message.success('搜索完成');
    },
    handleReset() {
      this.searchForm = {
        borrower: '',
        overdueLevel: ''
      };
      this.currentPage = 1;
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleSendReminder(row) {
      this.currentReminder = row;
      this.reminderType = 'sms';
      this.reminderRemark = '';
      this.reminderDialogVisible = true;
    },
    confirmSendReminder() {
      const typeText = { sms: '短信', email: '邮件', wechat: '微信' };
      this.$message.success(`${typeText[this.reminderType]}提醒已发送给 ${this.currentReminder.borrower}`);
      this.reminderDialogVisible = false;
    },
    handleReturn(row) {
      this.$confirm(`确认归还《${row.bookName}》吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = 'returned';
        row.returnDate = this.formatDate(new Date());
        this.$message.success('归还成功！');
      }).catch(() => {});
    },
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }
  }
};
</script>

<style scoped>
.stat-item {
  display: flex;
  align-items: center;
}
.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  margin-right: 15px;
}
.stat-info {
  flex: 1;
}
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}
.stat-label {
  font-size: 14px;
  color: #909399;
}
</style>