Vue.use(ELEMENT);

let mockRooms = [
    {
        id: 1,
        name: '豪华大床房',
        type: 'deluxe',
        price: 399,
        originalPrice: 499,
        area: 35,
        bedType: '1.8米大床',
        maxGuests: 2,
        facilities: ['WiFi', '空调', '独立卫浴', '迷你吧'],
        images: ['https://images.unsplash.com/photo-1618773928148-b36017?w=600'],
        description: '宽敞明亮的豪华大床房，配备高品质床品，享受舒适睡眠体验',
        status: 'available',
        total: 10,
        available: 5
    },
    {
        id: 2,
        name: '标准双床房',
        type: 'standard',
        price: 299,
        originalPrice: 399,
        area: 30,
        bedType: '1.2米双床',
        maxGuests: 2,
        facilities: ['WiFi', '空调', '独立卫浴'],
        images: ['https://images.unsplash.com/photo-1590490360182-3d48d568?w=600'],
        description: '温馨舒适的标准双床房，适合朋友或家人出行首选',
        status: 'available',
        total: 15,
        available: 8
    },
    {
        id: 3,
        name: '商务套房',
        type: 'suite',
        price: 599,
        originalPrice: 799,
        area: 50,
        bedType: '2.0米大床',
        maxGuests: 2,
        facilities: ['WiFi', '空调', '独立卫浴', '迷你吧', '办公区', '浴缸'],
        images: ['https://images.unsplash.com/photo-1582719478250-c87a81?w=600'],
        description: '豪华商务套房，独立办公区域，满足商务人士需求',
        status: 'available',
        total: 5,
        available: 2
    },
    {
        id: 4,
        name: '家庭亲子房',
        type: 'family',
        price: 459,
        originalPrice: 559,
        area: 40,
        bedType: '1.8米+1.2米',
        maxGuests: 3,
        facilities: ['WiFi', '空调', '独立卫浴', '儿童用品', '迷你吧'],
        images: ['https://images.unsplash.com/photo-1566665797739-167fa3?w=600'],
        description: '温馨家庭房，配备儿童用品，让家庭出行更舒适',
        status: 'available',
        total: 8,
        available: 3
    }
];

let mockOrders = [
    {
        id: 'ORD202405001',
        roomName: '豪华大床房',
        guestName: '张三',
        phone: '138****1234',
        checkinDate: '2024-05-20',
        checkoutDate: '2024-05-22',
        days: 2,
        price: 798,
        status: 'confirmed',
        createTime: '2024-05-15 10:30:00',
        idCard: '110101199001011234'
    },
    {
        id: 'ORD202405002',
        roomName: '标准双床房',
        guestName: '李四',
        phone: '139****5678',
        checkinDate: '2024-05-18',
        checkoutDate: '2024-05-20',
        days: 2,
        price: 598,
        status: 'checkedin',
        createTime: '2024-05-14 14:20:00',
        idCard: '310101199202022345',
        roomNumber: '302'
    },
    {
        id: 'ORD202405003',
        roomName: '商务套房',
        guestName: '王五',
        phone: '137****9012',
        checkinDate: '2024-05-16',
        checkoutDate: '2024-05-17',
        days: 1,
        price: 599,
        status: 'completed',
        createTime: '2024-05-13 09:15:00',
        idCard: '440101198803033456',
        roomNumber: '501'
    },
    {
        id: 'ORD202405004',
        roomName: '家庭亲子房',
        guestName: '赵六',
        phone: '136****3456',
        checkinDate: '2024-05-25',
        checkoutDate: '2024-05-28',
        days: 3,
        price: 1377,
        status: 'pending',
        createTime: '2024-05-16 11:45:00',
        idCard: '510101199504044567'
    }
];

const app = new Vue({
    el: '#app',
    router,
    data: {
        orders: mockOrders,
        rooms: mockRooms,
        activeIndex: '1'
    },
    methods: {
        handleSelect(key, keyPath) {
            const routeMap = {
                '1': '/rooms',
                '2': '/booking',
                '3': '/checkin',
                '4': '/orders',
                '5': '/checkout'
            };
            this.$router.push(routeMap[key]);
        },
        addOrder(order) {
            this.orders.unshift(order);
        },
        updateOrderStatus(orderId, status, extraData = {}) {
            const order = this.orders.find(o => o.id === orderId);
            if (order) {
                order.status = status;
                Object.assign(order, extraData);
            }
        },
        checkRoomAvailability(roomId, checkinDate, checkoutDate) {
            const room = this.rooms.find(r => r.id === roomId);
            if (!room) return { available: false, message: '房型不存在' };
            
            if (!checkinDate || !checkoutDate) return { available: false, message: '请选择入住和退房日期' };
            
            const start = new Date(checkinDate);
            const end = new Date(checkoutDate);
            if (start >= end) return { available: false, message: '退房日期必须晚于入住日期' };
            
            const overlappingOrders = this.orders.filter(o => {
                if (o.status === 'cancelled' || o.status === 'completed') return false;
                if (o.roomName !== room.name) return false;
                const orderCheckin = new Date(o.checkinDate);
                const orderCheckout = new Date(o.checkoutDate);
                return !(end <= orderCheckin || start >= orderCheckout);
            });
            
            const bookedCount = overlappingOrders.length;
            const remaining = room.total - bookedCount;
            
            if (remaining <= 0) {
                return {
                    available: false,
                    message: room.name + '在所选日期范围内已售罄，共被预订' + bookedCount + '间',
                    remaining: 0,
                    booked: bookedCount,
                    total: room.total
                };
            }
            
            return {
                available: true,
                message: '可预订，剩余' + remaining + '间',
                remaining: remaining,
                booked: bookedCount,
                total: room.total
            };
        },
        getRoomPrice(roomName) {
            const room = this.rooms.find(r => r.name === roomName);
            return room ? room.price : 0;
        }
    },
    watch: {
        '$route.path'(newPath) {
            const indexMap = {
                '/rooms': '1',
                '/booking': '2',
                '/checkin': '3',
                '/orders': '4',
                '/checkout': '5'
            };
            this.activeIndex = indexMap[newPath] || '1';
        }
    },
    template: `
        <el-container style="height: 100vh;">
            <el-header>
                <div class="logo">🏨 酒店预订系统</div>
                <span>欢迎使用酒店管理系统</span>
            </el-header>
            <el-container>
                <el-aside width="200px">
                    <el-menu
                        :default-active="activeIndex"
                        class="el-menu-vertical-demo"
                        @select="handleSelect"
                        background-color="#545c64"
                        text-color="#fff"
                        active-text-color="#ffd04b">
                        <el-menu-item index="1">
                            <i class="el-icon-house"></i>
                            <span>房型列表</span>
                        </el-menu-item>
                        <el-menu-item index="2">
                            <i class="el-icon-edit-outline"></i>
                            <span>在线预订</span>
                        </el-menu-item>
                        <el-menu-item index="3">
                            <i class="el-icon-date"></i>
                            <span>入住登记</span>
                        </el-menu-item>
                        <el-menu-item index="4">
                            <i class="el-icon-document"></i>
                            <span>订单管理</span>
                        </el-menu-item>
                        <el-menu-item index="5">
                            <i class="el-icon-s-finance"></i>
                            <span>退房结算</span>
                        </el-menu-item>
                    </el-menu>
                </el-aside>
                <el-main>
                    <router-view></router-view>
                </el-main>
            </el-container>
        </el-container>
    `
});