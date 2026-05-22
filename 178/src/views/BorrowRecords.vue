<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">借阅记录</h2>
    </div>
    <div class="card-wrapper">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="图书名称">
            <el-input v-model="searchForm.bookName" placeholder="请输入图书名称" clearable style="width: 150px;"></el-input>
          </el-form-item>
          <el-form-item label="图书分类">
            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable style="width: 150px;">
              <el-option v-for="item in categoryList" :key="item" :label="item" :value="item"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="借阅人">
            <el-input v-model="searchForm.borrower" placeholder="请输入借阅人" clearable style="width: 120px;"></el-input>
          </el-form-item>
          <el-form-item label="借阅日期">
            <el-date-picker
              v-model="searchForm.borrowDateStart"
              type="date"
              placeholder="开始日期"
              value-format="yyyy-MM-dd"
              style="width: 140px;">
            </el-date-picker>
            <span style="margin: 0 5px;">至</span>
            <el-date-picker
              v-model="searchForm.borrowDateEnd"
              type="date"
              placeholder="结束日期"
              value-format="yyyy-MM-dd"
              style="width: 140px;">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="归还状态">
            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable style="width: 120px;">
              <el-option label="借阅中" value="borrowed"></el-option>
              <el-option label="已归还" value="returned"></el-option>
              <el-option label="已逾期" value="overdue"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="table-wrapper">
        <el-table :data="filteredRecords" border stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
          <el-table-column prop="bookName" label="图书名称" min-width="180"></el-table-column>
          <el-table-column label="分类" width="100" align="center">
            <template slot-scope="scope">
              {{ getBookCategory(scope.row.bookId) }}
            </template>
          </el-table-column>
          <el-table-column prop="borrower" label="借阅人" width="100" align="center"></el-table-column>
          <el-table-column prop="borrowDate" label="借阅日期" width="120" align="center"></el-table-column>
          <el-table-column prop="dueDate" label="应还日期" width="120" align="center"></el-table-column>
          <el-table-column prop="returnDate" label="归还日期" width="120" align="center">
            <template slot-scope="scope">
              {{ scope.row.returnDate || '-' }}
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="small">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150" align="center">
            <template slot-scope="scope">
              <el-button v-if="scope.row.status !== 'returned'" type="success" size="mini" @click="handleReturn(scope.row)">归还</el-button>
              <el-button type="info" size="mini" @click="handleView(scope.row)">详情</el-button>
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

    <el-dialog title="借阅详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentRecord">
        <el-descriptions-item label="图书名称">{{ currentRecord.bookName }}</el-descriptions-item>
        <el-descriptions-item label="借阅人">{{ currentRecord.borrower }}</el-descriptions-item>
        <el-descriptions-item label="借阅日期">{{ currentRecord.borrowDate }}</el-descriptions-item>
        <el-descriptions-item label="应还日期">{{ currentRecord.dueDate }}</el-descriptions-item>
        <el-descriptions-item label="归还日期">{{ currentRecord.returnDate || '-' }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="getStatusType(currentRecord.status)" size="small">
            {{ getStatusText(currentRecord.status) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { bookList, borrowRecords, categoryList } from '@/mock/data';

export default {
  name: 'BorrowRecords',
  data() {
    return {
      bookList: bookList,
      borrowRecords: borrowRecords,
      categoryList: categoryList,
      searchForm: {
        bookName: '',
        borrower: '',
        category: '',
        borrowDateStart: '',
        borrowDateEnd: '',
        status: ''
      },
      currentPage: 1,
      pageSize: 10,
      detailDialogVisible: false,
      currentRecord: null
    };
  },
  computed: {
    filteredRecords() {
      let list = this.borrowRecords;
      if (this.searchForm.bookName) {
        list = list.filter(item => item.bookName.includes(this.searchForm.bookName));
      }
      if (this.searchForm.category) {
        list = list.filter(item => {
          const book = this.bookList.find(b => b.id === item.bookId);
          return book && book.category === this.searchForm.category;
        });
      }
      if (this.searchForm.borrower) {
        list = list.filter(item => item.borrower.includes(this.searchForm.borrower));
      }
      if (this.searchForm.borrowDateStart) {
        list = list.filter(item => item.borrowDate >= this.searchForm.borrowDateStart);
      }
      if (this.searchForm.borrowDateEnd) {
        list = list.filter(item => item.borrowDate <= this.searchForm.borrowDateEnd);
      }
      if (this.searchForm.status) {
        list = list.filter(item => item.status === this.searchForm.status);
      }
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return list.slice(start, end);
    },
    total() {
      let list = this.borrowRecords;
      if (this.searchForm.bookName) {
        list = list.filter(item => item.bookName.includes(this.searchForm.bookName));
      }
      if (this.searchForm.category) {
        list = list.filter(item => {
          const book = this.bookList.find(b => b.id === item.bookId);
          return book && book.category === this.searchForm.category;
        });
      }
      if (this.searchForm.borrower) {
        list = list.filter(item => item.borrower.includes(this.searchForm.borrower));
      }
      if (this.searchForm.borrowDateStart) {
        list = list.filter(item => item.borrowDate >= this.searchForm.borrowDateStart);
      }
      if (this.searchForm.borrowDateEnd) {
        list = list.filter(item => item.borrowDate <= this.searchForm.borrowDateEnd);
      }
      if (this.searchForm.status) {
        list = list.filter(item => item.status === this.searchForm.status);
      }
      return list.length;
    }
  },
  methods: {
    getStatusType(status) {
      const map = { borrowed: 'primary', returned: 'success', overdue: 'danger' };
      return map[status] || 'info';
    },
    getStatusText(status) {
      const map = { borrowed: '借阅中', returned: '已归还', overdue: '已逾期' };
      return map[status] || '未知';
    },
    getBookCategory(bookId) {
      const book = this.bookList.find(b => b.id === bookId);
      return book ? book.category : '-';
    },
    increaseStock(bookId) {
      const book = this.bookList.find(item => item.id === bookId);
      if (book) {
        book.stock += 1;
      }
    },
    handleSearch() {
      this.currentPage = 1;
      this.$message.success('搜索完成');
    },
    handleReset() {
      this.searchForm = {
        bookName: '',
        borrower: '',
        category: '',
        borrowDateStart: '',
        borrowDateEnd: '',
        status: ''
      };
      this.currentPage = 1;
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    handleReturn(row) {
      this.$confirm('确认归还该图书吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        row.status = 'returned';
        row.returnDate = this.formatDate(new Date());
        this.increaseStock(row.bookId);
        this.$message.success('归还成功！库存已自动更新');
      }).catch(() => {});
    },
    handleView(row) {
      this.currentRecord = row;
      this.detailDialogVisible = true;
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
</style>