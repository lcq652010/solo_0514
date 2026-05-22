import axios from 'axios';

const request = axios.create({
  baseURL: '/api',
  timeout: 10000
});

export function applyOvertime(data) {
  return request({
    url: '/overtime/apply',
    method: 'post',
    data
  });
}

export function getMyOvertimeRecords(params) {
  return request({
    url: '/overtime/my-records',
    method: 'get',
    params
  });
}

export function getApprovalList(params) {
  return request({
    url: '/overtime/approval-list',
    method: 'get',
    params
  });
}

export function approveOvertime(data) {
  return request({
    url: '/overtime/approve',
    method: 'post',
    data
  });
}

export function getStatistics(params) {
  return request({
    url: '/overtime/statistics',
    method: 'get',
    params
  });
}

export function getLedger(params) {
  return request({
    url: '/overtime/ledger',
    method: 'get',
    params
  });
}

export default request;
