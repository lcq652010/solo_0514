const store = {
  data: {
    appointmentRecords: [
      {
        appointmentNo: 'AP20240115001',
        petName: '豆豆',
        petType: '狗',
        breed: '金毛',
        petGender: '公',
        age: 3,
        weight: 25,
        ownerName: '张三',
        phone: '13800138000',
        backupPhone: '',
        appointmentDate: '2024-01-15',
        timeSlot: '08:00-09:00',
        department: '内科',
        doctor: '张医生',
        symptoms: '食欲不振，精神萎靡，持续两天',
        status: '待就诊'
      },
      {
        appointmentNo: 'AP20240115002',
        petName: '咪咪',
        petType: '猫',
        breed: '英短',
        petGender: '母',
        age: 2,
        weight: 4,
        ownerName: '李四',
        phone: '13900139000',
        backupPhone: '',
        appointmentDate: '2024-01-15',
        timeSlot: '09:00-10:00',
        department: '皮肤科',
        doctor: '王医生',
        symptoms: '皮肤瘙痒，频繁抓挠，有脱毛现象',
        status: '已就诊'
      },
      {
        appointmentNo: 'AP20240116001',
        petName: '旺财',
        petType: '狗',
        breed: '泰迪',
        petGender: '公',
        age: 5,
        weight: 8,
        ownerName: '王五',
        phone: '13700137000',
        backupPhone: '',
        appointmentDate: '2024-01-16',
        timeSlot: '14:00-15:00',
        department: '外科',
        doctor: '李医生',
        symptoms: '后腿跛行，不愿活动',
        status: '已取消'
      },
      {
        appointmentNo: 'AP20240114001',
        petName: '花花',
        petType: '猫',
        breed: '布偶',
        petGender: '母',
        age: 1,
        weight: 3,
        ownerName: '赵六',
        phone: '13600136000',
        backupPhone: '',
        appointmentDate: '2024-01-14',
        timeSlot: '10:00-11:00',
        department: '疫苗接种',
        doctor: '刘医生',
        symptoms: '常规疫苗接种',
        status: '已过期'
      }
    ],
    petRecords: [
      {
        petName: '咪咪',
        petType: '猫',
        breed: '英短',
        ownerName: '李四',
        phone: '13900139000'
      },
      {
        petName: '旺财',
        petType: '狗',
        breed: '泰迪',
        ownerName: '王五',
        phone: '13700137000'
      },
      {
        petName: '豆豆',
        petType: '狗',
        breed: '金毛',
        ownerName: '张三',
        phone: '13800138000'
      },
      {
        petName: '花花',
        petType: '猫',
        breed: '布偶',
        ownerName: '赵六',
        phone: '13600136000'
      }
    ]
  },
  listeners: [],
  
  subscribe(callback) {
    this.listeners.push(callback)
  },
  
  notify() {
    this.listeners.forEach(callback => callback())
  },
  
  addAppointment(appointment) {
    this.data.appointmentRecords.unshift(appointment)
    this.notify()
  },
  
  updateAppointmentStatus(appointmentNo, status) {
    const record = this.data.appointmentRecords.find(r => r.appointmentNo === appointmentNo)
    if (record) {
      record.status = status
      this.notify()
    }
  },
  
  addPet(pet) {
    if (!this.data.petRecords.some(p => 
      p.petName === pet.petName && 
      p.ownerName === pet.ownerName && 
      p.phone === pet.phone
    )) {
      this.data.petRecords.push(pet)
      this.notify()
    }
  },
  
  getAppointments() {
    return this.data.appointmentRecords
  },
  
  getPets() {
    return this.data.petRecords
  },
  
  getBookedSlots(doctor, date) {
    return this.data.appointmentRecords
      .filter(r => r.doctor === doctor && r.appointmentDate === date && r.status !== '已取消')
      .map(r => r.timeSlot)
  }
}

export default store
