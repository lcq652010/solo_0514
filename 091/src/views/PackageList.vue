<template>
  <div class="package-list">
    <el-card class="search-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="套餐名称">
          <el-input v-model="searchForm.name" placeholder="请输入套餐名称"></el-input>
        </el-form-item>
        <el-form-item label="套餐类型">
          <el-select v-model="searchForm.type" placeholder="请选择套餐类型">
            <el-option label="全部" value=""></el-option>
            <el-option label="入职体检" value="entry"></el-option>
            <el-option label="常规体检" value="regular"></el-option>
            <el-option label="高端体检" value="premium"></el-option>
            <el-option label="妇科体检" value="gynecology"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-row :gutter="20" class="package-row">
      <el-col :span="8" v-for="item in packageList" :key="item.id">
        <el-card class="package-card" shadow="hover">
          <div class="package-header">
            <img :src="item.image" :alt="item.name" class="package-image" />
            <el-tag :type="getTagType(item.type)" size="small" class="package-tag">
              {{ getTypeName(item.type) }}
            </el-tag>
          </div>
          <div class="package-content">
            <h3 class="package-name">{{ item.name }}</h3>
            <p class="package-desc">{{ item.description }}</p>
            <div class="package-items">
              <span v-for="(check, idx) in item.checkItems.slice(0, 4)" :key="idx" class="check-item">
                {{ check }}
              </span>
              <span v-if="item.checkItems.length > 4" class="check-item more">
                +{{ item.checkItems.length - 4 }}项
              </span>
            </div>
          </div>
          <div class="package-footer">
            <div class="price-info">
              <span class="original-price">¥{{ item.originalPrice }}</span>
              <span class="current-price">¥{{ item.currentPrice }}</span>
            </div>
            <el-button type="primary" size="small" @click="handleAppointment(item)">
              立即预约
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-pagination
      class="pagination"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="pagination.page"
      :page-sizes="[6, 12, 24]"
      :page-size="pagination.size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="pagination.total"
    ></el-pagination>
  </div>
</template>

<script>
export default {
  name: 'PackageList',
  data() {
    return {
      searchForm: {
        name: '',
        type: ''
      },
      pagination: {
        page: 1,
        size: 6,
        total: 12
      },
      packageList: []
    }
  },
  created() {
    this.loadPackageList()
  },
  methods: {
    loadPackageList() {
      const mockData = [
        {
          id: 1,
          name: '入职基础体检套餐',
          type: 'entry',
          description: '适用于新员工入职体检，包含基础检查项目',
          originalPrice: 299,
          currentPrice: 199,
          image: 'https://via.placeholder.com/280x160/409EFF/ffffff?text=入职体检',
          checkItems: ['一般检查', '血常规', '尿常规', '肝功能', '胸部X光', '心电图']
        },
        {
          id: 2,
          name: '青年常规体检套餐',
          type: 'regular',
          description: '适合18-35岁青年人群的常规健康检查',
          originalPrice: 599,
          currentPrice: 399,
          image: 'https://via.placeholder.com/280x160/67C23A/ffffff?text=常规体检',
          checkItems: ['一般检查', '血常规', '尿常规', '肝功能', '肾功能', '血脂', '血糖', '腹部B超']
        },
        {
          id: 3,
          name: '精英尊享体检套餐',
          type: 'premium',
          description: '高端全面体检，包含肿瘤标志物、甲状腺等深度检查',
          originalPrice: 1999,
          currentPrice: 1599,
          image: 'https://via.placeholder.com/280x160/E6A23C/ffffff?text=高端体检',
          checkItems: ['一般检查', '血常规', '尿常规', '肝功能', '肾功能', '血脂', '血糖', '肿瘤标志物', '甲状腺功能', '胸部CT']
        },
        {
          id: 4,
          name: '女性专属体检套餐',
          type: 'gynecology',
          description: '针对女性健康的专项检查，包含妇科、乳腺等检查',
          originalPrice: 899,
          currentPrice: 699,
          image: 'https://via.placeholder.com/280x160/F56C6C/ffffff?text=妇科体检',
          checkItems: ['一般检查', '血常规', '尿常规', '妇科检查', '白带常规', 'TCT', '乳腺B超', '子宫附件B超']
        },
        {
          id: 5,
          name: '中年全面体检套餐',
          type: 'regular',
          description: '适合35-55岁中年人群，关注心脑血管健康',
          originalPrice: 1299,
          currentPrice: 999,
          image: 'https://via.placeholder.com/280x160/909399/ffffff?text=中年体检',
          checkItems: ['一般检查', '血常规', '尿常规', '肝功能', '肾功能', '血脂', '血糖', '心电图', '心脏彩超', '颈动脉彩超']
        },
        {
          id: 6,
          name: '老年关爱体检套餐',
          type: 'premium',
          description: '专为55岁以上老年人设计，全面评估健康状况',
          originalPrice: 1699,
          currentPrice: 1299,
          image: 'https://via.placeholder.com/280x160/9B59B6/ffffff?text=老年体检',
          checkItems: ['一般检查', '血常规', '尿常规', '肝功能', '肾功能', '血脂', '血糖', '骨密度', '头颅CT', '肿瘤标志物']
        }
      ]
      
      let filtered = mockData
      
      if (this.searchForm.name) {
        filtered = filtered.filter(item => 
          item.name.includes(this.searchForm.name)
        )
      }
      
      if (this.searchForm.type) {
        filtered = filtered.filter(item => 
          item.type === this.searchForm.type
        )
      }
      
      this.pagination.total = filtered.length
      
      const start = (this.pagination.page - 1) * this.pagination.size
      const end = start + this.pagination.size
      this.packageList = filtered.slice(start, end)
    },
    handleSearch() {
      this.pagination.page = 1
      this.loadPackageList()
    },
    handleReset() {
      this.searchForm = {
        name: '',
        type: ''
      }
      this.pagination.page = 1
      this.loadPackageList()
    },
    handleSizeChange(val) {
      this.pagination.size = val
      this.loadPackageList()
    },
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadPackageList()
    },
    handleAppointment(item) {
      this.$router.push({
        path: '/appointment',
        query: { packageId: item.id, packageName: item.name }
      })
    },
    getTagType(type) {
      const map = {
        entry: '',
        regular: 'success',
        premium: 'warning',
        gynecology: 'danger'
      }
      return map[type] || ''
    },
    getTypeName(type) {
      const map = {
        entry: '入职体检',
        regular: '常规体检',
        premium: '高端体检',
        gynecology: '妇科体检'
      }
      return map[type] || type
    }
  }
}
</script>

<style scoped>
.package-list {
  padding: 0;
}

.search-card {
  margin-bottom: 20px;
}

.package-row {
  margin-bottom: 20px;
}

.package-card {
  margin-bottom: 20px;
  height: 100%;
}

.package-header {
  position: relative;
  margin: -20px -20px 15px -20px;
}

.package-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: 4px 4px 0 0;
}

.package-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.package-content {
  flex: 1;
}

.package-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.package-desc {
  font-size: 14px;
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
}

.package-items {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.check-item {
  padding: 4px 10px;
  background-color: #f5f7fa;
  border-radius: 12px;
  font-size: 12px;
  color: #606266;
}

.check-item.more {
  color: #409EFF;
  background-color: #ecf5ff;
}

.package-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.price-info {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.original-price {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
}

.current-price {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.pagination {
  text-align: right;
  padding: 20px 0;
}
</style>
