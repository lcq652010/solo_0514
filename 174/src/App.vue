<template>
  <div id="app">
    <div class="header">
      <h1>水务自助缴费清单打印终端运维管理系统</h1>
    </div>
    
    <div class="container">
      <el-card class="search-card">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="设备编号">
            <el-input v-model="searchForm.deviceCode" placeholder="请输入设备编号"></el-input>
          </el-form-item>
          <el-form-item label="服务厅名称">
            <el-input v-model="searchForm.serviceHall" placeholder="请输入服务厅名称"></el-input>
          </el-form-item>
          <el-form-item label="设备状态">
            <el-select v-model="searchForm.status" placeholder="全部状态" clearable>
              <el-option label="正常" value="normal"></el-option>
              <el-option label="故障" value="fault"></el-option>
              <el-option label="维护中" value="maintenance"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">搜索</el-button>
            <el-button @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <el-card class="table-card">
        <div class="table-header">
          <span class="table-title">设备列表</span>
          <el-button type="danger" @click="handleReport">故障上报</el-button>
        </div>
        
        <el-table
          ref="deviceTable"
          :data="tableData"
          border
          stripe
          :row-class-name="getRowClassName"
          @selection-change="handleSelectionChange"
          style="width: 100%">
          <el-table-column type="selection" width="55"></el-table-column>
          <el-table-column prop="deviceCode" label="设备编号" width="130" align="center"></el-table-column>
          <el-table-column prop="serviceHall" label="供水服务厅" min-width="140" align="center"></el-table-column>
          <el-table-column prop="location" label="具体点位" min-width="160" align="center"></el-table-column>
          <el-table-column prop="status" label="设备状态" width="100" align="center">
            <template slot-scope="scope">
              <el-tag :type="getStatusType(scope.row.status)" size="small">
                {{ getStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="读卡模块" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.cardReader ? 'success' : 'danger'" size="mini">
                {{ scope.row.cardReader ? '正常' : '异常' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="清单打印" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.printer ? 'success' : 'danger'" size="mini">
                {{ scope.row.printer ? '正常' : '异常' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="网络通信" width="110" align="center">
            <template slot-scope="scope">
              <el-tag :type="scope.row.network ? 'success' : 'danger'" size="mini">
                {{ scope.row.network ? '正常' : '异常' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="130" align="center">
            <template slot-scope="scope">
              <el-button size="mini" type="text" @click="handleReportSingle(scope.row)">故障上报</el-button>
            </template>
          </el-table-column>
        </el-table>

        <div class="pagination">
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="pagination.currentPage"
            :page-sizes="[10, 20, 30, 50]"
            :page-size="pagination.pageSize"
            layout="total, sizes, prev, pager, next, jumper"
            :total="pagination.total">
          </el-pagination>
        </div>
      </el-card>
    </div>

    <el-dialog
      title="故障上报"
      :visible.sync="dialogVisible"
      width="600px"
      @close="handleDialogClose">
      <el-form :model="reportForm" :rules="reportRules" ref="reportForm" label-width="100px">
        <el-form-item label="工单编号">
          <el-input v-model="reportForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="设备编号" prop="deviceCode">
          <el-select v-model="reportForm.deviceCode" placeholder="请选择设备" style="width: 100%" filterable>
            <el-option
              v-for="device in abnormalDevices"
              :key="device.deviceCode"
              :label="device.deviceCode + ' - ' + device.serviceHall + ' (' + getStatusText(device.status) + ')'"
              :value="device.deviceCode">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="问题说明" prop="problemDescription">
          <el-input
            type="textarea"
            v-model="reportForm.problemDescription"
            :rows="5"
            placeholder="请详细描述故障问题">
          </el-input>
        </el-form-item>
        <el-form-item label="上报时间">
          <el-input v-model="reportForm.reportTime" disabled></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    abnormalDevices() {
      return this.allDevices.filter(device => 
        device.status === 'fault' || device.status === 'maintenance'
      );
    }
  },
  data() {
    return {
      searchForm: {
        deviceCode: '',
        serviceHall: '',
        status: ''
      },
      allDevices: [],
      tableData: [],
      selectedDevices: [],
      currentFilteredData: [],
      pagination: {
        currentPage: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      reportForm: {
        orderNo: '',
        deviceCode: '',
        problemDescription: '',
        reportTime: ''
      },
      reportRules: {
        deviceCode: [
          { required: true, message: '请选择设备', trigger: 'change' },
          { validator: this.validateDeviceStatus, trigger: 'change' }
        ],
        problemDescription: [
          { required: true, message: '请填写问题说明', trigger: 'blur' },
          { min: 10, message: '问题说明至少10个字符，请详细描述故障情况', trigger: 'blur' },
          { max: 500, message: '问题说明不能超过500个字符', trigger: 'blur' },
          { validator: this.validateDescription, trigger: 'blur' }
        ]
      },
      mockData: [
        { deviceCode: 'WATER-001', serviceHall: '东区供水服务厅', location: '一楼大厅入口右侧', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-002', serviceHall: '东区供水服务厅', location: '二楼业务办理区', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-003', serviceHall: '西区供水服务厅', location: '服务大厅左侧', status: 'fault', cardReader: false, printer: true, network: true },
        { deviceCode: 'WATER-004', serviceHall: '西区供水服务厅', location: '24小时自助服务区', status: 'maintenance', cardReader: true, printer: true, network: false },
        { deviceCode: 'WATER-005', serviceHall: '南区供水服务厅', location: '大门入口处', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-006', serviceHall: '南区供水服务厅', location: '业务窗口旁', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-007', serviceHall: '北区供水服务厅', location: '自助缴费区1号位', status: 'fault', cardReader: true, printer: false, network: true },
        { deviceCode: 'WATER-008', serviceHall: '北区供水服务厅', location: '自助缴费区2号位', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-009', serviceHall: '中心供水服务厅', location: '一楼大堂A区', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-010', serviceHall: '中心供水服务厅', location: '一楼大堂B区', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-011', serviceHall: '中心供水服务厅', location: '二楼西侧', status: 'maintenance', cardReader: true, printer: false, network: true },
        { deviceCode: 'WATER-012', serviceHall: '开发区供水服务厅', location: '服务中心大厅', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-013', serviceHall: '开发区供水服务厅', location: '企业服务区', status: 'fault', cardReader: false, printer: false, network: true },
        { deviceCode: 'WATER-014', serviceHall: '高新区供水服务厅', location: '政务中心一楼', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-015', serviceHall: '高新区供水服务厅', location: '政务中心二楼', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-016', serviceHall: '滨海新区供水服务厅', location: '便民服务点A', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-017', serviceHall: '滨海新区供水服务厅', location: '便民服务点B', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-018', serviceHall: '老城区供水服务厅', location: '营业厅门口', status: 'fault', cardReader: true, printer: true, network: false },
        { deviceCode: 'WATER-019', serviceHall: '老城区供水服务厅', location: '缴费窗口旁', status: 'normal', cardReader: true, printer: true, network: true },
        { deviceCode: 'WATER-020', serviceHall: '新城区供水服务厅', location: '市民广场东侧', status: 'normal', cardReader: true, printer: true, network: true }
      ]
    };
  },
  created() {
    this.initData();
  },
  methods: {
    initData() {
      this.allDevices = [...this.mockData];
      this.handleSearch();
    },
    getStatusType(status) {
      const statusMap = {
        normal: 'success',
        fault: 'danger',
        maintenance: 'warning'
      };
      return statusMap[status] || 'info';
    },
    getStatusText(status) {
      const statusMap = {
        normal: '正常',
        fault: '故障',
        maintenance: '维护中'
      };
      return statusMap[status] || '未知';
    },
    getRowClassName({ row }) {
      if (row.status === 'fault') {
        return 'fault-row';
      } else if (row.status === 'maintenance') {
        return 'maintenance-row';
      }
      return '';
    },
    validateDeviceStatus(rule, value, callback) {
      if (value) {
        const device = this.allDevices.find(d => d.deviceCode === value);
        if (device && device.status === 'normal') {
          callback(new Error('该设备状态正常，无需上报故障'));
        } else {
          callback();
        }
      } else {
        callback();
      }
    },
    validateDescription(rule, value, callback) {
      if (value) {
        const invalidKeywords = ['测试', 'test', '随便', '暂无', '不知道'];
        const hasInvalidKeyword = invalidKeywords.some(keyword => 
          value.toLowerCase().includes(keyword)
        );
        if (hasInvalidKeyword) {
          callback(new Error('问题说明不能包含无效描述，请详细描述真实故障情况'));
          return;
        }
        const validPattern = /[\u4e00-\u9fa5a-zA-Z]{5,}/;
        if (!validPattern.test(value)) {
          callback(new Error('请使用有效字符描述故障情况'));
          return;
        }
        callback();
      } else {
        callback();
      }
    },
    handleSearch() {
      let filteredData = [...this.allDevices];
      
      if (this.searchForm.deviceCode && this.searchForm.deviceCode.trim()) {
        const keyword = this.searchForm.deviceCode.trim().toLowerCase();
        filteredData = filteredData.filter(item => 
          item.deviceCode.toLowerCase().includes(keyword)
        );
      }
      
      if (this.searchForm.serviceHall && this.searchForm.serviceHall.trim()) {
        const keyword = this.searchForm.serviceHall.trim();
        filteredData = filteredData.filter(item => 
          item.serviceHall.includes(keyword)
        );
      }
      
      if (this.searchForm.status) {
        filteredData = filteredData.filter(item => 
          item.status === this.searchForm.status
        );
      }
      
      this.pagination.total = filteredData.length;
      this.currentFilteredData = filteredData;
      this.updateTableData();
    },
    handleReset() {
      this.searchForm = {
        deviceCode: '',
        serviceHall: '',
        status: ''
      };
      this.pagination.currentPage = 1;
      this.handleSearch();
    },
    updateTableData() {
      const filteredData = this.currentFilteredData || this.allDevices;
      const start = (this.pagination.currentPage - 1) * this.pagination.pageSize;
      const end = start + this.pagination.pageSize;
      this.tableData = filteredData.slice(start, end);
    },
    handleSizeChange(val) {
      this.pagination.pageSize = val;
      this.pagination.currentPage = 1;
      this.updateTableData();
    },
    handleCurrentChange(val) {
      this.pagination.currentPage = val;
      this.updateTableData();
    },
    handleSelectionChange(selection) {
      this.selectedDevices = selection;
    },
    handleReport() {
      if (this.selectedDevices.length === 0) {
        this.$message.warning('请先选择要上报的设备');
        return;
      }
      if (this.selectedDevices.length > 1) {
        this.$message.warning('每次只能上报一台设备');
        return;
      }
      this.openDialog(this.selectedDevices[0].deviceCode);
    },
    handleReportSingle(row) {
      this.openDialog(row.deviceCode);
    },
    openDialog(deviceCode) {
      this.reportForm.orderNo = this.generateOrderNo();
      this.reportForm.deviceCode = deviceCode;
      this.reportForm.problemDescription = '';
      this.reportForm.reportTime = this.getCurrentTime();
      this.dialogVisible = true;
    },
    generateOrderNo() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0');
      return `WO${year}${month}${day}${hours}${minutes}${seconds}${random}`;
    },
    getCurrentTime() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      const hours = String(now.getHours()).padStart(2, '0');
      const minutes = String(now.getMinutes()).padStart(2, '0');
      const seconds = String(now.getSeconds()).padStart(2, '0');
      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },
    handleDialogClose() {
      this.$refs.reportForm.resetFields();
    },
    handleSubmit() {
      if (!this.reportForm.deviceCode) {
        this.$message.error('请先选择要上报的设备！');
        return;
      }
      this.$refs.reportForm.validate((valid) => {
        if (valid) {
          this.$message.success('故障上报成功！工单编号：' + this.reportForm.orderNo);
          this.dialogVisible = false;
          this.$refs.deviceTable.clearSelection();
        }
      });
    }
  }
};
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
  padding: 20px 40px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.header h1 {
  color: #fff;
  font-size: 24px;
  font-weight: 500;
}

.container {
  padding: 20px 40px;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
}

.table-card {
  background: #fff;
  border-radius: 4px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.table-title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}

.dialog-footer {
  text-align: right;
}

.el-table .fault-row {
  background-color: #fef0f0 !important;
}

.el-table .fault-row:hover > td {
  background-color: #fde2e2 !important;
}

.el-table .maintenance-row {
  background-color: #fdf6ec !important;
}

.el-table .maintenance-row:hover > td {
  background-color: #faecd8 !important;
}

.el-table .fault-row td,
.el-table .maintenance-row td {
  background-color: inherit !important;
}
</style>