<template>
  <div class="page-container">
    <div class="page-header">
      <h2 class="page-title">会员信息列表</h2>
    </div>

    <el-form :model="searchForm" inline class="search-form">
      <el-form-item label="会员编号">
        <el-input v-model="searchForm.memberNo" placeholder="请输入会员编号" clearable></el-input>
      </el-form-item>
      <el-form-item label="会员姓名">
        <el-input v-model="searchForm.name" placeholder="请输入会员姓名" clearable></el-input>
      </el-form-item>
      <el-form-item label="手机号码">
        <el-input v-model="searchForm.phone" placeholder="请输入手机号码" clearable></el-input>
      </el-form-item>
      <el-form-item label="会员状态">
        <el-select v-model="searchForm.status" placeholder="请选择会员状态" clearable>
          <el-option label="正常" :value="1"></el-option>
          <el-option label="禁用" :value="0"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleSearch">
          <i class="el-icon-search"></i> 搜索
        </el-button>
        <el-button @click="handleReset">
          <i class="el-icon-refresh"></i> 重置
        </el-button>
      </el-form-item>
    </el-form>

    <div class="table-toolbar">
      <el-button type="primary" @click="handleAdd">
        <i class="el-icon-plus"></i> 新增会员
      </el-button>
    </div>

    <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
      <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
      <el-table-column prop="memberNo" label="会员编号" width="120" align="center"></el-table-column>
      <el-table-column prop="name" label="姓名" width="100" align="center"></el-table-column>
      <el-table-column prop="phone" label="手机号" width="130" align="center"></el-table-column>
      <el-table-column prop="level" label="会员等级" width="110" align="center">
        <template slot-scope="scope">
          <el-tag v-if="scope.row.level === '钻石会员'" type="danger" size="small">{{ scope.row.level }}</el-tag>
          <el-tag v-else-if="scope.row.level === '金卡会员'" type="warning" size="small">{{ scope.row.level }}</el-tag>
          <el-tag v-else-if="scope.row.level === '银卡会员'" type="success" size="small">{{ scope.row.level }}</el-tag>
          <el-tag v-else size="small">{{ scope.row.level }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="balance" label="账户余额" width="120" align="center">
        <template slot-scope="scope">
          <span class="balance-text">¥{{ scope.row.balance | formatMoney }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="point" label="积分" width="100" align="center"></el-table-column>
      <el-table-column prop="status" label="状态" width="90" align="center">
        <template slot-scope="scope">
          <el-tag :class="scope.row.status === 1 ? 'status-tag active' : 'status-tag inactive'" size="small">
            {{ scope.row.status === 1 ? '正常' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="registerTime" label="注册时间" width="170" align="center"></el-table-column>
      <el-table-column label="操作" width="240" align="center" fixed="right">
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleView(scope.row)">查看详情</el-button>
          <el-button type="text" size="small" @click="handleRecharge(scope.row)">充值</el-button>
          <el-button type="text" size="small" @click="handleConsume(scope.row)">消费</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
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
  </div>
</template>

<script>
import { getMembers } from '@/mock/data'
import { EventBus } from '@/utils/eventBus'

export default {
  name: 'MemberList',
  data() {
    return {
      loading: false,
      searchForm: {
        memberNo: '',
        name: '',
        phone: '',
        status: null
      },
      allMembers: [],
      tableData: [],
      pagination: {
        page: 1,
        size: 10,
        total: 0,
        sizes: [10, 20, 50, 100]
      }
    }
  },
  created() {
    this.loadData()
    EventBus.$on('refreshTransactions', () => {
      this.loadData()
    })
  },
  beforeDestroy() {
    EventBus.$off('refreshTransactions')
  },
  methods: {
    loadData() {
      this.loading = true
      setTimeout(() => {
        this.allMembers = getMembers()
        this.filterData()
        this.loading = false
      }, 300)
    },
    filterData() {
      let filtered = [...this.allMembers]

      if (this.searchForm.memberNo) {
        filtered = filtered.filter(m => m.memberNo.includes(this.searchForm.memberNo))
      }
      if (this.searchForm.name) {
        filtered = filtered.filter(m => m.name.includes(this.searchForm.name))
      }
      if (this.searchForm.phone) {
        filtered = filtered.filter(m => m.phone.includes(this.searchForm.phone))
      }
      if (this.searchForm.status !== null && this.searchForm.status !== '') {
        filtered = filtered.filter(m => m.status === this.searchForm.status)
      }

      this.pagination.total = filtered.length
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.tableData = filtered.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.filterData()
    },
    handleReset() {
      this.searchForm = {
        memberNo: '',
        name: '',
        phone: '',
        status: null
      }
      this.pagination.page = 1
      this.filterData()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.pagination.page = 1
      this.filterData()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.filterData()
    },
    handleAdd() {
      this.$message.info('新增会员功能待实现')
    },
    handleView(row) {
      this.$router.push(`/member/${row.id}`)
    },
    handleRecharge(row) {
      this.$router.push(`/recharge/${row.id}`)
    },
    handleConsume(row) {
      this.$router.push(`/consume/${row.id}`)
    }
  }
}
</script>

<style scoped lang="scss">
.balance-text {
  color: #e6a23c;
  font-weight: bold;
}
</style>
