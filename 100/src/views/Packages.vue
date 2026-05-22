<template>
  <div class="page-container">
    <h1 class="page-title">保养套餐</h1>
    
    <el-row :gutter="20">
      <el-col :span="8" v-for="pkg in packages" :key="pkg.id">
        <el-card class="package-card" shadow="hover">
          <div slot="header" class="card-header">
            <span :class="['package-tag', pkg.tagClass]">{{ pkg.tag }}</span>
            <span class="package-name">{{ pkg.name }}</span>
          </div>
          
          <div class="package-price">
            <span class="currency">¥</span>
            <span class="price">{{ pkg.price }}</span>
            <span class="original-price" v-if="pkg.originalPrice">¥{{ pkg.originalPrice }}</span>
          </div>
          
          <div class="package-items">
            <div v-for="(item, index) in pkg.items" :key="index" class="package-item">
              <i class="el-icon-check"></i> {{ item }}
            </div>
          </div>
          
          <div class="package-desc">{{ pkg.description }}</div>
          
          <el-button 
            type="primary" 
            class="reserve-btn"
            @click="goToReserve(pkg)"
          >
            立即预约
          </el-button>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: 'Packages',
  data() {
    return {
      packages: [
        {
          id: 1,
          name: '基础保养套餐',
          tag: '热销',
          tagClass: 'tag-hot',
          price: 299,
          originalPrice: 399,
          items: [
            '更换机油（4L）',
            '机油滤清器更换',
            '全车安全检测',
            '车内消毒服务'
          ],
          description: '适合日常家用车辆，5000公里或6个月保养周期'
        },
        {
          id: 2,
          name: '标准保养套餐',
          tag: '推荐',
          tagClass: 'tag-recommend',
          price: 599,
          originalPrice: 799,
          items: [
            '更换全合成机油（4L）',
            '机油滤清器更换',
            '空气滤清器更换',
            '空调滤清器更换',
            '全车安全检测',
            '发动机舱清洁'
          ],
          description: '全方位保养，10000公里或12个月保养周期'
        },
        {
          id: 3,
          name: '尊享保养套餐',
          tag: '尊享',
          tagClass: 'tag-premium',
          price: 1299,
          originalPrice: 1699,
          items: [
            '更换高端全合成机油（6L）',
            '机油滤清器更换',
            '空气滤清器更换',
            '空调滤清器更换',
            '燃油滤清器更换',
            '变速箱油更换',
            '全车深度检测',
            '发动机积碳清洗',
            '全车内饰清洁'
          ],
          description: '豪华级保养，适合高端车型，15000公里保养周期'
        },
        {
          id: 4,
          name: '刹车系统养护',
          tag: '安全',
          tagClass: 'tag-safe',
          price: 399,
          originalPrice: 499,
          items: [
            '刹车片检查更换',
            '刹车油更换',
            '刹车盘光面处理',
            '刹车系统深度检测'
          ],
          description: '确保行车安全，建议每2万公里或2年进行一次'
        },
        {
          id: 5,
          name: '空调系统养护',
          tag: '清凉',
          tagClass: 'tag-cool',
          price: 299,
          originalPrice: 399,
          items: [
            '空调滤芯更换',
            '空调管路清洗',
            '蒸发器清洁消毒',
            '冷媒压力检测补充'
          ],
          description: '夏季必备，让车内空气清新凉爽'
        },
        {
          id: 6,
          name: '漆面养护套餐',
          tag: '美容',
          tagClass: 'tag-beauty',
          price: 699,
          originalPrice: 999,
          items: [
            '全车精细洗车',
            '漆面抛光处理',
            '纳米镀膜保护',
            '轮毂清洁上光'
          ],
          description: '让爱车焕然一新，持久光亮如新'
        }
      ]
    }
  },
  methods: {
    goToReserve(pkg) {
      this.$router.push({
        path: '/reserve',
        query: { packageId: pkg.id, packageName: pkg.name }
      })
    }
  }
}
</script>

<style scoped>
.package-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.package-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.package-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  color: #fff;
  width: fit-content;
}

.tag-hot {
  background: #f56c6c;
}

.tag-recommend {
  background: #409eff;
}

.tag-premium {
  background: #e6a23c;
}

.tag-safe {
  background: #67c23a;
}

.tag-cool {
  background: #909399;
}

.tag-beauty {
  background: #f08d49;
}

.package-name {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.package-price {
  margin: 20px 0;
}

.currency {
  font-size: 16px;
  color: #f56c6c;
  vertical-align: top;
}

.price {
  font-size: 36px;
  font-weight: 600;
  color: #f56c6c;
}

.original-price {
  font-size: 14px;
  color: #909399;
  text-decoration: line-through;
  margin-left: 10px;
}

.package-items {
  margin: 20px 0;
}

.package-item {
  padding: 8px 0;
  color: #606266;
  font-size: 14px;
}

.package-item i {
  color: #67c23a;
  margin-right: 8px;
}

.package-desc {
  color: #909399;
  font-size: 13px;
  margin: 20px 0;
  padding-top: 15px;
  border-top: 1px solid #ebeef5;
}

.reserve-btn {
  width: 100%;
  height: 44px;
  font-size: 16px;
}
</style>
