new Vue({
    el: '#app',
    data: {
        searchDeviceId: '',
        searchHallName: '',
        currentPage: 1,
        pageSize: 8,
        jumpPage: '',
        showModal: false,
        reportForm: {
            orderNo: '',
            selectedDeviceId: '',
            description: ''
        },
        formErrors: {
            selectedDeviceId: '',
            description: ''
        },
        statusFilter: '',
        devices: [
            { id: 1, deviceId: 'PWR-2026-001', hallName: '城东供电营业厅', location: '一楼大厅左侧', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:30:25' },
            { id: 2, deviceId: 'PWR-2026-002', hallName: '城西供电营业厅', location: '二楼服务台旁', status: 'fault', meterStatus: 'fault', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-15 14:22:18' },
            { id: 3, deviceId: 'PWR-2026-003', hallName: '城南供电营业厅', location: '正门入口处', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 08:45:33' },
            { id: 4, deviceId: 'PWR-2026-004', hallName: '城北供电营业厅', location: 'VIP服务区', status: 'offline', meterStatus: 'offline', printerStatus: 'offline', idCardStatus: 'offline', lastOnline: '2026-05-14 11:20:45' },
            { id: 5, deviceId: 'PWR-2026-005', hallName: '中心营业厅', location: '自助服务区A区', status: 'maintenance', meterStatus: 'maintenance', printerStatus: 'maintenance', idCardStatus: 'normal', lastOnline: '2026-05-16 07:00:00' },
            { id: 6, deviceId: 'PWR-2026-006', hallName: '城东供电营业厅', location: '自助服务区B区', status: 'normal', meterStatus: 'normal', printerStatus: 'fault', idCardStatus: 'normal', lastOnline: '2026-05-16 09:28:15' },
            { id: 7, deviceId: 'PWR-2026-007', hallName: '开发区营业厅', location: '一楼大厅右侧', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:15:42' },
            { id: 8, deviceId: 'PWR-2026-008', hallName: '高新区营业厅', location: '二楼走廊尽头', status: 'fault', meterStatus: 'normal', printerStatus: 'fault', idCardStatus: 'fault', lastOnline: '2026-05-15 16:30:22' },
            { id: 9, deviceId: 'PWR-2026-009', hallName: '城西供电营业厅', location: '自助服务区', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:05:18' },
            { id: 10, deviceId: 'PWR-2026-010', hallName: '中心营业厅', location: '大堂经理台旁', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:32:00' },
            { id: 11, deviceId: 'PWR-2026-011', hallName: '城南供电营业厅', location: '二楼客服中心', status: 'offline', meterStatus: 'offline', printerStatus: 'offline', idCardStatus: 'offline', lastOnline: '2026-05-13 09:45:30' },
            { id: 12, deviceId: 'PWR-2026-012', hallName: '城北供电营业厅', location: '营业大厅入口', status: 'maintenance', meterStatus: 'normal', printerStatus: 'maintenance', idCardStatus: 'maintenance', lastOnline: '2026-05-16 06:30:00' },
            { id: 13, deviceId: 'PWR-2026-013', hallName: '开发区营业厅', location: 'VIP客户专区', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:20:15' },
            { id: 14, deviceId: 'PWR-2026-014', hallName: '高新区营业厅', location: '一楼自助区', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'fault', lastOnline: '2026-05-16 09:25:40' },
            { id: 15, deviceId: 'PWR-2026-015', hallName: '城东供电营业厅', location: '三楼办公区', status: 'fault', meterStatus: 'fault', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-15 10:15:28' },
            { id: 16, deviceId: 'PWR-2026-016', hallName: '中心营业厅', location: '电费缴纳专区', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:35:50' },
            { id: 17, deviceId: 'PWR-2026-017', hallName: '城西供电营业厅', location: '业务办理区', status: 'offline', meterStatus: 'offline', printerStatus: 'offline', idCardStatus: 'offline', lastOnline: '2026-05-12 14:30:22' },
            { id: 18, deviceId: 'PWR-2026-018', hallName: '城南供电营业厅', location: '客户休息区旁', status: 'normal', meterStatus: 'normal', printerStatus: 'normal', idCardStatus: 'normal', lastOnline: '2026-05-16 09:18:33' }
        ]
    },
    computed: {
        filteredDevices: function() {
            var self = this;
            return this.devices.filter(function(device) {
                var matchDeviceId = true;
                var matchHallName = true;
                var matchStatus = true;
                
                if (self.searchDeviceId) {
                    matchDeviceId = device.deviceId.toLowerCase().indexOf(self.searchDeviceId.toLowerCase()) !== -1;
                }
                
                if (self.searchHallName) {
                    matchHallName = device.hallName.toLowerCase().indexOf(self.searchHallName.toLowerCase()) !== -1;
                }
                
                if (self.statusFilter) {
                    matchStatus = device.status === self.statusFilter;
                }
                
                return matchDeviceId && matchHallName && matchStatus;
            });
        },
        paginatedDevices: function() {
            var start = (this.currentPage - 1) * this.pageSize;
            var end = start + this.pageSize;
            return this.filteredDevices.slice(start, end);
        },
        totalPages: function() {
            return Math.ceil(this.filteredDevices.length / this.pageSize);
        },
        visiblePages: function() {
            var pages = [];
            var start = Math.max(1, this.currentPage - 2);
            var end = Math.min(this.totalPages, this.currentPage + 2);
            
            for (var i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        },
        totalDevices: function() {
            return this.devices.length;
        },
        normalCount: function() {
            return this.devices.filter(function(d) { return d.status === 'normal'; }).length;
        },
        faultCount: function() {
            return this.devices.filter(function(d) { return d.status === 'fault'; }).length;
        },
        offlineCount: function() {
            return this.devices.filter(function(d) { return d.status === 'offline'; }).length;
        },
        selectedDeviceInfo: function() {
            if (!this.reportForm.selectedDeviceId) {
                return '请先选择设备';
            }
            var device = this.devices.find(function(d) { 
                return d.id == this.reportForm.selectedDeviceId; 
            }.bind(this));
            if (device) {
                return device.location + ' - ' + this.getStatusText(device.status);
            }
            return '';
        },
        isFormValid: function() {
            return this.reportForm.selectedDeviceId && this.reportForm.description.trim();
        },
        reportTime: function() {
            var now = new Date();
            return now.getFullYear() + '-' + 
                   String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                   String(now.getDate()).padStart(2, '0') + ' ' + 
                   String(now.getHours()).padStart(2, '0') + ':' + 
                   String(now.getMinutes()).padStart(2, '0') + ':' + 
                   String(now.getSeconds()).padStart(2, '0');
        }
    },
    watch: {
        searchDeviceId: function() {
            this.currentPage = 1;
        },
        searchHallName: function() {
            this.currentPage = 1;
        },
        statusFilter: function() {
            this.currentPage = 1;
        },
        filteredDevices: function() {
            if (this.currentPage > this.totalPages) {
                this.currentPage = Math.max(1, this.totalPages);
            }
        }
    },
    methods: {
        getRowClass: function(status) {
            if (status === 'fault') {
                return 'row-fault';
            }
            if (status === 'offline') {
                return 'row-offline';
            }
            return '';
        },
        getStatusClass: function(status) {
            var classMap = {
                'normal': 'status-normal',
                'fault': 'status-fault',
                'offline': 'status-offline',
                'maintenance': 'status-maintenance'
            };
            return classMap[status] || '';
        },
        getStatusText: function(status) {
            var textMap = {
                'normal': '正常',
                'fault': '故障',
                'offline': '离线',
                'maintenance': '维护中'
            };
            return textMap[status] || status;
        },
        resetSearch: function() {
            this.searchDeviceId = '';
            this.searchHallName = '';
            this.statusFilter = '';
            this.currentPage = 1;
            this.jumpPage = '';
        },
        goToPage: function(page) {
            var targetPage = parseInt(page);
            if (targetPage >= 1 && targetPage <= this.totalPages) {
                this.currentPage = targetPage;
                this.jumpPage = '';
            }
        },
        validateForm: function() {
            this.formErrors.selectedDeviceId = '';
            this.formErrors.description = '';
            
            if (!this.reportForm.selectedDeviceId) {
                this.formErrors.selectedDeviceId = '请选择故障设备';
            }
            
            if (!this.reportForm.description || !this.reportForm.description.trim()) {
                this.formErrors.description = '请填写故障描述';
            } else if (this.reportForm.description.trim().length < 5) {
                this.formErrors.description = '故障描述至少需要5个字符';
            }
            
            return !this.formErrors.selectedDeviceId && !this.formErrors.description;
        },
        generateOrderNo: function() {
            var now = new Date();
            var timestamp = now.getFullYear() + 
                           String(now.getMonth() + 1).padStart(2, '0') + 
                           String(now.getDate()).padStart(2, '0') +
                           String(now.getHours()).padStart(2, '0') + 
                           String(now.getMinutes()).padStart(2, '0') + 
                           String(now.getSeconds()).padStart(2, '0');
            var random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
            return 'WO' + timestamp + random;
        },
        openReportModal: function() {
            this.reportForm = {
                orderNo: this.generateOrderNo(),
                selectedDeviceId: '',
                description: ''
            };
            this.formErrors = {
                selectedDeviceId: '',
                description: ''
            };
            this.showModal = true;
        },
        closeModal: function() {
            this.showModal = false;
        },
        submitReport: function() {
            if (!this.validateForm()) {
                return;
            }
            
            var device = this.devices.find(function(d) { 
                return d.id == this.reportForm.selectedDeviceId; 
            }.bind(this));
            
            alert('故障上报成功！\n\n工单编号：' + this.reportForm.orderNo + 
                  '\n设备编号：' + device.deviceId + 
                  '\n所属营业厅：' + device.hallName + 
                  '\n故障描述：' + this.reportForm.description +
                  '\n\n我们将尽快安排维修人员处理！');
            
            this.closeModal();
        }
    }
});
