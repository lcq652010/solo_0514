<template>
  <div class="homework-submit">
    <h1 class="page-title">作业提交</h1>
    <div class="page-card">
      <el-tabs v-model="activeTab" @tab-click="handleTabClick">
        <el-tab-pane label="待提交" name="not_submitted">
          <span slot="label">
            <i class="el-icon-time"></i> 待提交
            <el-badge :value="homeworkStats.notSubmitted" class="item" :hidden="!homeworkStats.notSubmitted"></el-badge>
          </span>
          <homework-table :list="tabData.notSubmitted" :show-submit="true" @submit="handleSubmit"></homework-table>
        </el-tab-pane>
        <el-tab-pane label="已提交" name="submitted">
          <span slot="label">
            <i class="el-icon-upload"></i> 已提交
            <el-badge :value="homeworkStats.submitted" class="item" :hidden="!homeworkStats.submitted"></el-badge>
          </span>
          <homework-table :list="tabData.submitted" :show-submit="false"></homework-table>
        </el-tab-pane>
        <el-tab-pane label="已批改" name="graded">
          <span slot="label">
            <i class="el-icon-s-check"></i> 已批改
            <el-badge :value="homeworkStats.graded" class="item" :hidden="!homeworkStats.graded"></el-badge>
          </span>
          <homework-table :list="tabData.graded" :show-submit="false" :show-grade="true"></homework-table>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog
      title="提交作业"
      :visible.sync="submitDialogVisible"
      width="600px"
      :close-on-click-modal="false"
    >
      <div v-if="currentHomework">
        <el-alert
          title="作业信息"
          type="info"
          :closable="false"
          style="margin-bottom: 20px;"
        >
          <p>课程：{{ currentHomework.courseName }}</p>
          <p>作业：{{ currentHomework.title }}</p>
          <p>要求：{{ currentHomework.description }}</p>
          <p>截止时间：{{ currentHomework.deadline }}</p>
        </el-alert>

        <el-form :model="submitForm" label-width="80px">
          <el-form-item label="作业内容">
            <el-input
              v-model="submitForm.content"
              type="textarea"
              :rows="6"
              placeholder="请输入作业内容..."
              maxlength="5000"
              show-word-limit
            ></el-input>
          </el-form-item>
          <el-form-item label="上传附件">
            <el-upload
              ref="upload"
              action="#"
              :auto-upload="false"
              :on-change="handleFileChange"
              :on-remove="handleFileRemove"
              :file-list="submitForm.files"
              multiple
              limit="3"
            >
              <el-button size="small" type="primary">选择文件</el-button>
              <div slot="tip" class="el-upload__tip">最多上传3个文件，支持 zip、rar、pdf、doc、docx 格式</div>
            </el-upload>
          </el-form-item>
          <el-form-item label="备注">
            <el-input
              v-model="submitForm.remark"
              type="textarea"
              :rows="2"
              placeholder="其他需要说明的内容（选填）"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="submitDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSubmit" :loading="submitting">确认提交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { homeworkList } from '@/mock/data'

const HomeworkTable = {
  name: 'HomeworkTable',
  props: {
    list: Array,
    showSubmit: Boolean,
    showGrade: Boolean
  },
  template: `
    <div>
      <div v-if="list.length === 0" class="empty-state">
        <i class="el-icon-document"></i>
        <p>暂无作业</p>
      </div>
      <el-table v-else :data="list" border stripe style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
        <el-table-column prop="courseName" label="所属课程" min-width="200"></el-table-column>
        <el-table-column prop="title" label="作业标题" min-width="250"></el-table-column>
        <el-table-column prop="deadline" label="截止时间" width="180" align="center"></el-table-column>
        <el-table-column v-if="showGrade" prop="score" label="得分" width="100" align="center">
          <template slot-scope="scope">
            <span :style="{ color: scope.row.score >= 80 ? '#67C23A' : scope.row.score >= 60 ? '#E6A23C' : '#F56C6C', fontWeight: 'bold' }">
              {{ scope.row.score }} 分
            </span>
          </template>
        </el-table-column>
        <el-table-column v-if="showGrade" label="教师评语" min-width="200">
          <template slot-scope="scope">
            {{ scope.row.comment || '暂无评语' }}
          </template>
        </el-table-column>
        <el-table-column label="提交状态" width="120" align="center">
          <template slot-scope="scope">
            <el-tag v-if="scope.row.status === 'not_submitted'" type="danger" size="small">待提交</el-tag>
            <el-tag v-else-if="scope.row.status === 'submitted'" type="warning" size="small">已提交</el-tag>
            <el-tag v-else type="success" size="small">已批改</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" type="info" @click="$emit('view', scope.row)">查看详情</el-button>
            <el-button v-if="showSubmit" size="mini" type="primary" @click="$emit('submit', scope.row)">提交作业</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  `
}

export default {
  name: 'HomeworkSubmit',
  components: {
    HomeworkTable
  },
  data() {
    return {
      activeTab: 'not_submitted',
      allHomework: homeworkList,
      submitDialogVisible: false,
      currentHomework: null,
      submitForm: {
        content: '',
        files: [],
        remark: ''
      },
      submitting: false
    }
  },
  computed: {
    tabData() {
      return {
        not_submitted: this.allHomework.filter(h => h.status === 'not_submitted'),
        submitted: this.allHomework.filter(h => h.status === 'submitted'),
        graded: this.allHomework.filter(h => h.status === 'graded')
      }
    },
    homeworkStats() {
      return {
        notSubmitted: this.tabData.not_submitted.length,
        submitted: this.tabData.submitted.length,
        graded: this.tabData.graded.length
      }
    }
  },
  methods: {
    handleTabClick(tab) {
      console.log('切换到:', tab.name)
    },
    handleSubmit(row) {
      this.currentHomework = row
      this.submitForm = {
        content: '',
        files: [],
        remark: ''
      }
      this.submitDialogVisible = true
    },
    handleFileChange(file, fileList) {
      this.submitForm.files = fileList
    },
    handleFileRemove(file, fileList) {
      this.submitForm.files = fileList
    },
    confirmSubmit() {
      if (!this.submitForm.content.trim()) {
        this.$message.warning('请输入作业内容')
        return
      }
      this.submitting = true
      setTimeout(() => {
        this.submitting = false
        this.submitDialogVisible = false
        this.currentHomework.status = 'submitted'
        this.currentHomework.submitTime = new Date().toLocaleString()
        this.$message.success('作业提交成功！')
      }, 1000)
    }
  }
}
</script>
