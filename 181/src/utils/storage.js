const STORAGE_KEY = 'express_station_data'

function getData() {
  const data = localStorage.getItem(STORAGE_KEY)
  return data ? JSON.parse(data) : { packages: [], pickupRecords: [] }
}

function saveData(data) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data))
}

export const packageStorage = {
  addPackage(packageData) {
    const data = getData()
    data.packages.push({
      ...packageData,
      inboundTime: new Date().toLocaleString(),
      status: '待取件'
    })
    saveData(data)
  },

  getPackageByTrackingNo(trackingNo) {
    const data = getData()
    return data.packages.find(p => p.trackingNo === trackingNo)
  },

  getPackageByPickupCode(pickupCode) {
    const data = getData()
    return data.packages.find(p => p.pickupCode === pickupCode)
  },

  updatePackageStatus(trackingNo, status) {
    const data = getData()
    const pkg = data.packages.find(p => p.trackingNo === trackingNo)
    if (pkg) {
      pkg.status = status
      saveData(data)
    }
  },

  getAllPackages() {
    return getData().packages
  },

  exists(trackingNo) {
    const data = getData()
    return data.packages.some(p => p.trackingNo === trackingNo)
  },

  deletePackage(trackingNo) {
    const data = getData()
    data.packages = data.packages.filter(p => p.trackingNo !== trackingNo)
    saveData(data)
  }
}

export const pickupRecordStorage = {
  addRecord(record) {
    const data = getData()
    data.pickupRecords.unshift({
      ...record,
      pickupTime: new Date().toLocaleString(),
      operator: '管理员'
    })
    saveData(data)
  },

  getAllRecords() {
    return getData().pickupRecords
  },

  getTodayRecords() {
    const today = new Date().toLocaleDateString()
    return getData().pickupRecords.filter(r => 
      new Date(r.pickupTime).toLocaleDateString() === today
    )
  }
}

export default {
  packageStorage,
  pickupRecordStorage
}
