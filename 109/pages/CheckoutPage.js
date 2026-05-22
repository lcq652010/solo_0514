const CheckoutPage = {
    template: `
        <div class="page-container">
            <div class="page-header">
                <h2>💰 退房结算</h2>
                <p>为入住客人办理退房和费用结算</p>
            </div>
            
            <div class="search-bar">
                <el-row :gutter="20">
                    <el-col :span="8">
                        <el-input v-model="searchKeyword" placeholder="输入房间号/订单号搜索" clearable>
                            <el-button slot="append" icon="el-icon-search" @click="searchOrder">搜索</el-button>
                        </el-input>
                    </el-col>
                </el-row>
            </div>
            
            <el-card class="card-shadow" v-if="selectedOrder">
                <div slot="header" style="display: flex; justify-content: space-between; align-items: center;">
                    <span>📄 退房信息确认</span>
                    <el-tag type="primary">入住中</el-tag>
                </div>
                
                <el-descriptions :column="2" border>
                    <el-descriptions-item label="订单号">{{ selectedOrder.id }}</el-descriptions-item>
                    <el-descriptions-item label="房间号">{{ selectedOrder.roomNumber }}</el-descriptions-item>
                    <el-descriptions-item label="房型">{{ selectedOrder.roomName }}</el-descriptions-item>
                    <el-descriptions-item label="入住人">{{ selectedOrder.guestName }}</el-descriptions-item>
                    <el-descriptions-item label="预订入住">{{ selectedOrder.checkinDate }}</el-descriptions-item>
                    <el-descriptions-item label="预订退房">{{ selectedOrder.checkoutDate }}</el-descriptions-item>
                    <el-descriptions-item label="实际入住">
                        <el-date-picker v-model="actualCheckin" type="date" placeholder="实际入住日期" size="small" style="width: 140px;"></el-date-picker>
                    </el-descriptions-item>
                    <el-descriptions-item label="实际退房">
                        <el-date-picker v-model="actualCheckout" type="date" placeholder="实际退房日期" size="small" style="width: 140px;"></el-date-picker>
                    </el-descriptions-item>
                    <el-descriptions-item label="实际入住天数">
                        <span style="color: #409eff; font-weight: 600;">{{ actualDays }} 晚</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="房型单价">
                        <span style="color: #f56c6c; font-weight: 600;">¥{{ roomPrice }}/晚</span>
                    </el-descriptions-item>
                    <el-descriptions-item label="押金">¥{{ selectedOrder.deposit || 200 }}</el-descriptions-item>
                </el-descriptions>
                
                <el-divider content-position="left">消费明细</el-divider>
                
                <el-table :data="billItems" border style="margin: 20px 0;">
                    <el-table-column prop="name" label="费用项目"></el-table-column>
                    <el-table-column label="数量" width="100" align="center">
                        <template slot-scope="scope">
                            <el-input-number v-if="scope.$index > 0" v-model="scope.row.count" :min="0" size="small" @change="updateBillItemAmount(scope.$index)"></el-input-number>
                            <span v-else>{{ scope.row.count }}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="price" label="单价" width="120" align="center">
                        <template slot-scope="scope">¥{{ scope.row.price }}</template>
                    </el-table-column>
                    <el-table-column prop="amount" label="金额" width="120" align="center">
                        <template slot-scope="scope">¥{{ scope.row.amount }}</template>
                    </el-table-column>
                </el-table>
                
                <div style="background: #f5f7fa; padding: 20px; border-radius: 4px;">
                    <el-row :gutter="20">
                        <el-col :span="8">
                            <div class="amount-label">房费 ({{ actualDays || 0 }}晚 × ¥{{ roomPrice }})</div>
                            <div style="font-size: 18px; color: #303133; font-weight: 600;">¥{{ calculatedRoomFee }}</div>
                        </el-col>
                        <el-col :span="8">
                            <div class="amount-label">其他消费</div>
                            <div style="font-size: 18px; color: #e6a23c;">¥{{ otherAmount }}</div>
                        </el-col>
                        <el-col :span="8">
                            <div class="amount-label">应付总额</div>
                            <div class="amount-display">¥{{ totalAmount }}</div>
                        </el-col>
                    </el-row>
                    <el-divider></el-divider>
                    <el-row :gutter="20">
                        <el-col :span="8">
                            <div class="amount-label">已收押金</div>
                            <div style="font-size: 18px; color: #67c23a;">¥{{ selectedOrder.deposit || 200 }}</div>
                        </el-col>
                        <el-col :span="8">
                            <div class="amount-label">优惠减免</div>
                            <el-input-number v-model="discount" :min="0" :max="totalAmount" size="small"></el-input-number>
                        </el-col>
                        <el-col :span="8">
                            <div class="amount-label">实收金额</div>
                            <div class="amount-display">¥{{ actualPay }}</div>
                        </el-col>
                    </el-row>
                </div>
                
                <el-form :model="checkoutForm" label-width="100px" style="margin-top: 20px;">
                    <el-form-item label="支付方式">
                        <el-radio-group v-model="checkoutForm.payMethod">
                            <el-radio label="cash">现金</el-radio>
                            <el-radio label="wechat">微信支付</el-radio>
                            <el-radio label="alipay">支付宝</el-radio>
                            <el-radio label="card">刷卡</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="备注">
                        <el-input type="textarea" v-model="checkoutForm.remark" :rows="2" placeholder="特殊备注"></el-input>
                    </el-form-item>
                </el-form>
                
                <div style="text-align: center; margin-top: 20px;">
                    <el-checkbox v-model="printInvoice">打印发票</el-checkbox>
                    <el-divider direction="vertical"></el-divider>
                    <el-checkbox v-model="returnDeposit">退还押金</el-checkbox>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <el-button type="primary" size="large" :loading="checkingOut" @click="confirmCheckout" icon="el-icon-check">
                        确认退房结算
                    </el-button>
                    <el-button size="large" @click="clearSelection">取消</el-button>
                </div>
            </el-card>
            
            <div v-else>
                <div class="search-bar">
                    <h4 style="margin-bottom: 10px;"><i class="el-icon-date"></i> 在住客人列表</h4>
                </div>
                <div class="table-container">
                    <el-table :data="checkedinOrders" border stripe>
                        <el-table-column prop="id" label="订单号" width="140"></el-table-column>
                        <el-table-column prop="roomNumber" label="房间号" width="100">
                            <template slot-scope="scope">
                                <el-tag type="success" size="small">{{ scope.row.roomNumber }}</el-tag>
                            </template>
                        </el-table-column>
                        <el-table-column prop="roomName" label="房型"></el-table-column>
                        <el-table-column prop="guestName" label="入住人" width="100"></el-table-column>
                        <el-table-column prop="checkinDate" label="入住日期" width="120"></el-table-column>
                        <el-table-column prop="checkoutDate" label="预计退房" width="120"></el-table-column>
                        <el-table-column prop="price" label="房费" width="100">
                            <template slot-scope="scope">
                                <span style="color: #f56c6c;">¥{{ scope.row.price }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="操作" width="120" fixed="right">
                            <template slot-scope="scope">
                                <el-button type="primary" size="mini" @click="selectOrder(scope.row)" icon="el-icon-s-finance">
                                    退房结算
                                </el-button>
                            </template>
                        </el-table-column>
                    </el-table>
                </div>
                
                <el-empty v-if="checkedinOrders.length === 0" description="暂无在住客人" style="margin-top: 50px;"></el-empty>
            </div>
        </div>
    `,
    data() {
        return {
            searchKeyword: '',
            selectedOrder: null,
            checkingOut: false,
            discount: 0,
            printInvoice: false,
            returnDeposit: true,
            actualCheckin: '',
            actualCheckout: '',
            checkoutForm: {
                payMethod: 'wechat',
                remark: ''
            },
            billItems: [
                { name: '房费', count: 1, price: 0, amount: 0 },
                { name: '迷你吧消费', count: 0, price: 50, amount: 0 },
                { name: '洗衣服务', count: 0, price: 30, amount: 0 }
            ]
        };
    },
    computed: {
        checkedinOrders() {
            let orders = this.$root.orders.filter(o => o.status === 'checkedin');
            if (this.searchKeyword) {
                orders = orders.filter(o => 
                    o.id.includes(this.searchKeyword) || 
                    (o.roomNumber && o.roomNumber.includes(this.searchKeyword))
                );
            }
            return orders;
        },
        roomPrice() {
            if (!this.selectedOrder) return 0;
            return this.$root.getRoomPrice(this.selectedOrder.roomName);
        },
        actualDays() {
            if (!this.actualCheckin || !this.actualCheckout) return 0;
            const start = new Date(this.actualCheckin).getTime();
            const end = new Date(this.actualCheckout).getTime();
            return Math.max(0, Math.ceil((end - start) / (1000 * 60 * 60 * 24)));
        },
        calculatedRoomFee() {
            return this.roomPrice * this.actualDays;
        },
        otherAmount() {
            return this.billItems.slice(1).reduce((sum, item) => sum + item.amount, 0);
        },
        totalAmount() {
            return this.calculatedRoomFee + this.otherAmount;
        },
        actualPay() {
            return Math.max(0, this.totalAmount - (this.selectedOrder?.deposit || 200) - this.discount);
        }
    },
    mounted() {
        if (this.$route.query.orderId) {
            const order = this.$root.orders.find(o => o.id === this.$route.query.orderId);
            if (order) {
                this.selectOrder(order);
            }
        }
    },
    watch: {
        actualDays() {
            this.updateRoomFee();
        },
        roomPrice() {
            this.updateRoomFee();
        },
        billItems: {
            deep: true,
            handler() {
                // 账单变化时 computed 会自动重新计算
            }
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
            this.actualCheckin = order.checkinDate;
            this.actualCheckout = order.checkoutDate;
            this.discount = 0;
            this.$nextTick(() => {
                this.updateRoomFee();
            });
        },
        updateRoomFee() {
            this.billItems[0].count = this.actualDays || 0;
            this.billItems[0].price = this.roomPrice;
            this.billItems[0].amount = this.calculatedRoomFee;
        },
        updateBillItemAmount(index) {
            this.billItems[index].amount = this.billItems[index].price * this.billItems[index].count;
        },
        clearSelection() {
            this.selectedOrder = null;
            this.searchKeyword = '';
        },
        confirmCheckout() {
            this.$confirm('确认退房并完成结算吗？', '提示', { type: 'warning' }).then(() => {
                this.checkingOut = true;
                setTimeout(() => {
                    this.$root.updateOrderStatus(this.selectedOrder.id, 'completed', {
                        checkoutTime: new Date().toLocaleString('zh-CN'),
                        totalAmount: this.totalAmount,
                        actualPay: this.actualPay
                    });
                    this.$message.success('退房结算完成！感谢您的光临！');
                    if (this.printInvoice) {
                        this.$message.info('发票已打印');
                    }
                    this.checkingOut = false;
                    this.clearSelection();
                }, 1500);
            });
        }
    }
};