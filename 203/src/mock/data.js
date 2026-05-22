export const materials = [
  { value: 'silk-100', label: '100%桑蚕丝', price: 200, desc: '上等桑蚕丝，光泽柔润，手感细腻' },
  { value: 'silk-mix', label: '桑蚕丝混纺', price: 150, desc: '桑蚕丝与优质纤维混纺，经济实惠' },
  { value: 'tussah', label: '柞蚕丝', price: 180, desc: '野生柞蚕丝，质地坚挺，纹理粗犷' },
  { value: 'brocade', label: '织锦缎', price: 250, desc: '传统织锦工艺，花色繁复，华贵典雅' }
]

export const patterns = [
  { value: 'landscape', label: '山水', desc: '青山绿水，意境悠远' },
  { value: 'flower', label: '花卉', desc: '牡丹、荷花、梅花等传统花卉' },
  { value: 'figure', label: '人物', desc: '仕女、罗汉等传统人物纹样' },
  { value: 'bird', label: '花鸟', desc: '花鸟虫鱼，生机盎然' },
  { value: 'calligraphy', label: '书法', desc: '名家书法，墨香四溢' },
  { value: 'dragon', label: '龙凤', desc: '龙凤呈祥，吉祥如意' }
]

export const densities = [
  { value: 'normal', label: '常规密度(80经/吋)', priceMultiplier: 1 },
  { value: 'high', label: '高密度(120经/吋)', priceMultiplier: 1.5 },
  { value: 'super', label: '超高密度(160经/吋)', priceMultiplier: 2 }
]

export const edgeTypes = [
  { value: 'normal', label: '普通包边', price: 30 },
  { value: 'silk', label: '真丝滚边', price: 60 },
  { value: 'gold', label: '金线包边', price: 100 },
  { value: 'jade', label: '玉石包边', price: 150 }
]

export const stepNames = ['经线', '纹样起稿', '戗色织造', '修剪', '包边', '整烫', '质检', '完工']

export const mockOrders = [
  {
    id: 'ORD20260518001',
    orderNo: 'KS20260518001',
    material: 'silk-100',
    materialLabel: '100%桑蚕丝',
    sizeWidth: 30,
    sizeHeight: 20,
    pattern: 'landscape',
    patternLabel: '山水',
    density: 'high',
    densityLabel: '高密度(120经/吋)',
    edgeType: 'silk',
    edgeTypeLabel: '真丝滚边',
    customerName: '张三',
    customerPhone: '138****8888',
    remark: '希望山水意境更加淡雅',
    status: 'processing',
    currentStep: 3,
    createTime: 1715990400000,
    price: 660,
    steps: [
      { name: '经线', completed: true, time: 1715990400000 },
      { name: '纹样起稿', completed: true, time: 1716076800000 },
      { name: '戗色织造', completed: true, time: 1716163200000 },
      { name: '修剪', completed: false, time: null },
      { name: '包边', completed: false, time: null },
      { name: '整烫', completed: false, time: null },
      { name: '质检', completed: false, time: null },
      { name: '完工', completed: false, time: null }
    ]
  },
  {
    id: 'ORD20260518002',
    orderNo: 'KS20260518002',
    material: 'brocade',
    materialLabel: '织锦缎',
    sizeWidth: 35,
    sizeHeight: 22,
    pattern: 'dragon',
    patternLabel: '龙凤',
    density: 'super',
    densityLabel: '超高密度(160经/吋)',
    edgeType: 'gold',
    edgeTypeLabel: '金线包边',
    customerName: '李四',
    customerPhone: '139****6666',
    remark: '婚庆用品，希望更喜庆',
    status: 'pending',
    currentStep: 0,
    createTime: 1716076800000,
    price: 1450,
    steps: [
      { name: '经线', completed: false, time: null },
      { name: '纹样起稿', completed: false, time: null },
      { name: '戗色织造', completed: false, time: null },
      { name: '修剪', completed: false, time: null },
      { name: '包边', completed: false, time: null },
      { name: '整烫', completed: false, time: null },
      { name: '质检', completed: false, time: null },
      { name: '完工', completed: false, time: null }
    ]
  },
  {
    id: 'ORD20260518003',
    orderNo: 'KS20260518003',
    material: 'tussah',
    materialLabel: '柞蚕丝',
    sizeWidth: 28,
    sizeHeight: 18,
    pattern: 'calligraphy',
    patternLabel: '书法',
    density: 'normal',
    densityLabel: '常规密度(80经/吋)',
    edgeType: 'normal',
    edgeTypeLabel: '普通包边',
    customerName: '王五',
    customerPhone: '137****5555',
    remark: '',
    status: 'completed',
    currentStep: 7,
    createTime: 1715904000000,
    price: 402,
    steps: [
      { name: '经线', completed: true, time: 1715904000000 },
      { name: '纹样起稿', completed: true, time: 1715990400000 },
      { name: '戗色织造', completed: true, time: 1716076800000 },
      { name: '修剪', completed: true, time: 1716163200000 },
      { name: '包边', completed: true, time: 1716249600000 },
      { name: '整烫', completed: true, time: 1716336000000 },
      { name: '质检', completed: true, time: 1716422400000 },
      { name: '完工', completed: true, time: 1716508800000 }
    ]
  }
]
