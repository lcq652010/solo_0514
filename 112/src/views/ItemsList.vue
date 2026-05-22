<template>
  <div class="items-list">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="事项名称">
          <el-input v-model="searchForm.name" placeholder="请输入事项名称" clearable></el-input>
        </el-form-item>
        <el-form-item label="事项类型">
          <el-select v-model="searchForm.type" placeholder="请选择" clearable>
            <el-option label="行政许可" value="行政许可"></el-option>
            <el-option label="公共服务" value="公共服务"></el-option>
            <el-option label="行政确认" value="行政确认"></el-option>
            <el-option label="其他事项" value="其他事项"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
          <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="table-card">
      <div slot="header" class="card-header">
        <span>办事事项列表</span>
        <el-button type="primary" size="small" icon="el-icon-plus">新增事项</el-button>
      </div>
      
      <el-table :data="tableData" border stripe style="width: 100%">
        <el-table-column prop="id" label="事项编号" width="120" align="center"></el-table-column>
        <el-table-column prop="name" label="事项名称" min-width="200" show-overflow-tooltip></el-table-column>
        <el-table-column prop="type" label="事项类型" width="120" align="center">
          <template slot-scope="scope">
            <el-tag :type="getTagType(scope.row.type)" size="small">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="department" label="办理部门" width="150" align="center"></el-table-column>
        <el-table-column prop="handleTime" label="承诺时限" width="120" align="center"></el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '正常' ? 'success' : 'info'" size="small">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="success" size="mini" icon="el-icon-date" @click="handleAppointment(scope.row)">预约</el-button>
            <el-button type="danger" size="mini" icon="el-icon-delete" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.page"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pagination.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total">
        </el-pagination>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ItemsList',
  data() {
    return {
      searchForm: {
        name: '',
        type: ''
      },
      pagination: {
        page: 1,
        size: 10,
        total: 0
      },
      tableData: []
    }
  },
  created() {
    this.loadData()
  },
  methods: {
    loadData() {
      const mockData = [
        { id: 'SX001', name: '居民身份证办理', type: '行政许可', department: '公安局', handleTime: '15个工作日', status: '正常' },
        { id: 'SX002', name: '不动产权登记', type: '行政确认', department: '自然资源局', handleTime: '30个工作日', status: '正常' },
        { id: 'SX003', name: '社保卡申领', type: '公共服务', department: '人力资源和社会保障局', handleTime: '20个工作日', status: '正常' },
        { id: 'SX004', name: '营业执照办理', type: '行政许可', department: '市场监督管理局', handleTime: '7个工作日', status: '正常' },
        { id: 'SX005', name: '税务登记证办理', type: '行政确认', department: '税务局', handleTime: '10个工作日', status: '暂停' },
        { id: 'SX006', name: '公积金提取', type: '公共服务', department: '住房公积金管理中心', handleTime: '3个工作日', status: '正常' },
        { id: 'SX007', name: '出入境证件办理', type: '行政许可', department: '出入境管理局', handleTime: '10个工作日', status: '正常' },
        { id: 'SX008', name: '医疗保险报销', type: '公共服务', department: '医疗保障局', handleTime: '15个工作日', status: '正常' },
        { id: 'SX009', name: '养老保险转移', type: '公共服务', department: '人力资源和社会保障局', handleTime: '45个工作日', status: '正常' },
        { id: 'SX010', name: '准生证办理', type: '行政确认', department: '卫生健康委员会', handleTime: '5个工作日', status: '正常' }
      ]
      this.tableData = mockData
      this.pagination.total = mockData.length
    },
    getTagType(type) {
      const typeMap = {
        '行政许可': 'danger',
        '公共服务': 'success',
        '行政确认': 'warning',
        '其他事项': 'info'
      }
      return typeMap[type] || 'info'
    },
    handleSearch() {
      this.$message.success('搜索成功')
    },
    handleReset() {
      this.searchForm = { name: '', type: '' }
      this.loadData()
    },
    handleEdit(row) {
      this.$message.info(`编辑事项：${row.name}`)
    },
    handleAppointment(row) {
      this.$router.push({
        path: '/appointment',
        query: { itemId: row.id, itemName: row.name }
      })
    },
    handleDelete(row) {
      this.$confirm(`确定要删除事项：${row.name}吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSizeChange(val) {
      this.pagination.size = val
    },
    handleCurrentChange(val) {
      this.pagination.page = val
    }
  }
}
</script>

<style scoped>
.items-list {
  height: 100%;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  margin: 0;
}

.table-card {
  height: calc(100% - 120px);
  display: flex;
  flex-direction: column;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-table {
  flex: 1;
}

.pagination {
  display: flex;
  justify-content: flex-end;
  padding: 20px 0 0;
}
</style>
