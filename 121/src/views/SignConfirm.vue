<template>
  <div class="page-card">
    <div class="page-title">签收确认</div>
    
    <el-table :data="tableData" border stripe style="width: 100%" v-loading="loading">
      <el-table-column prop="orderNo" label="订单号" width="180"></el-table-column>
      <el-table-column prop="receiverName" label="收件人" width="100"></el-table-column>
      <el-table-column prop="receiverPhone" label="联系电话" width="130"></el-table-column>
      <el-table-column prop="receiverAddress" label="收件地址" show-overflow-tooltip></el-table-column>
      <el-table-column prop="packageName" label="包裹名称" width="120"></el-table-column>
      <el-table-column label="状态" width="100">
        <template slot-scope="scope">
          <el-tag :type="statusMap[scope.row.status].type" size="small">
            {{ statusMap[scope.row.status].label }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template slot-scope="scope">
          <el-button
            v-if="scope.row.status === 'delivering'"
            type="success"
            size="small"
            @click="handleSign(scope.row)"
          >
            签收
          </el-button>
          <el-button size="small" @click="handleDetail(scope.row)">详情</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="签收确认" :visible.sync="dialogVisible" width="500px">
      <el-form :model="signForm" label-width="80px">
        <el-form-item label="订单号">
          <el-input v-model="signForm.orderNo" disabled></el-input>
        </el-form-item>
        <el-form-item label="签收人" prop="signer">
          <el-input v-model="signForm.signer" placeholder="请输入签收人姓名"></el-input>
        </el-form-item>
        <el-form-item label="签收时间">
          <el-date-picker
            v-model="signForm.signTime"
            type="datetime"
            placeholder="选择签收时间"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="签收方式">
          <el-radio-group v-model="signForm.signType">
            <el-radio label="本人签收">本人签收</el-radio>
            <el-radio label="代收">代收</el-radio>
            <el-radio label="驿站">驿站</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input type="textarea" v-model="signForm.remark" :rows="3"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmSign">确认签收</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mockPackages, statusMap, mockTracking } from '@/mock/data.js';
import { EventBus } from '@/utils/eventBus.js';

export default {
  name: 'SignConfirm',
  data() {
    return {
      loading: false,
      tableData: [],
      statusMap: statusMap,
      dialogVisible: false,
      currentRow: null,
      signingIds: new Set(),
      signForm: {
        orderNo: '',
        signer: '',
        signTime: new Date(),
        signType: '本人签收',
        remark: ''
      }
    };
  },
  created() {
    this.loadData();
    EventBus.$on('packageStatusUpdated', () => {
      this.loadData();
    });
  },
  beforeDestroy() {
    EventBus.$off('packageStatusUpdated');
  },
  methods: {
    loadData() {
      this.loading = true;
      setTimeout(() => {
        this.tableData = [...mockPackages].filter(item => 
          item.status === 'delivering' || item.status === 'signed'
        );
        this.loading = false;
      }, 300);
    },
    handleSign(row) {
      if (row.status === 'signed') {
        this.$message.warning('该包裹已签收，不可重复操作');
        return;
      }
      if (this.signingIds.has(row.id)) {
        this.$message.warning('该包裹正在签收中，请稍候');
        return;
      }
      this.currentRow = row;
      this.signForm = {
        orderNo: row.orderNo,
        signer: row.receiverName,
        signTime: new Date(),
        signType: '本人签收',
        remark: ''
      };
      this.dialogVisible = true;
    },
    confirmSign() {
      if (!this.signForm.signer) {
        this.$message.warning('请输入签收人姓名');
        return;
      }
      
      const item = mockPackages.find(p => p.id === this.currentRow.id);
      if (!item) {
        this.$message.error('未找到该订单信息');
        return;
      }
      
      if (item.status === 'signed') {
        this.$message.warning('该包裹已签收，不可重复操作');
        this.dialogVisible = false;
        this.loadData();
        return;
      }
      
      this.signingIds.add(item.id);
      
      item.status = 'signed';
      item.signTime = this.signForm.signTime;
      item.signer = this.signForm.signer;
      item.signType = this.signForm.signType;
      
      const tracking = mockTracking.find(t => t.orderNo === item.orderNo);
      if (tracking) {
        tracking.tracks.unshift({
          time: this.formatDate(this.signForm.signTime),
          status: '已签收',
          location: item.receiverAddress,
          operator: this.signForm.signer + '(' + this.signForm.signType + ')',
          remark: this.signForm.remark || '包裹已成功签收'
        });
      }
      
      EventBus.$emit('packageStatusUpdated', {
        orderNo: item.orderNo,
        status: 'signed'
      });
      
      this.$message.success('签收成功！');
      this.dialogVisible = false;
      this.loadData();
      setTimeout(() => {
        this.signingIds.delete(item.id);
      }, 1000);
    },
    formatDate(date) {
      const d = new Date(date);
      const pad = n => n.toString().padStart(2, '0');
      return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
    },
    handleDetail(row) {
      this.$alert(`
        订单号：${row.orderNo}\n
        收件人：${row.receiverName}\n
        联系电话：${row.receiverPhone}\n
        收件地址：${row.receiverAddress}\n
        包裹名称：${row.packageName}\n
        包裹重量：${row.weight}kg\n
        ${row.signer ? '签收人：' + row.signer : ''}
        ${row.signType ? '签收方式：' + row.signType : ''}
      `, '订单详情');
    }
  }
};
</script>

<style scoped>
.dialog-footer {
  text-align: right;
}
</style>
