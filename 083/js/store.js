const Store = {
    state: {
        orders: [
            {
                id: 'ORD001',
                customerName: '张三',
                phone: '13800138001',
                copperType: '紫铜',
                holeDiameter: 3,
                style: '莲花型',
                engraving: true,
                engravingContent: '平安如意',
                status: 2,
                createTime: '2024-01-15 10:30:00'
            },
            {
                id: 'ORD002',
                customerName: '李四',
                phone: '13900139002',
                copperType: '黄铜',
                holeDiameter: 4,
                style: '祥云型',
                engraving: false,
                engravingContent: '',
                status: 4,
                createTime: '2024-01-16 14:20:00'
            },
            {
                id: 'ORD003',
                customerName: '王五',
                phone: '13700137003',
                copperType: '青铜',
                holeDiameter: 5,
                style: '竹节型',
                engraving: true,
                engravingContent: '禅',
                status: 1,
                createTime: '2024-01-17 09:15:00'
            }
        ],
        copperTypes: ['紫铜', '黄铜', '青铜', '白铜'],
        styles: ['莲花型', '祥云型', '竹节型', '如意型', '回纹型'],
        statusList: ['熔铜', '制模', '浇铸', '打磨', '做旧', '完工']
    },

    addOrder(order) {
        const newOrder = {
            id: 'ORD' + String(this.state.orders.length + 1).padStart(3, '0'),
            ...order,
            status: 0,
            createTime: new Date().toLocaleString('zh-CN', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            }).replace(/\//g, '-')
        };
        this.state.orders.unshift(newOrder);
        return newOrder;
    },

    updateOrderStatus(orderId, status) {
        const order = this.state.orders.find(o => o.id === orderId);
        if (order) {
            order.status = status;
        }
    },

    getAllOrders() {
        return this.state.orders;
    },

    getCopperTypes() {
        return this.state.copperTypes;
    },

    getStyles() {
        return this.state.styles;
    },

    getStatusList() {
        return this.state.statusList;
    }
};