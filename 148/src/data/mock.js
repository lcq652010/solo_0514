export const movies = [
  {
    id: 1,
    title: '流浪地球3',
    poster: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=sci-fi%20movie%20poster%20space%20earth%20future&image_size=portrait_4_3',
    rating: 9.5,
    duration: 173,
    type: '科幻/冒险',
    director: '郭帆',
    actors: '吴京, 刘德华, 李雪健',
    description: '太阳即将毁灭，人类在地球表面建造出巨大的推进器，寻找新的家园。面对前所未有的危机，联合政府制定了一个名为"流浪地球"的计划，试图带着地球逃离太阳系，寻找人类新的居住地。',
    releaseDate: '2025-01-22'
  },
  {
    id: 2,
    title: '封神第三部',
    poster: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=chinese%20mythology%20movie%20poster%20warrior%20gods&image_size=portrait_4_3',
    rating: 8.8,
    duration: 148,
    type: '神话/动作',
    director: '乌尔善',
    actors: '费翔, 李雪健, 黄渤',
    description: '纣王覆灭，天下未定。武王伐纣的最终决战即将打响，封神榜的秘密也将揭晓。仙魔大战一触即发，谁将主宰三界命运？',
    releaseDate: '2025-02-10'
  },
  {
    id: 3,
    title: '速度与激情11',
    poster: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=car%20racing%20movie%20poster%20fast%20cars%20action&image_size=portrait_4_3',
    rating: 8.2,
    duration: 135,
    type: '动作/犯罪',
    director: '林诣彬',
    actors: '范·迪塞尔, 杰森·斯坦森',
    description: '多姆和他的家族面临前所未有的威胁，一个来自过去的神秘敌人誓言要复仇。为了保护家人，他们必须再次集结，展开一场跨越全球的极速冒险。',
    releaseDate: '2025-03-15'
  },
  {
    id: 4,
    title: '唐人街探案4',
    poster: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=detective%20comedy%20movie%20poster%20mystery%20china%20town&image_size=portrait_4_3',
    rating: 8.5,
    duration: 130,
    type: '喜剧/悬疑',
    director: '陈思诚',
    actors: '王宝强, 刘昊然',
    description: '唐仁和秦风再次踏上探案之旅，这次他们来到了伦敦，卷入了一桩涉及国际犯罪组织的惊天大案。笑料与推理并存，真相即将揭晓。',
    releaseDate: '2025-02-01'
  },
  {
    id: 5,
    title: '阿凡达3：水之道续集',
    poster: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=avatar%20movie%20poster%20alien%20planet%20ocean%20blue&image_size=portrait_4_3',
    rating: 9.1,
    duration: 190,
    type: '科幻/冒险',
    director: '詹姆斯·卡梅隆',
    actors: '萨姆·沃辛顿, 佐伊·索尔达娜',
    description: '杰克和奈蒂莉继续在潘多拉星球探索新的秘境，这次他们将深入神秘的地下世界，发现更多关于这个星球的秘密，同时也要面对更强大的敌人。',
    releaseDate: '2025-04-20'
  },
  {
    id: 6,
    title: '我和我的父辈2',
    poster: 'https://trae-api-cn.mchost.guru/api/ide/v1/text_to_image?prompt=chinese%20family%20drama%20movie%20poster%20generations%20nostalgia&image_size=portrait_4_3',
    rating: 8.3,
    duration: 150,
    type: '剧情/家庭',
    director: '多位导演',
    actors: '吴京, 章子怡, 徐峥',
    description: '通过四个不同时代的故事，展现中国几代人之间的亲情传承与时代变迁。从改革开放到新时代，每个家庭都有自己的奋斗与感动。',
    releaseDate: '2025-01-28'
  }
]

export const cinemas = [
  { id: 1, name: '星光影城（旗舰店）', address: '北京市朝阳区建国路88号', distance: '1.2km' },
  { id: 2, name: '星光影城（CBD店）', address: '北京市朝阳区国贸三期B1层', distance: '2.5km' },
  { id: 3, name: '星光影城（西单店）', address: '北京市西城区西单大悦城8层', distance: '3.8km' },
  { id: 4, name: '星光影城（中关村店）', address: '北京市海淀区中关村大街1号', distance: '5.2km' }
]

