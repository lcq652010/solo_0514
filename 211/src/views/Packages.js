window.Packages = {
  template: `
    <div class="packages-page">
      <h2 class="page-title">
        <i class="el-icon-gift"></i>
        摄影套餐
      </h2>
      
      <div class="filter-bar">
        <el-radio-group v-model="filterTag" @change="filterPackages">
          <el-radio-button label="全部">全部</el-radio-button>
          <el-radio-button label="热销">热销</el-radio-button>
          <el-radio-button label="情侣">情侣</el-radio-button>
          <el-radio-button label="婚纱">婚纱</el-radio-button>
          <el-radio-button label="儿童">儿童</el-radio-button>
          <el-radio-button label="商业">商业</el-radio-button>
        </el-radio-group>
      </div>

      <el-row :gutter="24">
        <el-col :xs="24" :sm="12" :md="8" v-for="pkg in filteredPackages" :key="pkg.id">
          <el-card class="package-card card-shadow" shadow="hover">
            <div class="card-image">
              <img :src="pkg.image" :alt="pkg.name" />
              <div class="discount-badge" v-if="pkg.originalPrice > pkg.price">
                {{ Math.round((1 - pkg.price / pkg.originalPrice) * 100) }}% OFF
              </div>
              <div class="tags">
                <el-tag
                  v-for="tag in pkg.tags"
                  :key="tag"
                  :class="{ 'tag-hot': tag === '热销' || tag === '婚纱' }"
                  size="mini">
                  {{ tag }}
                </el-tag>
              </div>
            </div>
            <div class="card-content">
              <h3 class="package-name">{{ pkg.name }}</h3>
              <p class="package-desc">{{ pkg.description }}</p>
              <div class="package-info">
                <span><i class="el-icon-time"></i> {{ pkg.duration }}</span>
                <span><i class="el-icon-picture"></i> {{ pkg.photos }}张</span>
                <span><i class="el-icon-magic-stick"></i> {{ pkg.retouched }}张精修</span>
              </div>
              <div class="scenes">
                <span class="scene-label">拍摄场景：</span>
                <span v-for="scene in pkg.scenes" :key="scene" class="scene-tag">{{ scene }}</span>
              </div>
              <div class="price-row">
                <div class="price">
                  <span class="symbol">¥</span>
                  <span class="amount">{{ pkg.price }}</span>
                  <span class="original" v-if="pkg.originalPrice > pkg.price">¥{{ pkg.originalPrice }}</span>
                </div>
                <el-button type="primary" size="small" @click="bookNow(pkg)">
                  立即预订
                </el-button>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-dialog
        :visible.sync="detailVisible"
        :title="selectedPackage ? selectedPackage.name : ''"
        width="600px">
        <div v-if="selectedPackage" class="package-detail">
          <img :src="selectedPackage.image" class="detail-image" />
          <div class="detail-info">
            <div class="detail-price">
              <span class="symbol">¥</span>
              <span class="amount">{{ selectedPackage.price }}</span>
              <span class="original" v-if="selectedPackage.originalPrice > selectedPackage.price">
                原价 ¥{{ selectedPackage.originalPrice }}
              </span>
            </div>
            <p class="detail-desc">{{ selectedPackage.description }}</p>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="拍摄时长">
                {{ selectedPackage.duration }}
              </el-descriptions-item>
              <el-descriptions-item label="拍摄张数">
                {{ selectedPackage.photos }}张
              </el-descriptions-item>
              <el-descriptions-item label="精修张数">
                {{ selectedPackage.retouched }}张
              </el-descriptions-item>
              <el-descriptions-item label="拍摄场景">
                {{ selectedPackage.scenes.join('、') }}
              </el-descriptions-item>
            </el-descriptions>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="detailVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmBooking">立即预订</el-button>
        </span>
      </el-dialog>
    </div>
  `,
  data() {
    return {
      filterTag: '全部',
      filteredPackages: [],
      detailVisible: false,
      selectedPackage: null
    };
  },
  computed: {
    packages() {
      return this.$store.state.packages;
    }
  },
  mounted() {
    this.filteredPackages = this.packages;
  },
  methods: {
    filterPackages() {
      if (this.filterTag === '全部') {
        this.filteredPackages = this.packages;
      } else {
        this.filteredPackages = this.packages.filter(p => 
          p.tags.some(t => t.includes(this.filterTag))
        );
      }
    },
    bookNow(pkg) {
      this.selectedPackage = pkg;
      this.detailVisible = true;
    },
    confirmBooking() {
      this.detailVisible = false;
      this.$router.push({
        path: '/booking',
        query: { packageId: this.selectedPackage.id }
      });
    }
  }
};
