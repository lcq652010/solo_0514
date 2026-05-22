<template>
  <div class="page-container">
    <div class="page-title">考试科目列表</div>
    
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索科目名称或代码"
        style="width: 300px;"
        clearable
        @input="handleSearch"
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
    </div>

    <el-table :data="paginatedSubjectList" border style="width: 100%;">
      <el-table-column prop="code" label="科目代码" width="140" align="center"></el-table-column>
      <el-table-column prop="name" label="科目名称" min-width="220"></el-table-column>
      <el-table-column prop="examType" label="考试类型" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="getExamTypeTagType(scope.row.examType)" size="small">
            {{ getExamTypeLabel(scope.row.examType) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="examDate" label="考试日期" width="120" align="center"></el-table-column>
      <el-table-column prop="examTime" label="考试时间" width="130" align="center"></el-table-column>
      <el-table-column prop="fee" label="报名费(元)" width="100" align="center"></el-table-column>
      <el-table-column label="报名进度" width="160" align="center">
        <template slot-scope="scope">
          <el-progress
            :percentage="Math.round((scope.row.enrolled / scope.row.quota) * 100)"
            :stroke-width="12"
            :show-text="true"
          ></el-progress>
          <div style="font-size: 12px; color: #909399; margin-top: 5px;">
            {{ scope.row.enrolled }}/{{ scope.row.quota }}人
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.status === 1 ? 'success' : scope.row.status === 0 ? 'info' : 'danger'" size="small">
            {{ statusMap[scope.row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" align="center">
        <template slot-scope="scope">
          <el-button
            v-if="!hasApplied(scope.row.id)"
            type="primary"
            size="small"
            @click="handleApply(scope.row)"
            :disabled="scope.row.status !== 1 || scope.row.enrolled >= scope.row.quota"
          >
            立即报名
          </el-button>
          <el-tag
            v-else
            type="warning"
            size="small"
          >
            {{ getApplyStatusText(scope.row.id) }}
          </el-tag>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
      style="margin-top: 20px; text-align: right;"
      background
      :page-size="pageSize"
      :total="filteredSubjectList.length"
      :current-page.sync="currentPage"
      layout="total, prev, pager, next, jumper"
      @current-change="handlePageChange"
    ></el-pagination>
  </div>
</template>

<script>
import { subjectList, statusMap, applicationRecords, applyStatusMap, examTypeList } from '@/mock/data.js'

export default {
  name: 'SubjectList',
  data() {
    return {
      subjectList,
      statusMap,
      applicationRecords,
      examTypeList,
      searchKeyword: '',
      pageSize: 10,
      currentPage: 1
    }
  },
  computed: {
    filteredSubjectList() {
      let result = this.subjectList
      if (!this.searchKeyword) {
        return result
      }
      const keyword = this.searchKeyword.toLowerCase()
      return result.filter(item => 
        item.name.toLowerCase().includes(keyword) || 
        item.code.toLowerCase().includes(keyword)
      )
    },
    paginatedSubjectList() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredSubjectList.slice(start, end)
    }
  },
  methods: {
    handleSearch() {
      this.currentPage = 1
    },
    handlePageChange() {
    },
    getExamTypeTagType(type) {
      const typeMap = {
        'computer': 'primary',
        'english': 'success',
        'teacher': 'warning'
      }
      return typeMap[type] || 'info'
    },
    getExamTypeLabel(type) {
      const found = this.examTypeList.find(item => item.value === type)
      return found ? found.label : type
    },
    hasApplied(subjectId) {
      return this.applicationRecords.some(record => 
        record.subjectId === subjectId && record.status !== 3
      )
    },
    getApplyStatusText(subjectId) {
      const record = this.applicationRecords.find(record => 
        record.subjectId === subjectId && record.status !== 3
      )
      if (record) {
        return applyStatusMap[record.status]
      }
      return '已报名'
    },
    handleApply(row) {
      this.$router.push({
        path: '/apply',
        query: { subjectId: row.id }
      })
    }
  }
}
</script>

<style scoped>
.search-bar {
  margin-bottom: 20px;
}
</style>
