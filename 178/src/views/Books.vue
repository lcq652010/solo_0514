<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">图书列表</h2>
    </div>
    <div class="card-wrapper">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm" class="demo-form-inline">
          <el-form-item label="当前读者">
            <el-input v-model="currentBorrowerNo" placeholder="请输入读者工号" style="width: 150px;"></el-input>
          </el-form-item>
          <el-form-item label="图书名称">
            <el-input v-model="searchForm.name" placeholder="请输入图书名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="分类">
            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
              <el-option v-for="item in categoryList" :key="item" :label="item" :value="item"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      <div class="table-wrapper">
        <el-table :data="filteredBooks" border stripe style="width: 100%">
          <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
          <el-table-column prop="isbn" label="ISBN" width="140" align="center"></el-table-column>
          <el-table-column prop="name" label="图书名称" min-width="180"></el-table-column>
          <el-table-column prop="author" label="作者" width="120"></el-table-column>
          <el-table-column prop="publisher" label="出版社" width="140"></el-table-column>
          <el-table-column prop="category" label="分类" width="100" align="center"></el-table-column>
          <el-table-column prop="stock" label="库存" width="80" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.stock > 10 ? 'success' : scope.row.stock > 5 ? 'warning' : 'danger'" size="small">
                {{ scope.row.stock }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="price" label="价格" width="100" align="center">
            <template slot-scope="scope">
              ¥{{ scope.row.price.toFixed(2) }}
            </template>
          </el-table-column>
          <el-table-column prop="publishDate" label="出版日期" width="120" align="center"></el-table-column>
          <el-table-column label="操作" width="200" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button 
                v-if="!hasBorrowed(scope.row.id)" 
                type="primary" 
                size="mini" 
                @click="handleBorrow(scope.row)" 
                :disabled="scope.row.stock <= 0">
                {{ scope.row.stock <= 0 ? '无库存' : '借阅' }}
              </el-button>
              <el-tag v-else type="warning" size="small">已借阅</el-tag>
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

    <el-dialog title="图书详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentBook">
        <el-descriptions-item label="ISBN">{{ currentBook.isbn }}</el-descriptions-item>
        <el-descriptions-item label="图书名称">{{ currentBook.name }}</el-descriptions-item>
        <el-descriptions-item label="作者">{{ currentBook.author }}</el-descriptions-item>
        <el-descriptions-item label="出版社">{{ currentBook.publisher }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentBook.category }}</el-descriptions-item>
        <el-descriptions-item label="库存">{{ currentBook.stock }}</el-descriptions-item>
        <el-descriptions-item label="价格">¥{{ currentBook.price.toFixed(2) }}</el-descriptions-item>
        <el-descriptions-item label="出版日期">{{ currentBook.publishDate }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { bookList, categoryList, borrowRecords } from '@/mock/data';

export default {
  name: 'Books',
  data() {
    return {
      bookList: bookList,
      borrowRecords: borrowRecords,
      categoryList: categoryList,
      currentBorrowerNo: 'ST009',
      searchForm: {
        name: '',
        category: ''
      },
      currentPage: 1,
      pageSize: 10,
      detailDialogVisible: false,
      currentBook: null
    };
  },
  computed: {
    filteredBooks() {
      let list = this.bookList;
      if (this.searchForm.name) {
        list = list.filter(item => item.name.includes(this.searchForm.name));
      }
      if (this.searchForm.category) {
        list = list.filter(item => item.category === this.searchForm.category);
      }
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return list.slice(start, end);
    },
    total() {
      let list = this.bookList;
      if (this.searchForm.name) {
        list = list.filter(item => item.name.includes(this.searchForm.name));
      }
      if (this.searchForm.category) {
        list = list.filter(item => item.category === this.searchForm.category);
      }
      return list.length;
    }
  },
  methods: {
    handleSearch() {
      this.currentPage = 1;
      this.$message.success('搜索完成');
    },
    handleReset() {
      this.searchForm = {
        name: '',
        category: ''
      };
      this.currentPage = 1;
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    hasBorrowed(bookId) {
      return this.borrowRecords.some(record => 
        record.bookId === bookId && 
        record.borrowerNo === this.currentBorrowerNo && 
        record.status !== 'returned'
      );
    },
    handleBorrow(row) {
      if (row.stock <= 0) {
        this.$message.error('库存不足，无法借阅');
        return;
      }
      if (this.hasBorrowed(row.id)) {
        this.$message.error('您已借阅该图书且尚未归还');
        return;
      }
      this.$router.push({
        path: '/borrow/apply',
        query: { bookId: row.id, bookName: row.name, borrowerNo: this.currentBorrowerNo }
      });
    },
    handleView(row) {
      this.currentBook = row;
      this.detailDialogVisible = true;
    }
  }
};
</script>

<style scoped>
</style>