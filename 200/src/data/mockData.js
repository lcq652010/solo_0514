export const stoneTypes = [
  { value: 'duan', label: '端砚石' },
  { value: 'she', label: '歙砚石' },
  { value: 'tao', label: '洮砚石' },
  { value: 'chengni', label: '澄泥砚石' },
  { value: 'hongsi', label: '红丝砚石' },
  { value: 'songhua', label: '松花砚石' }
]

export const carvingStyles = [
  { value: 'plain', label: '素面' },
  { value: 'cloud_dragon', label: '云龙纹' },
  { value: 'landscape', label: '山水纹' },
  { value: 'plum_orchid', label: '梅兰竹菊' },
  { value: 'flowers_birds', label: '花鸟鱼虫' },
  { value: 'figures', label: '人物故事' },
  { value: 'auspicious', label: '吉祥图案' }
]

export const inkPoolShapes = [
  { value: 'round', label: '圆形' },
  { value: 'square', label: '方形' },
  { value: 'oval', label: '椭圆形' },
  { value: 'rectangle', label: '长方形' },
  { value: 'special', label: '异形' },
  { value: 'natural', label: '天然形' }
]

export const processSteps = [
  { key: 'quarrying', label: '采石' },
  { key: 'cutting', label: '切坯' },
  { key: 'shaping', label: '整形' },
  { key: 'carving', label: '雕刻' },
  { key: 'polishing', label: '打磨' },
  { key: 'waxing', label: '上蜡' },
  { key: 'inspecting', label: '质检' },
  { key: 'completed', label: '完工' }
]

export const statusLabels = {
  pending: '待处理',
  quarrying: '采石中',
  cutting: '切坯中',
  shaping: '整形中',
  carving: '雕刻中',
  polishing: '打磨中',
  waxing: '上蜡中',
  inspecting: '质检中',
  completed: '已完工'
}

export const statusColors = {
  pending: 'warning',
  quarrying: 'primary',
  cutting: 'primary',
  shaping: 'primary',
  carving: 'primary',
  polishing: 'primary',
  waxing: 'primary',
  inspecting: 'primary',
  completed: 'success'
}

const getTimeString = (hoursAgo) => {
  const date = new Date(Date.now() - hoursAgo * 60 * 60 * 1000)
  return date.toLocaleString('zh-CN', { 
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit',
    hour12: false
  }).replace(/\//g, '-')
}

export const mockOrders = [
  {
    id: 'ORD' + Date.now().toString().slice(-6),
    stoneType: 'songhua',
    length: 25,
    width: 18,
    carvingStyle: 'plain',
    inkPoolShape: 'round',
    status: 'pending',
    createdAt: getTimeString(2),
    processSteps: []
  },
  {
    id: 'ORD' + (Date.now() - 5 * 3600 * 1000).toString().slice(-6),
    stoneType: 'hongsi',
    length: 20,
    width: 14,
    carvingStyle: 'auspicious',
    inkPoolShape: 'oval',
    status: 'quarrying',
    createdAt: getTimeString(5),
    processSteps: [
      { status: 'quarrying', time: getTimeString(4) }
    ]
  },
  {
    id: 'ORD' + (Date.now() - 10 * 3600 * 1000).toString().slice(-6),
    stoneType: 'chengni',
    length: 28,
    width: 20,
    carvingStyle: 'figures',
    inkPoolShape: 'rectangle',
    status: 'pending',
    createdAt: getTimeString(10),
    processSteps: []
  },
  {
    id: 'ORD202401010001',
    stoneType: 'duan',
    length: 25,
    width: 18,
    carvingStyle: 'cloud_dragon',
    inkPoolShape: 'round',
    status: 'carving',
    createdAt: '2024-01-01 10:30:00',
    processSteps: [
      { status: 'quarrying', time: '2024-01-01 11:00:00' },
      { status: 'cutting', time: '2024-01-02 09:00:00' },
      { status: 'shaping', time: '2024-01-03 14:00:00' },
      { status: 'carving', time: '2024-01-05 10:00:00' }
    ]
  },
  {
    id: 'ORD202401020002',
    stoneType: 'she',
    length: 30,
    width: 20,
    carvingStyle: 'landscape',
    inkPoolShape: 'oval',
    status: 'polishing',
    createdAt: '2024-01-02 14:20:00',
    processSteps: [
      { status: 'quarrying', time: '2024-01-02 15:00:00' },
      { status: 'cutting', time: '2024-01-03 10:00:00' },
      { status: 'shaping', time: '2024-01-04 09:00:00' },
      { status: 'carving', time: '2024-01-06 11:00:00' },
      { status: 'polishing', time: '2024-01-08 08:00:00' }
    ]
  },
  {
    id: 'ORD202401030003',
    stoneType: 'tao',
    length: 22,
    width: 16,
    carvingStyle: 'plum_orchid',
    inkPoolShape: 'square',
    status: 'completed',
    createdAt: '2024-01-03 09:15:00',
    processSteps: [
      { status: 'quarrying', time: '2024-01-03 10:00:00' },
      { status: 'cutting', time: '2024-01-04 09:00:00' },
      { status: 'shaping', time: '2024-01-05 10:00:00' },
      { status: 'carving', time: '2024-01-07 09:00:00' },
      { status: 'polishing', time: '2024-01-09 10:00:00' },
      { status: 'waxing', time: '2024-01-10 09:00:00' },
      { status: 'inspecting', time: '2024-01-11 14:00:00' },
      { status: 'completed', time: '2024-01-12 10:00:00' }
    ]
  },
  {
    id: 'ORD202401050004',
    stoneType: 'chengni',
    length: 28,
    width: 19,
    carvingStyle: 'auspicious',
    inkPoolShape: 'special',
    status: 'pending',
    createdAt: '2024-01-05 16:45:00',
    processSteps: []
  },
  {
    id: 'ORD202401060005',
    stoneType: 'hongsi',
    length: 20,
    width: 15,
    carvingStyle: 'flowers_birds',
    inkPoolShape: 'natural',
    status: 'waxing',
    createdAt: '2024-01-06 11:30:00',
    processSteps: [
      { status: 'quarrying', time: '2024-01-06 14:00:00' },
      { status: 'cutting', time: '2024-01-07 09:00:00' },
      { status: 'shaping', time: '2024-01-08 10:00:00' },
      { status: 'carving', time: '2024-01-10 09:00:00' },
      { status: 'polishing', time: '2024-01-12 10:00:00' },
      { status: 'waxing', time: '2024-01-13 09:00:00' }
    ]
  }
]
