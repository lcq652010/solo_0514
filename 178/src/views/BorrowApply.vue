<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">借阅申请</h2>
    </div>
    <div class="card-wrapper">
      <div class="form-wrapper">
        <el-form :model="borrowForm" :rules="rules" ref="borrowForm" label-width="120px">
          <el-form-item label="借阅图书" prop="bookId">
            <el-select v-model="borrowForm.bookId" placeholder="请选择图书" style="width: 100%" @change="handleBookChange">
              <el-option 
                v-for="item in bookList" 
                :key="item.id" 
                :label="`${item.name} (库存: ${item.stock})`" 
                :value="item.id"
                :disabled="item.stock <= 0">
                <span style="float: left">{{ item.name }}</span>
                <span style="float: right; color: #8492a6; font-size: 13px">
                  <el-tag :type="item.stock > 5 ? 'success' : item.stock > 0 ? 'warning' : 'danger'" size="mini">
                    库存: {{ item.stock }}
                  </el-tag>
                </span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="借阅人" prop="borrower">
            <el-input v-model="borrowForm.borrower" placeholder="请输入借阅人姓名"></el-input>
          </el-form-item>
          <el-form-item label="借阅人工号" prop="borrowerNo">
            <el-input v-model="borrowForm.borrowerNo" placeholder="请输入借阅人工号"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="borrowForm.phone" placeholder="请输入联系电话"></el-input>
          </el-form-item>
          <el-form-item label="所属部门" prop="department">
            <el-select v-model="borrowForm.department" placeholder="请选择部门" style="width: 100%">
              <el-option label="技术部" value="技术部"></el-option>
              <el-option label="产品部" value="产品部"></el-option>
              <el-option label="运营部" value="运营部"></el-option>
              <el-option label="市场部" value="市场部"></el-option>
              <el-option label="人事部" value="人事部"></el-option>
              <el-option label="财务部" value="财务部"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="借阅日期" prop="borrowDate">
            <el-date-picker
              v-model="borrowForm.borrowDate"
              type="date"
              placeholder="选择借阅日期"
              style="width: 100%"
              value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="预计归还日期" prop="dueDate">
            <el-date-picker
              v-model="borrowForm.dueDate"
              type="date"
              placeholder="选择预计归还日期"
              style="width: 100%"
              value-format="yyyy-MM-dd">
            </el-date-picker>
          </el-form-item>
          <el-form-item label="借阅用途" prop="purpose">
            <el-input type="textarea" v-model="borrowForm.purpose" :rows="4" placeholder="请输入借阅用途"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交申请</el-button>
            <el-button @click="resetForm">重置</el-button>
            <el-button @click="goBack">返回</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { bookList, borrowRecords } from '@/mock/data';

export default {
  name: 'BorrowApply',
  data() {
    const validateDueDate = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请选择预计归还日期'));
      } else if (value <= this.borrowForm.borrowDate) {
        callback(new Error('预计归还日期必须晚于借阅日期'));
      } else {
        callback();
      }
    };
    return {
      bookList: bookList,
      borrowRecords: borrowRecords,
      selectedBookInfo: null,
      borrowForm: {
        bookId: '',
        borrower: '',
        borrowerNo: '',
        phone: '',
        department: '',
        borrowDate: '',
        dueDate: '',
        purpose: ''
      },
      rules: {
        bookId: [{ required: true, message: '请选择借阅图书', trigger: 'change' }],
        borrower: [
          { required: true, message: '请输入借阅人姓名', trigger: 'blur' },
          { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
        ],
        borrowerNo: [
          { required: true, message: '请输入借阅人工号', trigger: 'blur' },
          { pattern: /^[A-Za-z0-9]+$/, message: '工号只能包含字母和数字', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ],
        department: [{ required: true, message: '请选择所属部门', trigger: 'change' }],
        borrowDate: [{ required: true, message: '请选择借阅日期', trigger: 'change' }],
        dueDate: [{ required: true, validator: validateDueDate, trigger: 'change' }],
        purpose: [{ required: true, message: '请输入借阅用途', trigger: 'blur' }]
      }
    };
  },
  mounted() {
    if (this.$route.query.bookId) {
      this.borrowForm.bookId = parseInt(this.$route.query.bookId);
      this.handleBookChange(this.borrowForm.bookId);
    }
    if (this.$route.query.borrowerNo) {
      this.borrowForm.borrowerNo = this.$route.query.borrowerNo;
    }
    const today = new Date();
    const borrowDate = this.formatDate(today);
    const dueDate = this.formatDate(new Date(today.getTime() + 30 * 24 * 60 * 60 * 1000));
    this.borrowForm.borrowDate = borrowDate;
    this.borrowForm.dueDate = dueDate;
  },
  methods: {
    formatDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },
    handleBookChange(bookId) {
      this.selectedBookInfo = this.bookList.find(item => item.id === bookId);
    },
    checkStock(bookId) {
      const book = this.bookList.find(item => item.id === bookId);
      if (!book) {
        return { valid: false, message: '图书不存在' };
      }
      if (book.stock <= 0) {
        return { valid: false, message: `《${book.name}》库存不足，无法借阅` };
      }
      return { valid: true, message: '' };
    },
    checkDuplicateBorrow(bookId, borrowerNo) {
      const book = this.bookList.find(item => item.id === bookId);
      const hasBorrowed = this.borrowRecords.some(record => 
        record.bookId === bookId && 
        record.borrowerNo === borrowerNo && 
        record.status !== 'returned'
      );
      if (hasBorrowed) {
        return { valid: false, message: `您已借阅《${book.name}》且尚未归还，请勿重复借阅` };
      }
      return { valid: true, message: '' };
    },
    submitForm() {
      this.$refs.borrowForm.validate((valid) => {
        if (valid) {
          const stockCheck = this.checkStock(this.borrowForm.bookId);
          if (!stockCheck.valid) {
            this.$message.error(stockCheck.message);
            return;
          }
          const duplicateCheck = this.checkDuplicateBorrow(this.borrowForm.bookId, this.borrowForm.borrowerNo);
          if (!duplicateCheck.valid) {
            this.$message.error(duplicateCheck.message);
            return;
          }
          const book = this.bookList.find(item => item.id === this.borrowForm.bookId);
          book.stock -= 1;
          const newRecord = {
            id: this.borrowRecords.length + 1,
            bookId: this.borrowForm.bookId,
            bookName: book.name,
            borrower: this.borrowForm.borrower,
            borrowerNo: this.borrowForm.borrowerNo,
            borrowDate: this.borrowForm.borrowDate,
            dueDate: this.borrowForm.dueDate,
            returnDate: null,
            status: 'borrowed'
          };
          this.borrowRecords.push(newRecord);
          this.$message.success('借阅申请提交成功！');
          setTimeout(() => {
            this.$router.push('/borrow/records');
          }, 1000);
        } else {
          this.$message.error('请检查表单填写是否正确');
          return false;
        }
      });
    },
    resetForm() {
      this.$refs.borrowForm.resetFields();
      this.selectedBookInfo = null;
      const today = new Date();
      const borrowDate = this.formatDate(today);
      const dueDate = this.formatDate(new Date(today.getTime() + 30 * 24 * 60 * 60 * 1000));
      this.borrowForm.borrowDate = borrowDate;
      this.borrowForm.dueDate = dueDate;
    },
    goBack() {
      this.$router.back();
    }
  }
};
</script>

<style scoped>
</style>