<template>
  <div class="coach-list">
    <div class="page-title">教练列表</div>
    <div class="card-wrapper">
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="请输入教练姓名搜索"
          style="width: 300px; margin-right: 10px"
          clearable
          @keyup.enter.native="searchCoach"
        >
          <el-button slot="append" icon="el-icon-search" @click="searchCoach"></el-button>
        </el-input>
        <el-select v-model="searchSubject" placeholder="执教科目" style="width: 150px; margin-right: 10px">
          <el-option label="全部科目" value=""></el-option>
          <el-option label="科目二" value="科目二"></el-option>
          <el-option label="科目三" value="科目三"></el-option>
        </el-select>
        <el-button type="primary" @click="searchCoach">搜索</el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>

      <el-table
        :data="tableData"
        border
        style="width: 100%; margin-top: 20px"
        :row-class-name="tableRowClassName"
      >
        <el-table-column prop="id" label="编号" width="80" align="center"></el-table-column>
        <el-table-column label="头像" width="80" align="center">
          <template slot-scope="scope">
            <el-avatar :size="50" :src="scope.row.avatar"></el-avatar>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="姓名" width="100" align="center"></el-table-column>
        <el-table-column prop="gender" label="性别" width="80" align="center"></el-table-column>
        <el-table-column prop="subject" label="执教科目" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="small">{{ scope.row.subject }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="experience" label="教龄(年)" width="100" align="center"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="130" align="center"></el-table-column>
        <el-table-column prop="rating" label="评分" width="120" align="center">
          <template slot-scope="scope">
            <el-rate v-model="scope.row.rating" disabled show-score text-color="#ff9900" score-template="{value}分"></el-rate>
          </template>
        </el-table-column>
        <el-table-column prop="studentCount" label="学员数" width="100" align="center"></el-table-column>
        <el-table-column label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="scope.row.status === '在岗' ? 'success' : 'info'" size="small">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="center">
          <template slot-scope="scope">
            <el-button size="mini" type="primary" @click="viewDetail(scope.row)">查看详情</el-button>
            <el-button size="mini" type="success" @click="makeReservation(scope.row)">预约</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-wrapper">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[5, 10, 20, 50]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        >
        </el-pagination>
      </div>
    </div>

    <el-dialog title="教练详情" :visible.sync="detailDialogVisible" width="500px">
      <div v-if="currentCoach">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="姓名">{{ currentCoach.name }}</el-descriptions-item>
          <el-descriptions-item label="性别">{{ currentCoach.gender }}</el-descriptions-item>
          <el-descriptions-item label="执教科目">{{ currentCoach.subject }}</el-descriptions-item>
          <el-descriptions-item label="教龄">{{ currentCoach.experience }}年</el-descriptions-item>
          <el-descriptions-item label="联系电话">{{ currentCoach.phone }}</el-descriptions-item>
          <el-descriptions-item label="评分">
            <el-rate v-model="currentCoach.rating" disabled show-score text-color="#ff9900" score-template="{value}分"></el-rate>
          </el-descriptions-item>
          <el-descriptions-item label="个人简介">{{ currentCoach.intro }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CoachList',
  data() {
    return {
      searchKeyword: '',
      searchSubject: '',
      currentPage: 1,
      pageSize: 10,
      total: 0,
      tableData: [],
      detailDialogVisible: false,
      currentCoach: null,
      allCoaches: [
        {
          id: 1,
          name: '张教练',
          gender: '男',
          avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          subject: '科目二',
          experience: 8,
          phone: '13800138001',
          rating: 4.8,
          studentCount: 156,
          status: '在岗',
          intro: '从事驾培行业8年，教学经验丰富，耐心细致，擅长基础驾驶技巧培训，学员通过率高达95%以上。'
        },
        {
          id: 2,
          name: '李教练',
          gender: '女',
          avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
          subject: '科目三',
          experience: 6,
          phone: '13800138002',
          rating: 4.9,
          studentCount: 128,
          status: '在岗',
          intro: '性格温和，教学细致认真，擅长考前心理辅导，帮助学员克服考试紧张情绪。'
        },
        {
          id: 3,
          name: '王教练',
          gender: '男',
          avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          subject: '科目二',
          experience: 10,
          phone: '13800138003',
          rating: 4.7,
          studentCount: 235,
          status: '在岗',
          intro: '资深教练，从事驾培工作10年，教学风格严谨，方法独特，学员评价极高。'
        },
        {
          id: 4,
          name: '赵教练',
          gender: '男',
          avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          subject: '科目三',
          experience: 5,
          phone: '13800138004',
          rating: 4.6,
          studentCount: 98,
          status: '在岗',
          intro: '年轻有为，教学方法新颖，善于与年轻学员沟通，课堂氛围轻松愉快。'
        },
        {
          id: 5,
          name: '孙教练',
          gender: '女',
          avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
          subject: '科目二',
          experience: 7,
          phone: '13800138005',
          rating: 4.8,
          studentCount: 142,
          status: '休假',
          intro: '亲和力强，特别擅长辅导零基础学员，耐心讲解每个动作要领。'
        },
        {
          id: 6,
          name: '周教练',
          gender: '男',
          avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          subject: '科目三',
          experience: 12,
          phone: '13800138006',
          rating: 4.9,
          studentCount: 312,
          status: '在岗',
          intro: '金牌教练，多次获得优秀教练称号，学员通过率连续五年排名第一。'
        },
        {
          id: 7,
          name: '吴教练',
          gender: '男',
          avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png',
          subject: '科目二',
          experience: 4,
          phone: '13800138007',
          rating: 4.5,
          studentCount: 76,
          status: '在岗',
          intro: '新晋优秀教练，理论知识扎实，实操经验丰富，深受学员喜爱。'
        },
        {
          id: 8,
          name: '郑教练',
          gender: '女',
          avatar: 'https://cube.elemecdn.com/9/c2/f0ee8a3c7c9638a54940382568c9dpng.png',
          subject: '科目三',
          experience: 9,
          phone: '13800138008',
          rating: 4.7,
          studentCount: 189,
          status: '在岗',
          intro: '教学认真负责，注重细节培养，帮助学员养成良好的驾驶习惯。'
        }
      ]
    };
  },
  mounted() {
    this.loadData();
  },
  methods: {
    tableRowClassName({ rowIndex }) {
      if (rowIndex % 2 === 1) {
        return 'bg-gray-row';
      }
      return '';
    },
    loadData() {
      let data = [...this.allCoaches];
      
      if (this.searchKeyword) {
        data = data.filter(item => item.name.includes(this.searchKeyword));
      }
      
      if (this.searchSubject) {
        data = data.filter(item => item.subject === this.searchSubject);
      }
      
      this.total = data.length;
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.tableData = data.slice(start, end);
    },
    searchCoach() {
      this.currentPage = 1;
      this.loadData();
    },
    resetSearch() {
      this.searchKeyword = '';
      this.searchSubject = '';
      this.currentPage = 1;
      this.loadData();
    },
    handleSizeChange(val) {
      this.pageSize = val;
      this.loadData();
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      this.loadData();
    },
    viewDetail(row) {
      this.currentCoach = row;
      this.detailDialogVisible = true;
    },
    makeReservation(row) {
      this.$router.push({
        path: '/reservation',
        query: { coachId: row.id, coachName: row.name }
      });
    }
  }
};
</script>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}

.pagination-wrapper {
  margin-top: 20px;
  text-align: right;
}

.bg-gray-row {
  background-color: #f5f7fa;
}
</style>
