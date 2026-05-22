export const mockPackages = [
  {
    id: 1,
    orderNo: 'WL202405160001',
    senderName: '张三',
    senderPhone: '13800138001',
    senderAddress: '北京市朝阳区建国路88号',
    receiverName: '李四',
    receiverPhone: '13900139001',
    receiverAddress: '上海市浦东新区陆家嘴环路1000号',
    packageName: '电子产品',
    weight: 2.5,
    status: 'pending',
    createTime: '2024-05-16 09:00:00'
  },
  {
    id: 2,
    orderNo: 'WL202405160002',
    senderName: '王五',
    senderPhone: '13700137001',
    senderAddress: '广州市天河区天河路385号',
    receiverName: '赵六',
    receiverPhone: '13600136001',
    receiverAddress: '深圳市南山区科技园南路',
    packageName: '服装',
    weight: 1.2,
    status: 'picking',
    createTime: '2024-05-16 10:30:00'
  },
  {
    id: 3,
    orderNo: 'WL202405160003',
    senderName: '孙七',
    senderPhone: '13500135001',
    senderAddress: '杭州市西湖区文三路478号',
    receiverName: '周八',
    receiverPhone: '13400134001',
    receiverAddress: '南京市鼓楼区中山路1号',
    packageName: '书籍',
    weight: 3.8,
    status: 'delivering',
    createTime: '2024-05-15 14:20:00'
  },
  {
    id: 4,
    orderNo: 'WL202405160004',
    senderName: '吴九',
    senderPhone: '13300133001',
    senderAddress: '成都市武侯区人民南路四段',
    receiverName: '郑十',
    receiverPhone: '13200132001',
    receiverAddress: '重庆市渝中区解放碑步行街',
    packageName: '食品',
    weight: 5.0,
    status: 'signed',
    createTime: '2024-05-14 08:15:00'
  }
];

export const mockTracking = [
  {
    orderNo: 'WL202405160001',
    tracks: [
      {
        time: '2024-05-16 09:00:00',
        status: '已下单',
        location: '北京市朝阳区建国路88号',
        operator: '系统',
        remark: '订单创建成功，等待快递员揽收'
      }
    ]
  },
  {
    orderNo: 'WL202405160002',
    tracks: [
      {
        time: '2024-05-16 11:00:00',
        status: '揽收中',
        location: '广州市天河区营业点',
        operator: '快递员小王',
        remark: '快递员正在前往揽收地址'
      },
      {
        time: '2024-05-16 10:30:00',
        status: '已下单',
        location: '广州市天河区天河路385号',
        operator: '系统',
        remark: '订单创建成功，等待快递员揽收'
      }
    ]
  },
  {
    orderNo: 'WL202405160003',
    tracks: [
      {
        time: '2024-05-16 14:30:00',
        status: '派送中',
        location: '南京市鼓楼区配送站',
        operator: '快递员小张',
        remark: '快递员正在派送，请保持电话畅通'
      },
      {
        time: '2024-05-16 08:20:00',
        status: '已到达',
        location: '南京转运中心',
        operator: '系统',
        remark: '包裹已到达目的地城市，正在分拣中'
      },
      {
        time: '2024-05-15 22:10:00',
        status: '运输中',
        location: '杭州-南京干线',
        operator: '系统',
        remark: '包裹正在运输途中'
      },
      {
        time: '2024-05-15 18:00:00',
        status: '已发出',
        location: '杭州转运中心',
        operator: '系统',
        remark: '包裹已从杭州转运中心发出'
      },
      {
        time: '2024-05-15 14:20:00',
        status: '已揽收',
        location: '杭州市西湖区营业点',
        operator: '快递员小李',
        remark: '快递员已成功揽收包裹'
      }
    ]
  },
  {
    orderNo: 'WL202405160004',
    tracks: [
      {
        time: '2024-05-16 10:00:00',
        status: '已签收',
        location: '重庆市渝中区解放碑配送站',
        operator: '本人签收',
        remark: '包裹已成功签收，感谢使用我们的服务'
      },
      {
        time: '2024-05-16 08:30:00',
        status: '派送中',
        location: '重庆市渝中区配送站',
        operator: '快递员小陈',
        remark: '快递员正在派送，请保持电话畅通'
      },
      {
        time: '2024-05-15 20:00:00',
        status: '已到达',
        location: '重庆转运中心',
        operator: '系统',
        remark: '包裹已到达目的地城市'
      },
      {
        time: '2024-05-15 06:00:00',
        status: '运输中',
        location: '成都-重庆干线',
        operator: '系统',
        remark: '包裹正在运输途中'
      },
      {
        time: '2024-05-14 18:00:00',
        status: '已发出',
        location: '成都转运中心',
        operator: '系统',
        remark: '包裹已从成都转运中心发出'
      },
      {
        time: '2024-05-14 08:15:00',
        status: '已揽收',
        location: '成都市武侯区营业点',
        operator: '快递员小周',
        remark: '快递员已成功揽收包裹'
      }
    ]
  }
];

export const statusMap = {
  pending: { label: '待揽收', type: 'info' },
  picking: { label: '揽收中', type: 'warning' },
  delivering: { label: '派送中', type: 'primary' },
  signed: { label: '已签收', type: 'success' }
};
