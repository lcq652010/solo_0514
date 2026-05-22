<template>
  <div class="trainer-list">
    <div class="page-title">私教列表</div>
    <el-card>
      <el-table :data="trainerList" border style="width: 100%">
        <el-table-column prop="id" label="编号" width="80" align="center"></el-table-column>
        <el-table-column prop="name" label="姓名" width="120" align="center"></el-table-column>
        <el-table-column prop="avatar" label="头像" width="100" align="center">
          <template slot-scope="scope">
            <el-avatar :size="60" :src="scope.row.avatar"></el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="specialty" label="专长" align="center"></el-table-column>
        <el-table-column prop="experience" label="从业年限" width="120" align="center">
          <template slot-scope="scope">{{ scope.row.experience }}年</template>
        </el-table-column>
        <el-table-column prop="rating" label="评分" width="120" align="center">
          <template slot-scope="scope">
            <el-rate v-model="scope.row.rating" disabled show-score text-color="#ff9900"></el-rate>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="课时费" width="120" align="center">
          <template slot-scope="scope">¥{{ scope.row.price }}/课时</template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center">
          <template slot-scope="scope">
            <el-button type="primary" size="small" @click="bookTrainer(scope.row)">预约</el-button>
            <el-button type="info" size="small" @click="viewDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[5, 10, 20]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        style="margin-top: 20px; text-align: right;">
      </el-pagination>
    </el-card>

    <el-dialog title="私教详情" :visible.sync="detailVisible" width="500px">
      <div v-if="currentTrainer">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="姓名">{{ currentTrainer.name }}</el-descriptions-item>
          <el-descriptions-item label="专长">{{ currentTrainer.specialty }}</el-descriptions-item>
          <el-descriptions-item label="从业年限">{{ currentTrainer.experience }}年</el-descriptions-item>
          <el-descriptions-item label="个人简介">{{ currentTrainer.intro }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'TrainerList',
  data() {
    return {
      trainerList: [],
      currentPage: 1,
      pageSize: 10,
      total: 0,
      detailVisible: false,
      currentTrainer: null
    }
  },
  created() {
    this.loadTrainers()
  },
  methods: {
    loadTrainers() {
      const allTrainers = [
        { id: 1, name: '张教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '增肌训练、力量举', experience: 8, rating: 4.8, price: 300, intro: '国家一级健身教练，专注增肌训练8年，帮助超过500名学员达成健身目标。' },
        { id: 2, name: '李教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '减脂塑形、HIIT', experience: 6, rating: 4.9, price: 280, intro: 'ACE认证教练，擅长高效燃脂训练，科学饮食指导。' },
        { id: 3, name: '王教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '瑜伽、普拉提', experience: 10, rating: 5.0, price: 350, intro: '印度瑜伽学院认证，10年瑜伽教学经验，专注身心平衡。' },
        { id: 4, name: '陈教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '搏击、格斗', experience: 7, rating: 4.7, price: 320, intro: '前职业拳手，国家级搏击教练，教授实战技巧与防身术。' },
        { id: 5, name: '刘教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '康复训练、体态矫正', experience: 9, rating: 4.9, price: 400, intro: '运动康复学硕士，专注脊柱矫正与运动损伤康复。' },
        { id: 6, name: '赵教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: ' CrossFit、功能性训练', experience: 5, rating: 4.6, price: 260, intro: 'CrossFit L3认证教练，专注全面体能提升。' },
        { id: 7, name: '孙教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '少儿体适能', experience: 4, rating: 4.8, price: 240, intro: '少儿体适能认证教练，擅长儿童趣味健身。' },
        { id: 8, name: '周教练', avatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png', specialty: '孕期产后恢复', experience: 7, rating: 4.9, price: 380, intro: '孕产体适能专家，帮助宝妈健康恢复。' }
      ]
      this.total = allTrainers.length
      const start = (this.currentPage - 1) * this.pageSize
      const end = start + this.pageSize
      this.trainerList = allTrainers.slice(start, end)
    },
    handleSizeChange(val) {
      this.pageSize = val
      this.loadTrainers()
    },
    handleCurrentChange(val) {
      this.currentPage = val
      this.loadTrainers()
    },
    bookTrainer(trainer) {
      this.$router.push({
        path: '/booking',
        query: { trainerId: trainer.id, trainerName: trainer.name }
      })
    },
    viewDetail(trainer) {
      this.currentTrainer = trainer
      this.detailVisible = true
    }
  }
}
</script>

<style scoped>
.trainer-list {
  padding: 0;
}
</style>
