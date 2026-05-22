Vue.use(ELEMENT);

new Vue({
    el: '#app',
    data: function() {
        return {
            searchForm: {
                deviceId: '',
                branchName: '',
                status: ''
            },
            tableData: [],
            allDevices: [],
            pagination: {
                currentPage: 1,
                pageSize: 10,
                total: 0
            },
            faultDialogVisible: false,
            faultForm: {
                deviceId: '',
                deviceName: '',
                faultDescription: ''
            },
            workOrderId: '',
            rules: {
                deviceId: [
                    { required: true, message: '请选择设备', trigger: 'change' }
                ],
                faultDescription: [
                    { required: true, message: '请输入故障说明', trigger: 'blur' },
                    { min: 5, message: '故障说明至少5个字符', trigger: 'blur' }
                ]
            },
            statusOptions: [
                { label: '全部状态', value: '' },
                { label: '正常', value: 'normal' },
                { label: '故障', value: 'fault' },
                { label: '离线', value: 'offline' },
                { label: '维护中', value: 'maintenance' }
            ],
            moduleStatusMap: {
                normal: '正常',
                fault: '故障',
                offline: '离线'
            }
        };
    },
    computed: {
        filteredData: function() {
            var self = this;
            return this.allDevices.filter(function(device) {
                var matchDeviceId = true;
                var matchBranchName = true;
                var matchStatus = true;
                
                if (self.searchForm.deviceId) {
                    matchDeviceId = device.deviceId.toLowerCase().indexOf(self.searchForm.deviceId.toLowerCase()) !== -1;
                }
                
                if (self.searchForm.branchName) {
                    matchBranchName = device.branchName.toLowerCase().indexOf(self.searchForm.branchName.toLowerCase()) !== -1;
                }
                
                if (self.searchForm.status) {
                    matchStatus = device.status === self.searchForm.status;
                }
                
                return matchDeviceId && matchBranchName && matchStatus;
            });
        },
        paginatedData: function() {
            var start = (this.pagination.currentPage - 1) * this.pagination.pageSize;
            var end = start + this.pagination.pageSize;
            return this.filteredData.slice(start, end);
        }
    },
    watch: {
        'pagination.currentPage': function() {
            this.$nextTick(function() {
                this.$message({
                    type: 'info',
                    message: '已加载第 ' + this.pagination.currentPage + ' 页数据',
                    duration: 1000
                });
            });
        },
        'allDevices': {
            handler: function() {
                this.pagination.total = this.filteredData.length;
            },
            deep: true
        }
    },
    methods: {
        initMockData: function() {
            var branches = ['市民服务中心A区', '市民服务中心B区', '市民服务中心C区', '城东分中心', '城西分中心', '城南分中心', '城北分中心'];
            var areas = ['一楼大厅', '二楼服务区', '三楼办公区', '出入境大厅', '社保服务区', '公积金服务区', '不动产登记区'];
            var statuses = ['normal', 'fault', 'offline', 'maintenance'];
            var moduleStatuses = ['normal', 'fault', 'offline'];
            
            var devices = [];
            for (var i = 1; i <= 56; i++) {
                var mainStatus = statuses[Math.floor(Math.random() * statuses.length)];
                devices.push({
                    id: i,
                    deviceId: 'DEV' + String(i).padStart(4, '0'),
                    branchName: branches[Math.floor(Math.random() * branches.length)],
                    area: areas[Math.floor(Math.random() * areas.length)],
                    status: mainStatus,
                    idCardReader: mainStatus === 'offline' ? 'offline' : moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
                    voucherPrinter: mainStatus === 'offline' ? 'offline' : moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
                    infoVerification: mainStatus === 'offline' ? 'offline' : moduleStatuses[Math.floor(Math.random() * moduleStatuses.length)],
                    lastOnline: this.generateRandomDate()
                });
            }
            this.allDevices = devices;
            this.pagination.total = devices.length;
        },
        
        generateRandomDate: function() {
            var now = new Date();
            var days = Math.floor(Math.random() * 7);
            var hours = Math.floor(Math.random() * 24);
            var date = new Date(now.getTime() - days * 24 * 60 * 60 * 1000 - hours * 60 * 60 * 1000);
            return date.toLocaleString('zh-CN');
        },
        
        generateWorkOrderId: function() {
            var date = new Date();
            var year = date.getFullYear();
            var month = String(date.getMonth() + 1).padStart(2, '0');
            var day = String(date.getDate()).padStart(2, '0');
            var random = Math.floor(Math.random() * 10000).toString().padStart(4, '0');
            return 'WO' + year + month + day + random;
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
        
        getStatusClass: function(status) {
            return 'status-' + status;
        },
        
        getModuleStatusText: function(status) {
            return this.moduleStatusMap[status] || status;
        },
        
        handleSearch: function() {
            this.pagination.currentPage = 1;
            this.pagination.total = this.filteredData.length;
            this.$message({
                type: 'success',
                message: '搜索完成，共找到 ' + this.filteredData.length + ' 条记录'
            });
        },
        
        handleReset: function() {
            this.searchForm.deviceId = '';
            this.searchForm.branchName = '';
            this.searchForm.status = '';
            this.pagination.currentPage = 1;
            this.pagination.total = this.allDevices.length;
        },
        
        handleSizeChange: function(val) {
            this.pagination.pageSize = val;
        },
        
        handleCurrentChange: function(val) {
            this.pagination.currentPage = val;
        },
        
        openFaultDialog: function() {
            this.workOrderId = this.generateWorkOrderId();
            this.faultForm = {
                deviceId: '',
                deviceName: '',
                faultDescription: ''
            };
            this.faultDialogVisible = true;
        },
        
        openFaultDialogWithDevice: function(row) {
            this.workOrderId = this.generateWorkOrderId();
            this.faultForm = {
                deviceId: row.deviceId,
                deviceName: row.deviceId + ' - ' + row.branchName,
                faultDescription: ''
            };
            this.faultDialogVisible = true;
        },
        
        handleDeviceChange: function(val) {
            var device = this.allDevices.find(function(d) {
                return d.deviceId === val;
            });
            if (device) {
                this.faultForm.deviceName = device.deviceId + ' - ' + device.branchName;
            }
        },
        
        submitFaultReport: function() {
            var self = this;
            if (!this.faultForm.deviceId) {
                this.$message({
                    type: 'error',
                    message: '请选择设备后再提交'
                });
                return;
            }
            this.$refs.faultForm.validate(function(valid) {
                if (valid) {
                    self.$message({
                        type: 'success',
                        message: '故障上报成功！工单号：' + self.workOrderId
                    });
                    self.faultDialogVisible = false;
                    
                    var deviceIndex = self.allDevices.findIndex(function(d) {
                        return d.deviceId === self.faultForm.deviceId;
                    });
                    if (deviceIndex !== -1) {
                        self.$set(self.allDevices[deviceIndex], 'status', 'fault');
                        self.$set(self.allDevices[deviceIndex], 'voucherPrinter', 'fault');
                    }
                }
            });
        },
        
        getAvailableDevices: function() {
            return this.allDevices.filter(function(d) {
                return d.status !== 'maintenance';
            });
        },
        
        getRowClass: function(row) {
            if (row.status === 'fault') {
                return 'row-fault';
            } else if (row.status === 'offline') {
                return 'row-offline';
            }
            return '';
        }
    },
    mounted: function() {
        this.initMockData();
    },
    template: `
        <div>
            <div class="header">
                <h1>市民服务中心自助证明打印终端运维管理系统</h1>
            </div>
            
            <div class="container">
                <div class="search-bar">
                    <el-form :inline="true" :model="searchForm">
                        <el-form-item label="设备编号">
                            <el-input 
                                v-model="searchForm.deviceId" 
                                placeholder="请输入设备编号" 
                                clearable
                                style="width: 180px">
                            </el-input>
                        </el-form-item>
                        <el-form-item label="网点名称">
                            <el-input 
                                v-model="searchForm.branchName" 
                                placeholder="请输入网点名称" 
                                clearable
                                style="width: 180px">
                            </el-input>
                        </el-form-item>
                        <el-form-item label="设备状态">
                            <el-select 
                                v-model="searchForm.status" 
                                placeholder="请选择状态"
                                clearable
                                style="width: 120px">
                                <el-option
                                    v-for="item in statusOptions"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleSearch">搜索</el-button>
                            <el-button @click="handleReset">重置</el-button>
                            <el-button type="danger" class="btn-fault-report" @click="openFaultDialog">
                                <i class="el-icon-warning"></i> 故障上报
                            </el-button>
                        </el-form-item>
                    </el-form>
                </div>
                
                <div class="table-container">
                    <el-table 
                        :data="paginatedData" 
                        border 
                        style="width: 100%"
                        :header-cell-style="{background:'#fafafa'}"
                        :row-class-name="getRowClass">
                        <el-table-column 
                            type="index" 
                            label="序号" 
                            width="60"
                            align="center">
                        </el-table-column>
                        <el-table-column 
                            prop="deviceId" 
                            label="设备编号" 
                            width="120"
                            align="center">
                        </el-table-column>
                        <el-table-column 
                            prop="branchName" 
                            label="服务网点" 
                            min-width="160">
                        </el-table-column>
                        <el-table-column 
                            prop="area" 
                            label="摆放区域" 
                            width="120">
                        </el-table-column>
                        <el-table-column 
                            prop="status" 
                            label="设备状态" 
                            width="100"
                            align="center">
                            <template slot-scope="scope">
                                <el-tag :type="scope.row.status === 'normal' ? 'success' : scope.row.status === 'fault' ? 'danger' : scope.row.status === 'offline' ? 'info' : 'warning'" size="small">
                                    {{ getStatusText(scope.row.status) }}
                                </el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column 
                            prop="idCardReader" 
                            label="身份证读卡" 
                            width="110"
                            align="center">
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.idCardReader)">
                                    {{ getModuleStatusText(scope.row.idCardReader) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column 
                            prop="voucherPrinter" 
                            label="凭证打印" 
                            width="110"
                            align="center">
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.voucherPrinter)">
                                    {{ getModuleStatusText(scope.row.voucherPrinter) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column 
                            prop="infoVerification" 
                            label="信息核验" 
                            width="110"
                            align="center">
                            <template slot-scope="scope">
                                <span :class="getStatusClass(scope.row.infoVerification)">
                                    {{ getModuleStatusText(scope.row.infoVerification) }}
                                </span>
                            </template>
                        </el-table-column>
                        <el-table-column 
                            prop="lastOnline" 
                            label="最后在线时间" 
                            min-width="160"
                            align="center">
                        </el-table-column>
                        <el-table-column 
                            label="操作" 
                            width="100"
                            align="center">
                            <template slot-scope="scope">
                                <el-button 
                                    type="text" 
                                    size="small" 
                                    @click="openFaultDialogWithDevice(scope.row)"
                                    :disabled="scope.row.status === 'maintenance'">
                                    故障上报
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    
                    <div class="pagination-container">
                        <el-pagination
                            @size-change="handleSizeChange"
                            @current-change="handleCurrentChange"
                            :current-page="pagination.currentPage"
                            :page-sizes="[10, 20, 50, 100]"
                            :page-size="pagination.pageSize"
                            layout="total, sizes, prev, pager, next, jumper"
                            :total="filteredData.length">
                        </el-pagination>
                    </div>
                </div>
            </div>
            
            <el-dialog 
                title="故障上报" 
                :visible.sync="faultDialogVisible" 
                width="600px"
                :close-on-click-modal="false">
                <el-form 
                    ref="faultForm" 
                    :model="faultForm" 
                    :rules="rules" 
                    label-width="100px">
                    <el-form-item label="工单编号">
                        <span class="work-order-id">{{ workOrderId }}</span>
                    </el-form-item>
                    <el-form-item label="选择设备" prop="deviceId">
                        <el-select 
                            v-model="faultForm.deviceId" 
                            placeholder="请选择设备" 
                            style="width: 100%"
                            @change="handleDeviceChange"
                            filterable
                            clearable>
                            <el-option
                                v-for="device in getAvailableDevices()"
                                :key="device.deviceId"
                                :label="device.deviceId + ' - ' + device.branchName"
                                :value="device.deviceId">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="设备名称">
                        <el-input 
                            v-model="faultForm.deviceName" 
                            disabled
                            placeholder="自动填充">
                        </el-input>
                    </el-form-item>
                    <el-form-item label="故障说明" prop="faultDescription">
                        <el-input
                            type="textarea"
                            :rows="4"
                            v-model="faultForm.faultDescription"
                            placeholder="请详细描述故障情况，如：打印机卡纸、屏幕无响应、系统死机等">
                        </el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="faultDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="submitFaultReport">提 交</el-button>
                </span>
            </el-dialog>
        </div>
    `
});
