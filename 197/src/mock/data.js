export const paperCategories = [
  { value: '生宣', label: '生宣', price: 5, desc: '吸水性强，适合写意画' },
  { value: '熟宣', label: '熟宣', price: 6, desc: '吸水性弱，适合工笔画' },
  { value: '半生熟', label: '半生熟', price: 5.5, desc: '吸水性适中，适合楷书' },
  { value: '皮纸', label: '皮纸', price: 8, desc: '韧性强，适合书法创作' },
  { value: '麻纸', label: '麻纸', price: 7, desc: '质感粗犷，古朴典雅' }
]

export const sizePresets = [
  { name: '四尺整张', width: 138, height: 69 },
  { name: '四尺对开', width: 138, height: 34.5 },
  { name: '四尺三开', width: 69, height: 46 },
  { name: '六尺整张', width: 180, height: 97 },
  { name: '六尺对开', width: 180, height: 48.5 },
  { name: '八尺整张', width: 248, height: 129 }
]

export const curtainPatterns = [
  { value: '单丝路', label: '单丝路' },
  { value: '双丝路', label: '双丝路' },
  { value: '罗纹', label: '罗纹' },
  { value: '龟纹', label: '龟纹' },
  { value: '绳纹', label: '绳纹' },
  { value: '回纹', label: '回纹' }
]

export const goldProcessOptions = [
  { value: '描金龙', label: '描金龙', price: 20 },
  { value: '描金凤', label: '描金凤', price: 20 },
  { value: '描金云纹', label: '描金云纹', price: 15 },
  { value: '描金山水', label: '描金山水', price: 25 },
  { value: '描金花卉', label: '描金花卉', price: 18 },
  { value: '描金书法', label: '描金书法', price: 18 }
]

export const packagingOptions = [
  { value: '简装', label: '简装', price: 5, desc: '防潮纸包装' },
  { value: '锦盒装', label: '锦盒装', price: 30, desc: '高档锦盒，送礼佳品' },
  { value: '卷轴装', label: '卷轴装', price: 50, desc: '绫绢装裱，可直接悬挂' }
]

export const processSteps = [
  { name: '选纸', icon: 'el-icon-document' },
  { name: '裁切', icon: 'el-icon-scissors' },
  { name: '水印', icon: 'el-icon-picture' },
  { name: '描金', icon: 'el-icon-edit' },
  { name: '压平', icon: 'el-icon-s-check' },
  { name: '包装', icon: 'el-icon-box' },
  { name: '质检', icon: 'el-icon-view' },
  { name: '完工', icon: 'el-icon-circle-check' }
]

export const mockOrders = [
  {
    id: 'XZ202401010001',
    category: '生宣',
    size: { width: 138, height: 69, name: '四尺整张' },
    curtainPattern: '单丝路',
    goldProcesses: ['描金龙'],
    packaging: '锦盒装',
    quantity: 20,
    remark: '加急处理',
    status: 'processing',
    currentStep: 3,
    customerName: '张先生',
    customerPhone: '13800138001',
    createdAt: '2024-01-01 10:30:00',
    steps: [
      { name: '选纸', completed: true, time: '2024-01-01 11:00:00' },
      { name: '裁切', completed: true, time: '2024-01-01 14:20:00' },
      { name: '水印', completed: true, time: '2024-01-02 09:15:00' },
      { name: '描金', completed: false, time: null },
      { name: '压平', completed: false, time: null },
      { name: '包装', completed: false, time: null },
      { name: '质检', completed: false, time: null },
      { name: '完工', completed: false, time: null }
    ]
  },
  {
    id: 'XZ202401010002',
    category: '熟宣',
    size: { width: 69, height: 46, name: '四尺三开' },
    curtainPattern: '罗纹',
    goldProcesses: ['描金云纹', '描金山水'],
    packaging: '卷轴装',
    quantity: 10,
    remark: '',
    status: 'pending',
    currentStep: 0,
    customerName: '李女士',
    customerPhone: '13900139002',
    createdAt: '2024-01-01 14:45:00',
    steps: [
      { name: '选纸', completed: false, time: null },
      { name: '裁切', completed: false, time: null },
      { name: '水印', completed: false, time: null },
      { name: '描金', completed: false, time: null },
      { name: '压平', completed: false, time: null },
      { name: '包装', completed: false, time: null },
      { name: '质检', completed: false, time: null },
      { name: '完工', completed: false, time: null }
    ]
  },
  {
    id: 'XZ202401010003',
    category: '半生熟',
    size: { width: 138, height: 34.5, name: '四尺对开' },
    curtainPattern: '双丝路',
    goldProcesses: ['描金花卉'],
    packaging: '简装',
    quantity: 50,
    remark: '企业定制，需要发票',
    status: 'completed',
    currentStep: 8,
    customerName: '王总',
    customerPhone: '13700137003',
    createdAt: '2024-01-01 09:00:00',
    steps: [
      { name: '选纸', completed: true, time: '2024-01-01 09:30:00' },
      { name: '裁切', completed: true, time: '2024-01-01 10:45:00' },
      { name: '水印', completed: true, time: '2024-01-01 15:20:00' },
      { name: '描金', completed: true, time: '2024-01-02 10:10:00' },
      { name: '压平', completed: true, time: '2024-01-02 14:30:00' },
      { name: '包装', completed: true, time: '2024-01-03 09:15:00' },
      { name: '质检', completed: true, time: '2024-01-03 10:45:00' },
      { name: '完工', completed: true, time: '2024-01-03 11:00:00' }
    ]
  }
]
