const OrderList = {
    template: `
        <div class="page-container">
            <div class="page-header" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2>📋 订单管理</h2>
                    <p>查看和管理所有酒店预订订单</p>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <el-tag v-if="autoRefresh" type="success" size="small">
                        <i class="el-icon-refresh"></i> 自动刷新中
                    </el-tag>
                    <el-switch v-model="autoRefresh" active-text="自动刷新"></el-switch>
                    <el-button size="small" icon="el-icon-refresh" @click="forceRefresh">手动刷新</el-button>
                </div>
            </div>
            
            <div class="search-bar">
                <el-row :gutter="20">
                    <el-col :span="4">
                        <el-input v-model="searchKeyword" placeholder="订单号/姓名/手机号" clearable></el-input>
                    </el-col>
                    <el-col :span="4">
                        <el-select v-model="searchRoomType" placeholder="房型筛选" clearable style="width: 100%">
                            <el-option label="全部房型" value=""></el-option>
                            <el-option v-for="room in $root.rooms" :key="room.id" :label="room.name" :value="room.name"></el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="4">
                        <el-select v-model="searchStatus" placeholder="订单状态" clearable style="width: 100%">
                            <el-option label="全部状态" value=""></el-option>
                            <el-option label="待确认" value="pending"></el-option>
                            <el-option label="已确认" value="confirmed"></el-option>
                            <el-option label="已入住" value="checkedin"></el-option>
                            <el-option label="已完成" value="completed"></el-option>
                            <el-option label="已取消" value="cancelled"></el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="5">
                        <el-date-picker v-model="dateRange" type="daterange" range-separator="至" 
                            start-placeholder="入住开始日期" end-placeholder="入住结束日期" style="width: 100%"></el-date-picker>
                    </el-col>
                    <el-col :span="7">
                        <el-button type="primary" @click="handleSearch" icon="el-icon-search">搜索</el-button>
                        <el-button @click="resetSearch" icon="el-icon-refresh">重置</el-button>
                        <span style="margin-left: 15px; color: #909399;">
                            共 <span style="color: #409eff; font-weight: 600;">{{ paginatedOrders.length }}</span> 条记录
                        </span>
                    </el-col>
                </el-row>
            </div>
            
            <el-row :gutter="20" style="margin-bottom: 20px;">
                <el-col :span="6">
                    <el-card class="summary-card" shadow="hover">
                        <div class="amount-label">今日订单</div>
                        <div class="amount-display" style="font-size: 24px;">{{ todayCount }}</div>
                    </el-card>
                </el-col>
                <el-col :span="6">
                    <el-card class="summary-card" shadow="hover">
                        <div class="amount-label">待入住</div>
                        <div class="amount-display" style="font-size: 24px; color: #e6a23c;">{{ pendingCount }}</div>
                    </el-card>
                </el-col>
                <el-col :span="6">
                    <el-card class="summary-card" shadow="hover">
                        <div class="amount-label">入住中</div>
                        <div class="amount-display" style="font-size: 24px; color: #409eff;">{{ checkedinCount }}</div>
                    </el-card>
                </el-col>
                <el-col :span="6">
                    <el-card class="summary-card" shadow="hover">
                        <div class="amount-label">今日营收</div>
                        <div class="amount-display" style="font-size: 24px;">¥{{ todayRevenue }}</div>
                    </el-card>
                </el-col>
            </el-row>
            
            <div class="table-container">
                <el-table :data="paginatedOrders" border stripe v-loading="loading">
                    <el-table-column type="index" label="序号" width="60" align="center" :index="indexMethod"></el-table-column>
                    <el-table-column prop="id" label="订单号" width="140" align="center"></el-table-column>
                    <el-table-column prop="roomName" label="房型" align="center"></el-table-column>
                    <el-table-column prop="guestName" label="入住人" width="100" align="center"></el-table-column>
                    <el-table-column prop="phone" label="联系电话" width="120" align="center"></el-table-column>
                    <el-table-column prop="checkinDate" label="入住日期" width="120" align="center"></el-table-column>
                    <el-table-column prop="checkoutDate" label="退房日期" width="120" align="center"></el-table-column>
                    <el-table-column prop="days" label="天数" width="80" align="center">
                        <template slot-scope="scope">{{ scope.row.days }}晚</template>
                    </el-table-column>
                    <el-table-column prop="price" label="金额" width="100" align="center">
                        <template slot-scope="scope">
                            <span style="color: #f56c6c; font-weight: 600;">¥{{ scope.row.price }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="roomNumber" label="房间号" width="90" align="center">
                        <template slot-scope="scope">
                            <el-tag v-if="scope.row.roomNumber" size="mini" type="success">{{ scope.row.roomNumber }}</el-tag>
                            <span v-else style="color: #c0c4cc;">-</span>
                        </template>
                    </el-table-column>
                    <el-table-column label="状态" width="100" align="center">
                        <template slot-scope="scope">
                            <el-tag :type="getStatusType(scope.row.status)" size="small">
                                {{ getStatusText(scope.row.status) }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="createTime" label="创建时间" width="160" align="center"></el-table-column>
                    <el-table-column label="操作" width="220" fixed="right" align="center">
                        <template slot-scope="scope">
                            <el-button type="text" size="small" icon="el-icon-view" @click="viewDetail(scope.row)">详情</el-button>
                            <el-button v-if="scope.row.status === 'pending'" type="text" size="small" icon="el-icon-check" style="color: #67c23a;" @click="confirmOrder(scope.row)">确认</el-button>
                            <el-button v-if="scope.row.status === 'pending' || scope.row.status === 'confirmed'" type="text" size="small" icon="el-icon-close" style="color: #f56c6c;" @click="cancelOrder(scope.row)">取消</el-button>
                            <el-button v-if="scope.row.status === 'checkedin'" type="text" size="small" icon="el-icon-s-finance" style="color: #409eff;" @click="goCheckout(scope.row)">退房</el-button>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            
            <div style="margin-top: 20px; display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #909399; font-size: 14px;">
                    显示第 {{ (currentPage - 1) * pageSize + 1 }} - {{ Math.min(currentPage * pageSize, filteredOrders.length) }} 条，共 {{ filteredOrders.length }} 条
                </span>
                <el-pagination 
                    background 
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="filteredOrders.length"
                    :page-size="pageSize"
                    :page-sizes="[5, 10, 20, 50]"
                    :current-page="currentPage"
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange">
                </el-pagination>
            </div>
        </div>
    `,
    data() {
        return {
            searchKeyword: '',
            searchRoomType: '',
            searchStatus: '',
            dateRange: '',
            loading: false,
            autoRefresh: true,
            refreshTimer: null,
            currentPage: 1,
            pageSize: 10,
            lastOrderCount: 0
        };
    },
    computed: {
        filteredOrders() {
            let orders = this.$root.orders;
            
            // 关键词搜索
            if (this.searchKeyword) {
                orders = orders.filter(o => 
                    o.id.includes(this.searchKeyword) || 
                    o.guestName.includes(this.searchKeyword) || 
                    o.phone.includes(this.searchKeyword)
                );
            }
            
            // 房型筛选
            if (this.searchRoomType) {
                orders = orders.filter(o => o.roomName === this.searchRoomType);
            }
            
            // 状态筛选
            if (this.searchStatus) {
                orders = orders.filter(o => o.status === this.searchStatus);
            }
            
            // 日期范围筛选
            if (this.dateRange && this.dateRange.length === 2) {
                const startDate = this.formatDate(this.dateRange[0]);
                const endDate = this.formatDate(this.dateRange[1]);
                orders = orders.filter(o => {
                    return o.checkinDate >= startDate && o.checkinDate <= endDate;
                });
            }
            
            return orders;
        },
        paginatedOrders() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.filteredOrders.slice(start, end);
        },
        todayCount() {
            const today = new Date().toLocaleDateString();
            return this.$root.orders.filter(o => o.createTime.includes(today)).length;
        },
        pendingCount() {
            return this.$root.orders.filter(o => o.status === 'pending' || o.status === 'confirmed').length;
        },
        checkedinCount() {
            return this.$root.orders.filter(o => o.status === 'checkedin').length;
        },
        todayRevenue() {
            const today = new Date().toLocaleDateString();
            return this.$root.orders
                .filter(o => o.createTime.includes(today) && o.status !== 'cancelled')
                .reduce((sum, o) => sum + o.price, 0);
        }
    },
    mounted() {
        this.startAutoRefresh();
        this.lastOrderCount = this.$root.orders.length;
    },
    beforeDestroy() {
        this.stopAutoRefresh();
    },
    methods: {
        formatDate(date) {
            const d = new Date(date);
            const year = d.getFullYear();
            const month = String(d.getMonth() + 1).padStart(2, '0');
            const day = String(d.getDate()).padStart(2, '0');
            return `${year}-${month}-${day}`;
        },
        startAutoRefresh() {
            if (this.refreshTimer) clearInterval(this.refreshTimer);
            this.refreshTimer = setInterval(() => {
                this.checkForUpdates();
            }, 3000); // 每3秒检查一次
        },
        stopAutoRefresh() {
            if (this.refreshTimer) {
                clearInterval(this.refreshTimer);
                this.refreshTimer = null;
            }
        },
        checkForUpdates() {
            const currentCount = this.$root.orders.length;
            if (currentCount !== this.lastOrderCount) {
                this.lastOrderCount = currentCount;
                this.$message.info('订单列表已更新');
                // 如果当前页超出范围，回到第一页
                const maxPage = Math.ceil(this.filteredOrders.length / this.pageSize);
                if (this.currentPage > maxPage && maxPage > 0) {
                    this.currentPage = 1;
                }
            }
        },
        forceRefresh() {
            this.loading = true;
            setTimeout(() => {
                this.loading = false;
                this.$message.success('刷新成功');
            }, 500);
        },
        indexMethod(index) {
            return (this.currentPage - 1) * this.pageSize + index + 1;
        },
        handleSizeChange(val) {
            this.pageSize = val;
            this.currentPage = 1;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        },
        getStatusType(status) {
            const types = {
                pending: 'warning',
                confirmed: 'info',
                checkedin: 'primary',
                completed: 'success',
                cancelled: 'danger'
            };
            return types[status] || 'info';
        },
        getStatusText(status) {
            const texts = {
                pending: '待确认',
                confirmed: '已确认',
                checkedin: '已入住',
                completed: '已完成',
                cancelled: '已取消'
            };
            return texts[status] || status;
        },
        handleSearch() {
            this.currentPage = 1;
            this.$message.success('搜索完成，找到 ' + this.filteredOrders.length + ' 条记录');
        },
        resetSearch() {
            this.searchKeyword = '';
            this.searchRoomType = '';
            this.searchStatus = '';
            this.dateRange = '';
            this.currentPage = 1;
        },
        viewDetail(order) {
            this.$alert(`
                订单号：${order.id}\n
                房型：${order.roomName}\n
                入住人：${order.guestName}\n
                手机：${order.phone}\n
                入住：${order.checkinDate}\n
                退房：${order.checkoutDate}\n
                入住天数：${order.days}晚\n
                金额：¥${order.price}\n
                房间号：${order.roomNumber || '未分配'}\n
                状态：${this.getStatusText(order.status)}\n
                创建时间：${order.createTime}
            `, '订单详情');
        },
        confirmOrder(order) {
            this.$confirm('确认该订单吗？', '提示').then(() => {
                this.$root.updateOrderStatus(order.id, 'confirmed');
                this.$message.success('订单已确认');
            });
        },
        cancelOrder(order) {
            this.$confirm('确定取消该订单吗？', '提示', { type: 'warning' }).then(() => {
                this.$root.updateOrderStatus(order.id, 'cancelled');
                this.$message.success('订单已取消');
            });
        },
        goCheckout(order) {
            this.$router.push({
                path: '/checkout',
                query: { orderId: order.id }
            });
        }
    },
    watch: {
        autoRefresh(val) {
            if (val) {
                this.startAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        }
    }
};
