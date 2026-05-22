<template>
  <div class="course-list">
    <h1 class="page-title">课程列表</h1>
    <div class="page-card">
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="课程名称">
            <el-input v-model="searchForm.name" placeholder="请输入课程名称" clearable></el-input>
          </el-form-item>
          <el-form-item label="课程分类">
            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
              <el-option label="前端开发" value="前端开发"></el-option>
              <el-option label="后端开发" value="后端开发"></el-option>
              <el-option label="数据科学" value="数据科学"></el-option>
              <el-option label="设计" value="设计"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <i class="el-icon-search"></i> 搜索
            </el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="table-container">
        <el-table
          :data="tableData"
          border
          stripe
          style="width: 100%"
        >
          <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
          <el-table-column prop="name" label="课程名称" min-width="200"></el-table-column>
          <el-table-column prop="teacher" label="授课老师" width="120" align="center"></el-table-column>
          <el-table-column prop="category" label="课程分类" width="120" align="center"></el-table-column>
          <el-table-column prop="duration" label="课时" width="100" align="center">
            <template slot-scope="scope">
              {{ scope.row.duration }} 课时
            </template>
          </el-table-column>
          <el-table-column prop="students" label="学习人数" width="120" align="center"></el-table-column>
          <el-table-column prop="price" label="价格" width="100" align="center">
            <template slot-scope="scope">
              <span style="color: #F56C6C; font-weight: bold;">¥{{ scope.row.price }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.status === 'published' ? 'success' : 'info'">
                {{ scope.row.status === 'published' ? '已发布' : '草稿' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="140" align="center"></el-table-column>
          <el-table-column label="操作" width="200" align="center" fixed="right">
            <template slot-scope="scope">
              <el-button size="mini" type="primary" @click="handleView(scope.row)">查看详情</el-button>
              <el-button
                v-if="!isEnrolled(scope.row.id)"
                size="mini"
                type="success"
                @click="handleEnroll(scope.row)"
              >
                立即报名
              </el-button>
              <el-button
                v-else
                size="mini"
                disabled
              >
                <i class="el-icon-check"></i> 已报名
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pagination.currentPage"
          :page-sizes="[5, 10, 20]"
          :page-size="pagination.pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="pagination.total"
        ></el-pagination>
      </div>
    </div>

    <el-dialog
      title="课程详情"
      :visible.sync="detailDialogVisible"
      width="600px"
    >
      <div v-if="currentCourse">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="课程名称">{{ currentCourse.name }}</el-descriptions-item>
          <el-descriptions-item label="授课老师">{{ currentCourse.teacher }}</el-descriptions-item>
          <el-descriptions-item label="课程分类">{{ currentCourse.category }}</el-descriptions-item>
          <el-descriptions-item label="课时">{{ currentCourse.duration }} 课时</el-descriptions-item>
          <el-descriptions-item label="学习人数">{{ currentCourse.students }} 人</el-descriptions-item>
          <el-descriptions-item label="价格">¥{{ currentCourse.price }}</el-descriptions-item>
          <el-descriptions-item label="课程描述">{{ currentCourse.description }}</el-descriptions-item>
        </el-descriptions>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button
          v-if="currentCourse && !isEnrolled(currentCourse.id)"
          type="primary"
          @click="handleEnroll(currentCourse)"
        >
          立即报名
        </el-button>
        <el-button
          v-else
          type="success"
          disabled
        >
          <i class="el-icon-check"></i> 已报名
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { courses, enrollmentRecords } from '@/mock/data'

export default {
  name: 'CourseList',
  data() {
    return {
      searchForm: {
        name: '',
        category: ''
      },
      allCourses: courses,
      enrollmentRecords: enrollmentRecords,
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: courses.length
      },
      detailDialogVisible: false,
      currentCourse: null
    }
  },
  computed: {
    tableData() {
      const { currentPage, pageSize } = this.pagination
      const start = (currentPage - 1) * pageSize
      const end = start + pageSize
      return this.filteredCourses.slice(start, end)
    },
    filteredCourses() {
      return this.allCourses.filter(course => {
        const nameMatch = !this.searchForm.name || course.name.includes(this.searchForm.name)
        const categoryMatch = !this.searchForm.category || course.category === this.searchForm.category
        return nameMatch && categoryMatch
      })
    }
  },
  methods: {
    isEnrolled(courseId) {
      return this.enrollmentRecords.some(record => record.courseId === courseId)
    },
    handleSearch() {
      this.pagination.currentPage = 1
      this.pagination.total = this.filteredCourses.length
    },
    handleReset() {
      this.searchForm = {
        name: '',
        category: ''
      }
      this.handleSearch()
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val
    },
    handleView(row) {
      this.currentCourse = row
      this.detailDialogVisible = true
    },
    handleEnroll(row) {
      if (this.isEnrolled(row.id)) {
        this.$message.warning('您已报名该课程，无需重复报名！')
        return
      }
      this.$router.push({
        path: '/enroll',
        query: { courseId: row.id, courseName: row.name }
      })
    }
  }
}
</script>
