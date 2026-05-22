const BookingForm = {
    template: `
        <div class="page-container">
            <div class="page-header">
                <h2>📝 在线预订</h2>
                <p>填写预订信息，享受舒适住宿体验</p>
            </div>
            
            <el-card class="card-shadow">
                <div class="form-container">
                    <el-form :model="bookingForm" :rules="rules" ref="bookingForm" label-width="120px">
                        <el-form-item label="选择房型" prop="roomId">
                            <el-select v-model="bookingForm.roomId" placeholder="请选择房型" style="width: 100%" @change="onRoomChange">
                                <el-option v-for="room in $root.rooms" :key="room.id" :label="room.name" :value="room.id">
                                    <span>{{ room.name }}</span>
                                    <span style="float: right; color: #f56c6c;">¥{{ room.price }}/晚</span>
                                </el-option>
                            </el-select>
                        </el-form-item>
                        
                        <el-form-item label="入住日期" prop="checkinDate">
                            <el-date-picker v-model="bookingForm.checkinDate" type="date" placeholder="选择入住日期" style="width: 100%" :picker-options="pickerOptionsStart" @change="calculatePrice"></el-date-picker>
                        </el-form-item>
                        
                        <el-form-item label="退房日期" prop="checkoutDate">
                            <el-date-picker v-model="bookingForm.checkoutDate" type="date" placeholder="选择退房日期" style="width: 100%" :picker-options="pickerOptionsEnd" @change="calculatePrice"></el-date-picker>
                        </el-form-item>
                        
                        <el-form-item label="入住天数">
                            <span style="color: #409eff; font-weight: 600; font-size: 16px;">{{ days }} 晚</span>
                        </el-form-item>
                        
                        <el-form-item v-if="availability" label="库存状态">
                            <el-tag :type="availability.available ? 'success' : 'danger'" size="small">
                                {{ availability.message }}
                            </el-tag>
                            <span v-if="availability.available" style="margin-left: 10px; color: #606266;">
                                已预订: {{ availability.booked }} / 总计: {{ availability.total }}
                            </span>
                        </el-form-item>
                        
                        <el-form-item label="入住人姓名" prop="guestName">
                            <el-input v-model="bookingForm.guestName" placeholder="请输入入住人姓名" maxlength="20"></el-input>
                        </el-form-item>
                        
                        <el-form-item label="手机号码" prop="phone">
                            <el-input v-model="bookingForm.phone" placeholder="请输入手机号码" maxlength="11"></el-input>
                        </el-form-item>
                        
                        <el-form-item label="身份证号" prop="idCard">
                            <el-input v-model="bookingForm.idCard" placeholder="请输入身份证号码" maxlength="18"></el-input>
                        </el-form-item>
                        
                        <el-form-item label="入住人数" prop="guests">
                            <el-input-number v-model="bookingForm.guests" :min="1" :max="4"></el-input-number>
                            <span style="margin-left: 10px; color: #909399;">人</span>
                        </el-form-item>
                        
                        <el-form-item label="特殊要求">
                            <el-input type="textarea" v-model="bookingForm.remark" :rows="3" placeholder="如有特殊要求请在此说明（如：高楼层、无烟房等）"></el-input>
                        </el-form-item>
                        
                        <el-form-item>
                            <el-checkbox v-model="agreement">我已阅读并同意<a href="#" style="color: #409eff;">《酒店预订服务协议》</a></el-checkbox>
                        </el-form-item>
                    </el-form>
                </div>
                
                <div style="background: #f5f7fa; padding: 20px; border-radius: 4px; margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-size: 14px; color: #909399;">预计房费：</span>
                            <span class="amount-display">¥{{ totalPrice }}</span>
                            <span v-if="days > 0" style="color: #909399; font-size: 14px;">（¥{{ selectedRoom?.price || 0 }} × {{ days }}晚）</span>
                        </div>
                        <div>
                            <el-button size="large" @click="resetForm">重置</el-button>
                            <el-button type="primary" size="large" :disabled="!agreement" @click="submitBooking" icon="el-icon-check">
                                提交预订
                            </el-button>
                        </div>
                    </div>
                </div>
            </el-card>
        </div>
    `,
    data() {
        const validatePhone = (rule, value, callback) => {
            const reg = /^1[3-9]\d{9}$/;
            if (!value) {
                callback(new Error('请输入手机号码'));
            } else if (!reg.test(value)) {
                callback(new Error('请输入正确的手机号码'));
            } else {
                callback();
            }
        };
        
        const validateIdCard = (rule, value, callback) => {
            const reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
            if (!value) {
                callback(new Error('请输入身份证号码'));
            } else if (!reg.test(value)) {
                callback(new Error('请输入正确的身份证号码'));
            } else {
                callback();
            }
        };
        
        return {
            bookingForm: {
                roomId: null,
                roomName: '',
                checkinDate: '',
                checkoutDate: '',
                guestName: '',
                phone: '',
                idCard: '',
                guests: 1,
                remark: ''
            },
            rules: {
                roomId: [{ required: true, message: '请选择房型', trigger: 'change' }],
                checkinDate: [{ required: true, message: '请选择入住日期', trigger: 'change' }],
                checkoutDate: [{ required: true, message: '请选择退房日期', trigger: 'change' }],
                guestName: [{ required: true, message: '请输入入住人姓名', trigger: 'blur' }],
                phone: [{ required: true, validator: validatePhone, trigger: 'blur' }],
                idCard: [{ required: true, validator: validateIdCard, trigger: 'blur' }],
                guests: [{ required: true, message: '请选择入住人数', trigger: 'change' }]
            },
            agreement: false,
            availability: null,
            pickerOptionsStart: {
                disabledDate(time) {
                    return time.getTime() < Date.now() - 8.64e7;
                }
            },
            pickerOptionsEnd: {
                disabledDate(time) {
                    return time.getTime() < Date.now();
                }
            }
        };
    },
    computed: {
        selectedRoom() {
            return this.$root.rooms.find(r => r.id === this.bookingForm.roomId);
        },
        days() {
            if (!this.bookingForm.checkinDate || !this.bookingForm.checkoutDate) return 0;
            const start = new Date(this.bookingForm.checkinDate).getTime();
            const end = new Date(this.bookingForm.checkoutDate).getTime();
            return Math.max(0, Math.ceil((end - start) / (1000 * 60 * 60 * 24)));
        },
        totalPrice() {
            if (!this.selectedRoom || !this.days) return 0;
            return this.selectedRoom.price * this.days;
        }
    },
    mounted() {
        if (this.$route.query.roomId) {
            this.bookingForm.roomId = parseInt(this.$route.query.roomId);
            this.bookingForm.roomName = this.$route.query.roomName;
        }
    },
    methods: {
        onRoomChange() {
            if (this.selectedRoom) {
                this.bookingForm.roomName = this.selectedRoom.name;
            }
            this.checkAvailability();
        },
        calculatePrice() {
            if (this.bookingForm.checkinDate && this.bookingForm.checkoutDate) {
                if (this.bookingForm.checkinDate >= this.bookingForm.checkoutDate) {
                    this.$message.warning('退房日期必须晚于入住日期');
                    this.bookingForm.checkoutDate = '';
                } else {
                    this.checkAvailability();
                }
            }
        },
        checkAvailability() {
            if (this.bookingForm.roomId && this.bookingForm.checkinDate && this.bookingForm.checkoutDate) {
                this.availability = this.$root.checkRoomAvailability(
                    this.bookingForm.roomId,
                    this.bookingForm.checkinDate,
                    this.bookingForm.checkoutDate
                );
            } else {
                this.availability = null;
            }
        },
        submitBooking() {
            this.checkAvailability();
            
            if (this.availability && !this.availability.available) {
                this.$message.error(this.availability.message);
                return;
            }
            
            this.$refs.bookingForm.validate((valid) => {
                if (valid) {
                    if (this.days <= 0) {
                        this.$message.warning('入住天数必须大于0');
                        return;
                    }
                    
                    const orderId = 'ORD' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + String(Math.floor(Math.random() * 1000)).padStart(3, '0');
                    const order = {
                        id: orderId,
                        roomName: this.selectedRoom.name,
                        guestName: this.bookingForm.guestName,
                        phone: this.bookingForm.phone.slice(0, 3) + '****' + this.bookingForm.phone.slice(7),
                        checkinDate: this.bookingForm.checkinDate,
                        checkoutDate: this.bookingForm.checkoutDate,
                        days: this.days,
                        price: this.totalPrice,
                        status: 'pending',
                        createTime: new Date().toLocaleString('zh-CN'),
                        idCard: this.bookingForm.idCard
                    };
                    
                    this.$root.addOrder(order);
                    this.$message.success('预订成功！');
                    this.$router.push('/orders');
                } else {
                    this.$message.error('请完善预订信息');
                    return false;
                }
            });
        },
        resetForm() {
            this.$refs.bookingForm.resetFields();
            this.agreement = false;
        }
    }
};