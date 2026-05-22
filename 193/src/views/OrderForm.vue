<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="clearfix">
        <span>货单下单</span>
      </div>
      
      <el-form :model="orderForm" :rules="rules" ref="orderForm" label-width="120px" class="order-form">
        <el-divider content-position="left">发货人信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发货单位" prop="sender">
              <el-input v-model="orderForm.sender" placeholder="请输入发货单位名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="senderPhone">
              <el-input v-model="orderForm.senderPhone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="发货地址" prop="senderAddress">
              <el-input type="textarea" v-model="orderForm.senderAddress" :rows="2" placeholder="请输入详细发货地址"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">收货人信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="收货单位" prop="receiver">
              <el-input v-model="orderForm.receiver" placeholder="请输入收货单位名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系电话" prop="receiverPhone">
              <el-input v-model="orderForm.receiverPhone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="收货地址" prop="receiverAddress">
              <el-input type="textarea" v-model="orderForm.receiverAddress" :rows="2" placeholder="请输入详细收货地址"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">货物信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="货物名称" prop="goodsName">
              <el-input v-model="orderForm.goodsName" placeholder="请输入货物名称"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="货物重量(吨)" prop="goodsWeight">
              <el-input-number 
                v-model="orderForm.goodsWeight" 
                :min="0.01" 
                :max="100"
                :step="0.1" 
                :precision="2"
                style="width: 100%">
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="货物体积(m³)" prop="goodsVolume">
              <el-input-number 
                v-model="orderForm.goodsVolume" 
                :min="0.01" 
                :max="500"
                :step="0.1" 
                :precision="2"
                style="width: 100%">
              </el-input-number>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="运输线路" prop="routeId">
              <el-select v-model="orderForm.routeId" placeholder="请选择运输线路" style="width: 100%" @change="calculateFreight">
                <el-option v-for="route in routeList" :key="route.id" :label="route.name" :value="route.id"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="预估运费">
              <el-input v-model="estimatedFreight" readonly style="width: 100%">
                <template slot="append">元</template>
              </el-input>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="要求到达时间" prop="requireTime">
              <el-date-picker
                v-model="orderForm.requireTime"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
                value-format="yyyy-MM-dd">
              </el-date-picker>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="货物类型" prop="goodsType">
              <el-select v-model="orderForm.goodsType" placeholder="请选择货物类型" style="width: 100%">
                <el-option label="普通货物" value="普通货物"></el-option>
                <el-option label="易碎品" value="易碎品"></el-option>
                <el-option label="危险品" value="危险品"></el-option>
                <el-option label="冷藏货物" value="冷藏货物"></el-option>
                <el-option label="贵重物品" value="贵重物品"></el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="备注说明">
              <el-input type="textarea" v-model="orderForm.remark" :rows="3" placeholder="请输入其他需要说明的信息"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="submitForm" size="large">提交订单</el-button>
          <el-button @click="resetForm" size="large">重置表单</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import { orderApi, routeList, calculateFreight } from '../api/mockData'

export default {
  name: 'OrderForm',
  data() {
    const validateWeight = (rule, value, callback) => {
      if (!value && value !== 0) {
        callback(new Error('请输入货物重量'))
      } else if (isNaN(value)) {
        callback(new Error('货物重量必须是数字'))
      } else if (value <= 0) {
        callback(new Error('货物重量必须大于0'))
      } else if (value < 0.01) {
        callback(new Error('货物重量不能小于0.01吨'))
      } else if (value > 100) {
        callback(new Error('货物重量不能超过100吨，请分批运输'))
      } else {
        callback()
      }
    }
    const validateVolume = (rule, value, callback) => {
      if (!value && value !== 0) {
        callback(new Error('请输入货物体积'))
      } else if (isNaN(value)) {
        callback(new Error('货物体积必须是数字'))
      } else if (value <= 0) {
        callback(new Error('货物体积必须大于0'))
      } else if (value < 0.01) {
        callback(new Error('货物体积不能小于0.01m³'))
      } else if (value > 500) {
        callback(new Error('货物体积不能超过500m³，请分批运输'))
      } else {
        callback()
      }
    }
    return {
      routeList: routeList,
      estimatedFreight: 0,
      orderForm: {
        sender: '',
        senderPhone: '',
        senderAddress: '',
        receiver: '',
        receiverPhone: '',
        receiverAddress: '',
        goodsName: '',
        goodsWeight: 1,
        goodsVolume: 1,
        requireTime: '',
        goodsType: '普通货物',
        routeId: null,
        remark: ''
      },
      rules: {
        sender: [
          { required: true, message: '请输入发货单位名称', trigger: 'blur' }
        ],
        senderPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$|^0\d{2,3}-?\d{7,8}$/, message: '请输入正确的电话号码', trigger: 'blur' }
        ],
        senderAddress: [
          { required: true, message: '请输入发货地址', trigger: 'blur' }
        ],
        receiver: [
          { required: true, message: '请输入收货单位名称', trigger: 'blur' }
        ],
        receiverPhone: [
          { required: true, message: '请输入联系电话', trigger: 'blur' },
          { pattern: /^1[3-9]\d{9}$|^0\d{2,3}-?\d{7,8}$/, message: '请输入正确的电话号码', trigger: 'blur' }
        ],
        receiverAddress: [
          { required: true, message: '请输入收货地址', trigger: 'blur' }
        ],
        goodsName: [
          { required: true, message: '请输入货物名称', trigger: 'blur' }
        ],
        goodsWeight: [
          { required: true, validator: validateWeight, trigger: 'blur' }
        ],
        goodsVolume: [
          { required: true, validator: validateVolume, trigger: 'blur' }
        ],
        routeId: [
          { required: true, message: '请选择运输线路', trigger: 'change' }
        ],
        requireTime: [
          { required: true, message: '请选择要求到达时间', trigger: 'change' }
        ]
      }
    }
  },
  watch: {
    'orderForm.goodsWeight': function() {
      this.calculateFreight()
    },
    'orderForm.goodsVolume': function() {
      this.calculateFreight()
    }
  },
  methods: {
    calculateFreight() {
      if (this.orderForm.routeId && this.orderForm.goodsWeight && this.orderForm.goodsVolume) {
        this.estimatedFreight = calculateFreight(this.orderForm.goodsWeight, this.orderForm.goodsVolume, this.orderForm.routeId)
      } else {
        this.estimatedFreight = 0
      }
    },
    submitForm() {
      this.$refs.orderForm.validate(async (valid) => {
        if (valid) {
          try {
            await orderApi.add(this.orderForm)
            this.$message({
              type: 'success',
              message: '订单提交成功！'
            })
            this.resetForm()
          } catch (error) {
            this.$message.error('订单提交失败，请重试')
          }
        } else {
          this.$message.error('请检查表单填写是否正确')
          return false
        }
      })
    },
    resetForm() {
      this.$refs.orderForm.resetFields()
      this.estimatedFreight = 0
    }
  }
}
</script>

<style scoped>
.order-form {
  padding: 20px;
}
.el-divider {
  margin: 15px 0;
}
</style>
