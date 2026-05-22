<template>
  <div class="page-container">
    <div class="page-title">预约记录列表</div>
    
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索客户姓名/车牌号"
        style="width: 200px; margin-right: 10px"
        clearable
        @clear="handleSearch"
      ></el-input>
      <el-select v-model="filterTechnician" placeholder="选择技师" style="width: 140px; margin-right: 10px" clearable>
        <el-option label="全部技师" value=""></el-option>
        <el-option
          v-for="tech in technicianList"
          :key="tech.id"
          :label="tech.name"
          :value="tech.name"
        ></el-option>
      </el-select>
      <el-select v-model="filterCarModel" placeholder="车辆品牌" style="width: 120px; margin-right: 10px" clearable>
        <el-option label="全部品牌" value=""></el-option>
        <el-option label="奥迪" value="奥迪"></el-option>
        <el-option label="宝马" value="宝马"></el-option>
        <el-option label="奔驰" value="奔驰"></el-option>
        <el-option label="大众" value="大众"></el-option>
        <el-option label="丰田" value="丰田"></el-option>
        <el-option label="本田" value="本田"></el-option>
        <el-option label="其他" value="其他"></el-option>
      </el-select>
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        style="width: 350px; margin-right: 10px"
      ></el-date-picker>
      <el-select v-model="filterStatus" placeholder="预约状态" style="width: 130px; margin-right: 10px" clearable>
        <el-option label="全部状态" value=""></el-option>
        <el-option label="待确认" value="待确认"></el-option>
        <el-option label="已确认" value="已确认"></el-option>
        <el-option label="已完成" value="已完成"></el-option>
        <el-option label="已取消" value="已取消"></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
      <el-button style="margin-left: 10px" @click="handleReset">重置</el-button>
    </div>

    <div class="table-container">
      <el-table :data="paginatedData" border style="width: 100%" v-loading="loading">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="orderNo" label="预约单号" width="150" align="center"></el-table-column>
        <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
        <el-table-column prop="plateNumber" label="车牌号" width="110" align="center"></el-table-column>
        <el-table-column prop="carInfo" label="车辆信息" width="130" align="center"></el-table-column>
        <el-table-column prop="packageName" label="保养项目" min-width="150"></el-table-column>
        <el-table-column prop="technicianName" label="服务技师" width="100" align="center"></el-table-column>
        <el-table-column prop="appointmentDate" label="预约日期" width="120" align="center"></el-table-column>
        <el-table-column prop="appointmentTime" label="预约时段" width="120" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusTagType(scope.row.status)" size="small">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="180" align="center"></el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="handleView(scope.row)">详情</el-button>
            <el-button size="mini" type="warning" @click="handleEdit(scope.row)" v-if="scope.row.status !== '已完成' && scope.row.status !== '已取消'">编辑</el-button>
            <el-button size="mini" type="success" @click="handleConfirm(scope.row)" v-if="scope.row.status === '待确认'">确认</el-button>
            <el-button size="mini" type="danger" @click="handleCancel(scope.row)" v-if="scope.row.status !== '已完成' && scope.row.status !== '已取消'">取消</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="pagination-container">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog title="预约详情" :visible.sync="detailDialogVisible" width="700px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="预约单号">{{ currentDetail.orderNo }}</el-descriptions-item>
        <el-descriptions-item label="预约状态">
          <el-tag :type="getStatusTagType(currentDetail.status)" size="small">{{ currentDetail.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="客户姓名">{{ currentDetail.customerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentDetail.phone }}</el-descriptions-item>
        <el-descriptions-item label="车牌号">{{ currentDetail.plateNumber }}</el-descriptions-item>
        <el-descriptions-item label="车辆信息">{{ currentDetail.carInfo }}</el-descriptions-item>
        <el-descriptions-item label="保养项目" :span="2">{{ currentDetail.packageName }}</el-descriptions-item>
        <el-descriptions-item label="服务技师">{{ currentDetail.technicianName }}</el-descriptions-item>
        <el-descriptions-item label="预约日期">{{ currentDetail.appointmentDate }}</el-descriptions-item>
        <el-descriptions-item label="预约时段">{{ currentDetail.appointmentTime }}</el-descriptions-item>
        <el-descriptions-item label="创建时间" :span="2">{{ currentDetail.createTime }}</el-descriptions-item>
        <el-descriptions-item label="备注信息" :span="2">{{ currentDetail.remark || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'Records',
  data() {
    return {
      loading: false,
      searchKeyword: '',
      filterTechnician: '',
      filterCarModel: '',
      filterStatus: '',
      dateRange: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      allRecordList: [],
      filteredList: [],
      paginatedData: [],
      detailDialogVisible: false,
      currentDetail: {},
      technicianList: [
        { id: 1, name: '张师傅', level: '高级技师' },
        { id: 2, name: '李师傅', level: '高级技师' },
        { id: 3, name: '王师傅', level: '中级技师' },
        { id: 4, name: '赵师傅', level: '中级技师' },
        { id: 5, name: '刘师傅', level: '初级技师' }
      ]
    }
  },
  created() {
    this.loadRecords()
  },
  activated() {
    if (localStorage.getItem('needRefreshRecords') === 'true') {
      this.loadRecords()
      localStorage.removeItem('needRefreshRecords')
    }
  },
  methods: {
    getStatusTagType(status) {
      const typeMap = {
        '待确认': 'warning',
        '已确认': 'primary',
        '已完成': 'success',
        '已取消': 'info'
      }
      return typeMap[status] || 'info'
    },
    getInitialData() {
      const today = new Date()
      const formatDate = (date) => {
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        const day = String(date.getDate()).padStart(2, '0')
        return `${year}-${month}-${day}`
      }
      
      return [
        { id: 1, orderNo: 'YY202401150001', customerName: '陈先生', phone: '13800138001', plateNumber: '京A12345', carInfo: '奥迪 A6L', packageName: '基础保养套餐', technicianName: '张师傅', appointmentDate: formatDate(new Date(today.getTime() + 86400000)), appointmentTime: '09:00 - 10:00', status: '已完成', createTime: '2024-01-14 10:30:00', remark: '' },
        { id: 2, orderNo: 'YY202401150002', customerName: '林女士', phone: '13800138002', plateNumber: '京B67890', carInfo: '宝马 5系', packageName: '深度保养套餐A', technicianName: '张师傅', status: '已确认', createTime: '2024-01-14 11:20:00' },
        { id: 3, orderNo: 'YY202401150003', customerName: '吴先生', phone: '13800138003', plateNumber: '京C11111', carInfo: '奔驰 E级', packageName: '豪华保养套餐', technicianName: '李师傅', status: '待确认', createTime: '2024-01-14 14:15:00', remark: '需要洗车服务' },
        { id: 4, orderNo: 'YY202401150004', customerName: '郑女士', phone: '13800138004', plateNumber: '京D22222', carInfo: '大众 迈腾', packageName: '常规保养套餐', technicianName: '王师傅', status: '已完成', createTime: '2024-01-13 09:45:00', remark: '' },
        { id: 5, orderNo: 'YY202401160001', customerName: '黄先生', phone: '13800138005', plateNumber: '京E33333', carInfo: '丰田 凯美瑞', packageName: '基础保养套餐', technicianName: '刘师傅', status: '已确认', createTime: '2024-01-14 16:30:00', remark: '' },
        { id: 6, orderNo: 'YY202401160002', customerName: '张先生', phone: '13800138006', plateNumber: '京F44444', carInfo: '本田 雅阁', packageName: '深度保养套餐B', technicianName: '赵师傅', status: '待确认', createTime: '2024-01-15 08:20:00', remark: '更换变速箱油' },
        { id: 7, orderNo: 'YY202401170001', customerName: '李女士', phone: '13800138007', plateNumber: '京G55555', carInfo: '奥迪 Q5', packageName: 'VIP尊享套餐', technicianName: '张师傅', status: '已取消', createTime: '2024-01-12 15:00:00', remark: '客户临时有事取消' },
        { id: 8, orderNo: 'YY202401170002', customerName: '王先生', phone: '13800138008', plateNumber: '京H66666', carInfo: '宝马 X3', packageName: '常规保养套餐', technicianName: '李师傅', status: '已完成', createTime: '2024-01-13 10:30:00', remark: '' },
        { id: 9, orderNo: 'YY202401180001', customerName: '赵先生', phone: '13800138009', plateNumber: '京I77777', carInfo: '奔驰 GLC', packageName: '深度保养套餐A', technicianName: '王师傅', status: '待确认', createTime: '2024-01-15 14:20:00', remark: '' },
        { id: 10, orderNo: 'YY202401180002', customerName: '刘女士', phone: '13800138010', plateNumber: '京J88888', carInfo: '大众 途观', packageName: '基础保养套餐', technicianName: '赵师傅', status: '已确认', createTime: '2024-01-14 09:10:00', remark: '' },
        { id: 11, orderNo: 'YY202401190001', customerName: '孙先生', phone: '13800138011', plateNumber: '京K99999', carInfo: '丰田 汉兰达', packageName: '豪华保养套餐', technicianName: '张师傅', status: '待确认', createTime: '2024-01-15 09:00:00', remark: '' },
        { id: 12, orderNo: 'YY202401190002', customerName: '周女士', phone: '13800138012', plateNumber: '京L11111', carInfo: '本田 CRV', packageName: '常规保养套餐', technicianName: '刘师傅', status: '已确认', createTime: '2024-01-15 10:30:00', remark: '' }
      ]
    },
    loadRecords() {
      this.loading = true
      setTimeout(() => {
        const savedRecords = JSON.parse(localStorage.getItem('appointmentRecords') || '[]')
        const initialData = this.getInitialData()
        this.allRecordList = [...savedRecords, ...initialData]
        this.filteredList = [...this.allRecordList]
        this.applyPagination()
        this.loading = false
      }, 300)
    },
    applyFilters() {
      let result = [...this.allRecordList]
      
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        result = result.filter(item => 
          item.customerName.toLowerCase().includes(keyword) || 
          item.plateNumber.toLowerCase().includes(keyword)
        )
      }
      
      if (this.filterTechnician) {
        result = result.filter(item => 
          item.technicianName === this.filterTechnician
        )
      }
      
      if (this.filterCarModel) {
        result = result.filter(item => 
          item.carInfo && item.carInfo.includes(this.filterCarModel)
        )
      }
      
      if (this.filterStatus) {
        result = result.filter(item => 
          item.status === this.filterStatus
        )
      }
      
      if (this.dateRange && this.dateRange.length === 2) {
        const startDate = this.formatDate(this.dateRange[0])
        const endDate = this.formatDate(this.dateRange[1])
        result = result.filter(item => {
          const itemDate = item.appointmentDate
          return itemDate >= startDate && itemDate <= endDate
        })
      }
      
      this.filteredList = result
      this.currentPage = 1
      this.applyPagination()
    },
    applyPagination() {
      this.total = this.filteredList.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.paginatedData = this.filteredList.slice(start, end)
    },
    formatDate(date) {
      if (!date) return ''
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      return `${year}-${month}-${day}`
    },
    handleSearch() {
      this.applyFilters()
    },
    handleReset() {
      this.searchKeyword = ''
      this.filterTechnician = ''
      this.filterCarModel = ''
      this.filterStatus = ''
      this.dateRange = ''
      this.currentPage = 1
      this.filteredList = [...this.allRecordList]
      this.applyPagination()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.applyPagination()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.applyPagination()
    },
    handleView(row) {
      this.currentDetail = row
      this.detailDialogVisible = true
    },
    handleEdit(row) {
      this.$message.info(`编辑预约 ${row.orderNo} 的功能`)
    },
    handleConfirm(row) {
      this.$confirm(`确定要确认预约 ${row.orderNo} 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.allRecordList.findIndex(r => r.id === row.id)
        if (index !== -1) {
          this.allRecordList[index].status = '已确认'
        }
        this.saveRecordsToLocal()
        this.applyFilters()
        this.$message.success('确认成功！')
      }).catch(() => {})
    },
    handleCancel(row) {
      this.$confirm(`确定要取消预约 ${row.orderNo} 吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.allRecordList.findIndex(r => r.id === row.id)
        if (index !== -1) {
          this.allRecordList[index].status = '已取消'
        }
        this.saveRecordsToLocal()
        this.applyFilters()
        this.$message.success('取消成功！')
      }).catch(() => {})
    },
    saveRecordsToLocal() {
      const savedRecords = this.allRecordList.filter(r => r.id > 1000000000000)
      localStorage.setItem('appointmentRecords', JSON.stringify(savedRecords))
    }
  }
}
</script>

<style scoped>
</style>
