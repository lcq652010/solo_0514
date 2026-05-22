<template>
  <div id="app">
    <div class="header">
      <h1>水务营业厅自助查缴打印终端运维管理系统</h1>
    </div>
    
    <div class="container">
      <div class="search-bar">
        <el-input 
          v-model="searchKeyword" 
          placeholder="请输入设备编号或营业厅名称" 
          style="width: 300px; margin-right: 10px;"
          clearable
          @clear="handleSearch"
        ></el-input>
        <el-button type="primary" @click="handleSearch">搜索</el-button>
        <el-button type="success" @click="openReportDialog" style="margin-left: 10px;">故障上报</el-button>
      </div>

      <el-table :data="filteredDevices" style="width: 100%" border>
        <el-table-column prop="deviceId" label="设备编号" width="150"></el-table-column>
        <el-table-column prop="hallName" label="营业厅名称" width="200"></el-table-column>
        <el-table-column prop="location" label="安装位置" width="250"></el-table-column>
        <el-table-column prop="status" label="设备状态" width="120">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)" size="medium">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template slot-scope="scope">
            <el-button type="text" size="small" @click="reportDeviceFault(scope.row)">
              故障上报
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
        </el-pagination>
      </div>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="dialogVisible"
      width="500px"
      @close="resetForm"
    >
      <el-form :model="reportForm" :rules="rules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderId" disabled></el-input>
        </el-form-item>
        <el-form-item label="选择设备" prop="deviceId">
          <el-select v-model="reportForm.deviceId" placeholder="请选择设备" style="width: 100%;">
            <el-option
              v-for="device in devices"
              :key="device.deviceId"
              :label="`${device.deviceId} - ${device.hallName}`"
              :value="device.deviceId">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="故障描述" prop="faultDescription">
          <el-input
            type="textarea"
            v-model="reportForm.faultDescription"
            :rows="4"
            placeholder="请详细描述故障情况">
          </el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitReport">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      searchKeyword: '',
      currentPage: 1,
      pageSize: 10,
      dialogVisible: false,
      reportForm: {
        orderId: '',
        deviceId: '',
        faultDescription: ''
      },
      rules: {
        deviceId: [
          { required: true, message: '请选择设备', trigger: 'change' }
        ],
        faultDescription: [
          { required: true, message: '请输入故障描述', trigger: 'blur' },
          { min: 5, message: '故障描述不能少于5个字', trigger: 'blur' }
        ]
      },
      devices: [
        { deviceId: 'W2024001', hallName: '城东营业厅', location: '一楼大厅入口右侧', status: '正常' },
        { deviceId: 'W2024002', hallName: '城东营业厅', location: '二楼服务区', status: '故障' },
        { deviceId: 'W2024003', hallName: '城西营业厅', location: '大厅服务台旁', status: '正常' },
        { deviceId: 'W2024004', hallName: '城西营业厅', location: '24小时自助服务区', status: '离线' },
        { deviceId: 'W2024005', hallName: '城南营业厅', location: '一楼大堂', status: '维护中' },
        { deviceId: 'W2024006', hallName: '城南营业厅', location: '二楼缴费区', status: '正常' },
        { deviceId: 'W2024007', hallName: '城北营业厅', location: '正门入口左侧', status: '正常' },
        { deviceId: 'W2024008', hallName: '城北营业厅', location: 'VIP服务区', status: '故障' },
        { deviceId: 'W2024009', hallName: '中心营业厅', location: '自助服务区A区', status: '正常' },
        { deviceId: 'W2024010', hallName: '中心营业厅', location: '自助服务区B区', status: '离线' },
        { deviceId: 'W2024011', hallName: '开发区营业厅', location: '一楼大厅', status: '正常' },
        { deviceId: 'W2024012', hallName: '开发区营业厅', location: '二楼办公区', status: '维护中' },
        { deviceId: 'W2024013', hallName: '高新区营业厅', location: '服务大厅', status: '正常' },
        { deviceId: 'W2024014', hallName: '高新区营业厅', location: '企业服务区', status: '故障' },
        { deviceId: 'W2024015', hallName: '滨江营业厅', location: '一楼入口处', status: '正常' }
      ],
      orderCounter: 1
    }
  },
  computed: {
    filteredDevices() {
      let result = this.devices;
      
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase();
        result = result.filter(device => 
          device.deviceId.toLowerCase().includes(keyword) || 
          device.hallName.toLowerCase().includes(keyword)
        );
      }
      
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return result.slice(start, end);
    },
    total() {
      let result = this.devices;
      
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase();
        result = result.filter(device => 
          device.deviceId.toLowerCase().includes(keyword) || 
          device.hallName.toLowerCase().includes(keyword)
        );
      }
      
      return result.length;
    }
  },
  methods: {
    getStatusType(status) {
      const statusMap = {
        '正常': 'success',
        '故障': 'danger',
        '离线': 'info',
        '维护中': 'warning'
      };
      return statusMap[status] || 'info';
    },
    handleSearch() {
      this.currentPage = 1;
    },
    handleSizeChange(val) {
      this.pageSize = val;
    },
    handleCurrentChange(val) {
      this.currentPage = val;
    },
    generateOrderId() {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const counter = String(this.orderCounter).padStart(4, '0');
      return `GD${year}${month}${day}${counter}`;
    },
    openReportDialog() {
      this.reportForm.orderId = this.generateOrderId();
      this.dialogVisible = true;
    },
    reportDeviceFault(device) {
      this.reportForm.orderId = this.generateOrderId();
      this.reportForm.deviceId = device.deviceId;
      this.dialogVisible = true;
    },
    resetForm() {
      this.$refs.reportForm.resetFields();
      this.reportForm.faultDescription = '';
    },
    submitReport() {
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$message({
            type: 'success',
            message: `工单 ${this.reportForm.orderId} 提交成功！`
          });
          this.orderCounter++;
          this.dialogVisible = false;
          this.resetForm();
        }
      });
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  background-color: #f5f7fa;
}

#app {
  min-height: 100vh;
}

.header {
  background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%);
  color: white;
  padding: 20px 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  font-size: 24px;
  font-weight: 500;
}

.container {
  padding: 30px 40px;
}

.search-bar {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
