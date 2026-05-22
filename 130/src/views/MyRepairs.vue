<template>
  <div class="page-container">
    <h2 class="page-title">我的报修</h2>
    
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="所属楼栋">
        <el-select v-model="searchForm.building" placeholder="请选择" clearable>
          <el-option v-for="item in buildingOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="报修类型">
        <el-select v-model="searchForm.type" placeholder="请选择" clearable>
          <el-option v-for="item in repairTypes" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="处理状态">
        <el-select v-model="searchForm.status" placeholder="请选择" clearable>
          <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>

    <div class="table-container">
      <el-table :data="paginatedList" border style="width: 100%" v-loading="loading">
        <el-table-column prop="id" label="报修编号" width="100" align="center"></el-table-column>
        <el-table-column prop="title" label="报修标题" min-width="150"></el-table-column>
        <el-table-column prop="buildingName" label="所属楼栋" width="90" align="center"></el-table-column>
        <el-table-column prop="typeName" label="报修类型" width="100" align="center"></el-table-column>
        <el-table-column prop="urgencyName" label="紧急程度" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getUrgencyTagType(scope.row.urgency)" size="small">{{ scope.row.urgencyName }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :color="getStatusColor(scope.row.status)" size="small">{{ getStatusLabel(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="提交时间" width="160" align="center"></el-table-column>
        <el-table-column label="操作" width="220" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="viewProgress(scope.row.id)">查看进度</el-button>
            <el-button type="success" size="mini" @click="goEvaluate(scope.row.id)" v-if="scope.row.status === '3'">评价</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { statusOptions, repairTypes, buildingOptions } from '../mock/data'
import { RepairStore } from '../store/repairStore'
import { EventBus, Events } from '../utils/eventBus'

export default {
  name: 'MyRepairs',
  data() {
    return {
      statusOptions,
      repairTypes,
      buildingOptions,
      searchForm: {
        status: '',
        type: '',
        building: ''
      },
      loading: false,
      currentPage: 1,
      pageSize: 5
    }
  },
  computed: {
    repairList() {
      return RepairStore.getRepairList()
    },
    filteredList() {
      let list = [...this.repairList]
      if (this.searchForm.building) {
        list = list.filter(item => item.building === this.searchForm.building)
      }
      if (this.searchForm.type) {
        list = list.filter(item => item.type === this.searchForm.type)
      }
      if (this.searchForm.status) {
        list = list.filter(item => item.status === this.searchForm.status)
      }
      return list
    },
    paginatedList() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredList.slice(start, end)
    },
    total() {
      return this.filteredList.length
    }
  },
  mounted() {
    this.listenToStatusUpdates()
  },
  beforeDestroy() {
    EventBus.$off(Events.REPAIR_STATUS_UPDATED)
    EventBus.$off(Events.REPAIR_CREATED)
  },
  methods: {
    listenToStatusUpdates() {
      EventBus.$on(Events.REPAIR_STATUS_UPDATED, (data) => {
        this.$message.info(`报修单 ${data.id} 状态已更新为：${RepairStore.getStatusLabel(data.status)}`)
      })
      
      EventBus.$on(Events.REPAIR_CREATED, (newRepair) => {
        this.$message.success(`新报修单已创建：${newRepair.title}`)
        this.currentPage = 1
      })
    },
    getStatusLabel(status) {
      return RepairStore.getStatusLabel(status)
    },
    getStatusColor(status) {
      return RepairStore.getStatusColor(status)
    },
    getUrgencyTagType(urgency) {
      const map = { '1': '', '2': 'warning', '3': 'danger' }
      return map[urgency] || ''
    },
    search() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.currentPage = 1
      }, 300)
    },
    resetSearch() {
      this.searchForm = {
        status: '',
        type: '',
        building: ''
      }
      this.currentPage = 1
    },
    viewProgress(id) {
      this.$router.push(`/progress/${id}`)
    },
    goEvaluate(id) {
      this.$router.push(`/evaluation/${id}`)
    },
    handleSizeChange(val) {
      this.pageSize = val
    },
    handleCurrentChange(val) {
      this.currentPage = val
    }
  }
}
</script>

<style scoped>
.search-form {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  text-align: right;
}
</style>
