<template>
  <div class="attendee-select">
    <el-dialog
      title="选择参会人员"
      :visible.sync="visible"
      width="600px"
      @close="handleClose"
    >
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索姓名或部门"
          clearable
          style="width: 250px; margin-right: 16px;"
        >
          <i slot="prefix" class="el-input__icon el-icon-search"></i>
        </el-input>
        <el-select
          v-model="selectedDepartment"
          placeholder="选择部门"
          clearable
          style="width: 200px;"
        >
          <el-option
            v-for="dept in departments"
            :key="dept"
            :label="dept"
            :value="dept"
          ></el-option>
        </el-select>
      </div>
      <div class="employee-list">
        <el-checkbox
          v-model="checkAll"
          :indeterminate="isIndeterminate"
          @change="handleCheckAllChange"
          style="margin-bottom: 12px;"
        >
          全选
        </el-checkbox>
        <el-checkbox-group v-model="checkedEmployees" @change="handleCheckedChange">
          <div class="employee-grid">
            <el-checkbox
              v-for="emp in filteredEmployees"
              :key="emp.id"
              :label="emp.id"
              class="employee-item"
            >
              <span class="employee-name">{{ emp.name }}</span>
              <span class="employee-dept">{{ emp.department }}</span>
            </el-checkbox>
          </div>
        </el-checkbox-group>
      </div>
      <div slot="footer" class="dialog-footer">
        <span class="selected-count">已选择 {{ checkedEmployees.length }} 人</span>
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleConfirm">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { employees, departments } from '@/mock/employees'

export default {
  name: 'AttendeeSelect',
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      visible: false,
      searchKeyword: '',
      selectedDepartment: '',
      checkedEmployees: [],
      employees,
      departments
    }
  },
  computed: {
    filteredEmployees() {
      return this.employees.filter(emp => {
        const matchKeyword = !this.searchKeyword ||
          emp.name.includes(this.searchKeyword) ||
          emp.department.includes(this.searchKeyword)
        const matchDept = !this.selectedDepartment || emp.department === this.selectedDepartment
        return matchKeyword && matchDept
      })
    },
    checkAll: {
      get() {
        return this.filteredEmployees.length > 0 &&
          this.filteredEmployees.every(emp => this.checkedEmployees.includes(emp.id))
      },
      set(val) {}
    },
    isIndeterminate() {
      const checkedInFiltered = this.filteredEmployees.filter(emp =>
        this.checkedEmployees.includes(emp.id)
      ).length
      return checkedInFiltered > 0 && checkedInFiltered < this.filteredEmployees.length
    }
  },
  methods: {
    open() {
      this.checkedEmployees = [...this.value]
      this.visible = true
    },
    handleClose() {
      this.visible = false
      this.searchKeyword = ''
      this.selectedDepartment = ''
    },
    handleCheckAllChange(val) {
      if (val) {
        const filteredIds = this.filteredEmployees.map(emp => emp.id)
        this.checkedEmployees = [...new Set([...this.checkedEmployees, ...filteredIds])]
      } else {
        const filteredIds = this.filteredEmployees.map(emp => emp.id)
        this.checkedEmployees = this.checkedEmployees.filter(id => !filteredIds.includes(id))
      }
    },
    handleCheckedChange() {},
    handleConfirm() {
      const selected = this.employees.filter(emp => this.checkedEmployees.includes(emp.id))
      this.$emit('input', this.checkedEmployees)
      this.$emit('change', selected)
      this.handleClose()
    }
  }
}
</script>

<style lang="scss" scoped>
.attendee-select {
  .search-bar {
    display: flex;
    align-items: center;
    margin-bottom: 16px;
    padding-bottom: 16px;
    border-bottom: 1px solid #ebeef5;
  }

  .employee-list {
    max-height: 400px;
    overflow-y: auto;
  }

  .employee-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
  }

  .employee-item {
    width: calc(33.333% - 8px);
    margin-right: 0;
    padding: 8px 12px;
    border: 1px solid #dcdfe6;
    border-radius: 4px;
    box-sizing: border-box;
    transition: all 0.3s;

    &:hover {
      border-color: #409eff;
    }

    .el-checkbox__label {
      display: flex;
      flex-direction: column;
      padding-left: 8px;
    }

    .employee-name {
      font-weight: 500;
      color: #303133;
    }

    .employee-dept {
      font-size: 12px;
      color: #909399;
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .selected-count {
      color: #909399;
      font-size: 14px;
    }
  }
}
</style>
