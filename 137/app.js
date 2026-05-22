Vue.component('order-page', {
    template: `
        <div class="order-card">
            <h2 class="card-title">📝 折扇定制下单</h2>
            
            <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
                
                <div class="form-section">
                    <h3 class="section-title">竹骨材质选择 <span class="required-mark">*</span></h3>
                    <el-form-item prop="bambooMaterial">
                        <div class="radio-group-flex">
                            <div 
                                v-for="material in bambooMaterials" 
                                :key="material.value"
                                class="radio-item"
                                :class="{ active: orderForm.bambooMaterial === material.value }"
                                @click="selectBambooMaterial(material.value)"
                            >
                                <span class="icon">{{ material.icon }}</span>
                                <span class="label">{{ material.label }}</span>
                            </div>
                        </div>
                    </el-form-item>
                </div>

                <div class="form-section">
                    <h3 class="section-title">扇面款式选择 <span class="required-mark">*</span></h3>
                    <el-form-item prop="fanStyle">
                        <div class="radio-group-flex">
                            <div 
                                v-for="style in fanStyles" 
                                :key="style.value"
                                class="radio-item"
                                :class="{ active: orderForm.fanStyle === style.value }"
                                @click="selectFanStyle(style.value)"
                            >
                                <span class="icon">{{ style.icon }}</span>
                                <span class="label">{{ style.label }}</span>
                            </div>
                        </div>
                    </el-form-item>
                </div>

                <div class="form-section">
                    <h3 class="section-title">扇骨规格</h3>
                    <el-form-item label="扇骨长度" prop="boneLength">
                        <el-input-number 
                            v-model="orderForm.boneLength" 
                            :min="15" 
                            :max="40" 
                            :step="1"
                            size="medium"
                            @change="validateField('boneLength')"
                        ></el-input-number>
                        <span style="margin-left: 10px; color: #666;">厘米 <span class="required-mark">*</span></span>
                    </el-form-item>
                    <el-form-item label="扇骨数量" prop="boneCount">
                        <el-input-number 
                            v-model="orderForm.boneCount" 
                            :min="8" 
                            :max="30" 
                            :step="1"
                            size="medium"
                            @change="validateField('boneCount')"
                        ></el-input-number>
                        <span style="margin-left: 10px; color: #666;">根</span>
                    </el-form-item>
                </div>

                <div class="form-section">
                    <h3 class="section-title">扇面图案选择 <span class="required-mark">*</span></h3>
                    <el-form-item prop="pattern">
                        <div class="pattern-grid">
                            <div 
                                v-for="pattern in patterns" 
                                :key="pattern.value"
                                class="pattern-item"
                                :class="{ active: orderForm.pattern === pattern.value }"
                                @click="selectPattern(pattern.value)"
                            >
                                <div class="pattern-preview">{{ pattern.icon }}</div>
                                <span>{{ pattern.label }}</span>
                            </div>
                        </div>
                    </el-form-item>
                </div>

                <div class="form-section">
                    <h3 class="section-title">题字内容 <span class="required-mark">*</span></h3>
                    <el-form-item label="题字文字" prop="inscription">
                        <el-input 
                            type="textarea" 
                            v-model="orderForm.inscription" 
                            :rows="3"
                            placeholder="请输入您想要的题字内容"
                            maxlength="50"
                            show-word-limit
                        ></el-input>
                    </el-form-item>
                    <el-form-item label="题字字体" prop="fontStyle">
                        <el-select v-model="orderForm.fontStyle" placeholder="选择字体" style="width: 200px;">
                            <el-option label="楷书" value="kaishu"></el-option>
                            <el-option label="行书" value="xingshu"></el-option>
                            <el-option label="草书" value="caoshu"></el-option>
                            <el-option label="隶书" value="lishu"></el-option>
                        </el-select>
                    </el-form-item>
                </div>

                <div class="form-section">
                    <h3 class="section-title">客户信息</h3>
                    <el-form-item label="客户姓名" prop="customerName">
                        <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
                    </el-form-item>
                    <el-form-item label="联系电话" prop="phone">
                        <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
                    </el-form-item>
                    <el-form-item label="备注说明">
                        <el-input 
                            type="textarea" 
                            v-model="orderForm.remark" 
                            :rows="2"
                            placeholder="其他特殊要求"
                        ></el-input>
                    </el-form-item>
                </div>

                <div class="order-summary" v-if="showSummary">
                    <h3>📋 订单预览</h3>
                    <div class="summary-item">
                        <span>竹骨材质：</span>
                        <span>{{ getMaterialLabel }}</span>
                    </div>
                    <div class="summary-item">
                        <span>扇面款式：</span>
                        <span>{{ getStyleLabel }}</span>
                    </div>
                    <div class="summary-item">
                        <span>扇骨规格：</span>
                        <span>{{ orderForm.boneLength }}cm / {{ orderForm.boneCount }}根</span>
                    </div>
                    <div class="summary-item">
                        <span>扇面图案：</span>
                        <span>{{ getPatternLabel }}</span>
                    </div>
                    <div class="summary-item">
                        <span>题字内容：</span>
                        <span>{{ orderForm.inscription || '无' }}</span>
                    </div>
                </div>

                <el-form-item style="margin-top: 30px;">
                    <el-button 
                        type="primary" 
                        size="large" 
                        class="submit-btn"
                        @click="submitOrder"
                        :loading="submitting"
                    >
                        提交订单
                    </el-button>
                </el-form-item>
            </el-form>
        </div>
    `,
    data() {
        return {
            submitting: false,
            orderForm: {
                bambooMaterial: '',
                fanStyle: '',
                boneLength: 25,
                boneCount: 16,
                pattern: '',
                inscription: '',
                fontStyle: 'kaishu',
                customerName: '',
                phone: '',
                remark: ''
            },
            rules: {
                bambooMaterial: [
                    { required: true, message: '请选择竹骨材质', trigger: 'change' }
                ],
                fanStyle: [
                    { required: true, message: '请选择扇面款式', trigger: 'change' }
                ],
                boneLength: [
                    { required: true, message: '请输入扇骨长度', trigger: 'change' },
                    { type: 'number', min: 15, max: 40, message: '扇骨长度需在15-40厘米之间', trigger: 'change' }
                ],
                boneCount: [
                    { required: true, message: '请输入扇骨数量', trigger: 'change' },
                    { type: 'number', min: 8, max: 30, message: '扇骨数量需在8-30根之间', trigger: 'change' }
                ],
                pattern: [
                    { required: true, message: '请选择扇面图案', trigger: 'change' }
                ],
                inscription: [
                    { required: true, message: '请输入题字内容', trigger: 'blur' },
                    { min: 1, max: 50, message: '题字内容长度需在1-50字之间', trigger: 'blur' }
                ],
                fontStyle: [
                    { required: true, message: '请选择题字字体', trigger: 'change' }
                ],
                customerName: [
                    { required: true, message: '请输入客户姓名', trigger: 'blur' }
                ],
                phone: [
                    { required: true, message: '请输入联系电话', trigger: 'blur' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
                ]
            },
            bambooMaterials: [
                { value: 'maozhu', label: '毛竹', icon: '🎋' },
                { value: 'zizhu', label: '紫竹', icon: '🎍' },
                { value: 'xiangfeizhu', label: '湘妃竹', icon: '🌿' },
                { value: 'fengweizhu', label: '凤尾竹', icon: '🍃' }
            ],
            fanStyles: [
                { value: 'xuanzhi', label: '宣纸', icon: '📄' },
                { value: 'juanzhi', label: '绢纸', icon: '🎨' },
                { value: 'sidian', label: '丝缎', icon: '🎀' },
                { value: 'zhi', label: '纸本', icon: '📑' }
            ],
            patterns: [
                { value: 'shanshui', label: '山水', icon: '🏔️' },
                { value: 'huahui', label: '花卉', icon: '🌸' },
                { value: 'nniao', label: '花鸟', icon: '🐦' },
                { value: 'renwu', label: '人物', icon: '👤' },
                { value: 'shufa', label: '书法', icon: '✍️' },
                { value: 'kongan', label: '空白', icon: '⬜' }
            ]
        }
    },
    computed: {
        showSummary() {
            return this.orderForm.bambooMaterial && this.orderForm.fanStyle && this.orderForm.pattern;
        },
        getMaterialLabel() {
            const m = this.bambooMaterials.find(m => m.value === this.orderForm.bambooMaterial);
            return m ? m.label : '';
        },
        getStyleLabel() {
            const s = this.fanStyles.find(s => s.value === this.orderForm.fanStyle);
            return s ? s.label : '';
        },
        getPatternLabel() {
            const p = this.patterns.find(p => p.value === this.orderForm.pattern);
            return p ? p.label : '';
        }
    },
    methods: {
        selectBambooMaterial(value) {
            this.orderForm.bambooMaterial = value;
            this.validateField('bambooMaterial');
        },
        selectFanStyle(value) {
            this.orderForm.fanStyle = value;
            this.validateField('fanStyle');
        },
        selectPattern(value) {
            this.orderForm.pattern = value;
            this.validateField('pattern');
        },
        validateField(field) {
            this.$refs.orderForm.validateField(field);
        },
        submitOrder() {
            this.$refs.orderForm.validate((valid) => {
                if (valid) {
                    this.submitting = true;
                    setTimeout(() => {
                        this.$emit('submit-order', { ...this.orderForm });
                        this.$message.success('订单提交成功！');
                        this.resetForm();
                        this.submitting = false;
                    }, 1000);
                } else {
                    this.$message.error('请完善订单信息');
                    return false;
                }
            });
        },
        resetForm() {
            this.$refs.orderForm.resetFields();
            this.orderForm.boneLength = 25;
            this.orderForm.boneCount = 16;
            this.orderForm.fontStyle = 'kaishu';
        }
    }
});

Vue.component('admin-page', {
    props: ['orders'],
    template: `
        <div class="admin-card">
            <h2 class="card-title">🔧 订单管理后台</h2>
            
            <el-row :gutter="20" style="margin-bottom: 20px;">
                <el-col :span="6">
                    <el-card shadow="hover">
                        <div slot="header" style="color: #409EFF; font-weight: 600;">
                            总订单数
                        </div>
                        <div style="font-size: 28px; font-weight: bold; color: #409EFF;">
                            {{ orders.length }}
                        </div>
                    </el-card>
                </el-col>
                <el-col :span="6">
                    <el-card shadow="hover">
                        <div slot="header" style="color: #E6A23C; font-weight: 600;">
                            生产中
                        </div>
                        <div style="font-size: 28px; font-weight: bold; color: #E6A23C;">
                            {{ producingCount }}
                        </div>
                    </el-card>
                </el-col>
                <el-col :span="6">
                    <el-card shadow="hover">
                        <div slot="header" style="color: #67C23A; font-weight: 600;">
                            已完工
                        </div>
                        <div style="font-size: 28px; font-weight: bold; color: #67C23A;">
                            {{ completedCount }}
                        </div>
                    </el-card>
                </el-col>
                <el-col :span="6">
                    <el-card shadow="hover">
                        <div slot="header" style="color: #909399; font-weight: 600;">
                            待开工
                        </div>
                        <div style="font-size: 28px; font-weight: bold; color: #909399;">
                            {{ pendingCount }}
                        </div>
                    </el-card>
                </el-col>
            </el-row>

            <el-table 
                :data="orders" 
                border 
                style="width: 100%"
                v-loading="!orders.length"
                element-loading-text="暂无订单"
            >
                <el-table-column prop="orderId" label="订单号" width="130" sortable>
                    <template slot-scope="scope">
                        <el-tag type="info">{{ scope.row.orderId }}</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="customerName" label="客户姓名" width="100"></el-table-column>
                <el-table-column prop="phone" label="联系电话" width="120"></el-table-column>
                <el-table-column label="订单详情" min-width="200">
                    <template slot-scope="scope">
                        <div style="font-size: 12px; line-height: 1.6;">
                            <div>🎋 材质：{{ getMaterialLabel(scope.row.bambooMaterial) }}</div>
                            <div>📄 款式：{{ getStyleLabel(scope.row.fanStyle) }}</div>
                            <div>📏 规格：{{ scope.row.boneLength }}cm / {{ scope.row.boneCount }}根</div>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="生产工序" min-width="280">
                    <template slot-scope="scope">
                        <div class="process-timeline">
                            <el-steps :active="scope.row.currentProcess" size="small" direction="vertical">
                                <el-step 
                                    v-for="(step, index) in processSteps" 
                                    :key="index"
                                    :title="step"
                                >
                                </el-step>
                            </el-steps>
                        </div>
                    </template>
                </el-table-column>
                <el-table-column label="操作" width="200">
                    <template slot-scope="scope">
                        <div class="table-actions">
                            <el-button 
                                size="small" 
                                type="primary"
                                @click="nextStep(scope.row)"
                                :disabled="scope.row.currentProcess >= processSteps.length - 1"
                            >
                                下一工序
                            </el-button>
                            <el-button 
                                size="small" 
                                type="danger"
                                @click="viewDetail(scope.row)"
                            >
                                详情
                            </el-button>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
        </div>
    `,
    data() {
        return {
            processSteps: ['选竹', '开骨', '打磨', '穿面', '印刷', '题字', '装裱', '完工'],
            bambooMaterials: [
                { value: 'maozhu', label: '毛竹' },
                { value: 'zizhu', label: '紫竹' },
                { value: 'xiangfeizhu', label: '湘妃竹' },
                { value: 'fengweizhu', label: '凤尾竹' }
            ],
            fanStyles: [
                { value: 'xuanzhi', label: '宣纸' },
                { value: 'juanzhi', label: '绢纸' },
                { value: 'sidian', label: '丝缎' },
                { value: 'zhi', label: '纸本' }
            ]
        }
    },
    computed: {
        producingCount() {
            return this.orders.filter(o => o.currentProcess > 0 && o.currentProcess < 7).length;
        },
        completedCount() {
            return this.orders.filter(o => o.currentProcess === 7).length;
        },
        pendingCount() {
            return this.orders.filter(o => o.currentProcess === 0).length;
        }
    },
    methods: {
        getMaterialLabel(value) {
            const m = this.bambooMaterials.find(m => m.value === value);
            return m ? m.label : value;
        },
        getStyleLabel(value) {
            const s = this.fanStyles.find(s => s.value === value);
            return s ? s.label : value;
        },
        nextStep(order) {
            if (order.currentProcess < this.processSteps.length - 1) {
                this.$emit('update-process', order.orderId, order.currentProcess + 1);
                this.$message.success(`已进入下一工序：${this.processSteps[order.currentProcess + 1]}`);
            }
        },
        viewDetail(order) {
            const detail = `
订单号：${order.orderId}
客户：${order.customerName}
电话：${order.phone}
————————————
竹骨材质：${this.getMaterialLabel(order.bambooMaterial)}
扇面款式：${this.getStyleLabel(order.fanStyle)}
扇骨长度：${order.boneLength}cm
扇骨数量：${order.boneCount}根
扇面图案：${order.pattern}
题字内容：${order.inscription || '无'}
题字字体：${order.fontStyle}
备注：${order.remark || '无'}
————————————
当前工序：${this.processSteps[order.currentProcess]}
            `;
            this.$alert(detail, '订单详情', {
                confirmButtonText: '确定'
            });
        }
    }
});

new Vue({
    el: '#app',
    data() {
        return {
            currentPage: 'order',
            orders: [
                {
                    orderId: 'ORD2024001',
                    customerName: '张三',
                    phone: '13800138001',
                    bambooMaterial: 'maozhu',
                    fanStyle: 'xuanzhi',
                    boneLength: 25,
                    boneCount: 16,
                    pattern: 'shanshui',
                    inscription: '宁静致远',
                    fontStyle: 'kaishu',
                    remark: '请加急处理',
                    currentProcess: 3
                },
                {
                    orderId: 'ORD2024002',
                    customerName: '李四',
                    phone: '13900139002',
                    bambooMaterial: 'zizhu',
                    fanStyle: 'juanzhi',
                    boneLength: 30,
                    boneCount: 20,
                    pattern: 'huahui',
                    inscription: '',
                    fontStyle: 'xingshu',
                    remark: '',
                    currentProcess: 5
                },
                {
                    orderId: 'ORD2024003',
                    customerName: '王五',
                    phone: '13700137003',
                    bambooMaterial: 'xiangfeizhu',
                    fanStyle: 'sidian',
                    boneLength: 28,
                    boneCount: 18,
                    pattern: 'shufa',
                    inscription: '厚德载物',
                    fontStyle: 'caoshu',
                    remark: '',
                    currentProcess: 7
                }
            ]
        }
    },
    methods: {
        handleSubmitOrder(orderData) {
            const newOrder = {
                ...orderData,
                orderId: 'ORD' + Date.now().toString().slice(-8),
                currentProcess: 0
            };
            this.orders.unshift(newOrder);
        },
        handleUpdateProcess(orderId, newProcess) {
            const order = this.orders.find(o => o.orderId === orderId);
            if (order) {
                order.currentProcess = newProcess;
            }
        }
    }
});