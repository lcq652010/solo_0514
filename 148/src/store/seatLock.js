class SeatLockManager {
  constructor() {
    this.lockedSeats = new Map()
    this.soldSeats = new Map()
  }

  getKey(scheduleId, row, col) {
    return `${scheduleId}-${row}-${col}`
  }

  lockSeat(scheduleId, row, col, orderId) {
    const key = this.getKey(scheduleId, row, col)
    this.lockedSeats.set(key, {
      orderId,
      lockedAt: Date.now(),
      status: 'locked'
    })
  }

  unlockSeat(scheduleId, row, col) {
    const key = this.getKey(scheduleId, row, col)
    this.lockedSeats.delete(key)
  }

  markAsSold(scheduleId, row, col, orderId) {
    const key = this.getKey(scheduleId, row, col)
    this.soldSeats.set(key, {
      orderId,
      soldAt: Date.now()
    })
    this.lockedSeats.delete(key)
  }

  isSeatLocked(scheduleId, row, col) {
    const key = this.getKey(scheduleId, row, col)
    const lockInfo = this.lockedSeats.get(key)
    if (!lockInfo) return false
    const lockDuration = 15 * 60 * 1000
    if (Date.now() - lockInfo.lockedAt > lockDuration) {
      this.lockedSeats.delete(key)
      return false
    }
    return true
  }

  isSeatSold(scheduleId, row, col) {
    const key = this.getKey(scheduleId, row, col)
    return this.soldSeats.has(key)
  }

  getLockedSeats(scheduleId) {
    const locked = []
    this.lockedSeats.forEach((value, key) => {
      if (key.startsWith(`${scheduleId}-`)) {
        const [, row, col] = key.split('-')
        locked.push({ row: parseInt(row), col: parseInt(col), ...value })
      }
    })
    return locked
  }

  getSoldSeats(scheduleId) {
    const sold = []
    this.soldSeats.forEach((value, key) => {
      if (key.startsWith(`${scheduleId}-`)) {
        const [, row, col] = key.split('-')
        sold.push({ row: parseInt(row), col: parseInt(col), ...value })
      }
    })
    return sold
  }

  getLockInfo(scheduleId, row, col) {
    const key = this.getKey(scheduleId, row, col)
    return this.lockedSeats.get(key) || null
  }

  lockSeatsByOrder(scheduleId, seats, orderId) {
    seats.forEach(seat => {
      this.markAsSold(scheduleId, seat.row, seat.col, orderId)
    })
  }
}

export default new SeatLockManager()
