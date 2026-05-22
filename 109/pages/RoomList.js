const RoomList = {
    template: `
        <div class="page-container">
            <div class="page-header">
                <h2>🏨 房型列表</h2>
                <p>选择您心仪的房间类型</p>
            </div>
            
            <div class="search-bar">
                <el-row :gutter="20">
                    <el-col :span="6">
                        <el-select v-model="searchType" placeholder="房型筛选" clearable style="width: 100%">
                            <el-option label="全部房型" value=""></el-option>
                            <el-option label="豪华大床房" value="deluxe"></el-option>
                            <el-option label="标准双床房" value="standard"></el-option>
                            <el-option label="商务套房" value="suite"></el-option>
                            <el-option label="家庭亲子房" value="family"></el-option>
                        </el-select>
                    </el-col>
                    <el-col :span="6">
                        <el-input v-model="searchKeyword" placeholder="搜索房型名称" clearable></el-input>
                    </el-col>
                    <el-col :span="6">
                        <el-button type="primary" @click="handleSearch" icon="el-icon-search">搜索</el-button>
                        <el-button @click="resetSearch" icon="el-icon-refresh">重置</el-button>
                    </el-col>
                </el-row>
            </div>
            
            <el-row :gutter="20">
                <el-col :span="12" v-for="room in filteredRooms" :key="room.id">
                    <el-card class="room-card card-shadow">
                        <img :src="room.images[0]" :alt="room.name" class="room-image">
                        <div style="margin-top: 15px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                <h3 style="font-size: 18px; color: #303133;">{{ room.name }}</h3>
                                <el-tag type="success" v-if="room.available > 0">剩余 {{ room.available }} 间</el-tag>
                                <el-tag type="danger" v-else>已满房</el-tag>
                            </div>
                            <p style="color: #909399; font-size: 14px; margin-bottom: 10px;">{{ room.description }}</p>
                            <el-row :gutter="10" style="margin-bottom: 10px;">
                                <el-col :span="8">
                                    <span style="color: #606266; font-size: 13px;">
                                        <i class="el-icon-rank"></i> {{ room.area }}㎡
                                    </span>
                                </el-col>
                                <el-col :span="8">
                                    <span style="color: #606266; font-size: 13px;">
                                        <i class="el-icon-s-custom"></i> 最多{{ room.maxGuests }}人
                                    </span>
                                </el-col>
                                <el-col :span="8">
                                    <span style="color: #606266; font-size: 13px;">
                                        <i class="el-icon-date"></i> {{ room.bedType }}
                                    </span>
                                </el-col>
                            </el-row>
                            <div style="margin-bottom: 10px;">
                                <el-tag v-for="facility in room.facilities" :key="facility" size="mini" style="margin-right: 5px; margin-bottom: 5px;">
                                    {{ facility }}
                                </el-tag>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid #ebeef5;">
                                <div>
                                    <span style="color: #f56c6c; font-size: 24px; font-weight: 600;">¥{{ room.price }}</span>
                                    <span style="color: #909399; font-size: 14px;">/晚</span>
                                    <span style="color: #c0c4cc; font-size: 14px; text-decoration: line-through; margin-left: 10px;">¥{{ room.originalPrice }}</span>
                                </div>
                                <el-button type="primary" :disabled="room.available <= 0" @click="goBooking(room)" icon="el-icon-right">
                                    立即预订
                                </el-button>
                            </div>
                        </div>
                    </el-card>
                </el-col>
            </el-row>
        </div>
    `,
    data() {
        return {
            searchType: '',
            searchKeyword: ''
        };
    },
    computed: {
        filteredRooms() {
            let rooms = this.$root.rooms;
            if (this.searchType) {
                rooms = rooms.filter(r => r.type === this.searchType);
            }
            if (this.searchKeyword) {
                rooms = rooms.filter(r => r.name.includes(this.searchKeyword));
            }
            return rooms;
        }
    },
    methods: {
        handleSearch() {
            this.$message.success('搜索完成');
        },
        resetSearch() {
            this.searchType = '';
            this.searchKeyword = '';
        },
        goBooking(room) {
            this.$router.push({
                path: '/booking',
                query: { roomId: room.id, roomName: room.name, price: room.price }
            });
        }
    }
};