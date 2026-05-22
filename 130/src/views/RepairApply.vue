<template>
  <div class="page-container">
    <h2 class="page-title">报修申请</h2>
    <div class="form-container">
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="报修标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入报修标题" maxlength="50" show-word-limit></el-input>
        </el-form-item>
        
        <el-form-item label="报修类型" prop="type">
          <el-select v-model="form.type" placeholder="请选择报修类型" style="width: 100%">
            <el-option v-for="item in repairTypes" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="紧急程度" prop="urgency">
          <el-radio-group v-model="form.urgency">
            <el-radio v-for="item in urgencyLevels" :key="item.value" :label="item.value">{{ item.label }}</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="所属楼栋" prop="building">
          <el-select v-model="form.building" placeholder="请选择所属楼栋" style="width: 100%">
            <el-option v-for="item in buildingOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
          </el-select>
        </el-form-item>
        
        <el-form-item label="问题描述" prop="description">
          <el-input type="textarea" v-model="form.description" :rows="4" placeholder="请详细描述问题情况" maxlength="500" show-word-limit></el-input>
        </el-form-item>
        
        <el-form-item label="维修地址" prop="address">
          <el-input v-model="form.address" placeholder="请输入详细地址，如：1栋2单元301室"></el-input>
        </el-form-item>
        
        <el-form-item label="联系人" prop="contact">
          <el-input v-model="form.contact" placeholder="请输入联系人姓名"></el-input>
        </el-form-item>
        
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="form.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        
        <el-form-item label="上传图片">
          <div class="upload-tip">
            <i class="el-icon-info"></i>
            <span>支持 JPG、PNG、GIF 格式，单张图片不超过 5MB，最多上传 5 张</span>
          </div>
          <el-upload
            class="upload-demo"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :on-preview="handlePicturePreview"
            :on-remove="handleRemove"
            :before-upload="beforeUpload"
            :on-change="handleChange"
            :file-list="fileList"
            :limit="5"
            :on-exceed="handleExceed"
            accept="image/jpeg,image/png,image/gif"
          >
            <i class="el-icon-plus"></i>
          </el-upload>
          <el-dialog :visible.sync="dialogVisible" size="tiny">
            <img width="100%" :src="dialogImageUrl" alt="">
          </el-dialog>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="submitForm" size="large">提交报修</el-button>
          <el-button @click="resetForm" size="large">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { repairTypes, urgencyLevels, buildingOptions } from '../mock/data'
import { RepairStore } from '../store/repairStore'

export default {
  name: 'RepairApply',
  data() {
    return {
      repairTypes,
      urgencyLevels,
      buildingOptions,
      form: {
        title: '',
        type: '',
        urgency: '1',
        building: '',
        description: '',
        address: '',
        contact: '',
        phone: ''
      },
      rules: {
        title: [
          { required: true, message: '请输入报修标题', trigger: 'blur' },
          { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
        ],
        type: [
          { required: true, message: '请选择报修类型', trigger: 'change' }
        ],
        building: [
          { required: true, message: '请选择所属楼栋', trigger: 'change' }
        ],
        description: [
          { required: true, message: '请输入问题描述', trigger: 'blur' },
          { min: 5, max: 500, message: '长度在 5 到 500 个字符', trigger: 'blur' }
        ],
        address: [
          { required: true, message: '请输入维修地址', trigger: 'blur' }
        ],
        contact: [
          { required: true, message: '请输入联系人姓名', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
        ]
      },
      fileList: [],
      dialogImageUrl: '',
      dialogVisible: false,
      allowedTypes: ['image/jpeg', 'image/png', 'image/gif'],
      maxSize: 5 * 1024 * 1024,
      maxFiles: 5
    }
  },
  methods: {
    beforeUpload(file) {
      if (file.size === 0) {
        this.$message.error(`${file.name} 是空文件，请选择有效的图片文件`)
        return false
      }
      
      const isAllowedType = this.allowedTypes.includes(file.type)
      const isLtMaxSize = file.size < this.maxSize

      if (!isAllowedType) {
        this.$message.error('只支持 JPG、PNG、GIF 格式的图片！')
        return false
      }
      if (!isLtMaxSize) {
        this.$message.error('图片大小不能超过 5MB！')
        return false
      }
      return true
    },
    handleChange(file, fileList) {
      if (file.status === 'ready') {
        if (file.raw && file.raw.size === 0) {
          this.$message.error(`${file.name} 是空文件，请选择有效的图片文件`)
          this.fileList = fileList.filter(item => item.uid !== file.uid)
          return
        }
        
        const isAllowedType = this.allowedTypes.includes(file.raw.type)
        const isLtMaxSize = file.raw.size < this.maxSize
        
        if (!isAllowedType) {
          this.$message.error(`${file.name} 格式不支持，请上传 JPG、PNG、GIF 格式的图片`)
          this.fileList = fileList.filter(item => item.uid !== file.uid)
          return
        }
        if (!isLtMaxSize) {
          this.$message.error(`${file.name} 超过 5MB 限制`)
          this.fileList = fileList.filter(item => item.uid !== file.uid)
          return
        }
        this.$message.success(`${file.name} 上传成功`)
      }
      this.fileList = fileList
    },
    handleExceed(files, fileList) {
      this.$message.warning(`最多只能上传 ${this.maxFiles} 张图片，当前已选择 ${files.length} 张，共 ${fileList.length + files.length} 张`)
    },
    submitForm() {
      this.$refs.form.validate((valid) => {
        if (valid) {
          const typeItem = this.repairTypes.find(item => item.value === this.form.type)
          const urgencyItem = this.urgencyLevels.find(item => item.value === this.form.urgency)
          const buildingItem = this.buildingOptions.find(item => item.value === this.form.building)
          
          const repairData = {
            ...this.form,
            typeName: typeItem ? typeItem.label : '',
            urgencyName: urgencyItem ? urgencyItem.label : '',
            buildingName: buildingItem ? buildingItem.label : '',
            images: this.fileList.map(item => item.url || item.name)
          }
          
          RepairStore.addRepair(repairData)
          this.$message.success('报修申请提交成功！')
          this.$router.push('/my-repairs')
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.form.resetFields()
      this.fileList = []
    },
    handleRemove(file, fileList) {
      this.fileList = fileList
      this.$message.info('已移除图片')
    },
    handlePicturePreview(file) {
      this.dialogImageUrl = file.url
      this.dialogVisible = true
    }
  }
}
</script>

<style scoped>
.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-bottom: 10px;
  padding: 8px 12px;
  background: #f4f4f5;
  border-radius: 4px;
}

.upload-tip i {
  color: #409EFF;
  margin-right: 5px;
}

.upload-demo {
  width: 100%;
}

.upload-demo >>> .el-upload--picture-card {
  width: 100px;
  height: 100px;
  line-height: 100px;
}
</style>
