<template>
  <div class="page-card">
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索教练姓名或专长"
        style="width: 250px"
        clearable
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      <el-select v-model="filterStatus" placeholder="筛选状态" style="width: 120px" clearable>
        <el-option label="在线" value="online"></el-option>
        <el-option label="繁忙" value="busy"></el-option>
        <el-option label="离线" value="offline"></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch">
        <i class="el-icon-search"></i> 搜索
      </el-button>
      <el-button @click="handleReset">
        <i class="el-icon-refresh"></i> 重置
      </el-button>
    </div>

    <div class="table-container">
      <el-table
        :data="filteredTrainers"
        border
        style="width: 100%"
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column label="教练信息" width="220">
          <template slot-scope="scope">
            <div style="display: flex; align-items: center">
              <el-avatar
                :src="scope.row.avatar"
                size="50"
                style="margin-right: 12px"
              ></el-avatar>
              <div>
                <div style="font-weight: 500; color: #303133">{{ scope.row.name }}</div>
                <div style="font-size: 12px; color: #909399">{{ scope.row.phone }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="specialty" label="专长" min-width="180"></el-table-column>
        <el-table-column prop="experience" label="从业年限" width="100" align="center">
          <template slot-scope="scope">{{ scope.row.experience }}年</template>
        </el-table-column>
        <el-table-column prop="rating" label="评分" width="100" align="center">
          <template slot-scope="scope">
            <el-rate
              v-model="scope.row.rating"
              disabled
              show-score
              text-color="#ff9900"
              score-template="{value}"
            ></el-rate>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="课时费" width="100" align="center">
          <template slot-scope="scope">
            <span style="color: #f56c6c; font-weight: 500">¥{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center">
          <template slot-scope="scope">
            <el-button
              type="primary"
              size="small"
              icon="el-icon-edit"
              @click="handleBook(scope.row)"
            >
              约课
            </el-button>
            <el-button
              type="info"
              size="small"
              icon="el-icon-view"
              @click="handleView(scope.row)"
            >
              详情
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          :current-page="pagination.page"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          :page-sizes="[5, 10, 20, 50]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        ></el-pagination>
      </div>
    </div>

    <el-dialog title="教练详情" :visible.sync="detailVisible" width="500px">
      <div v-if="currentTrainer" style="text-align: center; padding: 20px">
        <el-avatar :src="currentTrainer.avatar" size="100"></el-avatar>
        <h3 style="margin: 20px 0 10px">{{ currentTrainer.name }}</h3>
        <el-tag type="success">{{ currentTrainer.specialty }}</el-tag>
        <el-descriptions :column="1" border style="margin-top: 20px">
          <el-descriptions-item label="从业年限">{{ currentTrainer.experience }}年</el-descriptions-item>
          <el-descriptions-item label="评分">
            <el-rate v-model="currentTrainer.rating" disabled show-score text-color="#ff9900"></el-rate>
          </el-descriptions-item>
          <el-descriptions-item label="课时费">
            <span style="color: #f56c6c; font-size: 18px; font-weight: bold">¥{{ currentTrainer.price }}/课时</span>
          </el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentTrainer.phone }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleBookFromDetail">立即约课</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { mockTrainers } from '@/mock/data'

export default {
  name: 'TrainerList',
  data() {
    return {
      trainers: mockTrainers,
      searchKeyword: '',
      filterStatus: '',
      pagination: {
        page: 1,
        pageSize: 10,
        total: mockTrainers.length
      },
      detailVisible: false,
      currentTrainer: null
    }
  },
  computed: {
    filteredTrainers() {
      let list = this.trainers
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase()
        list = list.filter(
          item =>
            item.name.toLowerCase().includes(keyword) ||
            item.specialty.toLowerCase().includes(keyword)
        )
      }
      if (this.filterStatus) {
        list = list.filter(item => item.status === this.filterStatus)
      }
      this.pagination.total = list.length
      const start = (this.pagination.page - 1) * this.pagination.pageSize
      const end = start + this.pagination.pageSize
      return list.slice(start, end)
    }
  },
  methods: {
    getStatusType(status) {
      const map = {
        online: 'success',
        busy: 'warning',
        offline: 'info'
      }
      return map[status] || 'info'
    },
    getStatusText(status) {
      const map = {
        online: '在线',
        busy: '繁忙',
        offline: '离线'
      }
      return map[status] || '未知'
    },
    tableRowClassName({ rowIndex }) {
      return rowIndex % 2 === 0 ? 'even-row' : 'odd-row'
    },
    handleSearch() {
      this.pagination.page = 1
    },
    handleReset() {
      this.searchKeyword = ''
      this.filterStatus = ''
      this.pagination.page = 1
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.page = val
    },
    handleBook(row) {
      this.$router.push({
        path: '/booking',
        query: { trainerId: row.id, trainerName: row.name }
      })
    },
    handleView(row) {
      this.currentTrainer = row
      this.detailVisible = true
    },
    handleBookFromDetail() {
      this.detailVisible = false
      if (this.currentTrainer) {
        this.handleBook(this.currentTrainer)
      }
    }
  }
}
</script>

<style scoped>
.even-row {
  background-color: #fafafa;
}
.odd-row {
  background-color: #fff;
}
</style>
