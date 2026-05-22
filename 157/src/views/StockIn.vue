<template>
  <div class="page-container">
    <div class="page-header">
      <span class="page-title">入库登记</span>
    </div>
    
    <el-card style="margin-bottom: 20px;">
      <div slot="header">
        <span>新增入库</span>
      </div>
      <el-form :model="stockInForm" :rules="rules" ref="stockInForm" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="用品名称" prop="supplyId">
              <el-select v-model="stockInForm.supplyId" placeholder="请选择用品" style="width: 100%" @change="handleSupplyChange">
                <el-option v-for="supply in supplies" :key="supply.id" :label="supply.name" :value="supply.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="当前库存">
              <el-input :value="currentSupply.stock" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="单位">
              <el-input :value="currentSupply.unit" disabled></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="入库数量" prop="quantity">
              <el-input-number v-model="stockInForm.quantity" :min="1" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="4">
            <el-form-item label="单价(元)" prop="price">
              <el-input-number v-model="stockInForm.price" :min="0" :precision="2" style="width: 100%"></el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="操作员" prop="operator">
              <el-input v-model="stockInForm.operator" placeholder="请输入操作员姓名"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="16">
            <el-form-item label="备注" prop="remark">
              <el-input v-model="stockInForm.remark" placeholder="请输入备注信息"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item>
          <el-button type="primary" @click="handleStockIn" :loading="submitLoading">
            <i class="el-icon-check"></i> 确认入库
          </el-button>
          <el-button @click="handleReset">
            <i class="el-icon-refresh"></i> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="search-bar">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="入库单号">
          <el-input v-model="searchForm.inNo" placeholder="请输入入库单号" clearable></el-input>
        </el-form-item>
        <el-form-item label="用品名称">
          <el-select v-model="searchForm.supplyId" placeholder="请选择用品" clearable>
            <el-option v-for="supply in supplies" :key="supply.id" :label="supply.name" :value="supply.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <i class="el-icon-search"></i> 搜索
          </el-button>
          <el-button @click="handleResetSearch">
            <i class="el-icon-refresh"></i> 重置
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="table-container">
      <el-table :data="tableData" border stripe>
        <el-table-column prop="inNo" label="入库单号" width="150" align="center"></el-table-column>
        <el-table-column prop="supplyName" label="用品名称" min-width="150"></el-table-column>
        <el-table-column prop="quantity" label="数量" width="100" align="center"></el-table-column>
        <el-table-column prop="unit" label="单位" width="80" align="center"></el-table-column>
        <el-table-column prop="price" label="单价(元)" width="100" align="center"></el-table-column>
        <el-table-column prop="totalPrice" label="总价(元)" width="100" align="center"></el-table-column>
        <el-table-column prop="operator" label="操作员" width="100" align="center"></el-table-column>
        <el-table-column prop="inTime" label="入库时间" width="180" align="center"></el-table-column>
        <el-table-column prop="remark" label="备注" min-width="150" show-overflow-tooltip></el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          :total="total"
          :page-size="pageSize"
          :current-page="currentPage"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
import { supplies, stockInRecords } from '@/api/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'StockIn',
  data() {
    return {
      supplies: supplies,
      submitLoading: false,
      stockInForm: {
        supplyId: '',
        quantity: 1,
        price: 0,
        operator: '',
        remark: ''
      },
      rules: {
        supplyId: [
          { required: true, message: '请选择用品', trigger: 'change' }
        ],
        quantity: [
          { required: true, message: '请输入入库数量', trigger: 'blur' },
          { type: 'number', message: '入库数量必须为数字', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (!value) {
                callback(new Error('请输入入库数量'))
              } else if (typeof value !== 'number' || isNaN(value)) {
                callback(new Error('入库数量必须为合法数字'))
              } else if (value <= 0) {
                callback(new Error('入库数量必须大于0'))
              } else if (!Number.isInteger(value)) {
                callback(new Error('入库数量必须为整数'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ],
        operator: [
          { required: true, message: '请输入操作员姓名', trigger: 'blur' }
        ]
      },
      searchForm: {
        inNo: '',
        supplyId: null
      },
      tableData: [],
      total: 0,
      pageSize: 10,
      currentPage: 1,
      dataList: []
    }
  },
  computed: {
    currentSupply() {
      const supply = this.supplies.find(s => s.id === this.stockInForm.supplyId)
      return supply || { stock: '-', unit: '-' }
    }
  },
  watch: {
    'stockInForm.supplyId'() {
      this.$forceUpdate()
    }
  },
  created() {
    this.dataList = [...stockInRecords]
    this.loadData()
    
    if (this.$route.query.supplyId) {
      this.stockInForm.supplyId = parseInt(this.$route.query.supplyId)
      this.handleSupplyChange()
    }
  },
  methods: {
    handleSupplyChange() {
      const supply = this.supplies.find(s => s.id === this.stockInForm.supplyId)
      if (supply) {
        this.stockInForm.price = supply.price
      }
    },
    loadData() {
      let filtered = [...this.dataList]
      
      if (this.searchForm.inNo) {
        filtered = filtered.filter(item => item.inNo.includes(this.searchForm.inNo))
      }
      
      if (this.searchForm.supplyId) {
        filtered = filtered.filter(item => item.supplyId === this.searchForm.supplyId)
      }
      
      this.total = filtered.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.tableData = filtered.slice(start, end)
    },
    handleSearch() {
      this.currentPage = 1
      this.loadData()
    },
    handleResetSearch() {
      this.searchForm = {
        inNo: '',
        supplyId: null
      }
      this.currentPage = 1
      this.loadData()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadData()
    },
    handlePageChange(val) {
      this.currentPage = val
      this.loadData()
    },
    handleStockIn() {
      this.$refs.stockInForm.validate((valid) => {
        if (valid) {
          if (!this.stockInForm.quantity || 
              typeof this.stockInForm.quantity !== 'number' || 
              isNaN(this.stockInForm.quantity) || 
              this.stockInForm.quantity <= 0 ||
              !Number.isInteger(this.stockInForm.quantity)) {
            this.$message.error('入库数量必须为合法正整数')
            return
          }
          
          this.submitLoading = true
          
          setTimeout(() => {
            const supply = this.supplies.find(s => s.id === this.stockInForm.supplyId)
            const newId = Math.max(...this.dataList.map(item => item.id), 0) + 1
            const now = new Date()
            const inNo = `IN${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}${String(newId).padStart(3, '0')}`
            
            const newRecord = {
              id: newId,
              inNo: inNo,
              supplyId: this.stockInForm.supplyId,
              supplyName: supply.name,
              quantity: this.stockInForm.quantity,
              unit: supply.unit,
              price: this.stockInForm.price,
              totalPrice: this.stockInForm.quantity * this.stockInForm.price,
              operator: this.stockInForm.operator,
              inTime: now.toLocaleString('zh-CN', { hour12: false }),
              remark: this.stockInForm.remark
            }
            
            this.dataList.unshift(newRecord)
            
            supply.stock += this.stockInForm.quantity
            
            this.submitLoading = false
            this.$message.success('入库成功，库存已自动更新')
            
            EventBus.$emit('stock-updated')
            
            this.handleReset()
            this.loadData()
          }, 1000)
        }
      })
    },
    handleReset() {
      this.$refs.stockInForm.resetFields()
      this.stockInForm = {
        supplyId: '',
        quantity: 1,
        price: 0,
        operator: '',
        remark: ''
      }
    }
  }
}
</script>
