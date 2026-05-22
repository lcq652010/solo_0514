import Vue from 'vue'
import { applicationList, interviewList, jobList } from '@/mock/data.js'

const state = Vue.observable({
  applications: [...applicationList],
  interviews: [...interviewList],
  jobs: jobList.filter(item => item.status === '招聘中')
})

export const store = {
  get applications() {
    return state.applications
  },
  get interviews() {
    return state.interviews
  },
  get jobs() {
    return state.jobs
  },
  
  addApplication(application) {
    state.applications.push(application)
  },
  
  updateApplicationStatus(id, status) {
    const index = state.applications.findIndex(item => item.id === id)
    if (index > -1) {
      state.applications[index].status = status
    }
  },
  
  updateApplicationByNamePhone(name, phone, status) {
    const index = state.applications.findIndex(item => item.name === name)
    if (index > -1) {
      state.applications[index].status = status
    }
  },
  
  addInterview(interview) {
    state.interviews.push(interview)
  },
  
  updateInterview(id, interview) {
    const index = state.interviews.findIndex(item => item.id === id)
    if (index > -1) {
      state.interviews.splice(index, 1, interview)
    }
  },
  
  updateInterviewResult(id, result) {
    const index = state.interviews.findIndex(item => item.id === id)
    if (index > -1) {
      state.interviews[index].result = result
      state.interviews[index].status = '已完成'
      
      const interview = state.interviews[index]
      if (result === '通过') {
        this.updateApplicationByNamePhone(interview.candidateName, '', '待录用')
      } else if (result === '不通过') {
        this.updateApplicationByNamePhone(interview.candidateName, '', '已拒绝')
      }
    }
  },
  
  deleteInterview(id) {
    const index = state.interviews.findIndex(item => item.id === id)
    if (index > -1) {
      state.interviews.splice(index, 1)
    }
  },
  
  getInterviewerBusyTimes(interviewer, excludeId = null) {
    return state.interviews.filter(item => {
      if (excludeId && item.id === excludeId) return false
      if (item.status === '已取消' || item.status === '已完成') return false
      return item.interviewer === interviewer
    }).map(item => item.time)
  }
}
