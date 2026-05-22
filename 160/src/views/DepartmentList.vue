<template>
  <div class="page-container">
    <h2 class="page-title">
      <i class="el-icon-office-building"></i>
      科室列表
    </h2>
    
    <div class="filter-bar">
      <el-switch
        v-model="hideRegistered"
        active-text="隐藏已挂号科室"
        inactive-text="显示全部科室"
      >
      </el-switch>
      <span class="registered-count">
        当前已挂号科室：{{ registeredDepartments.size }} 个
      </span>
    </div>
    
    <el-row :gutter="20" class="card-list">
      <el-col :span="6" v-for="dept in filteredDepartments" :key="dept.id">
        <el-card :body-style="{ padding: '0px' }" class="dept-card" shadow="hover">
          <div class="card-header" :class="{ disabled: dept.status === 0 }">
            <span class="dept-name">{{ dept.name }}</span>
            <el-tag :type="dept.status === 1 ? 'success' : 'info'" size="small">
              {{ dept.status === 1 ? '开诊' : '停诊' }}
            </el-tag>
          </div>
          <div class="card-content">
            <p class="dept-desc">{{ dept.description }}</p>
            <div class="card-info">
              <span><i class="el-icon-user"></i> {{ dept.doctorCount }} 位医生</span>
            </div>
          </div>
          <div class="card-footer">
            <el-button type="primary" size="small" @click="viewSchedule(dept)" :disabled="dept.status === 0">
              查看排班
            </el-button>
            <el-button type="success" size="small" @click="goRegister(dept)" :disabled="dept.status === 0">
              立即挂号
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { departments } from '@/mock/data';
import { store } from '@/store';

export default {
  name: 'DepartmentList',
  data() {
    return {
      departmentList: [...departments],
      hideRegistered: false,
      unsubscribe: null
    };
  },
  computed: {
    registrationList() {
      return store.getRegistrations();
    },
    registeredDepartments() {
      const today = new Date().toISOString().split('T')[0];
      const registeredDepts = new Set();
      this.registrationList.forEach(record => {
        if (record.date >= today && record.status !== 3) {
          registeredDepts.add(record.department);
        }
      });
      return registeredDepts;
    },
    filteredDepartments() {
      let data = [...this.departmentList];
      // 只显示开诊的科室
      data = data.filter(dept => dept.status === 1);
      // 如果开启隐藏已挂号科室
      if (this.hideRegistered) {
        data = data.filter(dept => !this.registeredDepartments.has(dept.name));
      }
      return data;
    }
  },
  mounted() {
    // 订阅数据变化
    this.unsubscribe = store.subscribe(() => {
      this.$forceUpdate();
    });
  },
  beforeDestroy() {
    if (this.unsubscribe) {
      this.unsubscribe();
    }
  },
  methods: {
    viewSchedule(dept) {
      this.$router.push({
        path: '/schedule',
        query: { department: dept.name }
      });
    },
    goRegister(dept) {
      this.$router.push({
        path: '/register',
        query: { department: dept.name }
      });
    }
  }
};
</script>

<style scoped>
.filter-bar {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 1px solid #EBEEF5;
  margin-bottom: 20px;
}

.registered-count {
  margin-left: 20px;
  color: #909399;
  font-size: 14px;
}

.card-list {
  margin-top: 20px;
}

.dept-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.dept-card:hover {
  transform: translateY(-5px);
}

.card-header {
  background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%);
  color: #fff;
  padding: 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-radius: 4px 4px 0 0;
}

.card-header.disabled {
  background: linear-gradient(135deg, #909399 0%, #b4b6ba 100%);
}

.dept-name {
  font-size: 18px;
  font-weight: 600;
}

.card-content {
  padding: 20px;
}

.dept-desc {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
  overflow: hidden;
}

.card-info {
  color: #909399;
  font-size: 13px;
}

.card-info i {
  margin-right: 5px;
  color: #409EFF;
}

.card-footer {
  padding: 15px 20px;
  border-top: 1px solid #EBEEF5;
  display: flex;
  justify-content: space-around;
}
</style>
