<template>
  <div class="page-container">
    <h1 class="page-title">我的预约</h1>
    
    <div class="card-wrapper">
      <div class="table-toolbar">
        <div class="toolbar-left">
          <el-button type="primary" @click="goToReserve">
            <i class="el-icon-plus"></i> 新增预约
          </el-button>
          <el-button @click="resetFilters">
            <i class="el-icon-refresh"></i> 重置筛选
          </el-button>
        </div>
        <div class="toolbar-right">
          <el-select v-model="filters.packageId" placeholder="按套餐筛选" style="width: 160px;" @change="filterRecords" clearable>
            <el-option label="全部套餐" value=""></el-option>
            <el-option 
              v-for="pkg in packages" 
              :key="pkg.id" 
              :label="pkg.name" 
              :value="pkg.id"
            ></el-option>
          </el-select>
          <el-date-picker
            v-model="filters.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 240px;"
            @change="filterRecords"
          ></el-date-picker>
          <el-select v-model="filters.status" placeholder="按状态筛选" style="width: 140px;" @change="filterRecords" clearable>
            <el-option label="全部状态" value=""></el-option>
            <el-option label="待确认" :value="0"></el-option>
            <el-option label="待施工" :value="1"></el-option>
            <el-option label="施工中" :value="2"></el-option>
            <el-option label="已完工" :value="3"></el-option>
            <el-option label="已取消" :value="4"></el-option>
          </el-select>
        </div>
      </div>
      
      <el-table
        :data="paginatedRecords"
        border
        style="width: 100%"
        empty-text="暂无预约记录"
      >
        <el-table-column prop="id" label="预约编号" width="140" align="center">
          <template slot-scope="scope">
            NO.{{ scope.row.id }}
          </template>
        </el-table-column>
        
        <el-table-column prop="ownerName" label="车主" width="100" align="center"></el-table-column>
        
        <el-table-column prop="carNumber" label="车牌号" width="120" align="center"></el-table-column>
        
        <el-table-column prop="carBrand" label="品牌" width="100" align="center"></el-table-column>
        
        <el-table-column label="保养套餐" align="center">
          <template slot-scope="scope">
            {{ getPackageName(scope.row.packageId) }}
          </template>
        </el-table-column>
        
        <el-table-column label="维修工位" width="140" align="center">
          <template slot-scope="scope">
            {{ getStationName(scope.row.stationId) }}
          </template>
        </el-table-column>
        
        <el-table-column label="预约时间" width="200" align="center">
          <template slot-scope="scope">
            <div>{{ formatDate(scope.row.reserveDate) }}</div>
            <div style="color: #909399; font-size: 12px;">{{ scope.row.reserveTime }}</div>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button 
              type="text" 
              size="small" 
              @click="viewProgress(scope.row)"
              v-if="scope.row.status >= 1 && scope.row.status <= 2"
            >
              查看进度
            </el-button>
            <el-button 
              type="text" 
              size="small" 
              @click="goEvaluate(scope.row)"
              v-if="scope.row.status === 3 && !scope.row.evaluated"
            >
              去评价
            </el-button>
            <el-button 
              type="text" 
              size="small" 
              @click="viewEvaluate(scope.row)"
              v-if="scope.row.status === 3 && scope.row.evaluated"
            >
              查看评价
            </el-button>
            <el-button 
              type="text" 
              size="small" 
              style="color: #f56c6c"
              @click="cancelReserve(scope.row)"
              v-if="scope.row.status === 0"
            >
              取消预约
            </el-button>
            <el-button 
              type="text" 
              size="small" 
              @click="deleteRecord(scope.row)"
              v-if="scope.row.status === 4"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination-wrapper">
        <div class="pagination-info">
          共 <span class="highlight">{{ filteredRecords.length }}</span> 条记录
        </div>
        <el-pagination
          background
          :page-size="pageSize"
          :total="filteredRecords.length"
          layout="total, sizes, prev, pager, next, jumper"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          @current-change="handlePageChange"
          @size-change="handleSizeChange"
        ></el-pagination>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Records',
  data() {
    return {
      records: [],
      currentPage: 1,
      pageSize: 10,
      pollingTimer: null,
      filters: {
        packageId: '',
        status: '',
        dateRange: []
      },
      packages: [
        { id: 1, name: '基础保养套餐' },
        { id: 2, name: '标准保养套餐' },
        { id: 3, name: '尊享保养套餐' },
        { id: 4, name: '刹车系统养护' },
        { id: 5, name: '空调系统养护' },
        { id: 6, name: '漆面养护套餐' }
      ],
      stations: [
        { id: 1, name: '1号工位 - 机修' },
        { id: 2, name: '2号工位 - 机修' },
        { id: 3, name: '3号工位 - 美容' },
        { id: 4, name: '4号工位 - 美容' },
        { id: 5, name: '5号工位 - 快修' }
      ]
    }
  },
  computed: {
    filteredRecords() {
      let result = [...this.records]
      
      if (this.filters.packageId !== '') {
        result = result.filter(item => item.packageId === this.filters.packageId)
      }
      
      if (this.filters.status !== '') {
        result = result.filter(item => item.status === this.filters.status)
      }
      
      if (this.filters.dateRange && this.filters.dateRange.length === 2) {
        const startDate = new Date(this.filters.dateRange[0])
        const endDate = new Date(this.filters.dateRange[1])
        endDate.setHours(23, 59, 59, 999)
        result = result.filter(item => {
          const itemDate = new Date(item.reserveDate)
          return itemDate >= startDate && itemDate <= endDate
        })
      }
      
      return result
    },
    paginatedRecords() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredRecords.slice(start, end)
    }
  },
  mounted() {
    this.loadRecords()
    this.startPolling()
  },
  activated() {
    this.loadRecords()
  },
  beforeDestroy() {
    this.stopPolling()
  },
  methods: {
    loadRecords() {
      this.records = JSON.parse(localStorage.getItem('reserveRecords') || '[]')
      if (this.records.length === 0) {
        this.addDemoData()
      }
    },
    startPolling() {
      this.pollingTimer = setInterval(() => {
        this.records = JSON.parse(localStorage.getItem('reserveRecords') || '[]')
      }, 3000)
    },
    stopPolling() {
      if (this.pollingTimer) {
        clearInterval(this.pollingTimer)
        this.pollingTimer = null
      }
    },
    addDemoData() {
      const demoData = [
        {
          id: 10001,
          ownerName: '张三',
          phone: '13800138001',
          carNumber: '京A88888',
          carBrand: '宝马',
          packageId: 2,
          stationId: 1,
          reserveDate: new Date().toISOString().split('T')[0],
          reserveTime: '10:00-11:00',
          consultant: '张经理',
          remark: '请尽快安排',
          status: 2,
          createTime: new Date().toLocaleString(),
          evaluated: false
        },
        {
          id: 10002,
          ownerName: '李四',
          phone: '13800138002',
          carNumber: '京B66666',
          carBrand: '奔驰',
          packageId: 3,
          stationId: 2,
          reserveDate: new Date(Date.now() + 86400000).toISOString().split('T')[0],
          reserveTime: '14:00-15:00',
          consultant: '李主管',
          remark: '',
          status: 1,
          createTime: new Date().toLocaleString(),
          evaluated: false
        },
        {
          id: 10003,
          ownerName: '王五',
          phone: '13800138003',
          carNumber: '京C99999',
          carBrand: '奥迪',
          packageId: 1,
          stationId: 3,
          reserveDate: new Date(Date.now() - 86400000).toISOString().split('T')[0],
          reserveTime: '09:00-10:00',
          consultant: '王技师',
          remark: '',
          status: 3,
          createTime: new Date(Date.now() - 86400000).toLocaleString(),
          evaluated: false
        },
        {
          id: 10004,
          ownerName: '赵六',
          phone: '13800138004',
          carNumber: '京D11111',
          carBrand: '丰田',
          packageId: 4,
          stationId: 4,
          reserveDate: new Date(Date.now() - 172800000).toISOString().split('T')[0],
          reserveTime: '15:00-16:00',
          consultant: '随机分配',
          remark: '',
          status: 3,
          createTime: new Date(Date.now() - 172800000).toLocaleString(),
          evaluated: true,
          score: 5,
          evaluateContent: '服务非常专业，效率很高！'
        }
      ]
      this.records = demoData
      localStorage.setItem('reserveRecords', JSON.stringify(demoData))
    },
    getPackageName(id) {
      const pkg = this.packages.find(p => p.id === id)
      return pkg ? pkg.name : '未知套餐'
    },
    getStationName(id) {
      const station = this.stations.find(s => s.id === id)
      return station ? station.name : '未分配'
    },
    getStatusText(status) {
      const statusMap = {
        0: '待确认',
        1: '待施工',
        2: '施工中',
        3: '已完工',
        4: '已取消'
      }
      return statusMap[status] || '未知'
    },
    getStatusType(status) {
      const typeMap = {
        0: 'warning',
        1: 'info',
        2: 'primary',
        3: 'success',
        4: 'danger'
      }
      return typeMap[status] || 'info'
    },
    formatDate(dateStr) {
      if (!dateStr) return ''
      const date = new Date(dateStr)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`
    },
    goToReserve() {
      this.$router.push('/reserve')
    },
    viewProgress(row) {
      this.$router.push({
        path: '/progress',
        query: { id: row.id }
      })
    },
    goEvaluate(row) {
      this.$router.push({
        path: '/evaluate',
        query: { id: row.id }
      })
    },
    viewEvaluate(row) {
      this.$alert(`评分：${row.score}星\n评价：${row.evaluateContent || '无'}`, '评价详情')
    },
    cancelReserve(row) {
      this.$confirm('确定要取消该预约吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.records.findIndex(r => r.id === row.id)
        if (index > -1) {
          this.records[index].status = 4
          localStorage.setItem('reserveRecords', JSON.stringify(this.records))
          this.$message.success('取消成功')
        }
      }).catch(() => {})
    },
    deleteRecord(row) {
      this.$confirm('确定要删除该记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.records.findIndex(r => r.id === row.id)
        if (index > -1) {
          this.records.splice(index, 1)
          localStorage.setItem('reserveRecords', JSON.stringify(this.records))
          this.$message.success('删除成功')
        }
      }).catch(() => {})
    },
    filterRecords() {
      this.currentPage = 1
    },
    resetFilters() {
      this.filters = {
        packageId: '',
        status: '',
        dateRange: []
      }
      this.currentPage = 1
    },
    handlePageChange(page) {
      this.currentPage = page
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
.table-toolbar {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}

.toolbar-left {
  display: flex;
  gap: 10px;
}

.toolbar-right {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination-info {
  font-size: 14px;
  color: #606266;
}

.pagination-info .highlight {
  color: #409eff;
  font-weight: 600;
  margin: 0 4px;
}
</style>
