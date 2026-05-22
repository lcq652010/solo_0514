export const mockTrainers = [
  {
    id: 1,
    name: '张教练',
    avatar: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20male%20fitness%20trainer%20portrait&image_size=square',
    specialty: '增肌训练、力量训练',
    experience: 8,
    rating: 4.9,
    price: 300,
    status: 'online',
    phone: '138****1234'
  },
  {
    id: 2,
    name: '李教练',
    avatar: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20female%20fitness%20trainer%20portrait&image_size=square',
    specialty: '瑜伽、普拉提、形体塑造',
    experience: 6,
    rating: 4.8,
    price: 280,
    status: 'online',
    phone: '139****5678'
  },
  {
    id: 3,
    name: '王教练',
    avatar: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20male%20bodybuilding%20trainer%20portrait&image_size=square',
    specialty: '减脂塑形、HIIT训练',
    experience: 5,
    rating: 4.7,
    price: 260,
    status: 'busy',
    phone: '137****9012'
  },
  {
    id: 4,
    name: '陈教练',
    avatar: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20male%20boxing%20trainer%20portrait&image_size=square',
    specialty: '拳击、格斗、体能训练',
    experience: 10,
    rating: 4.95,
    price: 350,
    status: 'online',
    phone: '136****3456'
  },
  {
    id: 5,
    name: '刘教练',
    avatar: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20female%20pilates%20trainer%20portrait&image_size=square',
    specialty: '康复训练、产后恢复',
    experience: 7,
    rating: 4.85,
    price: 320,
    status: 'offline',
    phone: '135****7890'
  }
]

export let mockBookings = [
  {
    id: 1,
    memberName: '张三',
    trainerId: 1,
    trainerName: '张教练',
    courseName: '增肌训练课',
    courseType: '1',
    date: '2024-05-18',
    time: '10:00-11:00',
    status: 'pending',
    createTime: '2024-05-15 14:30:00'
  },
  {
    id: 2,
    memberName: '李四',
    trainerId: 2,
    trainerName: '李教练',
    courseName: '瑜伽基础课',
    courseType: '3',
    date: '2024-05-17',
    time: '14:00-15:00',
    status: 'confirmed',
    createTime: '2024-05-14 09:20:00'
  },
  {
    id: 3,
    memberName: '王五',
    trainerId: 3,
    trainerName: '王教练',
    courseName: 'HIIT减脂课',
    courseType: '2',
    date: '2024-05-16',
    time: '19:00-20:00',
    status: 'completed',
    createTime: '2024-05-13 16:45:00'
  },
  {
    id: 4,
    memberName: '赵六',
    trainerId: 4,
    trainerName: '陈教练',
    courseName: '拳击入门课',
    courseType: '1',
    date: '2024-05-19',
    time: '15:00-16:00',
    status: 'cancelled',
    createTime: '2024-05-12 11:10:00'
  },
  {
    id: 5,
    memberName: '钱七',
    trainerId: 5,
    trainerName: '刘教练',
    courseName: '康复训练课',
    courseType: '3',
    date: '2024-05-20',
    time: '09:00-10:00',
    status: 'pending',
    createTime: '2024-05-14 10:20:00'
  },
  {
    id: 6,
    memberName: '孙八',
    trainerId: 1,
    trainerName: '张教练',
    courseName: '力量训练课',
    courseType: '1',
    date: '2024-05-21',
    time: '16:00-17:00',
    status: 'confirmed',
    createTime: '2024-05-13 08:15:00'
  }
]

export const mockMemberBalances = [
  {
    id: 1,
    memberName: '张三',
    phone: '138****1234',
    balance: 5,
    totalHours: 20,
    usedHours: 15
  },
  {
    id: 2,
    memberName: '李四',
    phone: '139****5678',
    balance: 2,
    totalHours: 10,
    usedHours: 8
  },
  {
    id: 3,
    memberName: '王五',
    phone: '137****9012',
    balance: 0,
    totalHours: 5,
    usedHours: 5
  },
  {
    id: 4,
    memberName: '赵六',
    phone: '136****3456',
    balance: 10,
    totalHours: 30,
    usedHours: 20
  }
]

export const mockSchedule = {
  '2024-05-16': [
    { trainerId: 1, trainerName: '张教练', time: '09:00-12:00', status: 'working' },
    { trainerId: 2, trainerName: '李教练', time: '14:00-18:00', status: 'working' },
    { trainerId: 3, trainerName: '王教练', time: '10:00-14:00', status: 'working' }
  ],
  '2024-05-17': [
    { trainerId: 1, trainerName: '张教练', time: '09:00-12:00', status: 'working' },
    { trainerId: 4, trainerName: '陈教练', time: '15:00-19:00', status: 'working' },
    { trainerId: 5, trainerName: '刘教练', time: '10:00-16:00', status: 'rest' }
  ],
  '2024-05-18': [
    { trainerId: 2, trainerName: '李教练', time: '09:00-17:00', status: 'working' },
    { trainerId: 3, trainerName: '王教练', time: '14:00-20:00', status: 'working' }
  ]
}
