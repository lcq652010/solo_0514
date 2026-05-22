<template>
  <div class="page-card">
    <el-form
      ref="bookForm"
      :model="bookForm"
      :rules="rules"
      label-width="100px"
      class="form-container"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="书名" prop="bookName">
            <el-input v-model="bookForm.bookName" placeholder="请输入书名"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="作者" prop="author">
            <el-input v-model="bookForm.author" placeholder="请输入作者"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="ISBN" prop="isbn">
            <el-input 
              v-model="bookForm.isbn" 
              placeholder="请输入ISBN号"
              @input="checkIsbnDuplicate"
            >
              <template slot="append">
                <span v-if="isbnChecking" style="color: #909399">检测中...</span>
                <span v-else-if="isbnExist" style="color: #f56c6c">已存在</span>
                <span v-else-if="isbnValid && bookForm.isbn" style="color: #67c23a">可用</span>
              </template>
            </el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="分类" prop="category">
            <el-select v-model="bookForm.category" placeholder="请选择分类" style="width: 100%">
              <el-option
                v-for="category in categories"
                :key="category"
                :label="category"
                :value="category"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="成色" prop="condition">
            <el-select v-model="bookForm.condition" placeholder="请选择成色" style="width: 100%" @change="calculatePrice">
              <el-option
                v-for="cond in conditions"
                :key="cond.value"
                :label="cond.label"
                :value="cond.value"
              ></el-option>
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="原价" prop="originalPrice">
            <el-input-number
              v-model="bookForm.originalPrice"
              :min="0"
              :precision="2"
              style="width: 100%"
              @change="calculatePrice"
            ></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="回收价">
            <el-input v-model="bookForm.recyclePrice" disabled></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="售卖价" prop="sellPrice">
            <el-input-number
              v-model="bookForm.sellPrice"
              :min="0"
              :precision="2"
              style="width: 100%"
            ></el-input-number>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item label="描述" prop="description">
        <el-input
          v-model="bookForm.description"
          type="textarea"
          :rows="4"
          placeholder="请输入书籍描述"
        ></el-input>
      </el-form-item>
      <el-divider content-position="left">卖家信息</el-divider>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="卖家姓名" prop="sellerName">
            <el-input v-model="bookForm.sellerName" placeholder="请输入卖家姓名"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="卖家电话" prop="sellerPhone">
            <el-input v-model="bookForm.sellerPhone" placeholder="请输入卖家电话"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-form-item style="text-align: center; margin-top: 30px">
        <el-button type="primary" @click="submitForm" :loading="loading">提交录入</el-button>
        <el-button @click="resetForm">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { bookCategories, bookConditions } from '../utils/mockData'
import { saveBook, saveRecycleRecord, initStorage, checkIsbnExists } from '../utils/storage'

export default {
  name: 'BookEntry',
  data() {
    const validateIsbn = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入ISBN号'))
      } else if (!/^\d{10,13}$/.test(value)) {
        callback(new Error('请输入正确的ISBN号'))
      } else {
        if (checkIsbnExists(value)) {
          callback(new Error('该ISBN已存在，请勿重复录入'))
        } else {
          callback()
        }
      }
    }
    return {
      loading: false,
      isbnChecking: false,
      isbnExist: false,
      isbnValid: false,
      categories: bookCategories,
      conditions: bookConditions,
      bookForm: {
        bookName: '',
        author: '',
        isbn: '',
        category: '',
        condition: '',
        originalPrice: null,
        recyclePrice: 0,
        sellPrice: null,
        description: '',
        sellerName: '',
        sellerPhone: '',
        status: 'pending'
      },
      rules: {
        bookName: [
          { required: true, message: '请输入书名', trigger: 'blur' },
          { min: 1, max: 100, message: '长度在 1 到 100 个字符', trigger: 'blur' }
        ],
        author: [
          { required: true, message: '请输入作者', trigger: 'blur' },
          { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
        ],
        isbn: [
          { validator: validateIsbn, trigger: 'blur' }
        ],
        category: [
          { required: true, message: '请选择分类', trigger: 'change' }
        ],
        condition: [
          { required: true, message: '请选择成色', trigger: 'change' }
        ],
        originalPrice: [
          { required: true, message: '请输入原价', trigger: 'blur' },
          { type: 'number', message: '请输入正确的价格', trigger: 'blur' }
        ],
        sellPrice: [
          { required: true, message: '请输入售卖价', trigger: 'blur' },
          { type: 'number', message: '请输入正确的价格', trigger: 'blur' }
        ],
        sellerName: [
          { required: true, message: '请输入卖家姓名', trigger: 'blur' },
          { min: 2, max: 20, message: '长度在 2 到 20 个字符', trigger: 'blur' }
        ],
        sellerPhone: [
          { required: true, message: '请输入卖家电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    initStorage()
  },
  methods: {
    checkIsbnDuplicate() {
      const isbn = this.bookForm.isbn
      if (!isbn || isbn.length < 10) {
        this.isbnExist = false
        this.isbnValid = false
        return
      }
      if (!/^\d{10,13}$/.test(isbn)) {
        this.isbnExist = false
        this.isbnValid = false
        return
      }
      this.isbnChecking = true
      setTimeout(() => {
        this.isbnExist = checkIsbnExists(isbn)
        this.isbnValid = !this.isbnExist
        this.isbnChecking = false
      }, 300)
    },
    calculatePrice() {
      if (this.bookForm.condition && this.bookForm.originalPrice) {
        const cond = this.conditions.find(c => c.value === this.bookForm.condition)
        if (cond) {
          this.bookForm.recyclePrice = (this.bookForm.originalPrice * cond.discount).toFixed(2)
        }
      }
    },
    submitForm() {
      this.$refs.bookForm.validate((valid) => {
        if (valid) {
          if (checkIsbnExists(this.bookForm.isbn)) {
            this.$message.error('该ISBN已存在，请勿重复录入')
            return
          }
          this.loading = true
          setTimeout(() => {
            const bookData = {
              bookName: this.bookForm.bookName,
              author: this.bookForm.author,
              isbn: this.bookForm.isbn,
              category: this.bookForm.category,
              condition: this.bookForm.condition,
              originalPrice: this.bookForm.originalPrice,
              recyclePrice: parseFloat(this.bookForm.recyclePrice),
              sellPrice: this.bookForm.sellPrice,
              description: this.bookForm.description,
              status: 'pending'
            }
            saveBook(bookData)
            const recycleRecord = {
              bookName: this.bookForm.bookName,
              author: this.bookForm.author,
              sellerName: this.bookForm.sellerName,
              sellerPhone: this.bookForm.sellerPhone,
              condition: this.bookForm.condition,
              originalPrice: this.bookForm.originalPrice,
              recyclePrice: parseFloat(this.bookForm.recyclePrice)
            }
            saveRecycleRecord(recycleRecord)
            this.$message.success('书籍录入成功！')
            this.resetForm()
            this.loading = false
          }, 500)
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.bookForm.resetFields()
      this.bookForm.recyclePrice = 0
      this.isbnExist = false
      this.isbnValid = false
      this.isbnChecking = false
    }
  }
}
</script>
