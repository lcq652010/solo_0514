<template>
  <div class="page-container">
    <h2 class="page-title">维修派单</h2>
    
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="所属楼栋">
        <el-select v-model="searchForm.building" placeholder="请选择" clearable>
          <el-option v-for="item in buildingOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="报修类型">
        <el-select v-model="searchForm.type" placeholder="请选择" clearable>
          <el-option v-for="item in repairTypes" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="search">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </el-form-item>
    </el-form>
    
    <el-tabs v-model="activeTab" @tab-click="handleTabClick">
      <el-tab-pane label="待派单" name="pending">
        <div class="table-container">
          <el-table :data="filteredPendingList" border style="width: 100%" v-loading="loading">
            <el-table-column type="selection" width="55" align="center"></el-table-column>
            <el-table-column prop="id" label="报修编号" width="100" align="center"></el-table-column>
            <el-table-column prop="title" label="报修标题" min-width="150"></el-table-column>
            <el-table-column prop="buildingName" label="所属楼栋" width="90" align="center"></el-table-column>
            <el-table-column prop="typeName" label="报修类型" width="100" align="center"></el-table-column>
            <el-table-column prop="urgencyName" label="紧急程度" width="100" align="center">
              <template slot-scope="scope">
                <el-tag :type="getUrgencyTagType(scope.row.urgency)" size="small">{{ scope.row.urgencyName }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="address" label="地址" min-width="150"></el-table-column>
            <el-table-column prop="contact" label="联系人" width="90" align="center"></el-table-column>
            <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
            <el-table-column prop="createTime" label="提交时间" width="160" align="center"></el-table-column>
            <el-table-column label="操作" width="120" align="center" fixed="right">
              <template slot-scope="scope">
                <el-button type="primary" size="mini" @click="openDispatchDialog(scope.row)">派单</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="已派单" name="dispatched">
        <div class="table-container">
          <el-table :data="filteredDispatchedList" border style="width: 100%" v-loading="loading">
            <el-table-column prop="id" label="报修编号" width="100" align="center"></el-table-column>
            <el-table-column prop="title" label="报修标题" min-width="150"></el-table-column>
            <el-table-column prop="buildingName" label="所属楼栋" width="90" align="center"></el-table-column>
            <el-table-column prop="typeName" label="报修类型" width="100" align="center"></el-table-column>
            <el-table-column prop="worker" label="维修人员" width="100" align="center"></el-table-column>
            <el-table-column prop="workerPhone" label="维修电话" width="120" align="center"></el-table-column>
            <el-table-column prop="status" label="状态" width="100" align="center">
              <template slot-scope="scope">
                <el-tag :color="getStatusColor(scope.row.status)" size="small">{{ getStatusLabel(scope.row.status) }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="dispatchTime" label="派单时间" width="160" align="center"></el-table-column>
            <el-table-column label="操作" width="120" align="center" fixed="right">
              <template slot-scope="scope">
                <el-button type="info" size="mini" @click="viewDetail(scope.row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog title="派单" :visible.sync="dispatchDialogVisible" width="500px">
      <el-form :model="dispatchForm" label-width="100px">
        <el-form-item label="报修编号">
          <span>{{ dispatchForm.id }}</span>
        </el-form-item>
        <el-form-item label="报修标题">
          <span>{{ dispatchForm.title }}</span>
        </el-form-item>
        <el-form-item label="维修人员" prop="workerId">
          <el-select v-model="dispatchForm.workerId" placeholder="请选择维修人员" style="width: 100%">
            <el-option v-for="worker in workers" :key="worker.id" :label="worker.name + ' (' + worker.skill + ')'" :value="worker.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="dispatchForm.remark" :rows="3" placeholder="请输入派单备注"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dispatchDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmDispatch">确认派单</el-button>
      </span>
    </el-dialog>

    <el-dialog title="报修详情" :visible.sync="detailDialogVisible" width="600px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="报修编号">{{ currentDetail.id }}</el-descriptions-item>
        <el-descriptions-item label="报修标题">{{ currentDetail.title }}</el-descriptions-item>
        <el-descriptions-item label="所属楼栋">{{ currentDetail.buildingName }}</el-descriptions-item>
        <el-descriptions-item label="报修类型">{{ currentDetail.typeName }}</el-descriptions-item>
        <el-descriptions-item label="紧急程度">{{ currentDetail.urgencyName }}</el-descriptions-item>
        <el-descriptions-item label="问题描述">{{ currentDetail.description }}</el-descriptions-item>
        <el-descriptions-item label="维修地址">{{ currentDetail.address }}</el-descriptions-item>
        <el-descriptions-item label="联系人">{{ currentDetail.contact }}</el-descriptions-item>
        <el-descriptions-item label="联系电话">{{ currentDetail.phone }}</el-descriptions-item>
        <el-descriptions-item label="维修人员" v-if="currentDetail.worker">{{ currentDetail.worker }}</el-descriptions-item>
        <el-descriptions-item label="维修电话" v-if="currentDetail.workerPhone">{{ currentDetail.workerPhone }}</el-descriptions-item>
        <el-descriptions-item label="提交时间">{{ currentDetail.createTime }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script>
import { statusOptions, workers, buildingOptions, repairTypes } from '../mock/data'
import { RepairStore } from '../store/repairStore'
import { EventBus, Events } from '../utils/eventBus'

export default {
  name: 'Dispatch',
  data() {
    return {
      statusOptions,
      workers,
      buildingOptions,
      repairTypes,
      activeTab: 'pending',
      loading: false,
      dispatchDialogVisible: false,
      detailDialogVisible: false,
      searchForm: {
        building: '',
        type: ''
      },
      dispatchForm: {
        id: '',
        title: '',
        workerId: '',
        remark: ''
      },
      currentDetail: {}
    }
  },
  computed: {
    repairList() {
      return RepairStore.getRepairList()
    },
    pendingList() {
      return this.repairList.filter(item => item.status === '0')
    },
    dispatchedList() {
      return this.repairList.filter(item => item.status !== '0')
    },
    filteredPendingList() {
      let list = [...this.pendingList]
      if (this.searchForm.building) {
        list = list.filter(item => item.building === this.searchForm.building)
      }
      if (this.searchForm.type) {
        list = list.filter(item => item.type === this.searchForm.type)
      }
      return list
    },
    filteredDispatchedList() {
      let list = [...this.dispatchedList]
      if (this.searchForm.building) {
        list = list.filter(item => item.building === this.searchForm.building)
      }
      if (this.searchForm.type) {
        list = list.filter(item => item.type === this.searchForm.type)
      }
      return list
    }
  },
  mounted() {
    this.listenToStatusUpdates()
  },
  beforeDestroy() {
    EventBus.$off(Events.REPAIR_STATUS_UPDATED)
    EventBus.$off(Events.REPAIR_CREATED)
  },
  methods: {
    listenToStatusUpdates() {
      EventBus.$on(Events.REPAIR_STATUS_UPDATED, (data) => {
        this.$message.info(`报修单 ${data.id} 状态已更新为：${RepairStore.getStatusLabel(data.status)}`)
      })
      
      EventBus.$on(Events.REPAIR_CREATED, (newRepair) => {
        this.$message.success(`收到新报修单：${newRepair.title}`)
      })
    },
    handleTabClick(tab, event) {
      console.log(tab, event)
    },
    getStatusLabel(status) {
      return RepairStore.getStatusLabel(status)
    },
    getStatusColor(status) {
      return RepairStore.getStatusColor(status)
    },
    getUrgencyTagType(urgency) {
      const map = { '1': '', '2': 'warning', '3': 'danger' }
      return map[urgency] || ''
    },
    openDispatchDialog(row) {
      this.dispatchForm = {
        id: row.id,
        title: row.title,
        workerId: '',
        remark: ''
      }
      this.dispatchDialogVisible = true
    },
    confirmDispatch() {
      if (!this.dispatchForm.workerId) {
        this.$message.warning('请选择维修人员')
        return
      }
      const worker = this.workers.find(w => w.id === this.dispatchForm.workerId)
      const result = RepairStore.dispatchRepair(
        this.dispatchForm.id, 
        worker.name, 
        worker.phone
      )
      
      if (result) {
        this.$message.success('派单成功！')
        this.dispatchDialogVisible = false
      }
    },
    viewDetail(row) {
      this.currentDetail = { ...row }
      this.detailDialogVisible = true
    },
    search() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
      }, 300)
    },
    resetSearch() {
      this.searchForm = {
        building: '',
        type: ''
      }
    }
  }
}
</script>

<style scoped>
.search-form {
  background: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  margin-bottom: 20px;
}
</style>
