export const mockOrders = [
  {
    id: 'ORD1715000001',
    material: '白藤',
    height: 25,
    diameter: 30,
    style: '平编',
    handle: '双提手',
    contact: '13800138001',
    currentProcess: 3,
    status: 'processing',
    createdAt: '2024-05-01T10:30:00.000Z',
    processTimes: [
      '2024-05-01T10:30:00.000Z',
      '2024-05-01T11:00:00.000Z',
      '2024-05-01T14:00:00.000Z',
      '2024-05-02T09:00:00.000Z',
      null,
      null,
      null,
      null
    ]
  },
  {
    id: 'ORD1715000002',
    material: '红藤',
    height: 20,
    diameter: 25,
    style: '绞编',
    handle: '藤编提手',
    contact: '13900139002',
    currentProcess: 7,
    status: 'completed',
    createdAt: '2024-04-28T09:00:00.000Z',
    processTimes: [
      '2024-04-28T09:00:00.000Z',
      '2024-04-28T09:30:00.000Z',
      '2024-04-28T12:00:00.000Z',
      '2024-04-28T14:00:00.000Z',
      '2024-04-29T09:00:00.000Z',
      '2024-04-29T11:00:00.000Z',
      '2024-04-29T14:00:00.000Z',
      '2024-04-29T16:00:00.000Z'
    ]
  },
  {
    id: 'ORD1715000003',
    material: '紫竹藤',
    height: 30,
    diameter: 35,
    style: '六角编',
    handle: '单提手',
    contact: '13700137003',
    currentProcess: 0,
    status: 'pending',
    createdAt: '2024-05-03T15:00:00.000Z',
    processTimes: [
      '2024-05-03T15:00:00.000Z',
      null,
      null,
      null,
      null,
      null,
      null,
      null
    ]
  }
]

export const materialOptions = [
  { value: '白藤', label: '白藤', desc: '质地柔韧，色泽洁白', price: 0 },
  { value: '红藤', label: '红藤', desc: '天然红色，高贵典雅', price: 20 },
  { value: '黄藤', label: '黄藤', desc: '金黄透亮，经久耐用', price: 15 },
  { value: '紫竹藤', label: '紫竹藤', desc: '紫黑高贵，收藏级', price: 50 }
]

export const styleOptions = [
  { value: '平编', label: '平编', desc: '经典简约' },
  { value: '绞编', label: '绞编', desc: '纹理交错' },
  { value: '六角编', label: '六角编', desc: '六边形花纹' },
  { value: '麻花编', label: '麻花编', desc: '麻花状纹理' }
]

export const handleOptions = [
  { value: '无提手', label: '无提手', price: 0 },
  { value: '单提手', label: '单提手', price: 10 },
  { value: '双提手', label: '双提手', price: 20 },
  { value: '藤编提手', label: '藤编提手', price: 30 }
]
