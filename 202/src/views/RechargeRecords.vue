<template>
  <div class="page-container">
    <div class="page-header">
      <div class="page-title">充值记录</div>
      <div class="page-subtitle">查看所有充值记录和交易状态</div>
    </div>

    <el-card class="mb-20">
      <el-form :inline="true">
        <el-form-item label="楼栋">
          <el-select v-model="filterBuilding" placeholder="全部楼栋" clearable style="width: 120px;" @change="handleBuildingFilter">
            <el-option
              v-for="building in buildingList"
              :key="building"
              :label="building"
              :value="building"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="宿舍">
          <el-select v-model="filterDormitory" placeholder="全部宿舍" clearable style="width: 150px;" @change="handleFilter">
            <el-option
              v-for="dorm in filteredDormitoryList"
              :key="dorm"
              :label="dorm"
              :value="dorm"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="filterType" placeholder="全部类型" clearable style="width: 120px;" @change="handleFilter">
            <el-option label="水费" value="water"></el-option>
            <el-option label="电费" value="electricity"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="支付状态">
          <el-select v-model="filterStatus" placeholder="全部状态" clearable style="width: 120px;" @change="handleFilter">
            <el-option label="成功" value="success"></el-option>
            <el-option label="处理中" value="pending"></el-option>
            <el-option label="失败" value="failed"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px;"
            @change="handleFilter"
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" class="mb-20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">充值总金额</div>
          <div class="value text-primary">
            {{ totalAmount.toFixed(2) }} <span class="unit">元</span>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">充值总次数</div>
          <div class="value">
            {{ totalCount }} <span class="unit">次</span>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">水费充值</div>
          <div class="value">
            {{ waterAmount.toFixed(2) }} <span class="unit">元</span>
          </div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="label">电费充值</div>
          <div class="value">
            {{ electricityAmount.toFixed(2) }} <span class="unit">元</span>
          </div>
        </div>
      </el-col>
    </el-row>

    <el-card>
      <el-table
        :data="paginatedRecords"
        border
        stripe
        style="width: 100%;"
        v-loading="loading"
      >
        <el-table-column
          prop="id"
          label="订单号"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <span class="text-primary">#{{ scope.row.id.toString().padStart(6, '0') }}</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="dormitory"
          label="宿舍"
          width="120"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="type"
          label="类型"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag :type="scope.row.type === 'water' ? 'primary' : 'warning'" size="mini">
              <i :class="scope.row.type === 'water' ? 'el-icon-water-cup' : 'el-icon-lightning'"></i>
              {{ scope.row.type === 'water' ? '水费' : '电费' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          prop="amount"
          label="充值金额"
          width="120"
          align="right"
        >
          <template slot-scope="scope">
            <span class="text-success" style="font-weight: 600;">{{ scope.row.amount.toFixed(2) }} 元</span>
          </template>
        </el-table-column>
        <el-table-column
          prop="payMethod"
          label="支付方式"
          width="120"
          align="center"
        >
          <template slot-scope="scope">
            <span v-if="scope.row.payMethod === '微信支付'">
              <i class="el-icon-chat-dot-round" style="color: #07c160;"></i> 微信
            </span>
            <span v-else-if="scope.row.payMethod === '支付宝'">
              <i class="el-icon-mobile-phone" style="color: #1677ff;"></i> 支付宝
            </span>
            <span v-else>
              <i class="el-icon-credit-pay"></i> 校园卡
            </span>
          </template>
        </el-table-column>
        <el-table-column
          prop="time"
          label="充值时间"
          min-width="180"
          align="center"
        ></el-table-column>
        <el-table-column
          prop="status"
          label="状态"
          width="100"
          align="center"
        >
          <template slot-scope="scope">
            <el-tag
              :type="scope.row.status === 'success' ? 'success' : scope.row.status === 'pending' ? 'warning' : 'danger'"
              size="mini"
            >
              {{ scope.row.status === 'success' ? '成功' : scope.row.status === 'pending' ? '处理中' : '失败' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="120"
          align="center"
          fixed="right"
        >
          <template slot-scope="scope">
            <el-button
              size="mini"
              type="text"
              @click="viewDetail(scope.row)"
            >详情</el-button>
            <el-button
              size="mini"
              type="text"
              v-if="scope.row.status === 'success'"
            >凭证</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="filteredRecords.length"
        ></el-pagination>
      </div>
    </el-card>

    <el-dialog
      title="充值详情"
      :visible.sync="detailDialogVisible"
      width="500px"
    >
      <el-descriptions :column="1" border v-if="currentRecord">
        <el-descriptions-item label="订单号">#{{ currentRecord.id.toString().padStart(6, '0') }}</el-descriptions-item>
        <el-descriptions-item label="宿舍">{{ currentRecord.dormitory }}</el-descriptions-item>
        <el-descriptions-item label="充值类型">
          {{ currentRecord.type === 'water' ? '水费' : '电费' }}
        </el-descriptions-item>
        <el-descriptions-item label="充值金额">
          <span class="text-success" style="font-size: 20px; font-weight: 600;">{{ currentRecord.amount.toFixed(2) }} 元</span>
        </el-descriptions-item>
        <el-descriptions-item label="支付方式">{{ currentRecord.payMethod }}</el-descriptions-item>
        <el-descriptions-item label="充值时间">{{ currentRecord.time }}</el-descriptions-item>
        <el-descriptions-item label="交易状态">
          <el-tag
            :type="currentRecord.status === 'success' ? 'success' : currentRecord.status === 'pending' ? 'warning' : 'danger'"
          >
            {{ currentRecord.status === 'success' ? '交易成功' : currentRecord.status === 'pending' ? '处理中' : '交易失败' }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getRechargeRecords, getDormitoryList, getDormitories } from '@/utils/mockData'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'RechargeRecords',
  data() {
    return {
      records: [],
      dormitoryList: [],
      filterBuilding: '',
      filterDormitory: '',
      filterType: '',
      filterStatus: '',
      dateRange: [],
      currentPage: 1,
      pageSize: 10,
      loading: false,
      detailDialogVisible: false,
      currentRecord: null
    }
  },
  computed: {
    buildingList() {
      const buildingSet = new Set()
      getDormitories().forEach(d => buildingSet.add(d.building))
      return Array.from(buildingSet)
    },
    filteredDormitoryList() {
      if (!this.filterBuilding) return this.dormitoryList
      return this.dormitoryList.filter(d => d.startsWith(this.filterBuilding))
    },
    filteredRecords() {
      let result = [...this.records]
      
      if (this.filterBuilding) {
        result = result.filter(r => r.dormitory.startsWith(this.filterBuilding))
      }
      
      if (this.filterDormitory) {
        result = result.filter(r => r.dormitory === this.filterDormitory)
      }
      
      if (this.filterType) {
        result = result.filter(r => r.type === this.filterType)
      }
      
      if (this.filterStatus) {
        result = result.filter(r => r.status === this.filterStatus)
      }
      
      if (this.dateRange && this.dateRange.length === 2) {
        const startDate = this.formatDate(this.dateRange[0])
        const endDate = this.formatDate(this.dateRange[1])
        result = result.filter(r => {
          const recordDate = r.time.split(' ')[0]
          return recordDate >= startDate && recordDate <= endDate
        })
      }
      
      return result
    },
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredRecords.slice(start, end)
    },
    totalAmount() {
      return this.filteredRecords.reduce((sum, r) => sum + r.amount, 0)
    },
    totalCount() {
      return this.filteredRecords.length
    },
    waterAmount() {
      return this.filteredRecords.filter(r => r.type === 'water').reduce((sum, r) => sum + r.amount, 0)
    },
    electricityAmount() {
      return this.filteredRecords.filter(r => r.type === 'electricity').reduce((sum, r) => sum + r.amount, 0)
    }
  },
  created() {
    this.loadRecords()
    this.dormitoryList = getDormitoryList()
    EventBus.$on('recharge-success', () => {
      this.loadRecords()
    })
  },
  beforeDestroy() {
    EventBus.$off('recharge-success')
  },
  activated() {
    this.loadRecords()
  },
  methods: {
    loadRecords() {
      this.records = getRechargeRecords()
    },
    formatDate(date) {
      const year = date.getFullYear()
      const month = (date.getMonth() + 1).toString().padStart(2, '0')
      const day = date.getDate().toString().padStart(2, '0')
      return `${year}/${month}/${day}`
    },
    handleBuildingFilter() {
      this.filterDormitory = ''
      this.currentPage = 1
    },
    handleFilter() {
      this.currentPage = 1
    },
    resetFilter() {
      this.filterBuilding = ''
      this.filterDormitory = ''
      this.filterType = ''
      this.filterStatus = ''
      this.dateRange = []
      this.currentPage = 1
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    viewDetail(record) {
      this.currentRecord = record
      this.detailDialogVisible = true
    }
  }
}
</script>

<style scoped>
.stat-card {
  background: #fff;
  border-radius: 4px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-card .label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.stat-card .value {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
}

.stat-card .unit {
  font-size: 14px;
  font-weight: normal;
  color: #909399;
  margin-left: 5px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
