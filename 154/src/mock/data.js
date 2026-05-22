export const ticketTypes = [
  {
    id: 1,
    name: '成人票',
    price: 120,
    originalPrice: 150,
    description: '适用于18-59周岁成人游客，包含景区所有景点',
    validDays: 1,
    maxPurchase: 10,
    dailyLimit: 100,
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=scenic%20spot%20adult%20ticket%20beautiful%20landscape&image_size=square_hd',
    tags: ['热门', '推荐']
  },
  {
    id: 2,
    name: '儿童票',
    price: 60,
    originalPrice: 80,
    description: '适用于1.2米-1.5米儿童，需成人陪同入园',
    validDays: 1,
    maxPurchase: 5,
    dailyLimit: 80,
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=happy%20children%20in%20park%20colorful&image_size=square_hd',
    tags: ['优惠']
  },
  {
    id: 3,
    name: '老年票',
    price: 80,
    originalPrice: 100,
    description: '适用于60周岁以上老人，需出示有效证件',
    validDays: 1,
    maxPurchase: 3,
    dailyLimit: 50,
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=elderly%20people%20enjoying%20nature%20park&image_size=square_hd',
    tags: ['优惠']
  },
  {
    id: 4,
    name: '学生票',
    price: 90,
    originalPrice: 120,
    description: '全日制本科及以下学生，需出示有效学生证',
    validDays: 1,
    maxPurchase: 5,
    dailyLimit: 60,
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=students%20in%20beautiful%20garden%20campus&image_size=square_hd',
    tags: ['优惠']
  },
  {
    id: 5,
    name: '家庭套票',
    price: 280,
    originalPrice: 360,
    description: '包含2成人+1儿童，一家三口出游首选',
    validDays: 1,
    maxPurchase: 2,
    dailyLimit: 30,
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=happy%20family%20in%20amusement%20park&image_size=square_hd',
    tags: ['超值', '推荐']
  },
  {
    id: 6,
    name: '两日通票',
    price: 200,
    originalPrice: 260,
    description: '两天内无限次入园，深度游览景区',
    validDays: 2,
    maxPurchase: 5,
    dailyLimit: 40,
    image: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sunset%20over%20beautiful%20scenic%20area&image_size=square_hd',
    tags: ['深度游']
  }
];

export const orders = [
  {
    id: 'ORD20240101001',
    ticketName: '成人票',
    quantity: 2,
    totalPrice: 240,
    visitorName: '张三',
    visitorPhone: '138****1234',
    visitDate: '2024-01-15',
    status: 'paid',
    createTime: '2024-01-10 09:30:00',
    ticketCode: 'TC202401150001'
  },
  {
    id: 'ORD20240101002',
    ticketName: '家庭套票',
    quantity: 1,
    totalPrice: 280,
    visitorName: '李四',
    visitorPhone: '139****5678',
    visitDate: '2024-01-16',
    status: 'used',
    createTime: '2024-01-11 14:20:00',
    ticketCode: 'TC202401160002',
    useTime: '2024-01-16 10:15:00'
  },
  {
    id: 'ORD20240101003',
    ticketName: '儿童票',
    quantity: 3,
    totalPrice: 180,
    visitorName: '王五',
    visitorPhone: '137****9012',
    visitDate: '2024-01-18',
    status: 'pending',
    createTime: '2024-01-12 16:45:00',
    ticketCode: 'TC202401180003'
  },
  {
    id: 'ORD20240101004',
    ticketName: '两日通票',
    quantity: 2,
    totalPrice: 400,
    visitorName: '赵六',
    visitorPhone: '136****3456',
    visitDate: '2024-01-20',
    status: 'refunded',
    createTime: '2024-01-08 11:00:00',
    ticketCode: 'TC202401200004',
    refundTime: '2024-01-09 09:00:00'
  }
];

export const statistics = {
  todayVisitors: 1256,
  todayOrders: 328,
  totalRevenue: 45680,
  remainingTickets: 5864,
  weeklyData: [
    { date: '周一', visitors: 890, orders: 230 },
    { date: '周二', visitors: 756, orders: 198 },
    { date: '周三', visitors: 923, orders: 245 },
    { date: '周四', visitors: 1012, orders: 278 },
    { date: '周五', visitors: 1345, orders: 356 },
    { date: '周六', visitors: 2156, orders: 568 },
    { date: '周日', visitors: 1987, orders: 512 }
  ]
};

export const statusMap = {
  pending: { label: '待支付', type: 'warning', color: '#E6A23C' },
  paid: { label: '已支付', type: 'success', color: '#67C23A' },
  used: { label: '已使用', type: 'info', color: '#909399' },
  refunded: { label: '已退款', type: 'danger', color: '#F56C6C' }
};

export function generateOrderId() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const random = String(Math.floor(Math.random() * 1000)).padStart(3, '0');
  return `ORD${year}${month}${day}${random}`;
}

export function generateTicketCode(visitDate) {
  const dateStr = visitDate.replace(/-/g, '').slice(2);
  const random = String(Math.floor(Math.random() * 10000)).padStart(4, '0');
  return `TC${dateStr}${random}`;
}

export function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

export function formatDateTime(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  const seconds = String(d.getSeconds()).padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

export function getDailySales(ticketName, visitDate) {
  const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
  const allOrders = [...localOrders, ...orders];
  const sales = allOrders
    .filter(order => 
      order.ticketName === ticketName && 
      order.visitDate === visitDate && 
      (order.status === 'paid' || order.status === 'used')
    )
    .reduce((sum, order) => sum + order.quantity, 0);
  return sales;
}

export function getTicketDailyLimit(ticketId) {
  const ticket = ticketTypes.find(t => t.id === ticketId);
  return ticket ? ticket.dailyLimit : 1000;
}

export function checkDailyLimit(ticketId, visitDate, quantity) {
  const ticket = ticketTypes.find(t => t.id === ticketId);
  if (!ticket) return { exceeded: false, remaining: 999 };
  
  const currentSales = getDailySales(ticket.name, visitDate);
  const remaining = ticket.dailyLimit - currentSales;
  const exceeded = remaining < quantity;
  
  return {
    exceeded,
    remaining: Math.max(0, remaining),
    limit: ticket.dailyLimit,
    current: currentSales
  };
}

export function checkTicketUsed(ticketCode) {
  const localOrders = JSON.parse(localStorage.getItem('orders') || '[]');
  const allOrders = [...localOrders, ...orders];
  const order = allOrders.find(o => o.ticketCode === ticketCode);
  
  if (!order) {
    return { exists: false, used: false };
  }
  
  return {
    exists: true,
    used: order.status === 'used',
    order: order
  };
}
