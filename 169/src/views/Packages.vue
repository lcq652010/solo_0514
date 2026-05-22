<template>
  <div class="page-container">
    <div class="page-title">保养套餐列表</div>
    
    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索套餐名称"
        style="width: 300px; margin-right: 10px"
        clearable
      >
        <i slot="prefix" class="el-input__icon el-icon-search"></i>
      </el-input>
      <el-select v-model="selectedType" placeholder="套餐类型" style="width: 150px; margin-right: 10px" clearable>
        <el-option label="全部类型" value=""></el-option>
        <el-option label="基础保养" value="基础保养"></el-option>
        <el-option label="深度保养" value="深度保养"></el-option>
        <el-option label="豪华保养" value="豪华保养"></el-option>
      </el-select>
      <el-button type="primary" @click="handleSearch">搜索</el-button>
    </div>

    <div class="card-grid">
      <el-card
        v-for="pkg in packageList"
        :key="pkg.id"
        shadow="hover"
        class="package-card"
      >
        <div slot="header" class="card-header">
          <span class="package-name">{{ pkg.name }}</span>
          <el-tag :type="getTagType(pkg.type)">{{ pkg.type }}</el-tag>
        </div>
        
        <div class="package-content">
          <p class="package-desc">{{ pkg.description }}</p>
          <div class="package-items">
            <div v-for="(item, index) in pkg.items" :key="index" class="package-item">
              <i class="el-icon-check" style="color: #67c23a"></i>
              <span>{{ item }}</span>
            </div>
          </div>
          <div class="package-footer">
            <div class="price-section">
              <span class="original-price" v-if="pkg.originalPrice">¥{{ pkg.originalPrice }}</span>
              <span class="current-price">¥{{ pkg.price }}</span>
            </div>
            <div class="duration">
              <i class="el-icon-time"></i>
              <span>{{ pkg.duration }}</span>
            </div>
          </div>
        </div>
        
        <div class="card-actions">
          <el-button size="small" type="primary" @click="handleAppoint(pkg)">立即预约</el-button>
          <el-button size="small" @click="handleDetail(pkg)">查看详情</el-button>
        </div>
      </el-card>
    </div>

    <div class="pagination-container">
      <el-pagination
        :current-page="currentPage"
        :page-sizes="[6, 12, 24]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Packages',
  data() {
    return {
      searchKeyword: '',
      selectedType: '',
      currentPage: 1,
      pageSize: 6,
      total: 0,
      packageList: []
    }
  },
  created() {
    this.loadPackageList()
  },
  methods: {
    getTagType(type) {
      const typeMap = {
        '基础保养': 'success',
        '深度保养': 'warning',
        '豪华保养': 'danger'
      }
      return typeMap[type] || 'info'
    },
    loadPackageList() {
      const mockData = [
        {
          id: 1,
          name: '基础保养套餐',
          type: '基础保养',
          description: '适合日常行驶的基础保养服务，保障车辆正常运行。',
          price: 299,
          originalPrice: 399,
          duration: '约1.5小时',
          items: ['更换机油', '更换机油滤芯', '全车安全检查', '轮胎气压调整']
        },
        {
          id: 2,
          name: '常规保养套餐',
          type: '基础保养',
          description: '标准保养服务，包含空气滤芯和空调滤芯更换。',
          price: 499,
          originalPrice: 599,
          duration: '约2小时',
          items: ['更换机油', '更换机油滤芯', '更换空气滤芯', '更换空调滤芯', '全车安全检查']
        },
        {
          id: 3,
          name: '深度保养套餐A',
          type: '深度保养',
          description: '深度养护服务，包含燃油系统清洗和节气门清洗。',
          price: 899,
          originalPrice: 1199,
          duration: '约3小时',
          items: ['更换机油', '更换三滤', '燃油系统清洗', '节气门清洗', '全车安全检查']
        },
        {
          id: 4,
          name: '深度保养套餐B',
          type: '深度保养',
          description: '全面深度养护，包含变速箱油更换和刹车系统保养。',
          price: 1299,
          originalPrice: 1699,
          duration: '约4小时',
          items: ['更换机油', '更换三滤', '更换变速箱油', '刹车系统保养', '全车安全检查']
        },
        {
          id: 5,
          name: '豪华保养套餐',
          type: '豪华保养',
          description: '尊享级保养服务，包含全车检测和深度清洁。',
          price: 1999,
          originalPrice: 2599,
          duration: '约5小时',
          items: ['全合成机油更换', '全车滤芯更换', '刹车系统深度保养', '发动机舱清洁', '内饰深度清洁', '全车检测']
        },
        {
          id: 6,
          name: 'VIP尊享套餐',
          type: '豪华保养',
          description: 'VIP专属服务，一对一专属技师服务，包含全车深度养护。',
          price: 2999,
          originalPrice: 3999,
          duration: '约6小时',
          items: ['进口全合成机油', '全车滤芯更换', '变速箱油更换', '刹车油更换', '防冻液更换', '全车深度检测', 'VIP专属休息区']
        }
      ]
      
      let filteredData = mockData
      
      if (this.searchKeyword) {
        filteredData = filteredData.filter(item => 
          item.name.includes(this.searchKeyword)
        )
      }
      
      if (this.selectedType) {
        filteredData = filteredData.filter(item => 
          item.type === this.selectedType
        )
      }
      
      this.total = filteredData.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.packageList = filteredData.slice(start, end)
    },
    handleSearch() {
      this.currentPage = 1
      this.loadPackageList()
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadPackageList()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadPackageList()
    },
    handleAppoint(pkg) {
      this.$router.push({
        path: '/appointment',
        query: { packageId: pkg.id, packageName: pkg.name }
      })
    },
    handleDetail(pkg) {
      this.$alert(pkg.description, `套餐详情 - ${pkg.name}`, {
        confirmButtonText: '确定'
      })
    }
  }
}
</script>

<style scoped>
.package-card {
  transition: transform 0.3s;
}

.package-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.package-name {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.package-desc {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.6;
}

.package-items {
  margin-bottom: 15px;
}

.package-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.package-item i {
  margin-right: 8px;
}

.package-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.price-section {
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

.duration {
  display: flex;
  align-items: center;
  color: #909399;
  font-size: 14px;
}

.duration i {
  margin-right: 5px;
}

.card-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px dashed #ebeef5;
}
</style>
