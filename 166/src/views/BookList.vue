<template>
  <div class="page-card">
    <div class="search-bar">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索书名/作者/ISBN"
            clearable
            @clear="loadData"
          >
            <el-button slot="append" icon="el-icon-search" @click="loadData"></el-button>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchCategory" placeholder="分类筛选" clearable style="width: 100%" @change="loadData">
            <el-option
              v-for="category in categories"
              :key="category"
              :label="category"
              :value="category"
            ></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchStatus" placeholder="状态筛选" clearable style="width: 100%" @change="loadData">
            <el-option label="待上架" value="pending"></el-option>
            <el-option label="售卖中" value="on_sale"></el-option>
            <el-option label="已售出" value="sold"></el-option>
            <el-option label="已下架" value="off_shelf"></el-option>
          </el-select>
        </el-col>
      </el-row>
    </div>
    <el-table :data="tableData" border style="width: 100%" v-loading="loading">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="bookName" label="书名" min-width="150"></el-table-column>
      <el-table-column prop="author" label="作者" width="120"></el-table-column>
      <el-table-column prop="isbn" label="ISBN" width="130"></el-table-column>
      <el-table-column prop="category" label="分类" width="100"></el-table-column>
      <el-table-column label="成色" width="100" align="center">
        <template slot-scope="scope">
          {{ getConditionLabel(scope.row.condition) }}
        </template>
      </el-table-column>
      <el-table-column prop="originalPrice" label="原价" width="90" align="center">
        <template slot-scope="scope">
          ¥{{ scope.row.originalPrice }}
        </template>
      </el-table-column>
      <el-table-column prop="sellPrice" label="售价" width="90" align="center">
        <template slot-scope="scope">
          <span style="color: #f56c6c; font-weight: bold">¥{{ scope.row.sellPrice }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="stock" label="库存" width="80" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.stock > 0 ? 'success' : 'danger'" size="small">
            {{ scope.row.stock }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="录入时间" width="160"></el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="220" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.status === 'pending'"
            type="success"
            size="small"
            @click="putOnSale(scope.row)"
          >上架</el-button>
          <el-button
            v-if="scope.row.status === 'on_sale'"
            type="warning"
            size="small"
            @click="offShelf(scope.row)"
          >下架</el-button>
          <el-button
            type="primary"
            size="small"
            @click="viewDetail(scope.row)"
          >详情</el-button>
          <el-button
            type="danger"
            size="small"
            @click="deleteBook(scope.row)"
          >删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        :current-page="page"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next, jumper"
        @current-change="handlePageChange"
      ></el-pagination>
    </div>

    <el-dialog title="书籍详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="2" border v-if="currentBook">
        <el-descriptions-item label="书名">{{ currentBook.bookName }}</el-descriptions-item>
        <el-descriptions-item label="作者">{{ currentBook.author }}</el-descriptions-item>
        <el-descriptions-item label="ISBN">{{ currentBook.isbn }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ currentBook.category }}</el-descriptions-item>
        <el-descriptions-item label="成色">{{ getConditionLabel(currentBook.condition) }}</el-descriptions-item>
        <el-descriptions-item label="原价">¥{{ currentBook.originalPrice }}</el-descriptions-item>
        <el-descriptions-item label="回收价">¥{{ currentBook.recyclePrice }}</el-descriptions-item>
        <el-descriptions-item label="售价"><span style="color: #f56c6c; font-weight: bold">¥{{ currentBook.sellPrice }}</span></el-descriptions-item>
        <el-descriptions-item label="库存">
          <el-tag :type="currentBook.stock > 0 ? 'success' : 'danger'" size="small">{{ currentBook.stock }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusMap[currentBook.status].type">
            {{ statusMap[currentBook.status].label }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="录入时间" :span="2">{{ currentBook.createTime }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ currentBook.description || '暂无描述' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { bookCategories, bookConditions, bookStatusMap } from '../utils/mockData'
import { getBooks, updateBookStatus, deleteBook as deleteBookApi, initStorage } from '../utils/storage'

export default {
  name: 'BookList',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      searchCategory: '',
      searchStatus: '',
      page: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      categories: bookCategories,
      conditions: bookConditions,
      statusMap: bookStatusMap,
      detailDialogVisible: false,
      currentBook: null
    }
  },
  mounted() {
    initStorage()
    this.loadData()
  },
  methods: {
    getConditionLabel(value) {
      const cond = this.conditions.find(c => c.value === value)
      return cond ? cond.label : value
    },
    loadData() {
      this.loading = true
      setTimeout(() => {
        let data = getBooks()
        if (this.searchKeyword) {
          data = data.filter(item => 
            item.bookName.includes(this.searchKeyword) || 
            item.author.includes(this.searchKeyword) ||
            item.isbn.includes(this.searchKeyword)
          )
        }
        if (this.searchCategory) {
          data = data.filter(item => item.category === this.searchCategory)
        }
        if (this.searchStatus) {
          data = data.filter(item => item.status === this.searchStatus)
        }
        this.total = data.length
        const start = (this.page - 1) * this.pageSize
        this.tableData = data.slice(start, start + this.pageSize)
        this.loading = false
      }, 300)
    },
    handlePageChange(page) {
      this.page = page
      this.loadData()
    },
    putOnSale(row) {
      this.$confirm('确认将该书籍上架售卖？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        updateBookStatus(row.id, 'on_sale')
        this.$message.success('上架成功！')
        this.loadData()
      }).catch(() => {})
    },
    offShelf(row) {
      this.$confirm('确认将该书籍下架？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        updateBookStatus(row.id, 'off_shelf')
        this.$message.success('下架成功！')
        this.loadData()
      }).catch(() => {})
    },
    viewDetail(row) {
      this.currentBook = row
      this.detailDialogVisible = true
    },
    deleteBook(row) {
      this.$confirm('确认删除该书籍？删除后无法恢复！', '警告', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteBookApi(row.id)
        this.$message.success('删除成功！')
        this.loadData()
      }).catch(() => {})
    }
  }
}
</script>
