<template>
  <div class="appointment-list">
    <div class="page-title">预约记录列表</div>
    <div class="card-wrapper">
      <el-row :gutter="20" style="margin-bottom: 20px;">
        <el-col :span="5">
          <el-input v-model="searchKey" placeholder="搜索姓名或手机号">
            <i slot="prefix" class="el-input__icon el-icon-search"></i>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchStatus" placeholder="预约状态" clearable style="width: 100%;">
            <el-option label="待服务" value="待服务"></el-option>
            <el-option label="服务中" value="服务中"></el-option>
            <el-option label="已完成" value="已完成"></el-option>
            <el-option label="已取消" value="已取消"></el-option>
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="searchPetType" placeholder="宠物类型" clearable style="width: 100%;">
            <el-option label="小型犬" value="小型犬"></el-option>
            <el-option label="中型犬" value="中型犬"></el-option>
            <el-option label="大型犬" value="大型犬"></el-option>
            <el-option label="猫咪" value="猫咪"></el-option>
            <el-option label="其他" value="其他"></el-option>
          </el-select>
        </el-col>
        <el-col :span="5">
          <el-date-picker
            v-model="searchDate"
            type="date"
            placeholder="选择预约日期"
            style="width: 100%;"
            value-format="yyyy-MM-dd"
          ></el-date-picker>
        </el-col>
        <el-col :span="6" style="text-align: right;">
          <el-button type="primary" @click="goToAppointment">
            <i class="el-icon-plus"></i> 新增预约
          </el-button>
          <el-button @click="handleRefresh">
            <i class="el-icon-refresh"></i> 刷新
          </el-button>
        </el-col>
      </el-row>

      <el-table :data="paginatedAppointmentList" border stripe style="width: 100%;">
        <el-table-column type="index" label="序号" width="60" align="center"></el-table-column>
        <el-table-column prop="ownerName" label="宠物主人" width="120"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130"></el-table-column>
        <el-table-column prop="petName" label="宠物名称" width="120"></el-table-column>
        <el-table-column prop="petType" label="宠物类型" width="100"></el-table-column>
        <el-table-column prop="beauticianName" label="美容师" width="110">
          <template slot-scope="scope">
            <span>{{ scope.row.beauticianName || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="appointmentDate" label="预约日期" width="120"></el-table-column>
        <el-table-column prop="appointmentTime" label="预约时段" width="120"></el-table-column>
        <el-table-column prop="servicePackage" label="服务项目" min-width="180">
          <template slot-scope="scope">
            <el-tag size="small" v-for="(item, index) in scope.row.servicePackage" :key="index" style="margin: 2px;">
              {{ item }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="createTime" label="创建时间" width="160"></el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template slot-scope="scope">
            <el-button size="small" type="success" @click="handleStartService(scope.row)" v-if="scope.row.status === '待服务'">
              开始服务
            </el-button>
            <el-button size="small" type="primary" @click="handleComplete(scope.row)" v-if="scope.row.status === '服务中'">
              完成服务
            </el-button>
            <el-button size="small" type="warning" @click="goToCheckout(scope.row)" v-if="scope.row.status === '已完成'">
              去结算
            </el-button>
            <el-button size="small" type="info" @click="handleView(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="handleCancel(scope.$index)" v-if="scope.row.status === '待服务'">取消</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        style="margin-top: 20px; text-align: right;"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="filteredAppointmentList.length"
      ></el-pagination>
    </div>

    <el-dialog
      title="预约详情"
      :visible.sync="viewDialogVisible"
      width="600px"
    >
      <el-descriptions :column="2" border>
        <el-descriptions-item label="宠物主人">{{ currentAppointment.ownerName }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentAppointment.phone }}</el-descriptions-item>
        <el-descriptions-item label="宠物名称">{{ currentAppointment.petName }}</el-descriptions-item>
        <el-descriptions-item label="宠物类型">{{ currentAppointment.petType }}</el-descriptions-item>
        <el-descriptions-item label="宠物性别">{{ currentAppointment.petGender }}</el-descriptions-item>
        <el-descriptions-item label="宠物体重">{{ currentAppointment.petWeight }}kg</el-descriptions-item>
        <el-descriptions-item label="预约日期">{{ currentAppointment.appointmentDate }}</el-descriptions-item>
        <el-descriptions-item label="预约时段">{{ currentAppointment.appointmentTime }}</el-descriptions-item>
        <el-descriptions-item label="美容师">{{ currentAppointment.beauticianName || '-' }}</el-descriptions-item>
        <el-descriptions-item label="是否会员">{{ currentAppointment.isMember ? '是' : '否' }}</el-descriptions-item>
        <el-descriptions-item label="会员卡号" v-if="currentAppointment.isMember">{{ currentAppointment.memberCardNo }}</el-descriptions-item>
        <el-descriptions-item label="服务项目" :span="2">
          <el-tag size="small" v-for="(item, index) in currentAppointment.servicePackage" :key="index" style="margin: 2px;">
            {{ item }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="特殊要求" :span="2">{{ currentAppointment.specialRequirements || '无' }}</el-descriptions-item>
        <el-descriptions-item label="预约状态">
          <el-tag :type="getStatusType(currentAppointment.status)">{{ currentAppointment.status }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ currentAppointment.createTime }}</el-descriptions-item>
      </el-descriptions>
      <div slot="footer" class="dialog-footer">
        <el-button @click="viewDialogVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'AppointmentList',
  data() {
    return {
      searchKey: '',
      searchStatus: '',
      searchPetType: '',
      searchDate: '',
      currentPage: 1,
      pageSize: 10,
      viewDialogVisible: false,
      currentAppointment: {},
      appointmentList: []
    }
  },
  created() {
    this.loadAppointmentList()
    window.addEventListener('storage', this.handleStorageChange)
  },
  beforeDestroy() {
    window.removeEventListener('storage', this.handleStorageChange)
  },
  methods: {
    loadAppointmentList() {
      const defaultAppointments = [
        {
          id: 1,
          ownerName: '张三',
          phone: '13800138001',
          petName: '豆豆',
          petType: '小型犬',
          petGender: '公',
          petWeight: 5.5,
          beautician: 1,
          beauticianName: '张美容师',
          appointmentDate: '2024-05-16',
          appointmentTime: '10:00-11:00',
          servicePackage: ['基础洗护套餐', '精致洗护套餐'],
          specialRequirements: '宠物有点怕水，请温柔一点',
          isMember: true,
          memberCardNo: 'VIP20240001',
          status: '待服务',
          createTime: '2024-05-15 14:30:00'
        },
        {
          id: 2,
          ownerName: '李四',
          phone: '13800138002',
          petName: '咪咪',
          petType: '猫咪',
          petGender: '母',
          petWeight: 3.2,
          beautician: 2,
          beauticianName: '李美容师',
          appointmentDate: '2024-05-16',
          appointmentTime: '14:00-15:00',
          servicePackage: ['猫咪专属套餐'],
          specialRequirements: '',
          isMember: true,
          memberCardNo: 'VIP20240002',
          status: '服务中',
          createTime: '2024-05-15 16:20:00'
        },
        {
          id: 3,
          ownerName: '王五',
          phone: '13800138003',
          petName: '旺财',
          petType: '中型犬',
          petGender: '公',
          petWeight: 15.0,
          beautician: 3,
          beauticianName: '王美容师',
          appointmentDate: '2024-05-15',
          appointmentTime: '09:00-10:00',
          servicePackage: ['豪华美容套餐'],
          specialRequirements: '需要做造型',
          isMember: true,
          memberCardNo: 'VIP20240003',
          status: '已完成',
          createTime: '2024-05-14 10:10:00'
        },
        {
          id: 4,
          ownerName: '赵六',
          phone: '13800138004',
          petName: '毛球',
          petType: '大型犬',
          petGender: '公',
          petWeight: 28.5,
          beautician: 4,
          beauticianName: '赵美容师',
          appointmentDate: '2024-05-17',
          appointmentTime: '15:00-16:00',
          servicePackage: ['大型犬洗护'],
          specialRequirements: '毛发比较厚，请仔细清洗',
          isMember: false,
          memberCardNo: '',
          status: '待服务',
          createTime: '2024-05-15 09:45:00'
        },
        {
          id: 5,
          ownerName: '孙七',
          phone: '13800138005',
          petName: '小白',
          petType: '小型犬',
          petGender: '母',
          petWeight: 4.0,
          beautician: 1,
          beauticianName: '张美容师',
          appointmentDate: '2024-05-14',
          appointmentTime: '11:00-12:00',
          servicePackage: ['医疗洗护套餐'],
          specialRequirements: '皮肤敏感，使用药用香波',
          isMember: true,
          memberCardNo: 'VIP20240005',
          status: '已取消',
          createTime: '2024-05-13 15:30:00'
        }
      ]
      const localList = JSON.parse(localStorage.getItem('appointments') || '[]')
      if (localList.length > 0) {
        this.appointmentList = [...localList, ...defaultAppointments]
      } else {
        this.appointmentList = defaultAppointments
      }
    },
    handleStorageChange(e) {
      if (e.key === 'appointments') {
        this.loadAppointmentList()
      }
    },
    saveAppointmentList() {
      localStorage.setItem('appointments', JSON.stringify(this.appointmentList))
    },
    getStatusType(status) {
      const typeMap = {
        '待服务': 'warning',
        '服务中': 'primary',
        '已完成': 'success',
        '已取消': 'info'
      }
      return typeMap[status] || ''
    },
    goToAppointment() {
      this.$router.push('/appointment')
    },
    handleRefresh() {
      this.searchKey = ''
      this.searchStatus = ''
      this.searchPetType = ''
      this.searchDate = ''
      this.currentPage = 1
      this.loadAppointmentList()
      this.$message.success('刷新成功')
    },
    handleStartService(row) {
      this.$confirm('确定要开始服务吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'primary'
      }).then(() => {
        row.status = '服务中'
        this.saveAppointmentList()
        this.$message.success('已开始服务')
      }).catch(() => {})
    },
    handleComplete(row) {
      this.$confirm('确定要完成服务吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'success'
      }).then(() => {
        row.status = '已完成'
        this.saveAppointmentList()
        this.$message.success('服务已完成')
      }).catch(() => {})
    },
    goToCheckout(row) {
      this.$router.push({
        path: '/checkout',
        query: { appointmentId: row.id }
      })
    },
    handleView(row) {
      this.currentAppointment = { ...row }
      this.viewDialogVisible = true
    },
    handleCancel(index) {
      this.$confirm('确定要取消该预约吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.appointmentList[index].status = '已取消'
        this.saveAppointmentList()
        this.$message.success('预约已取消')
      }).catch(() => {})
    },
    handleSizeChange(size) {
      this.pageSize = size
      this.currentPage = 1
    },
    handleCurrentChange(page) {
      this.currentPage = page
    }
  },
  computed: {
    filteredAppointmentList() {
      let list = this.appointmentList
      
      if (this.searchKey) {
        const key = this.searchKey.toLowerCase()
        list = list.filter(item => 
          (item.ownerName && item.ownerName.includes(key)) || 
          (item.phone && item.phone.includes(key)) ||
          (item.petName && item.petName.includes(key))
        )
      }
      if (this.searchStatus) {
        list = list.filter(item => item.status === this.searchStatus)
      }
      if (this.searchPetType) {
        list = list.filter(item => item.petType === this.searchPetType)
      }
      if (this.searchDate) {
        list = list.filter(item => item.appointmentDate === this.searchDate)
      }
      return list
    },
    paginatedAppointmentList() {
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      return this.filteredAppointmentList.slice(start, end)
    }
  }
}
</script>

<style scoped>
</style>
