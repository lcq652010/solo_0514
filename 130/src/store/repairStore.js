import Vue from 'vue'
import { repairList as initialRepairList, statusOptions } from '../mock/data'
import { EventBus, Events } from '../utils/eventBus'

const state = Vue.observable({
  repairList: [...initialRepairList]
})

export const RepairStore = {
  getRepairList() {
    return state.repairList
  },

  getRepairById(id) {
    return state.repairList.find(item => item.id === id)
  },

  addRepair(repairData) {
    const newRepair = {
      id: String(Date.now()),
      ...repairData,
      status: '0',
      createTime: this.getCurrentTime()
    }
    state.repairList.unshift(newRepair)
    EventBus.$emit(Events.REPAIR_CREATED, newRepair)
    return newRepair
  },

  updateRepairStatus(id, status, extraData = {}) {
    const index = state.repairList.findIndex(item => item.id === id)
    if (index > -1) {
      state.repairList[index] = {
        ...state.repairList[index],
        status,
        ...extraData
      }
      EventBus.$emit(Events.REPAIR_STATUS_UPDATED, {
        id,
        status,
        repair: state.repairList[index]
      })
      return state.repairList[index]
    }
    return null
  },

  dispatchRepair(id, worker, workerPhone) {
    const result = this.updateRepairStatus(id, '1', {
      worker,
      workerPhone,
      dispatchTime: this.getCurrentTime()
    })
    return result
  },

  startRepair(id) {
    return this.updateRepairStatus(id, '2', {
      startTime: this.getCurrentTime()
    })
  },

  completeRepair(id) {
    return this.updateRepairStatus(id, '3', {
      completeTime: this.getCurrentTime()
    })
  },

  evaluateRepair(id, evaluationData) {
    return this.updateRepairStatus(id, '4', {
      evaluation: evaluationData,
      evaluateTime: this.getCurrentTime()
    })
  },

  getCurrentTime() {
    const now = new Date()
    return now.getFullYear() + '-' + 
           String(now.getMonth() + 1).padStart(2, '0') + '-' + 
           String(now.getDate()).padStart(2, '0') + ' ' + 
           String(now.getHours()).padStart(2, '0') + ':' + 
           String(now.getMinutes()).padStart(2, '0') + ':' + 
           String(now.getSeconds()).padStart(2, '0')
  },

  getStatusLabel(status) {
    const item = statusOptions.find(opt => opt.value === status)
    return item ? item.label : '未知'
  },

  getStatusColor(status) {
    const item = statusOptions.find(opt => opt.value === status)
    return item ? item.color : '#909399'
  }
}
