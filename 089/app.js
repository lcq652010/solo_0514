Vue.component('order-form', {
    template: `
        <div class="order-form-container">
            <h2 class="page-title">茶宠定制下单</h2>
            <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="100px">
                <div class="form-layout">
                    <div class="form-left">
                        <el-form-item label="铁艺材质" prop="material">
                            <el-select v-model="orderForm.material" placeholder="请选择铁艺材质">
                                <el-option label="黑铁" value="黑铁"></el-option>
                                <el-option label="熟铁" value="熟铁"></el-option>
                                <el-option label="铸铁" value="铸铁"></el-option>
                                <el-option label="不锈钢" value="不锈钢"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="茶宠造型" prop="shape">
                            <el-input 
                                v-model="orderForm.shape" 
                                placeholder="请描述您想要的茶宠造型，如：貔貅、金蟾、狮子等"
                                type="textarea"
                                :rows="3">
                            </el-input>
                        </el-form-item>
                        <el-form-item label="高度 (cm)" prop="height">
                            <el-input-number 
                                v-model="orderForm.height" 
                                :min="3" 
                                :max="30" 
                                :step="1"
                                controls-position="right">
                            </el-input-number>
                        </el-form-item>
                        <el-form-item label="宽度 (cm)" prop="width">
                            <el-input-number 
                                v-model="orderForm.width" 
                                :min="3" 
                                :max="30" 
                                :step="1"
                                controls-position="right">
                            </el-input-number>
                        </el-form-item>
                    </div>
                    <div class="form-right">
                        <el-form-item label="表面处理" prop="surfaceTreatment">
                            <el-radio-group v-model="orderForm.surfaceTreatment">
                                <el-radio label="磨砂">磨砂</el-radio>
                                <el-radio label="抛光">抛光</el-radio>
                                <el-radio label="做旧">做旧</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="联系人" prop="contactName">
                            <el-input v-model="orderForm.contactName" placeholder="请输入您的姓名"></el-input>
                        </el-form-item>
                        <el-form-item label="联系电话" prop="contactPhone">
                            <el-input v-model="orderForm.contactPhone" placeholder="请输入您的联系电话"></el-input>
                        </el-form-item>
                        <el-form-item label="订单留言" prop="message">
                            <el-input 
                                v-model="orderForm.message" 
                                placeholder="请输入其他要求或留言"
                                type="textarea"
                                :rows="4">
                            </el-input>
                        </el-form-item>
                    </div>
                </div>
                <div class="submit-section">
                    <el-button type="primary" size="large" @click="submitForm" :loading="submitting">
                        提交订单
                    </el-button>
                    <el-button size="large" @click="resetForm">重置</el-button>
                </div>
            </el-form>
        </div>
    `,
    data() {
        return {
            submitting: false,
            orderForm: {
                material: '',
                shape: '',
                height: 10,
                width: 10,
                surfaceTreatment: '',
                contactName: '',
                contactPhone: '',
                message: ''
            },
            rules: {
                material: [
                    { required: true, message: '请选择铁艺材质', trigger: 'change' }
                ],
                shape: [
                    { required: true, message: '请输入茶宠造型', trigger: 'blur' }
                ],
                height: [
                    { required: true, message: '请输入高度', trigger: 'blur' },
                    { type: 'number', min: 3, max: 30, message: '高度需在 3-30cm 之间', trigger: 'blur' }
                ],
                width: [
                    { required: true, message: '请输入宽度', trigger: 'blur' },
                    { type: 'number', min: 3, max: 30, message: '宽度需在 3-30cm 之间', trigger: 'blur' }
                ],
                surfaceTreatment: [
                    { required: true, message: '请选择表面处理方式', trigger: 'change' }
                ],
                contactName: [
                    { required: true, message: '请输入联系人姓名', trigger: 'blur' }
                ],
                contactPhone: [
                    { required: true, message: '请输入联系电话', trigger: 'blur' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
                ]
            }
        };
    },
    methods: {
        submitForm() {
            this.$refs.orderForm.validate((valid) => {
                if (valid) {
                    this.submitting = true;
                    setTimeout(() => {
                        this.$emit('submit-order', { ...this.orderForm });
                        this.submitting = false;
                        const self = this;
                        this.$alert('您的茶宠定制订单已提交成功，我们会尽快安排生产！', '订单提交成功', {
                            confirmButtonText: '确定',
                            type: 'success',
                            callback() {
                                self.resetForm();
                            }
                        });
                    }, 1000);
                }
            });
        },
        resetForm() {
            this.$refs.orderForm.resetFields();
        }
    }
});

Vue.component('admin-panel', {
    props: ['orders'],
    data() {
        return {
            statusOrder: ['下料', '折弯', '焊接', '打磨', '表面处理', '防锈', '完工'],
            operator: ''
        };
    },
    template: `
        <div class="admin-container">
            <h2 class="page-title">订单管理</h2>
            <div class="operator-section">
                <el-input 
                    v-model="operator" 
                    placeholder="请输入操作人姓名" 
                    style="width: 200px;"
                    size="small">
                </el-input>
                <span class="operator-tip">修改状态前请先输入操作人</span>
            </div>
            <el-table :data="orders" border style="width: 100%" class="order-table" v-if="orders.length > 0">
                <el-table-column prop="orderId" label="订单号" width="120"></el-table-column>
                <el-table-column prop="material" label="材质" width="100"></el-table-column>
                <el-table-column prop="shape" label="造型" width="150" show-overflow-tooltip></el-table-column>
                <el-table-column label="尺寸" width="100">
                    <template slot-scope="scope">
                        {{ scope.row.height }} × {{ scope.row.width }} cm
                    </template>
                </el-table-column>
                <el-table-column prop="surfaceTreatment" label="表面处理" width="100"></el-table-column>
                <el-table-column prop="contactName" label="联系人" width="100"></el-table-column>
                <el-table-column prop="contactPhone" label="电话" width="120"></el-table-column>
                <el-table-column label="生产状态" width="150">
                    <template slot-scope="scope">
                        <span class="status-badge" :class="'status-' + scope.row.status">
                            {{ scope.row.status }}
                        </span>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                    <template slot-scope="scope">
                        <el-select 
                            v-model="scope.row.tempStatus" 
                            size="small" 
                            placeholder="修改状态"
                            @change="updateStatus(scope.row)"
                            style="width: 120px;">
                            <el-option 
                                v-for="status in getAvailableStatuses(scope.row.status)" 
                                :key="status" 
                                :label="status" 
                                :value="status">
                            </el-option>
                        </el-select>
                        <el-button 
                            type="text" 
                            size="small" 
                            @click="showDetail(scope.row)">
                            详情
                        </el-button>
                    </template>
                </el-table-column>
            </el-table>
            <div class="empty-tip" v-else>
                暂无订单数据
            </div>
        </div>
    `,
    mounted() {
        this.orders.forEach(order => {
            this.$set(order, 'tempStatus', order.status);
        });
    },
    watch: {
        orders: {
            handler(newOrders) {
                newOrders.forEach(order => {
                    if (order.tempStatus === undefined) {
                        this.$set(order, 'tempStatus', order.status);
                    }
                });
            },
            deep: true
        }
    },
    methods: {
        getAvailableStatuses(currentStatus) {
            const currentIndex = this.statusOrder.indexOf(currentStatus);
            if (currentIndex === -1 || currentStatus === '完工') {
                return [currentStatus];
            }
            return this.statusOrder.slice(currentIndex, currentIndex + 2);
        },
        updateStatus(order) {
            if (!this.operator || this.operator.trim() === '') {
                this.$message.warning('请先输入操作人姓名');
                order.tempStatus = order.status;
                return;
            }
            
            const currentIndex = this.statusOrder.indexOf(order.status);
            const newIndex = this.statusOrder.indexOf(order.tempStatus);
            
            if (newIndex === -1) {
                this.$message.error('无效的状态');
                order.tempStatus = order.status;
                return;
            }
            
            if (newIndex < currentIndex) {
                this.$message.error('不能回退到之前的工序状态');
                order.tempStatus = order.status;
                return;
            }
            
            if (newIndex > currentIndex + 1) {
                this.$message.error(`生产工序必须按顺序推进，当前是"${order.status}"，下一步只能是"${this.statusOrder[currentIndex + 1]}"`);
                order.tempStatus = order.status;
                return;
            }
            
            order.status = order.tempStatus;
            this.$emit('update-status', order.orderId, order.status, this.operator.trim());
            this.$message.success(`订单 ${order.orderId} 状态已更新为：${order.status}（操作人：${this.operator.trim()}）`);
        },
        showDetail(order) {
            let historyHtml = '';
            if (order.statusHistory && order.statusHistory.length > 0) {
                historyHtml = '<div class="history-section"><h4 style="margin: 15px 0 10px 0; color: #606266;">状态变更历史：</h4>';
                order.statusHistory.forEach((item, index) => {
                    historyHtml += `
                        <div class="detail-row">
                            <span class="detail-label">${index + 1}. ${item.status}：</span>
                            <span class="detail-value">${item.operator} - ${item.time}</span>
                        </div>
                    `;
                });
                historyHtml += '</div>';
            }
            
            this.$alert(`
                <div class="detail-content">
                    <div class="detail-row">
                        <span class="detail-label">订单号：</span>
                        <span class="detail-value">${order.orderId}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">铁艺材质：</span>
                        <span class="detail-value">${order.material}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">茶宠造型：</span>
                        <span class="detail-value">${order.shape}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">尺寸：</span>
                        <span class="detail-value">${order.height} × ${order.width} cm</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">表面处理：</span>
                        <span class="detail-value">${order.surfaceTreatment}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">联系人：</span>
                        <span class="detail-value">${order.contactName}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">联系电话：</span>
                        <span class="detail-value">${order.contactPhone}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">订单留言：</span>
                        <span class="detail-value">${order.message || '无'}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">当前状态：</span>
                        <span class="detail-value">${order.status}</span>
                    </div>
                    ${historyHtml}
                </div>
            `, '订单详情', {
                dangerouslyUseHTMLString: true,
                confirmButtonText: '确定'
            });
        }
    }
});

new Vue({
    el: '#app',
    data: {
        currentPage: 'order',
        currentOperator: '管理员',
        orders: [
            {
                orderId: 'ORD001',
                material: '黑铁',
                shape: '貔貅造型，头部微抬',
                height: 12,
                width: 8,
                surfaceTreatment: '做旧',
                contactName: '张先生',
                contactPhone: '13800138001',
                message: '希望做工精细一些',
                status: '焊接',
                tempStatus: '焊接',
                createTime: '2024-01-15 10:30:00',
                statusHistory: [
                    { status: '下料', operator: '张三', time: '2024-01-15 09:00:00' },
                    { status: '折弯', operator: '李四', time: '2024-01-15 10:00:00' },
                    { status: '焊接', operator: '王五', time: '2024-01-15 10:30:00' }
                ]
            },
            {
                orderId: 'ORD002',
                material: '熟铁',
                shape: '金蟾造型，三足鼎立',
                height: 10,
                width: 10,
                surfaceTreatment: '抛光',
                contactName: '李女士',
                contactPhone: '13800138002',
                message: '',
                status: '下料',
                tempStatus: '下料',
                createTime: '2024-01-16 14:20:00',
                statusHistory: [
                    { status: '下料', operator: '赵六', time: '2024-01-16 14:20:00' }
                ]
            },
            {
                orderId: 'ORD003',
                material: '不锈钢',
                shape: '小狮子造型，可爱风格',
                height: 8,
                width: 6,
                surfaceTreatment: '磨砂',
                contactName: '王先生',
                contactPhone: '13800138003',
                message: '作为茶宠赠送朋友',
                status: '完工',
                tempStatus: '完工',
                createTime: '2024-01-10 09:15:00',
                statusHistory: [
                    { status: '下料', operator: '张三', time: '2024-01-10 09:15:00' },
                    { status: '折弯', operator: '李四', time: '2024-01-10 10:00:00' },
                    { status: '焊接', operator: '王五', time: '2024-01-10 11:00:00' },
                    { status: '打磨', operator: '赵六', time: '2024-01-10 14:00:00' },
                    { status: '表面处理', operator: '钱七', time: '2024-01-10 15:00:00' },
                    { status: '防锈', operator: '孙八', time: '2024-01-10 16:00:00' },
                    { status: '完工', operator: '周九', time: '2024-01-10 17:00:00' }
                ]
            }
        ]
    },
    methods: {
        handleSubmitOrder(orderData) {
            const newOrder = {
                orderId: 'ORD' + String(this.orders.length + 1).padStart(3, '0'),
                ...orderData,
                status: '下料',
                tempStatus: '下料',
                createTime: new Date().toLocaleString(),
                statusHistory: [
                    { status: '下料', operator: '系统', time: new Date().toLocaleString() }
                ]
            };
            this.orders.unshift(newOrder);
        },
        handleUpdateStatus(orderId, newStatus, operator) {
            const order = this.orders.find(o => o.orderId === orderId);
            if (order) {
                order.status = newStatus;
                order.statusHistory.push({
                    status: newStatus,
                    operator: operator,
                    time: new Date().toLocaleString()
                });
            }
        }
    }
});