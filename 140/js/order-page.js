const OrderPage = {
    template: `
        <div class="order-page">
            <el-header class="page-header">
                <div class="header-content">
                    <h1>🎐 缂丝团扇定制</h1>
                    <el-button type="primary" @click="goToAdmin">管理员入口</el-button>
                </div>
            </el-header>
            
            <el-main class="main-content">
                <el-card class="order-card" shadow="hover">
                    <div slot="header" class="card-header">
                        <span>📝 定制订单信息</span>
                    </div>
                    
                    <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px">
                        <el-divider content-position="left">
                            <span class="divider-title">🎨 基础信息</span>
                        </el-divider>
                        
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-form-item label="客户姓名" prop="customerName">
                                    <el-input v-model="orderForm.customerName" placeholder="请输入您的姓名"></el-input>
                                </el-form-item>
                            </el-col>
                            <el-col :span="12">
                                <el-form-item label="联系电话" prop="phone">
                                    <el-input v-model="orderForm.phone" placeholder="请输入联系电话"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        
                        <el-divider content-position="left">
                            <span class="divider-title">🧵 缂丝底料选择</span>
                        </el-divider>
                        
                        <el-form-item label="底料类型" prop="fabric">
                            <el-radio-group v-model="orderForm.fabric">
                                <el-radio-button label="真丝绡">
                                    <div class="radio-content">
                                        <div class="radio-name">真丝绡</div>
                                        <div class="radio-desc">轻薄透明，质感细腻</div>
                                        <div class="radio-price">¥280</div>
                                    </div>
                                </el-radio-button>
                                <el-radio-button label="杭绸">
                                    <div class="radio-content">
                                        <div class="radio-name">杭绸</div>
                                        <div class="radio-desc">厚实耐用，色彩饱满</div>
                                        <div class="radio-price">¥350</div>
                                    </div>
                                </el-radio-button>
                                <el-radio-button label="宋锦">
                                    <div class="radio-content">
                                        <div class="radio-name">宋锦</div>
                                        <div class="radio-desc">花纹精美，质地坚韧</div>
                                        <div class="radio-price">¥420</div>
                                    </div>
                                </el-radio-button>
                                <el-radio-button label="绫罗">
                                    <div class="radio-content">
                                        <div class="radio-name">绫罗</div>
                                        <div class="radio-desc">光泽柔和，手感丝滑</div>
                                        <div class="radio-price">¥380</div>
                                    </div>
                                </el-radio-button>
                            </el-radio-group>
                        </el-form-item>
                        
                        <el-divider content-position="left">
                            <span class="divider-title">📐 扇面尺寸</span>
                        </el-divider>
                        
                        <el-row :gutter="20">
                            <el-col :span="7">
                                <el-form-item label="扇面长度" prop="length">
                                    <el-input-number v-model="orderForm.length" :min="15" :max="50" :step="1"></el-input-number>
                                    <span class="unit">cm</span>
                                </el-form-item>
                            </el-col>
                            <el-col :span="7">
                                <el-form-item label="扇面宽度" prop="width">
                                    <el-input-number v-model="orderForm.width" :min="10" :max="35" :step="1"></el-input-number>
                                    <span class="unit">cm</span>
                                </el-form-item>
                            </el-col>
                            <el-col :span="10">
                                <el-form-item label="尺寸说明">
                                    <span class="size-tip">长15-50cm，宽10-35cm，推荐长20-30cm，宽15-25cm</span>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        
                        <el-divider content-position="left">
                            <span class="divider-title">🌸 纹样题材</span>
                        </el-divider>
                        
                        <el-form-item label="纹样选择" prop="pattern">
                            <el-select v-model="orderForm.pattern" placeholder="请选择纹样题材" style="width: 100%;">
                                <el-option-group label="花鸟系列">
                                    <el-option label="牡丹凤凰" value="牡丹凤凰"></el-option>
                                    <el-option label="荷花鸳鸯" value="荷花鸳鸯"></el-option>
                                    <el-option label="梅花喜鹊" value="梅花喜鹊"></el-option>
                                    <el-option label="兰草蝴蝶" value="兰草蝴蝶"></el-option>
                                </el-option-group>
                                <el-option-group label="山水系列">
                                    <el-option label="江南水乡" value="江南水乡"></el-option>
                                    <el-option label="亭台楼阁" value="亭台楼阁"></el-option>
                                    <el-option label="远山近水" value="远山近水"></el-option>
                                </el-option-group>
                                <el-option-group label="吉祥系列">
                                    <el-option label="百福图" value="百福图"></el-option>
                                    <el-option label="万寿纹" value="万寿纹"></el-option>
                                    <el-option label="如意云纹" value="如意云纹"></el-option>
                                </el-option-group>
                                <el-option-group label="定制系列">
                                    <el-option label="自定义纹样（需沟通）" value="自定义纹样"></el-option>
                                </el-option-group>
                            </el-select>
                        </el-form-item>
                        
                        <el-divider content-position="left">
                            <span class="divider-title">🌈 配色方案</span>
                        </el-divider>
                        
                        <el-form-item label="配色方案" prop="colorScheme">
                            <el-checkbox-group v-model="orderForm.colorScheme">
                                <el-checkbox label="清雅素色">清雅素色</el-checkbox>
                                <el-checkbox label="典雅宫廷">典雅宫廷</el-checkbox>
                                <el-checkbox label="明艳喜庆">明艳喜庆</el-checkbox>
                                <el-checkbox label="水墨丹青">水墨丹青</el-checkbox>
                                <el-checkbox label="自定义配色">自定义配色</el-checkbox>
                            </el-checkbox-group>
                        </el-form-item>
                        
                        <el-divider content-position="left">
                            <span class="divider-title">🪵 扇柄材质</span>
                        </el-divider>
                        
                        <el-form-item label="扇柄材质" prop="handle">
                            <el-select v-model="orderForm.handle" placeholder="请选择扇柄材质" style="width: 100%;">
                                <el-option label="紫檀木（高贵典雅，质地坚硬）" value="紫檀木"></el-option>
                                <el-option label="黄杨木（色泽温润，纹理细腻）" value="黄杨木"></el-option>
                                <el-option label="湘妃竹（花纹独特，传统经典）" value="湘妃竹"></el-option>
                                <el-option label="象牙果（洁白如玉，手感温润）" value="象牙果"></el-option>
                                <el-option label="鸡翅木（纹理独特，经济实惠）" value="鸡翅木"></el-option>
                            </el-select>
                        </el-form-item>
                        
                        <el-divider content-position="left">
                            <span class="divider-title">📝 备注说明</span>
                        </el-divider>
                        
                        <el-form-item label="特殊要求">
                            <el-input
                                type="textarea"
                                :rows="4"
                                placeholder="请填写其他特殊要求或定制说明..."
                                v-model="orderForm.remarks">
                            </el-input>
                        </el-form-item>
                        
                        <el-form-item>
                            <el-button type="primary" size="large" @click="submitOrder" :loading="submitting">
                                提交定制订单
                            </el-button>
                            <el-button size="large" @click="resetForm">重置</el-button>
                            <el-button type="success" size="large" @click="submitAndView" :loading="submitting">
                                提交并查看订单
                            </el-button>
                        </el-form-item>
                    </el-form>
                </el-card>
            </el-main>
            
            <el-footer class="page-footer">
                <p>© 2024 缂丝团扇定制工坊 - 传承非遗，匠心独运</p>
            </el-footer>
        </div>
    `,
    data() {
        return {
            submitting: false,
            orderForm: {
                customerName: '',
                phone: '',
                fabric: '',
                length: 25,
                width: 20,
                pattern: '',
                colorScheme: [],
                handle: '',
                remarks: ''
            },
            rules: {
                customerName: [
                    { required: true, message: '请输入客户姓名', trigger: 'blur' }
                ],
                phone: [
                    { required: true, message: '请输入联系电话', trigger: 'blur' },
                    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
                ],
                fabric: [
                    { required: true, message: '请选择缂丝底料', trigger: 'change' }
                ],
                length: [
                    { required: true, message: '请输入扇面长度', trigger: 'change' },
                    { type: 'number', min: 15, max: 50, message: '扇面长度需在15-50cm之间', trigger: 'change' }
                ],
                width: [
                    { required: true, message: '请输入扇面宽度', trigger: 'change' },
                    { type: 'number', min: 10, max: 35, message: '扇面宽度需在10-35cm之间', trigger: 'change' }
                ],
                pattern: [
                    { required: true, message: '请选择纹样题材', trigger: 'change' }
                ],
                colorScheme: [
                    { type: 'array', required: true, message: '请选择配色方案', trigger: 'change', min: 1 }
                ],
                handle: [
                    { required: true, message: '请选择扇柄材质', trigger: 'change' }
                ]
            }
        }
    },
    methods: {
        goToAdmin() {
            this.$router.push('/admin')
        },
        submitOrder() {
            this.$refs.orderForm.validate((valid) => {
                if (valid) {
                    this.submitting = true
                    setTimeout(() => {
                        const order = {
                            id: 'ORD' + Date.now(),
                            ...this.orderForm,
                            status: 0,
                            statusText: '选料',
                            createTime: new Date().toLocaleString()
                        }
                        let orders = JSON.parse(localStorage.getItem('fanOrders') || '[]')
                        orders.unshift(order)
                        localStorage.setItem('fanOrders', JSON.stringify(orders))
                        
                        this.submitting = false
                        this.$message({
                            type: 'success',
                            message: '订单提交成功！我们将尽快与您联系确认定制细节。'
                        })
                        this.resetForm()
                    }, 1000)
                } else {
                    this.$message.error('请完善订单信息')
                    return false
                }
            })
        },
        submitAndView() {
            this.$refs.orderForm.validate((valid) => {
                if (valid) {
                    this.submitting = true
                    setTimeout(() => {
                        const order = {
                            id: 'ORD' + Date.now(),
                            ...this.orderForm,
                            status: 0,
                            statusText: '选料',
                            createTime: new Date().toLocaleString()
                        }
                        let orders = JSON.parse(localStorage.getItem('fanOrders') || '[]')
                        orders.unshift(order)
                        localStorage.setItem('fanOrders', JSON.stringify(orders))
                        
                        this.submitting = false
                        this.$message({
                            type: 'success',
                            message: '订单提交成功！正在跳转到订单管理页面...'
                        })
                        this.resetForm()
                        localStorage.setItem('scrollToLatest', 'true')
                        this.$router.push('/admin')
                    }, 1000)
                } else {
                    this.$message.error('请完善订单信息')
                    return false
                }
            })
        },
        resetForm() {
            this.$refs.orderForm.resetFields()
            this.orderForm.length = 25
            this.orderForm.width = 20
            this.orderForm.colorScheme = []
        }
    }
}