<template>
  <div class="binding-page">
    <div class="page-header">
      <div class="page-title">宿舍绑定管理</div>
      <div class="page-subtitle">绑定您的宿舍信息，方便后续查询和充值</div>
    </div>

    <div class="card-wrapper">
      <div class="card-header">
        <span class="card-title">已绑定宿舍</span>
        <el-button type="primary" size="small" icon="el-icon-plus" @click="showAddDialog">
          绑定新宿舍
        </el-button>
      </div>

      <el-row :gutter="20">
        <el-col :span="8" v-for="item in bindingList" :key="item.id">
          <div class="dormitory-card" :class="{ 'is-default': item.isDefault }">
            <div class="dormitory-header">
              <div class="dormitory-building">{{ item.building }}</div>
              <el-tag v-if="item.isDefault" type="success" size="small">默认</el-tag>
            </div>
            <div class="dormitory-room">
              <i class="el-icon-house"></i>
              {{ item.room }}
            </div>
            <div class="dormitory-time">
              绑定时间：{{ item.bindTime }}
            </div>
            <div class="dormitory-actions">
              <el-button
                v-if="!item.isDefault"
                type="text"
                size="small"
                @click="setDefault(item)"
              >
                设为默认
              </el-button>
              <el-button
                type="text"
                size="small"
                @click="viewDetail(item)"
              >
                查看详情
              </el-button>
              <el-button
                v-if="!item.isDefault"
                type="text"
                size="small"
                class="danger"
                @click="handleUnbind(item)"
              >
                解绑
              </el-button>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-empty v-if="bindingList.length === 0" description="暂无绑定的宿舍"></el-empty>
    </div>

    <div class="card-wrapper">
      <div class="card-header">
        <span class="card-title">快速绑定</span>
      </div>
      <div class="quick-bind-tips">
        <el-alert
          title="绑定说明"
          type="info"
          :closable="false"
          show-icon
        >
          <template slot-scope="{ type }">
            <div>1. 请准确选择您所居住的宿舍楼和房间号</div>
            <div>2. 绑定后可以快速查询水电用量和进行充值</div>
            <div>3. 同一账号最多可以绑定3个宿舍</div>
            <div>4. 默认宿舍会作为首选宿舍展示</div>
          </template>
        </el-alert>
      </div>

      <el-form
        ref="quickBindForm"
        :model="quickBindForm"
        :rules="quickBindRules"
        label-width="100px"
        class="quick-bind-form"
        style="margin-top: 30px;"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="选择楼栋" prop="building">
              <el-select
                v-model="quickBindForm.building"
                placeholder="请选择楼栋"
                style="width: 100%;"
                @change="onBuildingChange"
              >
                <el-option
                  v-for="item in buildingList"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="选择房间" prop="room">
              <el-select
                v-model="quickBindForm.room"
                placeholder="请先选择楼栋"
                style="width: 100%;"
                :disabled="!quickBindForm.building"
              >
                <el-option
                  v-for="room in currentRoomList"
                  :key="room"
                  :label="room"
                  :value="room"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="学生姓名">
          <el-input
            v-model="quickBindForm.studentName"
            placeholder="请输入学生姓名"
            style="width: 300px;"
          />
        </el-form-item>

        <el-form-item label="学号">
          <el-input
            v-model="quickBindForm.studentId"
            placeholder="请输入学号"
            style="width: 300px;"
          />
        </el-form-item>

        <el-form-item label="联系电话" prop="phone">
          <el-input
            v-model="quickBindForm.phone"
            placeholder="请输入联系电话"
            style="width: 300px;"
            maxlength="11"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" @click="submitQuickBind" :loading="submitting">
            立即绑定
          </el-button>
          <el-button size="large" @click="resetQuickBindForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <el-dialog
      title="绑定新宿舍"
      :visible.sync="addDialogVisible"
      width="500px"
      @close="resetAddForm"
    >
      <el-form
        ref="addForm"
        :model="addForm"
        :rules="addRules"
        label-width="100px"
      >
        <el-form-item label="选择楼栋" prop="building">
          <el-select
            v-model="addForm.building"
            placeholder="请选择楼栋"
            style="width: 100%;"
            @change="onBuildingChange"
          >
            <el-option
              v-for="item in buildingList"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="选择房间" prop="room">
          <el-select
            v-model="addForm.room"
            placeholder="请先选择楼栋"
            style="width: 100%;"
            :disabled="!addForm.building"
          >
            <el-option
              v-for="room in currentRoomList"
              :key="room"
              :label="room"
              :value="room"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="学生姓名" prop="studentName">
          <el-input v-model="addForm.studentName" placeholder="请输入学生姓名" />
        </el-form-item>

        <el-form-item label="学号" prop="studentId">
          <el-input v-model="addForm.studentId" placeholder="请输入学号" />
        </el-form-item>

        <el-form-item label="设为默认">
          <el-switch v-model="addForm.setDefault" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAddForm">确定</el-button>
      </div>
    </el-dialog>

    <el-dialog
      title="宿舍详情"
      :visible.sync="detailDialogVisible"
      width="600px"
    >
      <el-descriptions :column="2" border v-if="currentDormitory">
        <el-descriptions-item label="楼栋号">
          {{ currentDormitory.building }}
        </el-descriptions-item>
        <el-descriptions-item label="房间号">
          {{ currentDormitory.room }}
        </el-descriptions-item>
        <el-descriptions-item label="是否默认">
          <el-tag :type="currentDormitory.isDefault ? 'success' : 'info'" size="small">
            {{ currentDormitory.isDefault ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="绑定时间">
          {{ currentDormitory.bindTime }}
        </el-descriptions-item>
        <el-descriptions-item label="水费余额" :span="2">
          <span style="color: #67C23A; font-weight: 600;">¥{{ dormitoryInfo.waterBalance }}</span>
        </el-descriptions-item>
        <el-descriptions-item label="电费余额" :span="2">
          <span style="color: #67C23A; font-weight: 600;">¥{{ dormitoryInfo.electricBalance }}</span>
        </el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="goToRecharge">立即充值</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { buildingList, roomList, bindingDormitories, dormitoryInfo } from '@/data/mock.js'

export default {
  name: 'Binding',
  data() {
    return {
      submitting: false,
      addDialogVisible: false,
      detailDialogVisible: false,
      currentDormitory: null,
      buildingList,
      roomList,
      bindingList: [...bindingDormitories],
      dormitoryInfo,
      quickBindForm: {
        building: '',
        room: '',
        studentName: '',
        studentId: '',
        phone: ''
      },
      addForm: {
        building: '',
        room: '',
        studentName: '',
        studentId: '',
        setDefault: false
      },
      quickBindRules: {
        building: [
          { required: true, message: '请选择楼栋', trigger: 'change' }
        ],
        room: [
          { required: true, message: '请选择房间', trigger: 'change' }
        ],
        phone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号格式', trigger: 'blur' }
        ]
      },
      addRules: {
        building: [
          { required: true, message: '请选择楼栋', trigger: 'change' }
        ],
        room: [
          { required: true, message: '请选择房间', trigger: 'change' }
        ],
        studentName: [
          { required: true, message: '请输入学生姓名', trigger: 'blur' }
        ],
        studentId: [
          { required: true, message: '请输入学号', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    currentRoomList() {
      const building = this.quickBindForm.building || this.addForm.building
      return building ? (this.roomList[building] || []) : []
    }
  },
  methods: {
    showAddDialog() {
      if (this.bindingList.length >= 3) {
        this.$message.warning('最多只能绑定3个宿舍，请先解绑不需要的宿舍')
        return
      }
      this.addDialogVisible = true
    },
    onBuildingChange() {
      this.quickBindForm.room = ''
      this.addForm.room = ''
    },
    setDefault(dormitory) {
      this.bindingList.forEach(item => {
        item.isDefault = item.id === dormitory.id
      })
      this.$message.success(`已将${dormitory.building}${dormitory.room}设为默认宿舍`)
    },
    viewDetail(dormitory) {
      this.currentDormitory = dormitory
      this.detailDialogVisible = true
    },
    goToRecharge() {
      this.detailDialogVisible = false
      this.$router.push('/recharge')
    },
    handleUnbind(dormitory) {
      this.$confirm(`确定要解绑${dormitory.building}${dormitory.room}吗？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const index = this.bindingList.findIndex(item => item.id === dormitory.id)
        if (index > -1) {
          this.bindingList.splice(index, 1)
        }
        this.$message.success('已成功解绑')
      }).catch(() => {})
    },
    submitQuickBind() {
      this.$refs.quickBindForm.validate(valid => {
        if (valid) {
          this.submitting = true
          setTimeout(() => {
            const newId = Math.max(...this.bindingList.map(item => item.id)) + 1
            this.bindingList.push({
              id: newId,
              building: this.quickBindForm.building,
              room: this.quickBindForm.room,
              isDefault: this.bindingList.length === 0,
              bindTime: new Date().toLocaleString().replace(/\//g, '-')
            })
            this.submitting = false
            this.$message.success('宿舍绑定成功！')
            this.resetQuickBindForm()
          }, 1000)
        }
      })
    },
    resetQuickBindForm() {
      this.quickBindForm = {
        building: '',
        room: '',
        studentName: '',
        studentId: '',
        phone: ''
      }
      this.$refs.quickBindForm && this.$refs.quickBindForm.clearValidate()
    },
    submitAddForm() {
      this.$refs.addForm.validate(valid => {
        if (valid) {
          if (this.addForm.setDefault) {
            this.bindingList.forEach(item => {
              item.isDefault = false
            })
          }
          const newId = Math.max(...this.bindingList.map(item => item.id)) + 1
          this.bindingList.push({
            id: newId,
            building: this.addForm.building,
            room: this.addForm.room,
            isDefault: this.addForm.setDefault || this.bindingList.length === 0,
            bindTime: new Date().toLocaleString().replace(/\//g, '-')
          })
          this.addDialogVisible = false
          this.$message.success('宿舍绑定成功！')
        }
      })
    },
    resetAddForm() {
      this.addForm = {
        building: '',
        room: '',
        studentName: '',
        studentId: '',
        setDefault: false
      }
      this.$refs.addForm && this.$refs.addForm.clearValidate()
    }
  }
}
</script>

<style scoped>
.binding-page {
  width: 100%;
}

.dormitory-card {
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  transition: all 0.3s;
}

.dormitory-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.dormitory-card.is-default {
  border-color: #67C23A;
  background: #f0f9ff;
}

.dormitory-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 15px;
}

.dormitory-building {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.dormitory-room {
  font-size: 24px;
  font-weight: 600;
  color: #409EFF;
  margin-bottom: 10px;
}

.dormitory-room i {
  margin-right: 8px;
  font-size: 20px;
}

.dormitory-time {
  font-size: 13px;
  color: #909399;
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.dormitory-actions {
  display: flex;
  gap: 10px;
}

.dormitory-actions .el-button.danger {
  color: #F56C6C;
}

.quick-bind-tips {
  margin-bottom: 20px;
}

.quick-bind-form {
  padding: 10px 0;
}

.dialog-footer {
  text-align: right;
}
</style>
