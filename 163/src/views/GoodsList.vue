<template>
  <div class="page-container">
    <h2 class="page-title">商品拼团列表</h2>
    
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索商品名称"
        style="width: 250px;"
        clearable
      ></el-input>
      <el-select v-model="categoryFilter" placeholder="商品分类" clearable>
        <el-option v-for="cat in categories" :key="cat" :label="cat" :value="cat"></el-option>
      </el-select>
      <el-select v-model="statusFilter" placeholder="拼团状态" clearable>
        <el-option label="已成团" value="success"></el-option>
        <el-option label="拼团中" value="going"></el-option>
        <el-option label="拼团失败" value="fail"></el-option>
      </el-select>
    </div>

    <div class="card-list">
      <div
        v-for="goods in filteredGoods"
        :key="goods.id"
        class="goods-card"
      >
        <img :src="goods.image" :alt="goods.name" class="goods-image">
        <div class="goods-info">
          <h3 class="goods-name">{{ goods.name }}</h3>
          <div class="goods-price">
            <span class="group-price">¥{{ goods.groupPrice }}</span>
            <span class="original-price">¥{{ goods.originalPrice }}</span>
          </div>
          <div class="group-info">
            <span class="group-count">已参团 {{ goods.currentCount }}/{{ goods.needCount }} 人</span>
            <span :class="['group-status', getGroupStatusClass(goods)]">
              {{ getGroupStatusText(goods) }}
            </span>
          </div>
          <p style="font-size: 12px; color: #666; margin-bottom: 8px;">
            <el-tag :type="goods.stock > 0 ? 'success' : 'danger'" size="mini">
              库存：{{ goods.stock }} 件
            </el-tag>
            <el-tag size="mini" type="info" style="margin-left: 5px;">
              限购：{{ goods.limitBuy }} 件
            </el-tag>
            <el-tag size="mini" type="warning" style="margin-left: 5px;">
              {{ goods.category }}
            </el-tag>
          </p>
          <p style="font-size: 12px; color: #666; margin-bottom: 10px;">
            团长：{{ goods.leader }} | {{ goods.address }}
          </p>
          <el-button
            type="primary"
            size="small"
            class="btn-block"
            :disabled="goods.status !== 'going' || goods.stock <= 0"
            @click="goToOrder(goods)"
          >
            {{ goods.stock <= 0 ? '库存不足' : (goods.currentCount >= goods.needCount ? '已成团' : '立即参团') }}
          </el-button>
        </div>
      </div>
    </div>

    <el-empty v-if="filteredGoods.length === 0" description="暂无商品数据"></el-empty>
  </div>
</template>

<script>
import { goodsList, categories } from '../data/mock.js'

export default {
  name: 'GoodsList',
  data() {
    return {
      goodsList: goodsList,
      categories: categories,
      searchKeyword: '',
      categoryFilter: '',
      statusFilter: ''
    }
  },
  computed: {
    filteredGoods() {
      return this.goodsList.filter(item => {
        const matchKeyword = !this.searchKeyword || item.name.includes(this.searchKeyword)
        const matchCategory = !this.categoryFilter || this.categoryFilter === '全部' || item.category === this.categoryFilter
        const matchStatus = !this.statusFilter || item.status === this.statusFilter
        return matchKeyword && matchCategory && matchStatus
      })
    }
  },
  methods: {
    getStatusText(status) {
      const map = {
        going: '进行中',
        success: '拼团成功',
        fail: '拼团失败'
      }
      return map[status]
    },
    getGroupStatusText(goods) {
      if (goods.status === 'fail') {
        return '拼团失败'
      }
      if (goods.status === 'success' || goods.currentCount >= goods.needCount) {
        return '已成团'
      }
      return '待成团'
    },
    getGroupStatusClass(goods) {
      if (goods.status === 'success' || goods.currentCount >= goods.needCount) {
        return 'status-success'
      }
      if (goods.status === 'fail') {
        return 'status-fail'
      }
      return 'status-going'
    },
    goToOrder(goods) {
      this.$router.push({
        path: '/order',
        query: { goodsId: goods.id }
      })
    }
  }
}
</script>