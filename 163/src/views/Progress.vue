<template>
  <div class="page-container">
    <h2 class="page-title">拼团进度展示</h2>

    <div class="search-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索商品名称"
        style="width: 300px;"
        clearable
      ></el-input>
    </div>

    <div v-for="group in filteredGroups" :key="group.id" class="progress-card">
      <div class="progress-header">
        <div style="display: flex; align-items: center; gap: 15px;">
          <img :src="group.image" style="width: 80px; height: 60px; object-fit: cover; border-radius: 8px;">
          <div>
            <div class="progress-title">{{ group.goodsName }}</div>
            <div style="font-size: 14px; color: #666;">
              截止时间：{{ group.endTime }}
            </div>
          </div>
        </div>
        <el-tag :type="getGroupStatusType(group)" size="medium">
          {{ getGroupStatusText(group) }}
        </el-tag>
      </div>

      <el-progress
        :percentage="Math.round(group.currentCount / group.needCount * 100)"
        :stroke-width="20"
        :show-text="true"
        status="success"
      ></el-progress>

      <div style="margin-top: 20px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
          <span style="font-size: 16px; font-weight: bold;">
            <i class="el-icon-user-solid" style="color: #ff6b00;"></i>
            参团成员 ({{ group.currentCount }}/{{ group.needCount }})
          </span>
        </div>
        
        <div class="member-list">
          <div
            v-for="(member, index) in group.members"
            :key="index"
            style="display: flex; align-items: center; gap: 8px; padding: 10px 15px; background: #f5f7fa; border-radius: 8px;"
          >
            <div class="member-avatar">
              {{ member.name.charAt(0) }}
            </div>
            <div>
              <div style="font-weight: bold;">{{ member.name }}</div>
              <el-tag v-if="member.isLeader" size="mini" type="danger" style="margin-top: 3px;">
                团长
              </el-tag>
              <el-tag v-else size="mini" type="info" style="margin-top: 3px;">
                成员
              </el-tag>
            </div>
          </div>
          
          <div v-for="i in (group.needCount - group.currentCount)" :key="'empty-' + i">
            <div style="display: flex; align-items: center; gap: 8px; padding: 10px 15px; background: #fff; border: 2px dashed #dcdfe6; border-radius: 8px;">
              <div style="width: 40px; height: 40px; border-radius: 50%; background: #f5f7fa; display: flex; align-items: center; justify-content: center;">
                <i class="el-icon-plus" style="font-size: 20px; color: #999;"></i>
              </div>
              <div style="color: #999;">虚位以待</div>
            </div>
          </div>
        </div>
      </div>

      <div style="margin-top: 20px; text-align: right;">
        <el-button type="primary" :disabled="group.currentCount >= group.needCount" @click="joinGroup(group)">
          {{ group.currentCount >= group.needCount ? '已成团' : '立即参团' }}
        </el-button>
        <el-button @click="viewDetail(group)">
          查看详情
        </el-button>
      </div>
    </div>

    <el-empty v-if="filteredGroups.length === 0" description="暂无拼团数据"></el-empty>
  </div>
</template>

<script>
import { groupProgressList } from '../data/mock.js'

export default {
  name: 'Progress',
  data() {
    return {
      groupList: groupProgressList,
      searchKeyword: ''
    }
  },
  computed: {
    filteredGroups() {
      return this.groupList.filter(item => {
        return !this.searchKeyword || item.goodsName.includes(this.searchKeyword)
      })
    }
  },
  methods: {
    getGroupStatusText(group) {
      if (group.currentCount >= group.needCount) {
        return '已成团'
      }
      return `还差 ${group.needCount - group.currentCount} 人成团`
    },
    getGroupStatusType(group) {
      if (group.currentCount >= group.needCount) {
        return 'success'
      }
      return 'warning'
    },
    joinGroup(group) {
      if (group.currentCount >= group.needCount) {
        this.$message.warning('该拼团已成团，无法再参团')
        return
      }
      this.$prompt('请输入您的姓名', '参团确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputPattern: /.+/,
        inputErrorMessage: '请输入姓名'
      }).then(({ value }) => {
        group.currentCount++
        group.members.push({
          name: value,
          isLeader: false
        })
        if (group.currentCount >= group.needCount) {
          this.$message.success('恭喜！拼团已达成！')
        } else {
          this.$message.success('参团成功！')
        }
      }).catch(() => {
      })
    },
    viewDetail(group) {
      this.$alert(`
        <p><strong>商品：</strong>${group.goodsName}</p>
        <p><strong>当前人数：</strong>${group.currentCount}人</p>
        <p><strong>目标人数：</strong>${group.needCount}人</p>
        <p><strong>完成进度：</strong>${Math.round(group.currentCount / group.needCount * 100)}%</p>
        <p><strong>截止时间：</strong>${group.endTime}</p>
        <p><strong>团长：</strong>${group.members.find(m => m.isLeader)?.name || '暂无'}</p>
      `, '拼团详情', {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '确定'
      })
    }
  }
}
</script>