<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">图书归还</h2>
    </div>
    <div class="card-wrapper">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="借阅人工号">
            <el-input v-model="searchForm.borrowerNo" placeholder="请输入借阅人工号" clearable></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询借阅</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div v-if="borrowedList.length > 0" class="mb-20">
        <h3 style="margin-bottom: 15px; color: #606266;">待归还图书列表</h3>
        <el-table :data="borrowedList" border stripe style="width: 100%" @selection-change="handleSelectionChange">
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
          <el-table-column prop="bookName" label="图书名称" min-width="180"></el-table-column>
          <el-table-column prop="borrower" label="借阅人" width="100" align="center"></el-table-column>
          <el-table-column prop="borrowDate" label="借阅日期" width="120" align="center"></el-table-column>
          <el-table-column prop="dueDate" label="应还日期" width="120" align="center"></el-table-column>
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.status === 'overdue' ? 'danger' : 'primary'" size="small">
                {{ scope.row.status === 'overdue' ? '已逾期' : '借阅中' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="overdueDays" label="逾期天数" width="100" align="center">
            <template slot-scope="scope">
              <span v-if="scope.row.overdueDays > 0" style="color: #f56c6c;">{{ scope.row.overdueDays }}天</span>
              <span v-else>-</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" align="center">
            <template slot-scope="scope">
              <el-button type="success" size="mini" @click="handleSingleReturn(scope.row)">归还</el-button>
            </template>
          </el-table-column>
        </el-table>
        <div class="mt-20">
          <el-button type="success" @click="handleBatchReturn" :disabled="selectedRows.length === 0">
            批量归还 ({{ selectedRows.length }})
          </el-button>
        </div>
      </div>

      <div v-else-if="hasSearched" style="text-align: center; padding: 40px; color: #909399;">
        <i class="el-icon-info" style="font-size: 40px; margin-bottom: 15px; display: block;"></i>
        <p>该借阅人暂无待归还的图书</p>
      </div>

      <el-alert v-if="showReturnResult" :title="returnResultTitle" :type="returnResultType" :description="returnResultDesc" show-icon class="mb-20"></el-alert>
    </div>

    <el-dialog title="归还确认" :visible.sync="returnDialogVisible" width="500px">
      <div v-if="returningBook">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="图书名称">{{ returningBook.bookName }}</el-descriptions-item>
          <el-descriptions-item label="借阅人">{{ returningBook.borrower }}</el-descriptions-item>
          <el-descriptions-item label="借阅日期">{{ returningBook.borrowDate }}</el-descriptions-item>
          <el-descriptions-item label="应还日期">{{ returningBook.dueDate }}</el-descriptions-item>
          <el-descriptions-item label="归还日期">{{ today }}</el-descriptions-item>
          <el-descriptions-item label="逾期天数" v-if="returningBook.overdueDays > 0">
            <span style="color: #f56c6c;">{{ returningBook.overdueDays }}天</span>
          </el-descriptions-item>
        </el-descriptions>
        <div v-if="returningBook.overdueDays > 0" style="margin-top: 15px; padding: 10px; background-color: #fef0f0; border-radius: 4px;">
          <i class="el-icon-warning" style="color: #f56c6c;"></i>
          <span style="color: #f56c6c; margin-left: 5px;">该图书已逾期，请提醒借阅人按时归还</span>
        </div>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="returnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmReturn">确认归还</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { bookList, borrowRecords } from '@/mock/data';

export default {
  name: 'BookReturn',
  data() {
    return {
      searchForm: {
        borrowerNo: ''
      },
      borrowedList: [],
      selectedRows: [],
      hasSearched: false,
      returnDialogVisible: false,
      returningBook: null,
      today: '',
      showReturnResult: false,
      returnResultTitle: '',
      returnResultType: '',
      returnResultDesc: ''
    };
  },
  mounted() {
    this.today = this.formatDate(new Date());
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    calculateOverdueDays(dueDate) {
      const today = new Date();
      const due = new Date(dueDate);
      const diff = today - due;
      return diff > 0 ? Math.ceil(diff / (1000 * 60 * 60 * 24)) : 0;
    },
    handleSearch() {
      if (!this.searchForm.borrowerNo.trim()) {
        this.$message.warning('请输入借阅人工号');
        return;
      }
      this.hasSearched = true;
      this.showReturnResult = false;
      const borrowed = borrowRecords.filter(item => item.status !== 'returned');
      this.borrowedList = borrowed.map(item => ({
        ...item,
        overdueDays: this.calculateOverdueDays(item.dueDate)
      }));
      if (this.borrowedList.length > 0) {
        this.$message.success(`查询到 ${this.borrowedList.length} 本待归还图书`);
      }
    },
    handleReset() {
      this.searchForm.borrowerNo = '';
      this.borrowedList = [];
      this.selectedRows = [];
      this.hasSearched = false;
      this.showReturnResult = false;
    },
    handleSelectionChange(val) {
      this.selectedRows = val;
    },
    handleSingleReturn(row) {
      this.returningBook = row;
      this.returnDialogVisible = true;
    },
    increaseStock(bookId) {
      const book = bookList.find(item => item.id === bookId);
      if (book) {
        book.stock += 1;
      }
    },
    handleBatchReturn() {
      this.$confirm(`确认归还选中的 ${this.selectedRows.length} 本图书吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.selectedRows.forEach(row => {
          row.status = 'returned';
          row.returnDate = this.today;
          this.increaseStock(row.bookId);
        });
        this.borrowedList = this.borrowedList.filter(item => item.status !== 'returned');
        this.showReturnResult = true;
        this.returnResultTitle = '批量归还成功';
        this.returnResultType = 'success';
        this.returnResultDesc = `成功归还 ${this.selectedRows.length} 本图书，库存已自动更新`;
        this.selectedRows = [];
      }).catch(() => {});
    },
    confirmReturn() {
      this.returningBook.status = 'returned';
      this.returningBook.returnDate = this.today;
      this.increaseStock(this.returningBook.bookId);
      this.borrowedList = this.borrowedList.filter(item => item.status !== 'returned');
      this.returnDialogVisible = false;
      this.showReturnResult = true;
      this.returnResultTitle = '归还成功';
      this.returnResultType = 'success';
      this.returnResultDesc = `《${this.returningBook.bookName}》已成功归还，库存已自动更新`;
    }
  }
};
</script>

<style scoped>
</style>