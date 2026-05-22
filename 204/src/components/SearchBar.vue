<template>
  <div class="search-bar">
    <el-form :inline="true" :model="searchForm" class="search-form">
      <el-form-item label="设备编号">
        <el-input
          v-model="searchForm.deviceCode"
          placeholder="支持部分关键词匹配，如：001、TERM"
          clearable
          @keyup.enter.native="handleSearch"
        />
      </el-form-item>
      <el-form-item label="分馆/楼层">
        <el-input
          v-model="searchForm.branchName"
          placeholder="支持分馆名称或楼层，如：东区、1楼"
          clearable
          @keyup.enter.native="handleSearch"
        />
      </el-form-item>
      <el-form-item label="运行状态">
        <el-select
          v-model="searchForm.status"
          placeholder="全部状态"
          clearable
          style="width: 140px"
          @change="handleSearch"
        >
          <el-option label="在线" value="online" />
          <el-option label="离线" value="offline" />
          <el-option label="故障" value="fault" />
          <el-option label="维护中" value="maintaining" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleSearch">
          搜索
        </el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">
          重置
        </el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  data() {
    return {
      searchForm: {
        deviceCode: '',
        branchName: '',
        status: ''
      }
    }
  },
  methods: {
    handleSearch() {
      this.$emit('search', { ...this.searchForm })
    },
    handleReset() {
      this.searchForm.deviceCode = ''
      this.searchForm.branchName = ''
      this.searchForm.status = ''
      this.$emit('reset')
    }
  }
}
</script>

<style scoped lang="scss">
.search-bar {
  background: #fff;
  padding: 20px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  
  .search-form {
    margin: 0;
  }
}
</style>
