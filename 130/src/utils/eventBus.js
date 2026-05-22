import Vue from 'vue'
export const EventBus = new Vue()

export const Events = {
  REPAIR_STATUS_UPDATED: 'repair-status-updated',
  REPAIR_CREATED: 'repair-created'
}
