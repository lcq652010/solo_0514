export const stoneMaterials = [
  { value: 'shoushan', label: '寿山石', price: 280 },
  { value: 'qingtian', label: '青田石', price: 180 },
  { value: 'balin', label: '巴林石', price: 220 },
  { value: 'changhua', label: '昌化石', price: 250 },
  { value: 'tianhuang', label: '田黄石', price: 880 },
  { value: 'xuehua', label: '雪花石', price: 150 }
]

export const fontStyles = [
  { value: 'zhuanshu', label: '小篆' },
  { value: 'dazhuan', label: '大篆' },
  { value: 'mizhuan', label: '摹印篆' },
  { value: 'jiaguwen', label: '甲骨文' },
  { value: 'jinwen', label: '金文' }
]

export const sideOptions = [
  { value: 'none', label: '无边款' },
  { value: 'simple', label: '简单边款（姓名）' },
  { value: 'poem', label: '诗词边款' },
  { value: 'custom', label: '自定义边款' }
]

export const processSteps = [
  { id: 1, name: '选石', key: 'select' },
  { id: 2, name: '打磨', key: 'polish' },
  { id: 3, name: '上稿', key: 'draft' },
  { id: 4, name: '篆刻', key: 'carve' },
  { id: 5, name: '修边', key: 'trim' },
  { id: 6, name: '钤印', key: 'stamp' },
  { id: 7, name: '封蜡', key: 'wax' },
  { id: 8, name: '完工', key: 'finish' }
]

export const orders = [
  {
    id: 'ORD001',
    customerName: '张三',
    phone: '13800138001',
    stoneMaterial: 'shoushan',
    stoneMaterialLabel: '寿山石',
    size: 2.5,
    fontStyle: 'zhuanshu',
    fontStyleLabel: '小篆',
    sealContent: '宁静致远',
    sideOption: 'poem',
    sideOptionLabel: '诗词边款',
    sideContent: '海内存知己，天涯若比邻',
    currentStep: 4,
    createTime: '2026-05-15 10:30:00',
    price: 380,
    status: 'processing'
  },
  {
    id: 'ORD002',
    customerName: '李四',
    phone: '13900139002',
    stoneMaterial: 'qingtian',
    stoneMaterialLabel: '青田石',
    size: 3.0,
    fontStyle: 'dazhuan',
    fontStyleLabel: '大篆',
    sealContent: '上善若水',
    sideOption: 'simple',
    sideOptionLabel: '简单边款（姓名）',
    sideContent: '李四',
    currentStep: 2,
    createTime: '2026-05-16 14:20:00',
    price: 230,
    status: 'processing'
  },
  {
    id: 'ORD003',
    customerName: '王五',
    phone: '13700137003',
    stoneMaterial: 'tianhuang',
    stoneMaterialLabel: '田黄石',
    size: 2.0,
    fontStyle: 'jiaguwen',
    fontStyleLabel: '甲骨文',
    sealContent: '道法自然',
    sideOption: 'none',
    sideOptionLabel: '无边款',
    sideContent: '',
    currentStep: 8,
    createTime: '2026-05-14 09:15:00',
    price: 980,
    status: 'completed'
  }
]

export default {
  stoneMaterials,
  fontStyles,
  sideOptions,
  processSteps,
  orders
}
