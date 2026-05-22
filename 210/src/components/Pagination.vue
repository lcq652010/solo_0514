<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'Pagination',
  props: {
    current: {
      type: Number,
      default: 1,
    },
    total: {
      type: Number,
      default: 0,
    },
    pageSize: {
      type: Number,
      default: 10,
    },
  },
  computed: {
    totalPages(): number {
      return Math.ceil(this.total / this.pageSize)
    },
    startIndex(): number {
      if (this.total === 0) return 0
      return (this.current - 1) * this.pageSize + 1
    },
    endIndex(): number {
      const end = this.current * this.pageSize
      return Math.min(end, this.total)
    },
    pageNumbers(): (number | string)[] {
      const pages: (number | string)[] = []
      const total = this.totalPages
      const current = this.current

      if (total <= 7) {
        for (let i = 1; i <= total; i++) {
          pages.push(i)
        }
      } else {
        if (current <= 4) {
          for (let i = 1; i <= 5; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        } else if (current >= total - 3) {
          pages.push(1)
          pages.push('...')
          for (let i = total - 4; i <= total; i++) {
            pages.push(i)
          }
        } else {
          pages.push(1)
          pages.push('...')
          for (let i = current - 1; i <= current + 1; i++) {
            pages.push(i)
          }
          pages.push('...')
          pages.push(total)
        }
      }
      return pages
    },
  },
  methods: {
    changePage(page: number | string) {
      if (typeof page === 'number' && page !== this.current && page >= 1 && page <= this.totalPages) {
        this.$emit('change', page)
      }
    },
    onPrev() {
      if (this.current > 1) {
        this.$emit('change', this.current - 1)
      }
    },
    onNext() {
      if (this.current < this.totalPages) {
        this.$emit('change', this.current + 1)
      }
    },
    onPageSizeChange(e: Event) {
      const target = e.target as HTMLSelectElement
      this.$emit('update:pageSize', Number(target.value))
      this.$emit('change', 1)
    },
  },
})
</script>

<template>
  <div class="flex items-center justify-between mt-5 px-1">
    <div class="text-sm text-gray-600">
      共 <span class="font-medium text-gray-900">{{ total }}</span> 条，
      显示 <span class="font-medium text-gray-900">{{ startIndex }}</span> -
      <span class="font-medium text-gray-900">{{ endIndex }}</span> 条
    </div>
    <div class="flex items-center gap-3">
      <div class="flex items-center gap-1 text-sm text-gray-600">
        <span>每页</span>
        <select
          :value="pageSize"
          @change="onPageSizeChange"
          class="px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option :value="5">5</option>
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
        </select>
        <span>条</span>
      </div>
      <div class="flex items-center gap-1">
        <button
          type="button"
          @click="onPrev"
          :disabled="current === 1"
          :class="[
            'w-8 h-8 flex items-center justify-center rounded text-sm border transition-colors',
            current === 1
              ? 'bg-gray-50 text-gray-300 border-gray-200 cursor-not-allowed'
              : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50 hover:text-blue-600',
          ]"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <template v-for="(page, idx) in pageNumbers">
          <button
            v-if="typeof page === 'number'"
            :key="idx"
            type="button"
            @click="changePage(page)"
            :class="[
              'w-8 h-8 flex items-center justify-center rounded text-sm font-medium transition-colors',
              page === current
                ? 'bg-blue-600 text-white border border-blue-600'
                : 'bg-white text-gray-600 border border-gray-300 hover:bg-gray-50 hover:text-blue-600',
            ]"
          >
            {{ page }}
          </button>
          <span v-else :key="idx" class="px-2 text-gray-400 text-sm">
            {{ page }}
          </span>
        </template>
        <button
          type="button"
          @click="onNext"
          :disabled="current === totalPages || totalPages === 0"
          :class="[
            'w-8 h-8 flex items-center justify-center rounded text-sm border transition-colors',
            (current === totalPages || totalPages === 0)
              ? 'bg-gray-50 text-gray-300 border-gray-200 cursor-not-allowed'
              : 'bg-white text-gray-600 border-gray-300 hover:bg-gray-50 hover:text-blue-600',
          ]"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
