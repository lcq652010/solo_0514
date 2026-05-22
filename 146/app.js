Vue.component('order-page', {
    template: `
        <div class="order-page">
            <el-card class="order-form-card">
                <div slot="header">
                    <span>貔貅摆件定制订单</span>
                </div>
                
                <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
                    
                    <div class="form-section">
                        <div class="form-section-title">客户信息</div>
                        <el-form-item label="客户姓名" prop="customerName">
                            <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
                        </el-form-item>
                        <el-form-item label="联系电话" prop="phone">
                            <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
                        </el-form-item>
                    </div>
                    
                    <div class="form-section">
                        <div class="form-section-title">木材选择</div>
                        <el-form-item label="木材种类" prop="woodType">
                            <el-select v-model="orderForm.woodType" placeholder="请选择木材种类" style="width: 100%;">
                                <el-option 
                                    v-for="wood in woodOptions" 
                                    :key="wood.value" 
                                    :label="wood.label" 
                                    :value="wood.value"
                                >
                                    <div class="wood-option">
                                        <div class="wood-color" :style="{background: wood.color}"></div>
                                        <span>{{ wood.label }}</span>
                                        <span class="price-tag">+¥{{ wood.price }}</span>
                                    </div>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                    
                    <div class="form-section">
                        <div class="form-section-title">规格参数</div>
                        <el-form-item label="摆件高度 (cm)" prop="height">
                            <el-input-number 
                                v-model="orderForm.height" 
                                :min="15" 
                                :max="150" 
                                :step="5"
                                style="width: 100%;"
                            ></el-input-number>
                            <div style="color: #666; font-size: 12px; margin-top: 5px;">
                                高度范围：15-150cm，建议 20-50cm，每增加10cm加价¥200
                            </div>
                        </el-form-item>
                    </div>
                    
                    <div class="form-section">
                        <div class="form-section-title">造型设计</div>
                        <el-form-item label="造型姿态" prop="pose">
                            <el-radio-group v-model="orderForm.pose">
                                <el-radio-button 
                                    v-for="pose in poseOptions" 
                                    :key="pose.value" 
                                    :label="pose.value"
                                >
                                    {{ pose.label }}
                                </el-radio-button>
                            </el-radio-group>
                        </el-form-item>
                    </div>
                    
                    <div class="form-section">
                        <div class="form-section-title">工艺要求</div>
                        <el-form-item label="雕刻精细度" prop="detailLevel">
                            <el-select v-model="orderForm.detailLevel" placeholder="请选择雕刻精细度" style="width: 100%;">
                                <el-option 
                                    v-for="level in detailOptions" 
                                    :key="level.value" 
                                    :label="level.label" 
                                    :value="level.value"
                                >
                                    <span>{{ level.label }}</span>
                                    <span class="price-tag">+¥{{ level.price }}</span>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </div>
                    
                    <div class="form-section">
                        <div class="form-section-title">底座选择</div>
                        <el-form-item label="底座样式" prop="baseStyle">
                            <el-radio-group v-model="orderForm.baseStyle">
                                <el-radio 
                                    v-for="base in baseOptions" 
                                    :key="base.value" 
                                    :label="base.value"
                                >
                                    {{ base.label }}
                                    <span class="price-tag" v-if="base.price > 0">+¥{{ base.price }}</span>
                                </el-radio>
                            </el-radio-group>
                        </el-form-item>
                    </div>
                    
                    <div class="form-section">
                        <div class="form-section-title">备注信息</div>
                        <el-form-item label="特殊要求">
                            <el-input 
                                type="textarea" 
                                v-model="orderForm.remark" 
                                :rows="3"
                                placeholder="如有其他特殊要求请在此说明..."
                            ></el-input>
                        </el-form-item>
                    </div>
                    
                    <el-form-item>
                        <div style="text-align: center; margin-bottom: 15px;">
                            <span style="font-size: 18px; color: #8B4513;">
                                预估总价：<strong style="font-size: 24px; color: #e74c3c;">¥{{ totalPrice }}</strong>
                            </span>
                        </div>
                        <el-button 
                            type="primary" 
                            class="submit-btn" 
                            @click="submitOrder"
                            :loading="submitting"
                        >
                            提交订单
                        </el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </div>
    `,
    data() {
        return {
            submitting: false,
            orderForm: {
                customerName: '',
                phone: '',
                woodType: '',
                height: 30,
                pose: '',
                detailLevel: '',
                baseStyle: '',
                remark: ''
            },
            rules: {
                customerName: [
                    { required: true, message: '请输入客户姓名', trigger: 'blur' }
                ],
                phone: [
                    { required: true, message: '请输入联系电话', trigger: 'blur' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
                ],
                woodType: [
                    { required: true, message: '请选择木材种类', trigger: 'change' }
                ],
                height: [
                    { required: true, message: '请输入摆件高度', trigger: 'blur' },
                    { type: 'number', min: 15, max: 150, message: '摆件高度需在 15-150cm 之间', trigger: 'blur' }
                ],
                pose: [
                    { required: true, message: '请选择造型姿态', trigger: 'change' }
                ],
                detailLevel: [
                    { required: true, message: '请选择雕刻精细度', trigger: 'change' }
                ],
                baseStyle: [
                    { required: true, message: '请选择底座样式', trigger: 'change' }
                ]
            },
            woodOptions: [
                { label: '樟木', value: 'zhangmu', color: '#8B7355', price: 800 },
                { label: '红木', value: 'hongmu', color: '#8B0000', price: 1500 },
                { label: '紫檀木', value: 'zitan', color: '#4A2C2A', price: 3000 },
                { label: '黄花梨', value: 'huali', color: '#DEB887', price: 2500 },
                { label: '鸡翅木', value: 'jichi', color: '#654321', price: 1200 }
            ],
            poseOptions: [
                { label: '端坐纳福', value: 'sit' },
                { label: '昂首望天', value: 'look' },
                { label: '行走招财', value: 'walk' },
                { label: '卧姿守财', value: 'lay' }
            ],
            detailOptions: [
                { label: '标准工艺', value: 'standard', price: 0 },
                { label: '精细雕刻', value: 'fine', price: 500 },
                { label: '大师级精雕', value: 'master', price: 1500 }
            ],
            baseOptions: [
                { label: '无底座', value: 'none', price: 0 },
                { label: '圆形实木底座', value: 'round', price: 150 },
                { label: '方形祥云底座', value: 'square', price: 200 },
                { label: '莲花宝座底座', value: 'lotus', price: 350 }
            ]
        };
    },
    computed: {
        totalPrice() {
            let price = 0;
            const wood = this.woodOptions.find(w => w.value === this.orderForm.woodType);
            if (wood) price += wood.price;
            
            const heightExtra = Math.floor((this.orderForm.height - 20) / 10) * 200;
            if (heightExtra > 0) price += heightExtra;
            
            const detail = this.detailOptions.find(d => d.value === this.orderForm.detailLevel);
            if (detail) price += detail.price;
            
            const base = this.baseOptions.find(b => b.value === this.orderForm.baseStyle);
            if (base) price += base.price;
            
            return Math.max(price, 800);
        }
    },
    methods: {
        submitOrder() {
            this.$refs.orderForm.validate((valid) => {
                if (valid) {
                    this.submitting = true;
                    setTimeout(() => {
                        const now = new Date().toLocaleString('zh-CN');
                        const order = {
                            id: 'ORD' + Date.now(),
                            ...this.orderForm,
                            status: '选料',
                            statusIndex: 0,
                            createTime: now,
                            totalPrice: this.totalPrice,
                            isNew: true,
                            operationLogs: [
                                {
                                    status: '选料',
                                    statusIndex: 0,
                                    operationTime: now,
                                    remark: '订单创建，开始选料工序'
                                }
                            ]
                        };
                        this.$emit('order-submitted', order);
                        this.$message.success('订单提交成功！');
                        this.resetForm();
                        this.submitting = false;
                        this.$emit('navigate-to-admin');
                    }, 1000);
                }
            });
        },
        resetForm() {
            this.$refs.orderForm.resetFields();
            this.orderForm.height = 30;
        }
    }
});

Vue.component('admin-page', {
    props: ['orders'],
    template: `
        <div class="admin-page">
            <el-card class="admin-card">
                <div slot="header">
                    <span>订单管理中心</span>
                    <span style="float: right; font-size: 14px; font-weight: normal;">
                        共 {{ orders.length }} 个订单
                    </span>
                </div>
                
                <el-table 
                    :data="orders" 
                    border 
                    style="width: 100%"
                    :expand-row-keys="expandRows"
                    @expand-change="handleExpandChange"
                    :row-class-name="tableRowClassName"
                >
                    <el-table-column type="expand">
                        <template slot-scope="props">
                            <div class="order-detail-row">
                                <div class="order-detail-item">
                                    <span class="order-detail-label">客户姓名：</span>
                                    <span class="order-detail-value">{{ props.row.customerName }}</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">联系电话：</span>
                                    <span class="order-detail-value">{{ props.row.phone }}</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">木材种类：</span>
                                    <span class="order-detail-value">{{ getWoodLabel(props.row.woodType) }}</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">摆件高度：</span>
                                    <span class="order-detail-value">{{ props.row.height }} cm</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">造型姿态：</span>
                                    <span class="order-detail-value">{{ getPoseLabel(props.row.pose) }}</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">雕刻精细度：</span>
                                    <span class="order-detail-value">{{ getDetailLabel(props.row.detailLevel) }}</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">底座样式：</span>
                                    <span class="order-detail-value">{{ getBaseLabel(props.row.baseStyle) }}</span>
                                </div>
                                <div class="order-detail-item" v-if="props.row.remark">
                                    <span class="order-detail-label">特殊要求：</span>
                                    <span class="order-detail-value">{{ props.row.remark }}</span>
                                </div>
                                <div class="order-detail-item">
                                    <span class="order-detail-label">订单总价：</span>
                                    <span class="order-detail-value" style="color: #e74c3c; font-size: 18px;">
                                        ¥{{ props.row.totalPrice }}
                                    </span>
                                </div>
                                <div class="operation-logs-section" v-if="props.row.operationLogs && props.row.operationLogs.length > 0">
                                    <div class="operation-logs-title">操作日志</div>
                                    <div class="operation-log-item" v-for="(log, index) in props.row.operationLogs" :key="index">
                                        <span class="log-time">{{ log.operationTime }}</span>
                                        <span class="log-status">{{ log.status }}</span>
                                        <span class="log-remark">{{ log.remark }}</span>
                                    </div>
                                </div>
                            </div>
                        </template>
                    </el-table-column>
                    
                    <el-table-column prop="id" label="订单编号" width="160" align="center"></el-table-column>
                    <el-table-column prop="customerName" label="客户姓名" width="100" align="center"></el-table-column>
                    <el-table-column prop="woodType" label="木材" width="90" align="center">
                        <template slot-scope="scope">
                            {{ getWoodLabel(scope.row.woodType) }}
                        </template>
                    </el-table-column>
                    <el-table-column prop="height" label="高度(cm)" width="90" align="center"></el-table-column>
                    <el-table-column label="当前状态" width="120" align="center">
                        <template slot-scope="scope">
                            <el-tag 
                                size="medium"
                                class="status-tag"
                                :class="'status-tag-' + scope.row.status"
                            >
                                {{ scope.row.status }}
                            </el-tag>
                        </template>
                    </el-table-column>
                    <el-table-column prop="createTime" label="下单时间" width="180" align="center"></el-table-column>
                    <el-table-column label="生产流程" align="center">
                        <template slot-scope="scope">
                            <el-steps 
                                :active="scope.row.statusIndex" 
                                finish-status="success"
                                size="small"
                                direction="horizontal"
                                style="display: flex; justify-content: center;"
                            >
                                <el-step 
                                    v-for="(status, index) in statusList" 
                                    :key="index"
                                    :title="status"
                                    style="flex: 1;"
                                ></el-step>
                            </el-steps>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="200" align="center">
                        <template slot-scope="scope">
                            <el-button 
                                type="primary" 
                                size="small" 
                                icon="el-icon-check"
                                @click="updateStatus(scope.row)"
                                :disabled="scope.row.statusIndex >= statusList.length - 1"
                                style="margin-bottom: 5px;"
                            >
                                下一流程
                            </el-button>
                            <el-button 
                                v-if="scope.row.isNew"
                                type="warning" 
                                size="small" 
                                icon="el-icon-bell"
                                @click="clearNewFlag(scope.row)"
                            >
                                取消标记
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                
                <div v-if="orders.length === 0" class="empty-state">
                    <i class="el-icon-document"></i>
                    <p>暂无订单数据</p>
                </div>
            </el-card>
        </div>
    `,
    data() {
        return {
            expandRows: [],
            statusList: ['选料', '开料', '粗胚', '精雕', '打磨', '打蜡', '装配', '完工'],
            woodOptions: [
                { label: '樟木', value: 'zhangmu' },
                { label: '红木', value: 'hongmu' },
                { label: '紫檀木', value: 'zitan' },
                { label: '黄花梨', value: 'huali' },
                { label: '鸡翅木', value: 'jichi' }
            ],
            poseOptions: [
                { label: '端坐纳福', value: 'sit' },
                { label: '昂首望天', value: 'look' },
                { label: '行走招财', value: 'walk' },
                { label: '卧姿守财', value: 'lay' }
            ],
            detailOptions: [
                { label: '标准工艺', value: 'standard' },
                { label: '精细雕刻', value: 'fine' },
                { label: '大师级精雕', value: 'master' }
            ],
            baseOptions: [
                { label: '无底座', value: 'none' },
                { label: '圆形实木底座', value: 'round' },
                { label: '方形祥云底座', value: 'square' },
                { label: '莲花宝座底座', value: 'lotus' }
            ]
        };
    },
    methods: {
        handleExpandChange(row, expandedRows) {
            this.expandRows = expandedRows;
        },
        getWoodLabel(value) {
            const wood = this.woodOptions.find(w => w.value === value);
            return wood ? wood.label : value;
        },
        getPoseLabel(value) {
            const pose = this.poseOptions.find(p => p.value === value);
            return pose ? pose.label : value;
        },
        getDetailLabel(value) {
            const detail = this.detailOptions.find(d => d.value === value);
            return detail ? detail.label : value;
        },
        getBaseLabel(value) {
            const base = this.baseOptions.find(b => b.value === value);
            return base ? base.label : value;
        },
        tableRowClassName({ row }) {
            return row.isNew ? 'new-order-row' : '';
        },
        clearNewFlag(row) {
            this.$confirm('确认取消该订单的新标记吗？', '确认操作', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                this.$emit('clear-new-flag', row.id);
                this.$message.success('新订单标记已取消！');
            }).catch(() => {});
        },
        updateStatus(row) {
            if (row.statusIndex >= this.statusList.length - 1) {
                this.$message.warning('订单已完工，无法继续更新状态！');
                return;
            }
            
            const nextIndex = row.statusIndex + 1;
            const nextStatus = this.statusList[nextIndex];
            
            if (nextIndex !== row.statusIndex + 1) {
                this.$message.error('状态更新异常，不允许跳步更新！');
                return;
            }
            
            this.$confirm(
                `确认将订单状态从"${row.status}"更新为"${nextStatus}"吗？\n（工序必须依次递进，不可跳步或回改）`,
                '确认操作',
                {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }
            ).then(() => {
                this.$emit('status-updated', row.id, nextIndex, nextStatus);
                this.$message.success('状态更新成功！');
            }).catch(() => {});
        }
    }
});

