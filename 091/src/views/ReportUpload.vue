<template>
  <div class="report-upload">
    <el-card>
      <div slot="header" class="card-header">
        <span>报告上传</span>
      </div>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="upload-form"
      >
        <el-form-item label="选择记录" prop="recordId">
          <el-select
            v-model="form.recordId"
            placeholder="请选择对应的体检记录"
            style="width: 100%"
            @change="handleRecordChange"
          >
            <el-option
              v-for="item in recordList"
              :key="item.id"
              :label="`${item.id} - ${item.packageName}`"
              :value="item.id"
              :disabled="item.status !== 'completed'"
            >
              <span>{{ item.id }} - {{ item.packageName }}</span>
              <span style="float: right; color: #909399">
                {{ item.examDate }}
              </span>
            </el-option>
          </el-select>
          <div class="tip">
            <i class="el-icon-info"></i>
            仅可上传状态为"已完成"的体检报告
          </div>
        </el-form-item>

        <el-form-item label="报告名称" prop="reportName">
          <el-input v-model="form.reportName" placeholder="请输入报告名称"></el-input>
        </el-form-item>

        <el-form-item label="报告类型" prop="reportType">
          <el-radio-group v-model="form.reportType">
            <el-radio label="main">主报告</el-radio>
            <el-radio label="lab">检验报告</el-radio>
            <el-radio label="image">影像报告</el-radio>
            <el-radio label="other">其他</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="报告文件" prop="file">
          <el-upload
            ref="uploadRef"
            class="upload-demo"
            drag
            :action="uploadUrl"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-upload="beforeUpload"
            :on-success="onSuccess"
            :on-error="onError"
            :file-list="fileList"
            :limit="1"
            accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
            :auto-upload="false"
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">
              支持 pdf、doc、docx、jpg、jpeg、png 格式，单个文件不超过 10MB
            </div>
          </el-upload>
        </el-form-item>

        <el-form-item label="报告摘要" prop="summary">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="4"
            placeholder="请输入报告摘要（选填）"
          ></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="handleSubmit">
            提交上传
          </el-button>
          <el-button size="large" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card style="margin-top: 20px">
      <div slot="header" class="card-header">
        <span>已上传报告列表</span>
      </div>

      <el-table :data="uploadedList" border style="width: 100%">
        <el-table-column prop="recordId" label="记录编号" width="120" align="center"></el-table-column>
        <el-table-column prop="reportName" label="报告名称" min-width="180"></el-table-column>
        <el-table-column prop="reportType" label="报告类型" width="100" align="center">
          <template slot-scope="scope">
            {{ getReportTypeName(scope.row.reportType) }}
          </template>
        </el-table-column>
        <el-table-column prop="fileName" label="文件名" min-width="180"></el-table-column>
        <el-table-column prop="uploadTime" label="上传时间" width="160" align="center"></el-table-column>
        <el-table-column prop="uploader" label="上传人" width="100" align="center"></el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleDownload(scope.row)">
              下载
            </el-button>
            <el-button type="danger" size="mini" @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ReportUpload',
  data() {
    return {
      form: {
        recordId: '',
        reportName: '',
        reportType: 'main',
        summary: '',
        file: null
      },
      rules: {
        recordId: [
          { required: true, message: '请选择体检记录', trigger: 'change' }
        ],
        reportName: [
          { required: true, message: '请输入报告名称', trigger: 'blur' }
        ],
        reportType: [
          { required: true, message: '请选择报告类型', trigger: 'change' }
        ]
      },
      uploadUrl: '',
      fileList: [],
      recordList: [
        { id: 'REC001', packageName: '入职基础体检套餐', examDate: '2024-01-15', status: 'completed' },
        { id: 'REC002', packageName: '青年常规体检套餐', examDate: '2024-01-20', status: 'completed' },
        { id: 'REC003', packageName: '精英尊享体检套餐', examDate: '2024-01-25', status: 'scheduled' },
        { id: 'REC004', packageName: '女性专属体检套餐', examDate: '2024-01-05', status: 'cancelled' },
        { id: 'REC005', packageName: '中年全面体检套餐', examDate: '2024-01-08', status: 'completed' }
      ],
      uploadedList: [
        {
          id: 1,
          recordId: 'REC001',
          reportName: '入职体检主报告',
          reportType: 'main',
          fileName: 'REC001_入职体检主报告.pdf',
          uploadTime: '2024-01-18 10:30:00',
          uploader: '管理员'
        },
        {
          id: 2,
          recordId: 'REC001',
          reportName: '入职体检检验报告',
          reportType: 'lab',
          fileName: 'REC001_入职体检检验报告.pdf',
          uploadTime: '2024-01-18 10:35:00',
          uploader: '管理员'
        }
      ]
    }
  },
  methods: {
    handleRecordChange(val) {
      const record = this.recordList.find(item => item.id === val)
      if (record) {
        this.form.reportName = `${record.packageName}_报告`
      }
    },
    beforeUpload(file) {
      const isSizeValid = file.size / 1024 / 1024 < 10
      if (!isSizeValid) {
        this.$message.error('文件大小不能超过 10MB!')
      }
      return isSizeValid
    },
    onSuccess(response, file) {
      this.$message.success('文件上传成功')
    },
    onError(err, file) {
      this.$message.error('文件上传失败')
    },
    handleRemove(file, fileList) {
      this.form.file = null
    },
    handlePreview(file) {
      this.$message.info(`预览文件: ${file.name}`)
    },
    handleSubmit() {
      this.$refs.formRef.validate((valid) => {
        if (valid) {
          if (this.$refs.uploadRef.uploadFiles.length === 0) {
            this.$message.warning('请先上传报告文件')
            return
          }
          const newUpload = {
            id: this.uploadedList.length + 1,
            recordId: this.form.recordId,
            reportName: this.form.reportName,
            reportType: this.form.reportType,
            fileName: this.$refs.uploadRef.uploadFiles[0].name,
            uploadTime: new Date().toLocaleString(),
            uploader: '当前用户'
          }
          this.uploadedList.unshift(newUpload)
          this.$message.success('报告上传成功！')
          this.handleReset()
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    handleReset() {
      this.$refs.formRef.resetFields()
      this.$refs.uploadRef.clearFiles()
      this.fileList = []
    },
    handleDownload(row) {
      this.$message.success(`正在下载: ${row.fileName}`)
    },
    handleDelete(row) {
      this.$confirm('确定要删除该报告吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.uploadedList.findIndex(item => item.id === row.id)
        if (index > -1) {
          this.uploadedList.splice(index, 1)
        }
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    getReportTypeName(type) {
      const map = {
        main: '主报告',
        lab: '检验报告',
        image: '影像报告',
        other: '其他'
      }
      return map[type] || type
    }
  }
}
</script>

<style scoped>
.report-upload {
  padding: 0;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
}

.upload-form {
  max-width: 700px;
}

.tip {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

.tip i {
  margin-right: 4px;
}

.upload-demo {
  width: 100%;
}
</style>
