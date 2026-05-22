<template>
  <div class="process-steps-wrapper">
    <el-steps :active="currentProcess" finish-status="success" class="process-steps">
      <el-step
        v-for="(process, index) in processes"
        :key="process.id"
        :title="process.name"
        :icon="process.icon"
      >
        <template slot="description">
          <span v-if="processTimes && processTimes[index]" class="process-time">
            {{ formatTime(processTimes[index]) }}
          </span>
          <span v-else class="process-pending">未完成</span>
        </template>
      </el-step>
    </el-steps>
  </div>
</template>

<script>
export default {
  name: 'ProcessSteps',
  props: {
    currentProcess: {
      type: Number,
      required: true
    },
    processTimes: {
      type: Array,
      default: () => []
    }
  },
  computed: {
    processes() {
      return this.$store.state.processes
    }
  },
  methods: {
    formatTime(timeStr) {
      if (!timeStr) return ''
      const date = new Date(timeStr)
      return `${date.getMonth() + 1}/${date.getDate()} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
    }
  }
}
</script>

<style lang="scss" scoped>
.process-steps-wrapper {
  padding: 16px 0;

  .process-steps {
    ::v-deep .el-step__icon {
      font-size: 18px;
    }

    ::v-deep .el-step__title {
      font-size: 14px;
      font-weight: 500;
    }

    ::v-deep .el-step__description {
      font-size: 12px;
    }
  }

  .process-time {
    color: #228B22;
    font-size: 12px;
  }

  .process-pending {
    color: #999;
    font-size: 12px;
  }
}
</style>
