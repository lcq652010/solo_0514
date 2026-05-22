export const activities = [
  {
    id: 1,
    title: '2024年秋季迎新晚会',
    description: '欢迎新同学加入我们的大家庭，届时将有精彩的节目表演和互动游戏，还有丰厚奖品等你来拿！',
    content: '一、活动目的\n为欢迎2024级新同学加入社团大家庭，丰富课余生活，增进同学之间的交流与友谊。\n\n二、活动时间\n2024年9月15日 19:00-21:30\n\n三、活动地点\n学校大礼堂\n\n四、活动流程\n1. 开场表演\n2. 社团介绍\n3. 互动游戏\n4. 抽奖环节\n5. 自由交流',
    date: '2024-09-15',
    time: '19:00',
    location: '学校大礼堂',
    organizer: '学生会文艺部',
    type: '文艺活动',
    maxParticipants: 200,
    currentParticipants: 156,
    status: 'upcoming',
    coverImage: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=college%20welcome%20party%20stage%20performance&image_size=landscape_16_9'
  },
  {
    id: 2,
    title: '编程技术分享会',
    description: '邀请学长学姐分享编程经验，助你快速入门前端开发',
    content: '一、分享主题\n1. Vue.js 入门实战\n2. JavaScript 高级技巧\n3. 项目经验分享\n\n二、活动时间\n2024年9月20日 14:00-17:00\n\n三、活动地点\n计算机学院教学楼 302室',
    date: '2024-09-20',
    time: '14:00',
    location: '计算机学院302室',
    organizer: '编程技术社团',
    type: '学术讲座',
    maxParticipants: 50,
    currentParticipants: 42,
    status: 'upcoming',
    coverImage: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=programming%20workshop%20coding&image_size=landscape_16_9'
  },
  {
    id: 3,
    title: '户外拓展训练活动',
    description: '挑战自我，团队协作，增强团队凝聚力',
    content: '一、活动目的\n通过户外拓展活动，增强团队协作能力，挑战自我极限。\n\n二、活动时间\n2024年9月25日 08:00-18:00\n\n三、活动地点\n城郊拓展训练基地\n\n四、注意事项\n请穿着运动服和运动鞋',
    date: '2024-09-25',
    time: '08:00',
    location: '城郊拓展训练基地',
    organizer: '户外社团',
    type: '体育活动',
    maxParticipants: 30,
    currentParticipants: 30,
    status: 'upcoming',
    coverImage: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=outdoor%20team%20building%20activity&image_size=landscape_16_9'
  },
  {
    id: 4,
    title: '书法艺术展览',
    description: '欣赏优秀书法作品，感受传统文化魅力',
    content: '一、展览内容\n展出社团成员优秀书法作品50余幅，涵盖楷书、行书、草书等多种字体。\n\n二、展览时间\n2024年10月1日-10月7日\n\n三、展览地点\n学校美术馆',
    date: '2024-10-01',
    time: '09:00',
    location: '学校美术馆',
    organizer: '书法社团',
    type: '文化展览',
    maxParticipants: 500,
    currentParticipants: 0,
    status: 'upcoming',
    coverImage: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=chinese%20calligraphy%20art%20exhibition&image_size=landscape_16_9'
  },
  {
    id: 5,
    title: '篮球友谊赛',
    description: '以球会友，展示青春活力',
    content: '一、比赛安排\n各社团之间进行篮球友谊赛，增进交流，锻炼身体。\n\n二、比赛时间\n2024年9月28日 15:00-18:00\n\n三、比赛地点\n学校篮球场',
    date: '2024-09-28',
    time: '15:00',
    location: '学校篮球场',
    organizer: '体育社团',
    type: '体育活动',
    maxParticipants: 100,
    currentParticipants: 85,
    status: 'ongoing',
    coverImage: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=basketball%20game%20sports&image_size=landscape_16_9'
  }
]

export const myRegistrations = [
  {
    id: 1,
    activityId: 1,
    activityTitle: '2024年秋季迎新晚会',
    name: '张三',
    phone: '13800138000',
    registerTime: '2024-09-10 14:30',
    status: 'registered',
    checkedIn: false
  },
  {
    id: 2,
    activityId: 2,
    activityTitle: '编程技术分享会',
    name: '张三',
    phone: '13800138000',
    registerTime: '2024-09-12 09:15',
    status: 'registered',
    checkedIn: true
  },
  {
    id: 3,
    activityId: 5,
    activityTitle: '篮球友谊赛',
    name: '张三',
    phone: '13800138000',
    registerTime: '2024-09-20 16:45',
    status: 'registered',
    checkedIn: false
  },
  {
    id: 4,
    activityId: 4,
    activityTitle: '书法艺术展览',
    name: '张三',
    phone: '13800138000',
    registerTime: '2024-09-25 10:20',
    status: 'registered',
    checkedIn: false
  },
  {
    id: 5,
    activityId: 3,
    activityTitle: '户外拓展训练活动',
    name: '张三',
    phone: '13800138000',
    registerTime: '2024-09-18 08:00',
    status: 'registered',
    checkedIn: true
  },
  {
    id: 6,
    activityId: 1,
    activityTitle: '2024年秋季迎新晚会',
    name: '李四',
    phone: '13900139000',
    registerTime: '2024-09-05 15:30',
    status: 'cancelled',
    checkedIn: false
  },
  {
    id: 7,
    activityId: 2,
    activityTitle: '编程技术分享会',
    name: '王五',
    phone: '13700137000',
    registerTime: '2024-09-08 11:00',
    status: 'registered',
    checkedIn: false
  },
  {
    id: 8,
    activityId: 5,
    activityTitle: '篮球友谊赛',
    name: '赵六',
    phone: '13600136000',
    registerTime: '2024-09-15 14:20',
    status: 'registered',
    checkedIn: true
  },
  {
    id: 9,
    activityId: 1,
    activityTitle: '2024年秋季迎新晚会',
    name: '钱七',
    phone: '13500135000',
    registerTime: '2024-09-01 09:00',
    status: 'registered',
    checkedIn: false
  },
  {
    id: 10,
    activityId: 3,
    activityTitle: '户外拓展训练活动',
    name: '孙八',
    phone: '13400134000',
    registerTime: '2024-09-02 16:45',
    status: 'registered',
    checkedIn: false
  },
  {
    id: 11,
    activityId: 4,
    activityTitle: '书法艺术展览',
    name: '周九',
    phone: '13300133000',
    registerTime: '2024-08-28 10:30',
    status: 'registered',
    checkedIn: true
  },
  {
    id: 12,
    activityId: 2,
    activityTitle: '编程技术分享会',
    name: '吴十',
    phone: '13200132000',
    registerTime: '2024-08-25 14:00',
    status: 'cancelled',
    checkedIn: false
  }
]