new Vue({
    el: '#app',
    data: {
        currentPage: 'order',
        orders: [],
        statusList: ['选料', '开料', '粗胚', '精雕', '打磨', '打蜡', '装配', '完工']
    },
    created() {
        this.loadOrders();
    },
    methods: {
        handleMenuSelect(index) {
            this.currentPage = index;
        },
        handleOrderSubmitted(order) {
            this.orders.unshift(order);
            this.saveOrders();
            this.$nextTick(() => {
                this.currentPage = 'admin';
            });
        },
        handleNavigateToAdmin() {
            this.currentPage = 'admin';
        },
        handleStatusUpdated(orderId, targetIndex, targetStatus) {
            const order = this.orders.find(o => o.id === orderId);
            if (!order) {
                this.$message.error('订单不存在！');
                return;
            }
            
            if (targetIndex !== order.statusIndex + 1) {
                this.$message.error('不允许跳步或回改状态，必须依次递进！');
                return;
            }
            
            if (targetIndex < 0 || targetIndex >= this.statusList.length) {
                this.$message.error('状态索引超出有效范围！');
                return;
            }
            
            if (this.statusList[targetIndex] !== targetStatus) {
                this.$message.error('状态名称与索引不匹配！');
                return;
            }
            
            order.statusIndex = targetIndex;
            order.status = targetStatus;
            
            if (!order.operationLogs) {
                order.operationLogs = [];
            }
            order.operationLogs.push({
                status: targetStatus,
                statusIndex: targetIndex,
                operationTime: new Date().toLocaleString('zh-CN'),
                remark: `工序从"${this.statusList[targetIndex - 1]}"变更为"${targetStatus}"`
            });
            
            this.saveOrders();
            
            this.orders = [...this.orders];
        },
        handleClearNewFlag(orderId) {
            const order = this.orders.find(o => o.id === orderId);
            if (order) {
                order.isNew = false;
                this.saveOrders();
                this.orders = [...this.orders];
            }
        },
        saveOrders() {
            localStorage.setItem('woodCarvingOrders', JSON.stringify(this.orders));
        },
        loadOrders() {
            const saved = localStorage.getItem('woodCarvingOrders');
            if (saved) {
                const orders = JSON.parse(saved);
                this.orders = orders.map(order => ({
                    ...order,
                    isNew: order.isNew !== undefined ? order.isNew : false,
                    operationLogs: order.operationLogs || [
                        {
                            status: order.status || '选料',
                            statusIndex: order.statusIndex || 0,
                            operationTime: order.createTime,
                            remark: '历史订单数据'
                        }
                    ]
                }));
            }
        }
    }
});
