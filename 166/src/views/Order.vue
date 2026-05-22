<template>
  <div class="page-card">
    <el-row :gutter="20">
      <el-col :span="14">
        <h3 style="margin-bottom: 15px">书籍选购</h3>
        <div class="search-bar">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索书名/作者"
            clearable
            @clear="loadBooks"
          >
            <el-button slot="append" icon="el-icon-search" @click="loadBooks"></el-button>
          </el-input>
        </div>
        <el-table :data="bookList" border style="width: 100%" v-loading="loading" max-height="500">
          <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
          <el-table-column prop="bookName" label="书名" min-width="150"></el-table-column>
          <el-table-column prop="author" label="作者" width="120"></el-table-column>
          <el-table-column label="成色" width="100" align="center">
            <template slot-scope="scope">
              {{ getConditionLabel(scope.row.condition) }}
            </template>
          </el-table-column>
          <el-table-column prop="sellPrice" label="售价" width="100" align="center">
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
          <el-table-column label="操作" width="100" align="center">
            <template slot-scope="scope">
              <el-button
                type="primary"
                size="small"
                @click="addToCart(scope.row)"
                :disabled="scope.row.stock <= 0"
              >{{ scope.row.stock > 0 ? '购买' : '售罄' }}</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
      <el-col :span="10">
        <h3 style="margin-bottom: 15px">订单信息</h3>
        <el-card v-if="cartItems.length === 0" style="text-align: center; padding: 40px 0">
          <i class="el-icon-shopping-cart-empty" style="font-size: 48px; color: #909399"></i>
          <p style="margin-top: 15px; color: #909399">购物车为空，请选择书籍</p>
        </el-card>
        <el-card v-else>
          <el-table :data="cartItems" border size="small">
            <el-table-column prop="bookName" label="书名"></el-table-column>
            <el-table-column prop="sellPrice" label="单价" width="80" align="center">
              <template slot-scope="scope">
                ¥{{ scope.row.sellPrice }}
              </template>
            </el-table-column>
            <el-table-column label="数量" width="100" align="center">
              <template slot-scope="scope">
                <el-input-number
                  v-model="scope.row.quantity"
                  :min="1"
                  :max="scope.row.stock"
                  size="small"
                  @change="calculateTotal"
                ></el-input-number>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="70" align="center">
              <template slot-scope="scope">
                <el-button
                  type="danger"
                  size="mini"
                  icon="el-icon-delete"
                  @click="removeFromCart(scope.$index)"
                ></el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 15px; text-align: right; font-size: 16px">
            总计：<span style="color: #f56c6c; font-weight: bold; font-size: 20px">¥{{ totalPrice }}</span>
          </div>
          <el-divider></el-divider>
          <el-form :model="orderForm" :rules="orderRules" ref="orderForm" label-width="80px">
            <el-form-item label="买家姓名" prop="buyerName">
              <el-input v-model="orderForm.buyerName" placeholder="请输入姓名"></el-input>
            </el-form-item>
            <el-form-item label="联系电话" prop="buyerPhone">
              <el-input v-model="orderForm.buyerPhone" placeholder="请输入电话"></el-input>
            </el-form-item>
            <el-form-item label="收货地址" prop="buyerAddress">
              <el-input
                v-model="orderForm.buyerAddress"
                type="textarea"
                :rows="3"
                placeholder="请输入收货地址"
              ></el-input>
            </el-form-item>
            <el-form-item style="text-align: center; margin-bottom: 0">
              <el-button type="primary" @click="submitOrder" :loading="submitLoading" size="large">提交订单</el-button>
              <el-button @click="clearCart">清空购物车</el-button>
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>
    </el-row>

    <el-divider></el-divider>

    <h3 style="margin-bottom: 15px">订单列表</h3>
    <div class="search-bar">
      <el-row :gutter="20">
        <el-col :span="5">
          <el-input
            v-model="orderSearchKeyword"
            placeholder="搜索商品/买家/电话"
            clearable
            @clear="loadOrders"
          >
            <el-button slot="append" icon="el-icon-search" @click="loadOrders"></el-button>
          </el-input>
        </el-col>
        <el-col :span="3">
          <el-select v-model="orderSearchStatus" placeholder="状态筛选" clearable style="width: 100%" @change="loadOrders">
            <el-option label="待发货" value="pending"></el-option>
            <el-option label="已发货" value="shipped"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-date-picker
            v-model="orderSearchDateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 100%"
            clearable
            @change="loadOrders"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          ></el-date-picker>
        </el-col>
        <el-col :span="3">
          <el-button type="primary" @click="resetOrderSearch" style="width: 100%">重置筛选</el-button>
        </el-col>
      </el-row>
    </div>
    <el-table :data="orderList" border style="width: 100%" v-loading="orderLoading">
      <el-table-column prop="orderNo" label="订单号" width="180"></el-table-column>
      <el-table-column prop="bookName" label="商品" min-width="150"></el-table-column>
      <el-table-column prop="buyerName" label="买家" width="100"></el-table-column>
      <el-table-column prop="buyerPhone" label="联系电话" width="120"></el-table-column>
      <el-table-column prop="buyerAddress" label="收货地址" min-width="200"></el-table-column>
      <el-table-column prop="price" label="金额" width="100" align="center">
        <template slot-scope="scope">
          <span style="color: #f56c6c; font-weight: bold">¥{{ scope.row.price }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="createTime" label="下单时间" width="160"></el-table-column>
      <el-table-column prop="shipTime" label="发货时间" width="160">
        <template slot-scope="scope">
          {{ scope.row.shipTime || '-' }}
        </template>
      </el-table-column>
      <el-table-column label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" align="center">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.status === 'pending'"
            type="success"
            size="small"
            @click="shipOrder(scope.row)"
          >发货</el-button>
          <el-button
            v-if="scope.row.status === 'shipped'"
            type="primary"
            size="small"
            @click="completeOrder(scope.row)"
          >完成</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="pagination-container">
      <el-pagination
        :current-page="orderPage"
        :page-sizes="[5, 10, 20, 50]"
        :page-size="pageSize"
        :total="orderTotal"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="handleOrderPageChange"
        @size-change="handleOrderSizeChange"
      ></el-pagination>
    </div>
  </div>
</template>

<script>
import { bookConditions, orderStatusMap } from '../utils/mockData'
import { getBooks, getOrders, saveOrder, updateOrderStatus, initStorage } from '../utils/storage'

export default {
  name: 'Order',
  data() {
    return {
      loading: false,
      submitLoading: false,
      orderLoading: false,
      searchKeyword: '',
      orderSearchKeyword: '',
      orderSearchStatus: '',
      orderSearchDateRange: [],
      page: 1,
      orderPage: 1,
      pageSize: 10,
      bookList: [],
      cartItems: [],
      orderList: [],
      orderTotal: 0,
      totalPrice: 0,
      conditions: bookConditions,
      statusMap: orderStatusMap,
      orderForm: {
        buyerName: '',
        buyerPhone: '',
        buyerAddress: ''
      },
      orderRules: {
        buyerName: [
          { required: true, message: '请输入买家姓名', trigger: 'blur' }
        ],
        buyerPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
        ],
        buyerAddress: [
          { required: true, message: '请输入收货地址', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    initStorage()
    this.loadBooks()
    this.loadOrders()
  },
  methods: {
    getConditionLabel(value) {
      const cond = this.conditions.find(c => c.value === value)
      return cond ? cond.label : value
    },
    loadBooks() {
      this.loading = true
      setTimeout(() => {
        let data = getBooks().filter(book => book.status === 'on_sale')
        if (this.searchKeyword) {
          data = data.filter(item => 
            item.bookName.includes(this.searchKeyword) || 
            item.author.includes(this.searchKeyword)
          )
        }
        this.bookList = data
        this.loading = false
      }, 300)
    },
    filterOrderByDateRange(dateStr, dateRange) {
      if (!dateRange || dateRange.length !== 2) return true
      const [startDate, endDate] = dateRange
      const itemDate = dateStr.split(' ')[0]
      return itemDate >= startDate && itemDate <= endDate
    },
    loadOrders() {
      this.orderLoading = true
      setTimeout(() => {
        let data = getOrders()
        if (this.orderSearchKeyword) {
          data = data.filter(item => 
            item.bookName.includes(this.orderSearchKeyword) || 
            item.buyerName.includes(this.orderSearchKeyword) ||
            item.buyerPhone.includes(this.orderSearchKeyword)
          )
        }
        if (this.orderSearchStatus) {
          data = data.filter(item => item.status === this.orderSearchStatus)
        }
        data = data.filter(item => this.filterOrderByDateRange(item.createTime, this.orderSearchDateRange))
        this.orderTotal = data.length
        const start = (this.orderPage - 1) * this.pageSize
        this.orderList = data.slice(start, start + this.pageSize)
        this.orderLoading = false
      }, 300)
    },
    handleOrderPageChange(page) {
      this.orderPage = page
      this.loadOrders()
    },
    handleOrderSizeChange(size) {
      this.pageSize = size
      this.orderPage = 1
      this.loadOrders()
    },
    resetOrderSearch() {
      this.orderSearchKeyword = ''
      this.orderSearchStatus = ''
      this.orderSearchDateRange = []
      this.orderPage = 1
      this.loadOrders()
    },
    addToCart(book) {
      if (book.stock <= 0) {
        this.$message.error('该书籍库存不足')
        return
      }
      const existItem = this.cartItems.find(item => item.id === book.id)
      if (existItem) {
        if (existItem.quantity >= book.stock) {
          this.$message.error('超出库存限制')
          return
        }
        existItem.quantity += 1
      } else {
        this.cartItems.push({
          ...book,
          quantity: 1
        })
      }
      this.calculateTotal()
      this.$message.success('已添加到购物车')
    },
    removeFromCart(index) {
      this.cartItems.splice(index, 1)
      this.calculateTotal()
    },
    clearCart() {
      this.cartItems = []
      this.totalPrice = 0
    },
    calculateTotal() {
      this.totalPrice = this.cartItems.reduce((sum, item) => 
        sum + item.sellPrice * item.quantity, 0
      ).toFixed(2)
    },
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          if (this.cartItems.length === 0) {
            this.$message.warning('请选择要购买的书籍')
            return
          }
          const latestBooks = getBooks()
          for (const item of this.cartItems) {
            const realBook = latestBooks.find(b => b.id === item.id)
            if (!realBook || realBook.stock < item.quantity) {
              this.$message.error(`《${item.bookName}》库存不足，请调整购买数量`)
              this.loadBooks()
              return
            }
          }
          this.submitLoading = true
          setTimeout(() => {
            try {
              this.cartItems.forEach(item => {
                const order = {
                  bookId: item.id,
                  bookName: item.bookName,
                  buyerName: this.orderForm.buyerName,
                  buyerPhone: this.orderForm.buyerPhone,
                  buyerAddress: this.orderForm.buyerAddress,
                  quantity: item.quantity,
                  price: (item.sellPrice * item.quantity).toFixed(2)
                }
                saveOrder(order)
              })
              this.$message.success('订单提交成功！')
              this.clearCart()
              this.$refs.orderForm.resetFields()
              this.submitLoading = false
              this.loadOrders()
              this.loadBooks()
            } catch (error) {
              this.$message.error(error.message)
              this.submitLoading = false
              this.loadBooks()
            }
          }, 500)
        } else {
          this.$message.error('请检查订单信息填写是否正确')
          return false
        }
      })
    },
    shipOrder(row) {
      this.$confirm('确认发货？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        updateOrderStatus(row.id, 'shipped')
        this.$message.success('发货成功！')
        this.loadOrders()
      }).catch(() => {})
    },
    completeOrder(row) {
      this.$confirm('确认完成该订单？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        updateOrderStatus(row.id, 'completed')
        this.$message.success('订单已完成！')
        this.loadOrders()
      }).catch(() => {})
    }
  }
}
</script>
