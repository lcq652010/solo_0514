<template>
  <div class="service-packages">
    <div class="page-title">洗护服务套餐管理</div>
    <div class="card-wrapper">
      <el-button type="primary" @click="handleAdd">
        <i class="el-icon-plus"></i> 添加套餐
      </el-button>
      <el-divider></el-divider>
      
      <el-row :gutter="20">
        <el-col :span="8" v-for="(item, index) in packageList" :key="index">
          <el-card shadow="hover" class="package-card">
            <div slot="header" class="clearfix">
              <span class="package-name">{{ item.name }}</span>
              <span class="package-price" style="float: right; color: #409EFF;">¥{{ item.price }}</span>
            </div>
            <div class="package-content">
              <p><i class="el-icon-time"></i> 服务时长：{{ item.duration }}</p>
              <p><i class="el-icon-paperclip"></i> 服务项目：</p>
              <ul>
                <li v-for="(service, idx) in item.services" :key="idx">{{ service }}</li>
              </ul>
              <p><i class="el-icon-info"></i> 适用：{{ item.suitable }}</p>
            </div>
            <div slot="footer" class="card-footer">
              <el-button size="small" type="primary" @click="handleEdit(item)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(index)">删除</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="500px"
    >
      <el-form :model="formData" :rules="rules" ref="formData" label-width="100px">
        <el-form-item label="套餐名称" prop="name">
          <el-input v-model="formData.name"></el-input>
        </el-form-item>
        <el-form-item label="套餐价格" prop="price">
          <el-input-number v-model="formData.price" :min="0" :step="10"></el-input-number>
        </el-form-item>
        <el-form-item label="服务时长" prop="duration">
          <el-input v-model="formData.duration" placeholder="如：60分钟"></el-input>
        </el-form-item>
        <el-form-item label="适用宠物" prop="suitable">
          <el-input v-model="formData.suitable" placeholder="如：小型犬"></el-input>
        </el-form-item>
        <el-form-item label="服务项目" prop="services">
          <el-input
            type="textarea"
            v-model="servicesText"
            placeholder="每行一个服务项目"
            :rows="4"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ServicePackages',
  data() {
    return {
      dialogVisible: false,
      dialogTitle: '添加套餐',
      editIndex: -1,
      formData: {
        name: '',
        price: 0,
        duration: '',
        suitable: '',
        services: []
      },
      servicesText: '',
      rules: {
        name: [
          { required: true, message: '请输入套餐名称', trigger: 'blur' }
        ],
        price: [
          { required: true, message: '请输入套餐价格', trigger: 'blur' }
        ],
        duration: [
          { required: true, message: '请输入服务时长', trigger: 'blur' }
        ],
        suitable: [
          { required: true, message: '请输入适用宠物类型', trigger: 'blur' }
        ]
      },
      packageList: [
        {
          name: '基础洗护套餐',
          price: 88,
          duration: '60分钟',
          suitable: '小型犬/猫',
          services: ['洗澡', '吹干', '梳毛', '指甲修剪', '耳道清洁']
        },
        {
          name: '精致洗护套餐',
          price: 168,
          duration: '90分钟',
          suitable: '中小型犬',
          services: ['洗澡', '吹干', '梳毛', '指甲修剪', '耳道清洁', '挤肛门腺', 'SPA护理']
        },
        {
          name: '豪华美容套餐',
          price: 298,
          duration: '120分钟',
          suitable: '所有犬猫',
          services: ['洗澡', '吹干', '造型修剪', '指甲修剪', '耳道清洁', '挤肛门腺', 'SPA护理', '香水喷剂']
        },
        {
          name: '医疗洗护套餐',
          price: 198,
          duration: '90分钟',
          suitable: '皮肤敏感宠物',
          services: ['药浴', '吹干', '梳毛', '指甲修剪', '耳道清洁', '皮肤护理']
        },
        {
          name: '猫咪专属套餐',
          price: 128,
          duration: '75分钟',
          suitable: '猫咪专用',
          services: ['洗澡', '吹干', '梳毛', '指甲修剪', '耳道清洁', '猫毛护理', '去毛球']
        },
        {
          name: '大型犬洗护',
          price: 258,
          duration: '120分钟',
          suitable: '大型犬',
          services: ['洗澡', '吹干', '梳毛', '指甲修剪', '耳道清洁', '挤肛门腺', '深层清洁']
        }
      ]
    }
  },
  methods: {
    handleAdd() {
      this.dialogTitle = '添加套餐'
      this.editIndex = -1
      this.formData = {
        name: '',
        price: 0,
        duration: '',
        suitable: '',
        services: []
      }
      this.servicesText = ''
      this.dialogVisible = true
    },
    handleEdit(item) {
      this.dialogTitle = '编辑套餐'
      this.editIndex = this.packageList.indexOf(item)
      this.formData = { ...item }
      this.servicesText = item.services.join('\n')
      this.dialogVisible = true
    },
    handleDelete(index) {
      this.$confirm('确定要删除该套餐吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.packageList.splice(index, 1)
        this.$message.success('删除成功')
      }).catch(() => {})
    },
    handleSubmit() {
      this.$refs.formData.validate((valid) => {
        if (valid) {
          this.formData.services = this.servicesText.split('\n').filter(item => item.trim())
          if (this.editIndex === -1) {
            this.packageList.push({ ...this.formData })
            this.$message.success('添加成功')
          } else {
            this.packageList[this.editIndex] = { ...this.formData }
            this.$message.success('修改成功')
          }
          this.dialogVisible = false
        }
      })
    }
  }
}
</script>

<style scoped>
.package-card {
  margin-bottom: 20px;
}

.package-name {
  font-weight: bold;
  font-size: 16px;
}

.package-content {
  min-height: 180px;
}

.package-content p {
  margin-bottom: 10px;
  color: #606266;
}

.package-content ul {
  margin-left: 20px;
  margin-bottom: 10px;
}

.package-content li {
  color: #606266;
  line-height: 1.6;
}

.card-footer {
  text-align: right;
}
</style>
