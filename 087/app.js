Vue.use(ELEMENT);

new Vue({
    el: '#app',
    data: function() {
        return {
            searchDeviceNo: '',
            searchCommunity: '',
            currentPage: 1,
            pageSize: 10,
            total: 0,
            deviceList: [],
            dialogVisible: false,
            faultForm: {
                deviceId: '',
                deviceNo: '',
                description: ''
            },
            rules: {
                deviceId: [
                    { required: true, message: '请选择设备', trigger: 'change' }
                ],
                description: [
                    { required: true, message: '请填写故障描述', trigger: 'blur' },
                    { min: 5, message: '故障描述至少5个字符', trigger: 'blur' }
                ]
            },
            searchStatus: '',
            mockDevices: [
                { id: 1, deviceNo: 'SZ-2024-001', community: '朝阳区第一社区卫生服务中心', location: '门诊大厅入口处', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 08:30:00' },
                { id: 2, deviceNo: 'SZ-2024-002', community: '朝阳区第一社区卫生服务中心', location: '急诊楼一层', status: 'fault', cardReader: 'fault', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-15 14:20:00' },
                { id: 3, deviceNo: 'SZ-2024-003', community: '海淀区中关村社区卫生服务中心', location: '挂号收费处旁', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 09:15:00' },
                { id: 4, deviceNo: 'SZ-2024-004', community: '海淀区中关村社区卫生服务中心', location: '住院部大厅', status: 'offline', cardReader: 'offline', printer: 'offline', paymentModule: 'offline', lastOnline: '2024-05-14 16:45:00' },
                { id: 5, deviceNo: 'SZ-2024-005', community: '西城区德胜社区卫生服务中心', location: '主楼一层大厅', status: 'maintenance', cardReader: 'maintenance', printer: 'maintenance', paymentModule: 'maintenance', lastOnline: '2024-05-16 07:00:00' },
                { id: 6, deviceNo: 'SZ-2024-006', community: '西城区德胜社区卫生服务中心', location: '儿科门诊外', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 08:45:00' },
                { id: 7, deviceNo: 'SZ-2024-007', community: '东城区建国门社区卫生服务中心', location: '药房对面', status: 'normal', cardReader: 'normal', printer: 'fault', paymentModule: 'normal', lastOnline: '2024-05-16 09:00:00' },
                { id: 8, deviceNo: 'SZ-2024-008', community: '东城区建国门社区卫生服务中心', location: '二楼内科诊区', status: 'fault', cardReader: 'normal', printer: 'normal', paymentModule: 'fault', lastOnline: '2024-05-15 11:30:00' },
                { id: 9, deviceNo: 'SZ-2024-009', community: '丰台区方庄社区卫生服务中心', location: '正门入口左侧', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 08:00:00' },
                { id: 10, deviceNo: 'SZ-2024-010', community: '丰台区方庄社区卫生服务中心', location: '口腔科门外', status: 'offline', cardReader: 'offline', printer: 'offline', paymentModule: 'offline', lastOnline: '2024-05-13 09:20:00' },
                { id: 11, deviceNo: 'SZ-2024-011', community: '石景山八角社区卫生服务中心', location: '挂号大厅', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 08:30:00' },
                { id: 12, deviceNo: 'SZ-2024-012', community: '石景山八角社区卫生服务中心', location: '输液室旁', status: 'maintenance', cardReader: 'maintenance', printer: 'maintenance', paymentModule: 'maintenance', lastOnline: '2024-05-15 18:00:00' },
                { id: 13, deviceNo: 'SZ-2024-013', community: '通州区潞城社区卫生服务中心', location: '门诊楼一层', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 07:45:00' },
                { id: 14, deviceNo: 'SZ-2024-014', community: '通州区潞城社区卫生服务中心', location: '预防接种门诊', status: 'fault', cardReader: 'fault', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-14 15:30:00' },
                { id: 15, deviceNo: 'SZ-2024-015', community: '昌平区回龙观社区卫生服务中心', location: '主楼大厅中央', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 09:10:00' },
                { id: 16, deviceNo: 'SZ-2024-016', community: '昌平区回龙观社区卫生服务中心', location: '妇产科门诊外', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 08:55:00' },
                { id: 17, deviceNo: 'SZ-2024-017', community: '大兴区亦庄社区卫生服务中心', location: '急诊入口处', status: 'offline', cardReader: 'offline', printer: 'offline', paymentModule: 'offline', lastOnline: '2024-05-12 14:00:00' },
                { id: 18, deviceNo: 'SZ-2024-018', community: '大兴区亦庄社区卫生服务中心', location: '中医科诊区', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'normal', lastOnline: '2024-05-16 08:20:00' },
                { id: 19, deviceNo: 'SZ-2024-019', community: '顺义区空港社区卫生服务中心', location: '收费窗口旁', status: 'maintenance', cardReader: 'maintenance', printer: 'maintenance', paymentModule: 'maintenance', lastOnline: '2024-05-16 06:30:00' },
                { id: 20, deviceNo: 'SZ-2024-020', community: '顺义区空港社区卫生服务中心', location: '放射科外', status: 'normal', cardReader: 'normal', printer: 'normal', paymentModule: 'fault', lastOnline: '2024-05-16 09:05:00' }
            ],
            workOrders: []
        };
    },
    computed: {
        filteredDevices: function() {
            var self = this;
            return this.mockDevices.filter(function(item) {
                var matchDeviceNo = !self.searchDeviceNo || item.deviceNo.toLowerCase().includes(self.searchDeviceNo.toLowerCase());
                var matchCommunity = !self.searchCommunity || item.community.toLowerCase().includes(self.searchCommunity.toLowerCase());
                var matchStatus = !self.searchStatus || item.status === self.searchStatus;
                return matchDeviceNo && matchCommunity && matchStatus;
            });
        },
        stats: function() {
            var total = this.mockDevices.length;
            var normal = this.mockDevices.filter(function(d) { return d.status === 'normal'; }).length;
            var fault = this.mockDevices.filter(function(d) { return d.status === 'fault'; }).length;
            var maintenance = this.mockDevices.filter(function(d) { return d.status === 'maintenance'; }).length;
            return { total: total, normal: normal, fault: fault, maintenance: maintenance };
        },
        availableDevices: function() {
            return this.mockDevices.filter(function(item) {
                return item.status !== 'maintenance';
            });
        }
    },
    methods: {
        loadData: function() {
            var start = (this.currentPage - 1) * this.pageSize;
            var end = start + this.pageSize;
            this.deviceList = this.filteredDevices.slice(start, end);
            this.total = this.filteredDevices.length;
        },
        handleSearch: function() {
            this.currentPage = 1;
            this.loadData();
        },
        handleReset: function() {
            this.searchDeviceNo = '';
            this.searchCommunity = '';
            this.searchStatus = '';
            this.currentPage = 1;
            this.loadData();
        },
        handleSizeChange: function(val) {
            this.pageSize = val;
            this.loadData();
        },
        handleCurrentChange: function(val) {
            this.currentPage = val;
            this.loadData();
        },
        getStatusClass: function(status) {
            var statusMap = {
                'normal': 'status-normal',
                'fault': 'status-fault',
                'offline': 'status-offline',
                'maintenance': 'status-maintenance'
            };
            return statusMap[status] || '';
        },
        getStatusText: function(status) {
            var statusMap = {
                'normal': '正常',
                'fault': '故障',
                'offline': '离线',
                'maintenance': '维护中'
            };
            return statusMap[status] || status;
        },
        openFaultDialog: function(row) {
            this.$refs.faultForm.resetFields();
            this.faultForm.deviceId = row.id.toString();
            this.faultForm.deviceNo = row.deviceNo;
            this.faultForm.description = '';
            this.dialogVisible = true;
        },
        openNewFaultDialog: function() {
            this.$refs.faultForm.resetFields();
            this.faultForm.deviceId = '';
            this.faultForm.deviceNo = '';
            this.faultForm.description = '';
            this.dialogVisible = true;
        },
        generateWorkOrderNo: function() {
            var date = new Date();
            var year = date.getFullYear();
            var month = String(date.getMonth() + 1).padStart(2, '0');
            var day = String(date.getDate()).padStart(2, '0');
            var random = String(Math.floor(Math.random() * 10000)).padStart(4, '0');
            return 'WO' + year + month + day + random;
        },
        submitFault: function() {
            var self = this;
            this.$refs.faultForm.validate(function(valid) {
                if (valid) {
                    var workOrderNo = self.generateWorkOrderNo();
                    var workOrder = {
                        orderNo: workOrderNo,
                        deviceId: self.faultForm.deviceId,
                        deviceNo: self.faultForm.deviceNo,
                        description: self.faultForm.description,
                        createTime: new Date().toLocaleString('zh-CN'),
                        status: '待处理'
                    };
                    self.workOrders.push(workOrder);
                    
                    var device = self.mockDevices.find(function(d) {
                        return d.id === parseInt(self.faultForm.deviceId);
                    });
                    if (device) {
                        device.status = 'fault';
                    }
                    
                    self.dialogVisible = false;
                    self.$message({
                        type: 'success',
                        message: '故障上报成功！工单号：' + workOrderNo
                    });
                    self.loadData();
                } else {
                    return false;
                }
            });
        },
        handleDeviceChange: function(value) {
            var device = this.mockDevices.find(function(d) {
                return d.id === parseInt(value);
            });
            if (device) {
                this.faultForm.deviceNo = device.deviceNo;
            }
        },
        tableRowClassName: function(row) {
            if (row.row.status === 'fault') {
                return 'fault-row';
            } else if (row.row.status === 'offline') {
                return 'offline-row';
            }
            return '';
        }
    },
    mounted: function() {
        this.loadData();
    },
    template: `
        <div>
            <div class="header">
                <h1>🏥 社区医院自助缴费挂号终端运维管理系统</h1>
            </div>
            
            <div class="main-container">
                <div class="stats-cards">
                    <div class="stat-card total">
                        <h3>设备总数</h3>
                        <div class="stat-value">{{ stats.total }}</div>
                    </div>
                    <div class="stat-card normal">
                        <h3>正常运行</h3>
                        <div class="stat-value">{{ stats.normal }}</div>
                    </div>
                    <div class="stat-card fault">
                        <h3>故障设备</h3>
                        <div class="stat-value">{{ stats.fault }}</div>
                    </div>
                    <div class="stat-card maintenance">
                        <h3>维护中</h3>
                        <div class="stat-value">{{ stats.maintenance }}</div>
                    </div>
                </div>
                
                <div class="search-bar">
                    <el-input
                        v-model="searchDeviceNo"
                        placeholder="请输入设备编号"
                        clearable
                        @clear="handleSearch"
                    ></el-input>
                    <el-input
                        v-model="searchCommunity"
                        placeholder="请输入所属社区"
                        clearable
                        @clear="handleSearch"
                    ></el-input>
                    <el-select
                        v-model="searchStatus"
                        placeholder="设备状态"
                        clearable
                        @clear="handleSearch"
                        @change="handleSearch"
                        style="width: 140px"
                    >
                        <el-option label="全部状态" value=""></el-option>
                        <el-option label="正常" value="normal"></el-option>
                        <el-option label="故障" value="fault"></el-option>
                        <el-option label="离线" value="offline"></el-option>
                        <el-option label="维护中" value="maintenance"></el-option>
                    </el-select>
                    <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
                    <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
                    <el-button type="success" icon="el-icon-plus" @click="openNewFaultDialog">故障上报</el-button>
                </div>
                
                <div class="table-container">
                    <el-table
                        :data="deviceList"
                        :row-class-name="tableRowClassName"
                        border
                        style="width: 100%"
                    >
                        <el-table-column
                            prop="deviceNo"
                            label="设备编号"
                            width="150"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="community"
                            label="所属社区卫生服务中心"
                            min-width="220"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="location"
                            label="放置位置"
                            min-width="200"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            prop="status"
                            label="设备状态"
                            width="100"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.status)">
                                    {{ getStatusText(scope.row.status) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column
                            prop="cardReader"
                            label="读卡器"
                            width="100"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.cardReader)">
                                    {{ getStatusText(scope.row.cardReader) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column
                            prop="printer"
                            label="打印机"
                            width="100"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.printer)">
                                    {{ getStatusText(scope.row.printer) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column
                            prop="paymentModule"
                            label="支付模块"
                            width="100"
                            align="center"
                        >
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.paymentModule)">
                                    {{ getStatusText(scope.row.paymentModule) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column
                            prop="lastOnline"
                            label="最后在线时间"
                            width="160"
                            align="center"
                        ></el-table-column>
                        <el-table-column
                            label="操作"
                            width="150"
                            align="center"
                            fixed="right"
                        >
                            <template slot-scope="scope">
                                <div class="action-buttons">
                                    <el-button
                                        type="danger"
                                        size="small"
                                        icon="el-icon-warning"
                                        @click="openFaultDialog(scope.row)"
                                        :disabled="scope.row.status === 'maintenance'"
                                    >
                                        故障上报
                                    </el-button>
                                </div>
                            </template>
                        </el-table-column>
                    </el-table>
                    
                    <div class="pagination-container">
                        <el-pagination
                            @size-change="handleSizeChange"
                            @current-change="handleCurrentChange"
                            :current-page="currentPage"
                            :page-sizes="[10, 20, 50]"
                            :page-size="pageSize"
                            layout="total, sizes, prev, pager, next, jumper"
                            :total="total"
                        ></el-pagination>
                    </div>
                </div>
            </div>
            
            <el-dialog
                title="故障上报"
                :visible.sync="dialogVisible"
                width="500px"
                :close-on-click-modal="false"
            >
                <el-form :model="faultForm" :rules="rules" ref="faultForm" label-width="100px">
                    <el-form-item label="选择设备" prop="deviceId">
                        <el-select
                            v-model="faultForm.deviceId"
                            placeholder="请选择设备"
                            style="width: 100%"
                            @change="handleDeviceChange"
                        >
                            <el-option
                                v-for="item in availableDevices"
                                :key="item.id"
                                :label="item.deviceNo + ' - ' + item.community"
                                :value="item.id.toString()"
                            ></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="设备编号">
                        <el-input v-model="faultForm.deviceNo" disabled></el-input>
                    </el-form-item>
                    <el-form-item label="故障描述" prop="description">
                        <el-input
                            type="textarea"
                            v-model="faultForm.description"
                            :rows="4"
                            placeholder="请详细描述故障情况..."
                        ></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="dialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="submitFault">提 交</el-button>
                </div>
            </el-dialog>
        </div>
    `
});