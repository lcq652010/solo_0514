const CheckinPage = {
    template: `
        <div class="page-container">
            <div class="page-header">
                <h2>📋 入住登记</h2>
                <p>为已预订的客人办理入住手续</p>
            </div>
            
            <div class="search-bar">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-input v-model="searchKeyword" placeholder="输入订单号/姓名/手机号搜索" clearable>
                            <el-button slot="append" icon="el-icon-search" @click="searchOrder">搜索</el-button>
                        </el-input>
                    </el-col>
                </el-row>
            </div>
            
            <el-card class="card-shadow" v-if="selectedOrder">
                <div slot="header" style="display: flex; justify-content: space-between; align-items: center;">
                    <span>📄 订单信息</span>
                    <el-tag type="warning">待入住</el-tag>
                </div>
                
                <el-descriptions :column="2" border>
                    <el-descriptions-item label="订单号">{{ selectedOrder.id }}</el-descriptions-item>
                    <el-descriptions-item label="房型">{{ selectedOrder.roomName }}</el-descriptions-item>
                    <el-descriptions-item label="入住人">{{ selectedOrder.guestName }}</el-descriptions-item>
                    <el-descriptions-item label="联系电话">{{ selectedOrder.phone }}</el-descriptions-item>
                    <el-descriptions-item label="入住日期">{{ selectedOrder.checkinDate }}</el-descriptions-item>
                    <el-descriptions-item label="退房日期">{{ selectedOrder.checkoutDate }}</el-descriptions-item>
                    <el-descriptions-item label="入住天数">{{ selectedOrder.days }} 晚</el-descriptions-item>
                    <el-descriptions-item label="订单金额">¥{{ selectedOrder.price }}</el-descriptions-item>
                </el-descriptions>
                
                <el-divider content-position="left">办理入住</el-divider>
                
                <el-form :model="checkinForm" :rules="rules" ref="checkinForm" label-width="120px" class="form-container" style="margin-top: 20px;">
                    <el-form-item label="房间号" prop="roomNumber">
                        <el-input v-model="checkinForm.roomNumber" placeholder="请分配房间号" maxlength="10"></el-input>
                    </el-form-item>
                    
                    <el-form-item label="身份证验证">
                        <el-button type="success" icon="el-icon-camera" @click="verifyIdCard">读取身份证信息</el-button>
                        <span v-if="idVerified" style="color: #67c23a; margin-left: 10px;"><i class="el-icon-check"></i> 验证通过</span>
                    </el-form-item>
                    
                    <el-form-item label="押金金额">
                        <el-input-number v-model="checkinForm.deposit" :min="0" :step="100"></el-input-number>
                        <span style="margin-left: 10px; color: #909399;">元</span>
                    </el-form-item>
                    
                    <el-form-item label="支付方式">
                        <el-radio-group v-model="checkinForm.payMethod">
                            <el-radio label="cash">现金</el-radio>
                            <el-radio label="wechat">微信支付</el-radio>
                            <el-radio label="alipay">支付宝</el-radio>
                            <el-radio label="card">刷卡</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    
                    <el-form-item label="备注">
                        <el-input type="textarea" v-model="checkinForm.remark" :rows="2" placeholder="特殊备注"></el-input>
                    </el-form-item>
                    
                    <el-form-item>
                        <el-button type="primary" size="large" @click="confirmCheckin" :loading="checkingIn" icon="el-icon-check">
                            确认入住
                        </el-button>
                        <el-button size="large" @click="clearSelection">取消</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
            
            <div v-else>
                <div class="search-bar">
                    <h4 style="margin-bottom: 10px;"><i class="el-icon-document"></i> 待入住订单列表</h4>
                </div>
                <div class="table-container">
                    <el-table :data="pendingOrders" border stripe>
                        <el-table-column prop="id" label="订单号" width="150"></el-table-column>
                        <el-table-column prop="roomName" label="房型"></el-table-column>
                        <el-table-column prop="guestName" label="入住人" width="100"></el-table-column>
                        <el-table-column prop="phone" label="手机号" width="120"></el-table-column>
                        <el-table-column prop="checkinDate" label="入住日期" width="120"></el-table-column>
                        <el-table-column prop="price" label="金额" width="100">
                            <template slot-scope="scope">
                                <span style="color: #f56c6c;">¥{{ scope.row.price }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="状态" width="100">
                            <template slot-scope="scope">
                                <el-tag type="warning" size="small">待入住</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="120" fixed="right">
                            <template slot-scope="scope">
                                <el-button type="primary" size="mini" @click="selectOrder(scope.row)" icon="el-icon-edit">
                                    办理入住
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                
                <el-empty v-if="pendingOrders.length === 0" description="暂无待入住订单" style="margin-top: 50px;"></el-empty>
            </div>
        </div>
    `,
    data() {
        return {
            searchKeyword: '',
            selectedOrder: null,
            checkinForm: {
                roomNumber: '',
                deposit: 200,
                payMethod: 'wechat',
                remark: ''
            },
            idVerified: false,
            checkingIn: false,
            rules: {
                roomNumber: [{ required: true, message: '请输入房间号', trigger: 'blur' }]
            }
        };
    },
    computed: {
        pendingOrders() {
            let orders = this.$root.orders.filter(o => o.status === 'pending' || o.status === 'confirmed');
            if (this.searchKeyword) {
                orders = orders.filter(o => 
                    o.id.includes(this.searchKeyword) || 
                    o.guestName.includes(this.searchKeyword) || 
                    o.phone.includes(this.searchKeyword)
                );
            }
            return orders;
        }
    },
    methods: {
        searchOrder() {
            if (!this.searchKeyword) {
                this.$message.info('请输入搜索条件');
            }
        },
        selectOrder(order) {
            this.selectedOrder = order;
            this.idVerified = false;
        },
        clearSelection() {
            this.selectedOrder = null;
            this.searchKeyword = '';
        },
        verifyIdCard() {
            this.$message.success('身份证信息读取成功');
            this.idVerified = true;
        },
        confirmCheckin() {
            this.$refs.checkinForm.validate((valid) => {
                if (valid) {
                    this.checkingIn = true;
                    setTimeout(() => {
                        this.$root.updateOrderStatus(this.selectedOrder.id, 'checkedin', {
                            roomNumber: this.checkinForm.roomNumber,
                            deposit: this.checkinForm.deposit
                        });
                        this.$message.success('入住办理成功！房间号：' + this.checkinForm.roomNumber);
                        this.checkingIn = false;
                        this.clearSelection();
                    }, 1000);
                }
            });
        }
    }
};