<template>
  <div class="class-type">
    <div class="page-title">班型选择</div>
    <div class="card-wrapper">
      <el-row :gutter="20">
        <el-col :span="8" v-for="item in classList" :key="item.id">
          <el-card class="class-card" shadow="hover">
            <div slot="header" class="card-header">
              <span>{{ item.name }}</span>
              <el-tag type="success" size="small">{{ item.tag }}</el-tag>
            </div>
            <div class="class-content">
              <p class="price">
                <span class="price-label">价格：</span>
                <span class="price-value">¥{{ item.price }}</span>
              </p>
              <p class="desc">{{ item.description }}</p>
              <div class="features">
                <el-tag v-for="(feat, idx) in item.features" :key="idx" size="mini" style="margin-right: 5px; margin-bottom: 5px">
                  {{ feat }}
                </el-tag>
              </div>
            </div>
            <div class="card-footer">
              <el-button type="primary" @click="selectClass(item)" style="width: 100%">
                立即报名
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-dialog title="确认选择" :visible.sync="dialogVisible" width="400px">
      <div>
        <p>您已选择：<strong>{{ selectedClass?.name }}</strong></p>
        <p>价格：<strong>¥{{ selectedClass?.price }}</strong></p>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="goToReg">去报名</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'ClassType',
  data() {
    return {
      classList: [
        {
          id: 1,
          name: 'C1 普通班',
          tag: '热门',
          price: 3800,
          description: '手动挡标准课程，包含科目一至科目四全部培训',
          features: ['4人一车', '工作日练车', '基础学时足够', '免费补考1次']
        },
        {
          id: 2,
          name: 'C1 VIP班',
          tag: '推荐',
          price: 5800,
          description: '手动挡VIP课程，一对一教学，灵活安排时间',
          features: ['1人一车', '任意时间练车', '免费接送', '补考全包']
        },
        {
          id: 3,
          name: 'C2 自动档班',
          tag: '省心',
          price: 4200,
          description: '自动挡课程，操作简单，适合新手',
          features: ['4人一车', '工作日练车', '操作简单', '通过率高']
        },
        {
          id: 4,
          name: 'C2 VIP班',
          tag: '尊享',
          price: 6200,
          description: '自动挡VIP课程，一对一尊享服务',
          features: ['1人一车', '随到随学', '专车接送', '不过包赔']
        },
        {
          id: 5,
          name: '快速取证班',
          tag: '极速',
          price: 8800,
          description: '快速通道，优先安排考试，最快45天取证',
          features: ['一对一教学', '优先考试', '不过包赔', 'VIP服务']
        },
        {
          id: 6,
          name: '学生特惠班',
          tag: '优惠',
          price: 3200,
          description: '凭学生证专享，寒暑假集中训练',
          features: ['学生专享', '寒暑假集训', '价格优惠', '优先拿证']
        }
      ],
      dialogVisible: false,
      selectedClass: null
    };
  },
  methods: {
    selectClass(item) {
      this.selectedClass = item;
      this.dialogVisible = true;
    },
    goToReg() {
      this.dialogVisible = false;
      this.$router.push({
        path: '/student-reg',
        query: { classId: this.selectedClass.id, className: this.selectedClass.name }
      });
    }
  }
};
</script>

<style scoped>
.class-card {
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.class-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
}

.class-content {
  min-height: 180px;
}

.price {
  margin-bottom: 15px;
}

.price-label {
  color: #606266;
}

.price-value {
  color: #f56c6c;
  font-size: 24px;
  font-weight: bold;
}

.desc {
  color: #606266;
  margin-bottom: 15px;
  line-height: 1.5;
}

.features {
  margin-bottom: 20px;
}

.card-footer {
  border-top: 1px solid #ebeef5;
  padding-top: 15px;
}
</style>
