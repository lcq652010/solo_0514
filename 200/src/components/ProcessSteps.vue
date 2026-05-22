<template>
  <div class="process-steps">
    <div class="steps-container">
      <div 
        v-for="(step, index) in processSteps" 
        :key="step.key"
        :class="['step-item', getStepClass(step.key)]"
      >
        <div class="step-circle">
          <i v-if="isCompleted(step.key)" class="el-icon-check"></i>
          <span v-else>{{ index + 1 }}</span>
        </div>
        <div class="step-line" v-if="index < processSteps.length - 1"></div>
        <div class="step-label">{{ step.label }}</div>
        <div v-if="isCurrent(step.key)" class="current-badge">当前</div>
      </div>
    </div>
  </div>
</template>

<script>
import { processSteps } from '../data/mockData'

export default {
  name: 'ProcessSteps',
  props: {
    currentStatus: {
      type: String,
      default: 'pending'
    }
  },
  data() {
    return {
      processSteps
    }
  },
  methods: {
    getStepClass(stepKey) {
      const statusOrder = ['pending', 'quarrying', 'cutting', 'shaping', 'carving', 'polishing', 'waxing', 'inspecting', 'completed']
      const currentIndex = statusOrder.indexOf(this.currentStatus)
      const stepIndex = statusOrder.indexOf(stepKey)
      
      if (stepIndex < currentIndex || (stepIndex === currentIndex && stepKey === 'completed')) {
        return 'completed'
      } else if (stepIndex === currentIndex) {
        return 'current'
      }
      return ''
    },
    isCompleted(stepKey) {
      const statusOrder = ['pending', 'quarrying', 'cutting', 'shaping', 'carving', 'polishing', 'waxing', 'inspecting', 'completed']
      const currentIndex = statusOrder.indexOf(this.currentStatus)
      const stepIndex = statusOrder.indexOf(stepKey)
      return stepIndex < currentIndex || (stepIndex === currentIndex && stepKey === 'completed')
    },
    isCurrent(stepKey) {
      return this.currentStatus === stepKey && stepKey !== 'completed'
    }
  }
}
</script>

<style scoped>
.process-steps {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.steps-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  flex: 1;
}

.step-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #E8E8E8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  color: #999;
  transition: all 0.3s ease;
  z-index: 2;
}

.step-item.completed .step-circle {
  background: #67C23A;
  color: #fff;
}

.step-item.current .step-circle {
  background: #409EFF;
  color: #fff;
  box-shadow: 0 0 10px rgba(64, 158, 255, 0.5);
}

.step-line {
  position: absolute;
  top: 20px;
  left: 50%;
  width: 50%;
  height: 3px;
  background: #E8E8E8;
  z-index: 1;
}

.step-item.completed + .step-item .step-line {
  background: #67C23A;
}

.step-item.current + .step-item .step-line {
  background: linear-gradient(90deg, #409EFF 0%, #E8E8E8 100%);
}

.step-label {
  margin-top: 10px;
  font-size: 12px;
  color: #666;
  text-align: center;
}

.step-item.completed .step-label {
  color: #67C23A;
}

.step-item.current .step-label {
  color: #409EFF;
  font-weight: bold;
}

.current-badge {
  margin-top: 5px;
  font-size: 10px;
  color: #409EFF;
  background: rgba(64, 158, 255, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
}
</style>
