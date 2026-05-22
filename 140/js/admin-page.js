const statusList = [
    { value: 0, label: '选料', color: '#409EFF' },
    { value: 1, label: '纹样勾勒', color: '#67C23A' },
    { value: 2, label: '缂丝织造', color: '#E6A23C' },
    { value: 3, label: '熨烫定型', color: '#909399' },
    { value: 4, label: '装柄', color: '#F56C6C' },
    { value: 5, label: '包边', color: '#00CED1' },
    { value: 6, label: '质检', color: '#8B4513' },
    { value: 7, label: '完工', color: '#FFD700' }
]

const AdminPage = {
    template: `
        <div class="admin-page">
            <el-header class="page-header">
                <div class="header-content">
                    <h1>🎐 缂丝团扇 - 订单管理</h1>
                    <div>
                        <el-button type="success" @click="goToOrder">返回下单页</el-button>
                        <el-button type="primary" @click="refreshData">刷新数据</el-button>
                    </div>
                </div>
            </el-header>
            
            <el-main class="main-content">
                <el-card class="stats-card" shadow="hover">
                    <el-row :gutter="20">
                        <el-col :span="6" v-for="(item, index) in statusStats" :key="index">
                            <div class="stat-item">
                                <div class="stat-value" :style="{ color: statusList[index].color }">{{ item.count }}</div>
                                <div class="stat-label">{{ item.label }}</div>
                            </div>
                        </el-col>
                    </el-row>
                </el-card>
                
                <el-card class="filter-card" shadow="hover">
                    <el-form :inline="true" :model="filterForm" class="filter-form">
                        <el-form-item label="订单编号">
                            <el-input v-model="filterForm.orderId" placeholder="请输入订单编号" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="客户姓名">
                            <el-input v-model="filterForm.customerName" placeholder="请输入客户姓名" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="订单状态">
                            <el-select v-model="filterForm.status" placeholder="请选择状态" clearable>
                                <el-option v-for="item in statusList" :key="item.value" :label="item.label" :value="item.value"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="searchOrders">搜索</el-button>
                            <el-button @click="resetFilter">重置</el-button>
                        </el-form-item>
                    </el-form>
                </el-card>
                
                <el-card class="order-list-card" shadow="hover">
                    <div slot="header" class="card-header">
                        <span>📋 订单列表</span>
                        <span style="color: #909399; font-size: 14px;">共 {{ filteredOrders.length }} 条订单</span>
                    </div>
                    
                    <el-table ref="orderTable" :data="filteredOrders" style="width: 100%" border stripe :row-class-name="getRowClassName">
                        <el-table-column prop="id" label="订单编号" width="180" fixed>
                            <template slot-scope="scope">
                                <span style="color: #409EFF; font-weight: bold;">{{ scope.row.id }}</span>
                            </template>
                        </el-table-column>
                        
                        <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
                        <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
                        
                        <el-table-column label="定制详情" min-width="320">
                            <template slot-scope="scope">
                                <div class="order-detail">
                                    <div class="order-header" v-if="isNewOrder(scope.row)">
                                        <el-tag type="danger" effect="dark" size="mini">新订单</el-tag>
                                    </div>
                                    <p><strong>底料：</strong>{{ scope.row.fabric }}</p>
                                    <p><strong>尺寸：</strong>{{ scope.row.length || scope.row.diameter || 25 }} × {{ scope.row.width || 20 }}cm</p>
                                    <p><strong>纹样：</strong>{{ scope.row.pattern }}</p>
                                    <p><strong>配色：</strong>{{ scope.row.colorScheme && scope.row.colorScheme.join('、') }}</p>
                                    <p><strong>扇柄：</strong>{{ scope.row.handle }}</p>
                                </div>
                            </template>
                        </el-table-column>
                        
                        <el-table-column prop="statusText" label="当前状态" width="120">
                            <template slot-scope="scope">
                                <el-tag :type="getStatusType(scope.row.status)" size="small">
                                    {{ scope.row.statusText }}
                                </el-tag>
                            </template>
                        </el-table-column>
                        
                        <el-table-column label="生产进度" width="300">
                            <template slot-scope="scope">
                                <div class="progress-timeline">
                                    <el-steps :active="scope.row.status + 1" finish-status="success" align-center size="small">
                                        <el-step v-for="(item, index) in statusList" :key="index" :title="item.label"></el-step>
                                    </el-steps>
                                </div>
                            </template>
                        </el-table-column>
                        
                        <el-table-column prop="createTime" label="下单时间" width="160"></el-table-column>
                        
                        <el-table-column label="操作" width="200" fixed="right">
                            <template slot-scope="scope">
                                <el-button 
                                    type="primary" 
                                    size="small" 
                                    @click="updateStatus(scope.row)"
                                    :disabled="scope.row.status >= 7">
                                    更新状态
                                </el-button>
                                <el-button 
                                    type="danger" 
                                    size="small" 
                                    @click="deleteOrder(scope.row.id)">
                                    删除
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                    
                    <el-empty v-if="filteredOrders.length === 0" description="暂无订单数据"></el-empty>
                </el-card>
            </el-main>
            
            <el-dialog title="更新订单状态" :visible.sync="statusDialogVisible" width="550px">
                <el-form :model="currentOrder" label-width="100px">
                    <el-form-item label="订单编号">
                        <span>{{ currentOrder.id }}</span>
                    </el-form-item>
                    <el-form-item label="当前状态">
                        <el-tag :type="getStatusType(currentOrder.status)">{{ currentOrder.statusText }}</el-tag>
                    </el-form-item>
                    <el-form-item label="下一状态" v-if="currentOrder.status < 7">
                        <el-tag type="success" size="medium">{{ nextStatusText }}</el-tag>
                        <div style="margin-top: 8px; color: #606266; font-size: 13px;">
                            <i class="el-icon-info"></i> 生产工序需按顺序推进，不可跳级操作
                        </div>
                    </el-form-item>
                    <el-form-item v-else>
                        <el-tag type="warning" size="medium">已完成全部生产工序</el-tag>
                    </el-form-item>
                    <el-form-item label="操作人" v-if="currentOrder.status < 7" prop="operator">
                        <el-input v-model="operator" placeholder="请输入操作人姓名" clearable></el-input>
                    </el-form-item>
                    <el-form-item label="备注说明" v-if="currentOrder.status < 7">
                        <el-input type="textarea" :rows="2" v-model="statusRemark" placeholder="请填写状态更新说明..."></el-input>
                    </el-form-item>
                    <el-form-item label="操作历史" v-if="currentOrder.statusHistory && currentOrder.statusHistory.length > 0">
                        <div class="status-history">
                            <div v-for="(item, index) in currentOrder.statusHistory" :key="index" class="history-item">
                                <div class="history-status">
                                    <el-tag size="mini">{{ item.status }}</el-tag>
                                </div>
                                <div class="history-info">
                                    <span class="history-operator">操作人：{{ item.operator }}</span>
                                    <span class="history-time">{{ item.time }}</span>
                                </div>
                                <div v-if="item.remark" class="history-remark">{{ item.remark }}</div>
                            </div>
                        </div>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <el-button @click="statusDialogVisible = false">取 消</el-button>
                    <el-button type="primary" @click="confirmUpdateStatus" :disabled="currentOrder.status >= 7 || !operator">确 定</el-button>
                </div>
            </el-dialog>
            
            <el-footer class="page-footer">
                <p>© 2024 缂丝团扇定制工坊 - 订单管理系统</p>
            </el-footer>
        </div>
    `,
    data() {
        return {
            orders: [],
            filterForm: {
                orderId: '',
                customerName: '',
                status: null
            },
            statusDialogVisible: false,
            currentOrder: {},
            nextStatus: null,
            statusRemark: '',
            operator: ''
        }
    },
    computed: {
        filteredOrders() {
            return this.orders.filter(order => {
                const matchId = !this.filterForm.orderId || order.id.includes(this.filterForm.orderId)
                const matchName = !this.filterForm.customerName || order.customerName.includes(this.filterForm.customerName)
                const matchStatus = this.filterForm.status === null || order.status === this.filterForm.status
                return matchId && matchName && matchStatus
            })
        },
        statusStats() {
            const stats = statusList.map(item => ({
                label: item.label,
                count: 0
            }))
            this.orders.forEach(order => {
                if (order.status >= 0 && order.status < stats.length) {
                    stats[order.status].count++
                }
            })
            return stats
        },
        nextStatusText() {
            if (this.currentOrder.status < 7) {
                return statusList[this.currentOrder.status + 1].label
            }
            return ''
        }
    },
    mounted() {
        this.loadOrders()
        this.addMockData()
        this.checkScrollToLatest()
    },
    activated() {
        this.checkScrollToLatest()
    },
    watch: {
        '$route'() {
            this.checkScrollToLatest()
        }
    },
    methods: {
        goToOrder() {
            this.$router.push('/order')
        },
        refreshData() {
            this.loadOrders()
            this.$message.success('数据已刷新')
        },
        checkScrollToLatest() {
            const shouldScroll = localStorage.getItem('scrollToLatest')
            if (shouldScroll === 'true') {
                localStorage.removeItem('scrollToLatest')
                this.$nextTick(() => {
                    this.scrollToLatestOrder()
                    this.$message.info('已定位到最新订单')
                })
            }
        },
        loadOrders() {
            this.orders = JSON.parse(localStorage.getItem('fanOrders') || '[]')
        },
        addMockData() {
            if (this.orders.length === 0) {
                const mockOrders = [
                    {
                        id: 'ORD202401001',
                        customerName: '张小姐',
                        phone: '13800138001',
                        fabric: '真丝绡',
                        length: 25,
                        width: 20,
                        pattern: '牡丹凤凰',
                        colorScheme: ['清雅素色'],
                        handle: '湘妃竹',
                        remarks: '希望能尽快完成',
                        status: 2,
                        statusText: '缂丝织造',
                        createTime: '2024/1/15 10:30:00',
                        statusHistory: [
                            { status: '选料', operator: '王师傅', time: '2024/1/15 11:00:00', remark: '面料检查合格' },
                            { status: '纹样勾勒', operator: '李工', time: '2024/1/15 15:30:00', remark: '纹样设计完成' }
                        ]
                    },
                    {
                        id: 'ORD202401002',
                        customerName: '李先生',
                        phone: '13900139002',
                        fabric: '宋锦',
                        length: 30,
                        width: 25,
                        pattern: '江南水乡',
                        colorScheme: ['水墨丹青'],
                        handle: '紫檀木',
                        remarks: '送给长辈的礼物',
                        status: 5,
                        statusText: '包边',
                        createTime: '2024/1/16 14:20:00',
                        statusHistory: [
                            { status: '选料', operator: '王师傅', time: '2024/1/16 15:00:00', remark: '宋锦面料确认' },
                            { status: '纹样勾勒', operator: '张工', time: '2024/1/17 09:30:00', remark: '山水纹样确认' },
                            { status: '缂丝织造', operator: '陈师傅', time: '2024/1/18 16:00:00', remark: '织造完成' },
                            { status: '熨烫定型', operator: '刘工', time: '2024/1/19 10:00:00', remark: '定型效果良好' },
                            { status: '装柄', operator: '赵师傅', time: '2024/1/19 14:30:00', remark: '紫檀木柄安装完成' }
                        ]
                    },
                    {
                        id: 'ORD202401003',
                        customerName: '王女士',
                        phone: '13700137003',
                        fabric: '杭绸',
                        length: 22,
                        width: 18,
                        pattern: '百福图',
                        colorScheme: ['明艳喜庆'],
                        handle: '黄杨木',
                        remarks: '',
                        status: 7,
                        statusText: '完工',
                        createTime: '2024/1/10 09:15:00'
                    },
                    {
                        id: 'ORD202401004',
                        customerName: '赵先生',
                        phone: '13600136004',
                        fabric: '绫罗',
                        length: 28,
                        width: 22,
                        pattern: '梅花喜鹊',
                        colorScheme: ['典雅宫廷'],
                        handle: '鸡翅木',
                        remarks: '请加急处理',
                        status: 0,
                        statusText: '选料',
                        createTime: '2024/1/18 16:45:00'
                    }
                ]
                this.orders = mockOrders
                localStorage.setItem('fanOrders', JSON.stringify(mockOrders))
            }
        },
        getStatusType(status) {
            const types = ['', 'success', 'warning', 'info', 'danger', '']
            return types[status % types.length] || ''
        },
        searchOrders() {
            this.$message.success('搜索完成')
        },
        resetFilter() {
            this.filterForm = {
                orderId: '',
                customerName: '',
                status: null
            }
        },
        updateStatus(row) {
            this.currentOrder = { ...row }
            this.nextStatus = row.status + 1 < 8 ? row.status + 1 : null
            this.statusRemark = ''
            this.operator = ''
            this.statusDialogVisible = true
        },
        confirmUpdateStatus() {
            const index = this.orders.findIndex(o => o.id === this.currentOrder.id)
            if (index !== -1) {
                const nextStatus = this.currentOrder.status + 1
                if (nextStatus < 8) {
                    const historyRecord = {
                        status: statusList[nextStatus].label,
                        operator: this.operator,
                        time: new Date().toLocaleString(),
                        remark: this.statusRemark
                    }
                    
                    if (!this.orders[index].statusHistory) {
                        this.orders[index].statusHistory = []
                    }
                    this.orders[index].statusHistory.push(historyRecord)
                    
                    this.orders[index].status = nextStatus
                    this.orders[index].statusText = statusList[nextStatus].label
                    localStorage.setItem('fanOrders', JSON.stringify(this.orders))
                    this.statusDialogVisible = false
                    this.$message.success('状态更新成功，已推进至：' + statusList[nextStatus].label)
                }
            }
        },
        isNewOrder(order) {
            return order.status === 0
        },
        getRowClassName({ row }) {
            return this.isNewOrder(row) ? 'new-order-row' : ''
        },
        scrollToLatestOrder() {
            this.$nextTick(() => {
                const table = this.$refs.orderTable
                if (table) {
                    table.setCurrentRow(this.filteredOrders[0])
                    const row = document.querySelector('.el-table__body tr.current-row')
                    if (row) {
                        row.scrollIntoView({ behavior: 'smooth', block: 'center' })
                    }
                }
            })
        },
        deleteOrder(id) {
            this.$confirm('确认删除该订单吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                const index = this.orders.findIndex(o => o.id === id)
                if (index !== -1) {
                    this.orders.splice(index, 1)
                    localStorage.setItem('fanOrders', JSON.stringify(this.orders))
                    this.$message.success('删除成功')
                }
            }).catch(() => {})
        }
    }
}