export const schedules = [
  {
    id: 1,
    movieId: 1,
    cinemaId: 1,
    date: '2025-05-17',
    time: '10:30',
    endTime: '13:23',
    hall: '1号激光IMAX厅',
    price: 89,
    language: '国语',
    dimension: '3D'
  },
  {
    id: 2,
    movieId: 1,
    cinemaId: 1,
    date: '2025-05-17',
    time: '14:00',
    endTime: '16:53',
    hall: '2号杜比全景声厅',
    price: 79,
    language: '国语',
    dimension: '3D'
  },
  {
    id: 3,
    movieId: 1,
    cinemaId: 1,
    date: '2025-05-17',
    time: '18:30',
    endTime: '21:23',
    hall: '1号激光IMAX厅',
    price: 99,
    language: '国语',
    dimension: '3D'
  },
  {
    id: 4,
    movieId: 1,
    cinemaId: 2,
    date: '2025-05-17',
    time: '11:00',
    endTime: '13:53',
    hall: '3号普通厅',
    price: 59,
    language: '国语',
    dimension: '2D'
  },
  {
    id: 5,
    movieId: 2,
    cinemaId: 1,
    date: '2025-05-17',
    time: '09:30',
    endTime: '11:58',
    hall: '4号巨幕厅',
    price: 69,
    language: '国语',
    dimension: '2D'
  },
  {
    id: 6,
    movieId: 2,
    cinemaId: 1,
    date: '2025-05-17',
    time: '15:00',
    endTime: '17:28',
    hall: '2号杜比全景声厅',
    price: 79,
    language: '国语',
    dimension: '2D'
  },
  {
    id: 7,
    movieId: 3,
    cinemaId: 1,
    date: '2025-05-17',
    time: '20:00',
    endTime: '22:15',
    hall: '5号VIP厅',
    price: 128,
    language: '英语',
    dimension: '2D'
  },
  {
    id: 8,
    movieId: 4,
    cinemaId: 2,
    date: '2025-05-17',
    time: '13:00',
    endTime: '15:10',
    hall: '1号厅',
    price: 49,
    language: '国语',
    dimension: '2D'
  }
]

export const orders = [
  {
    id: 'ORD202505170001',
    movieTitle: '流浪地球3',
    cinemaName: '星光影城（旗舰店）',
    hall: '1号激光IMAX厅',
    sessionTime: '2025-05-17 18:30',
    seats: ['8排5座', '8排6座'],
    quantity: 2,
    totalPrice: 198,
    status: 'paid',
    createTime: '2025-05-17 10:30:25',
    phone: '138****8888'
  },
  {
    id: 'ORD202505160002',
    movieTitle: '封神第三部',
    cinemaName: '星光影城（CBD店）',
    hall: '4号巨幕厅',
    sessionTime: '2025-05-16 19:00',
    seats: ['5排12座'],
    quantity: 1,
    totalPrice: 69,
    status: 'completed',
    createTime: '2025-05-16 14:20:10',
    phone: '138****8888'
  },
  {
    id: 'ORD202505150003',
    movieTitle: '唐人街探案4',
    cinemaName: '星光影城（西单店）',
    hall: '2号厅',
    sessionTime: '2025-05-18 15:30',
    seats: ['6排8座', '6排9座', '6排10座'],
    quantity: 3,
    totalPrice: 147,
    status: 'paid',
    createTime: '2025-05-15 09:15:33',
    phone: '138****8888'
  },
  {
    id: 'ORD202505100004',
    movieTitle: '我和我的父辈2',
    cinemaName: '星光影城（中关村店）',
    hall: '3号厅',
    sessionTime: '2025-05-10 14:00',
    seats: ['7排3座', '7排4座'],
    quantity: 2,
    totalPrice: 86,
    status: 'refunded',
    createTime: '2025-05-09 20:10:45',
    phone: '138****8888'
  }
]

export function generateSeats(scheduleId) {
  const rows = 10
  const cols = 15
  const seats = []
  
  for (let r = 1; r <= rows; r++) {
    const row = []
    for (let c = 1; c <= cols; c++) {
      const isOccupied = Math.random() < 0.3
      row.push({
        row: r,
        col: c,
        status: isOccupied ? 'occupied' : 'available',
        id: `${r}-${c}`
      })
    }
    seats.push(row)
  }
  
  return seats
}
