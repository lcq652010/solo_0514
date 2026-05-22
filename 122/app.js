new Vue({
  el: '#app',
  data: {
    currentPage: 'order',
    submitting: false,
    processDialogVisible: false,
    selectedOrder: null,
    searchKeyword: '',
    filterStatus: '',
    currentOperator: '管理员',
    
    processSteps: ['熔银', '倒模', '整形', '抛光', '刻字', '组装', '质检', '完工'],
    
    styles: [
      { id: 'traditional', name: '传统吉祥锁', icon: '🔒', price: 299 },
      { id: 'peanut', name: '花生长命锁', icon: '🥜', price: 269 },
      { id: 'ingot', name: '元宝长命锁', icon: '💰', price: 279 },
      { id: 'heart', name: '心形长命锁', icon: '❤️', price: 259 }
    ],
    
    chains: [
      { id: 'simple', name: '简约O型链', price: 59 },
      { id: 'bead', name: '圆珠链', price: 79 },
      { id: 'twist', name: '麻花链', price: 89 },
      { id: 'box', name: '盒仔链', price: 99 }
    ],
    
    orderForm: {
      silverContent: '999',
      style: 'traditional',
      length: 45,
      width: 35,
      engravingFront: '',
      engravingBack: '',
      chain: 'simple',
      customerName: '',
      customerPhone: '',
      remark: ''
    },
    
    rules: {
      silverContent: [{ required: true, message: '请选择银含量', trigger: 'change' }],
      style: [{ required: true, message: '请选择款式', trigger: 'change' }],
      length: [
        { required: true, message: '请输入长度', trigger: 'blur' },
        { type: 'number', min: 25, max: 80, message: '长度范围为25-80mm，请输入合理尺寸', trigger: 'blur' }
      ],
      width: [
        { required: true, message: '请输入宽度', trigger: 'blur' },
        { type: 'number', min: 20, max: 60, message: '宽度范围为20-60mm，请输入合理尺寸', trigger: 'blur' }
      ],
      engravingFront: [{ required: true, message: '请输入正面刻字内容', trigger: 'blur' }],
      engravingBack: [{ required: true, message: '请输入背面刻字内容', trigger: 'blur' }],
      chain: [{ required: true, message: '请选择链条', trigger: 'change' }],
      customerName: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
      customerPhone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ]
    },
    
    orders: []
  },
  
  computed: {
    totalPrice() {
      const stylePrice = this.styles.find(s => s.id === this.orderForm.style)?.price || 0;
      const chainPrice = this.chains.find(c => c.id === this.orderForm.chain)?.price || 0;
      const silverPrice = this.orderForm.silverContent === '999' ? 100 : 
                          this.orderForm.silverContent === '925' ? 80 : 60;
      const sizePrice = Math.floor((this.orderForm.length * this.orderForm.width) / 100) * 10;
      return stylePrice + chainPrice + silverPrice + sizePrice;
    },
    
    filteredOrders() {
      let result = [...this.orders];
      
      if (this.searchKeyword) {
        result = result.filter(order => 
          order.id.includes(this.searchKeyword) || 
          order.customerName.includes(this.searchKeyword)
        );
      }
      
      if (this.filterStatus) {
        result = result.filter(order => order.status === this.filterStatus);
      }
      
      return result.sort((a, b) => new Date(b.createTime) - new Date(a.createTime));
    }
  },
  
  mounted() {
    this.loadOrders();
    this.addDemoOrders();
  },
  
  methods: {
    addDemoOrders() {
      if (this.orders.length === 0) {
        const demoOrders = [
          {
            id: 'ORD202401001',
            silverContent: '999',
            style: 'traditional',
            length: 45,
            width: 35,
            engravingFront: '长命百岁',
            engravingBack: '富贵吉祥',
            chain: 'bead',
            customerName: '张三',
            customerPhone: '13800138001',
            remark: '请尽快制作',
            totalPrice: 528,
            status: 'producing',
            currentStep: 3,
            processHistory: [
              { step: 0, stepName: '熔银', operator: '李师傅', operateTime: '2024-01-15 11:00:00' },
              { step: 1, stepName: '倒模', operator: '李师傅', operateTime: '2024-01-15 14:30:00' },
              { step: 2, stepName: '整形', operator: '王师傅', operateTime: '2024-01-16 09:15:00' }
            ],
            createTime: '2024-01-15 10:30:00'
          },
          {
            id: 'ORD202401002',
            silverContent: '925',
            style: 'heart',
            length: 40,
            width: 32,
            engravingFront: '宝宝',
            engravingBack: '平安',
            chain: 'simple',
            customerName: '李四',
            customerPhone: '13800138002',
            remark: '',
            totalPrice: 415,
            status: 'pending',
            currentStep: 0,
            processHistory: [],
            createTime: '2024-01-16 14:20:00'
          },
          {
            id: 'ORD202401003',
            silverContent: '999',
            style: 'ingot',
            length: 50,
            width: 38,
            engravingFront: '福',
            engravingBack: '2024',
            chain: 'box',
            customerName: '王五',
            customerPhone: '13800138003',
            remark: '送给孙子的礼物',
            totalPrice: 580,
            status: 'completed',
            currentStep: 8,
            processHistory: [
              { step: 0, stepName: '熔银', operator: '张师傅', operateTime: '2024-01-10 10:00:00' },
              { step: 1, stepName: '倒模', operator: '张师傅', operateTime: '2024-01-10 11:30:00' },
              { step: 2, stepName: '整形', operator: '李师傅', operateTime: '2024-01-10 14:00:00' },
              { step: 3, stepName: '抛光', operator: '王师傅', operateTime: '2024-01-11 09:00:00' },
              { step: 4, stepName: '刻字', operator: '陈师傅', operateTime: '2024-01-11 11:00:00' },
              { step: 5, stepName: '组装', operator: '李师傅', operateTime: '2024-01-11 14:00:00' },
              { step: 6, stepName: '质检', operator: '质检员', operateTime: '2024-01-12 09:00:00' },
              { step: 7, stepName: '完工', operator: '质检员', operateTime: '2024-01-12 10:00:00' }
            ],
            createTime: '2024-01-10 09:15:00'
          }
        ];
        this.orders = demoOrders;
        this.saveOrders();
      }
    },
    
    loadOrders() {
      const saved = localStorage.getItem('silverOrders');
      if (saved) {
        this.orders = JSON.parse(saved);
      }
    },
    
    saveOrders() {
      localStorage.setItem('silverOrders', JSON.stringify(this.orders));
    },
    
    submitOrder() {
      this.$refs.orderForm.validate((valid) => {
        if (valid) {
          this.submitting = true;
          
          this.$nextTick(() => {
            setTimeout(() => {
              const order = {
                id: 'ORD' + new Date().toISOString().slice(0, 10).replace(/-/g, '') + 
                      String(this.orders.length + 1).padStart(3, '0'),
                ...this.orderForm,
                totalPrice: this.totalPrice,
                status: 'pending',
                currentStep: 0,
                processHistory: [],
                createTime: this.formatDateTime(new Date())
              };
              
              this.orders.unshift(order);
              this.saveOrders();
              
              this.$forceUpdate();
              
              this.$message({
                message: '订单提交成功！订单号：' + order.id,
                type: 'success',
                duration: 3000
              });
              
              this.resetForm();
              this.submitting = false;
            }, 1000);
          });
        } else {
          this.$nextTick(() => {
            this.$message.error('请填写完整的订单信息');
          });
          return false;
        }
      });
    },
    
    resetForm() {
      this.$refs.orderForm.resetFields();
      this.orderForm.silverContent = '999';
      this.orderForm.style = 'traditional';
      this.orderForm.length = 45;
      this.orderForm.width = 35;
      this.orderForm.engravingFront = '';
      this.orderForm.engravingBack = '';
      this.orderForm.chain = 'simple';
      this.orderForm.customerName = '';
      this.orderForm.customerPhone = '';
      this.orderForm.remark = '';
      
      this.$nextTick(() => {
        this.$refs.orderForm.clearValidate();
      });
    },
    
    getStyleName(styleId) {
      const style = this.styles.find(s => s.id === styleId);
      return style ? style.name : styleId;
    },
    
    getChainName(chainId) {
      const chain = this.chains.find(c => c.id === chainId);
      return chain ? chain.name : chainId;
    },
    
    getStatusType(status) {
      const types = {
        pending: 'info',
        producing: 'warning',
        completed: 'success'
      };
      return types[status] || '';
    },
    
    getStatusText(status) {
      const texts = {
        pending: '待生产',
        producing: '生产中',
        completed: '已完工'
      };
      return texts[status] || status;
    },
    
    showProcessDialog(order) {
      this.selectedOrder = JSON.parse(JSON.stringify(order));
      this.processDialogVisible = true;
    },
    
    closeProcessDialog() {
      const index = this.orders.findIndex(o => o.id === this.selectedOrder.id);
      if (index !== -1) {
        this.$set(this.orders, index, this.selectedOrder);
      }
      this.processDialogVisible = false;
      this.selectedOrder = null;
    },
    
    updateProcessStep(index) {
      if (this.selectedOrder.status === 'completed') {
        this.$message.warning('订单已完工，无需更新工序');
        return;
      }
      
      if (this.selectedOrder.currentStep !== index) {
        this.$message.error('请严格按顺序完成工序，不可跳步');
        return;
      }
      
      if (index < 0 || index >= this.processSteps.length) {
        this.$message.error('工序索引无效');
        return;
      }
      
      const processRecord = {
        step: index,
        stepName: this.processSteps[index],
        operator: this.currentOperator,
        operateTime: this.formatDateTime(new Date())
      };
      
      if (!this.selectedOrder.processHistory) {
        this.selectedOrder.processHistory = [];
      }
      this.selectedOrder.processHistory.push(processRecord);
      
      this.selectedOrder.currentStep++;
      
      if (this.selectedOrder.currentStep >= this.processSteps.length) {
        this.selectedOrder.status = 'completed';
        this.selectedOrder.currentStep = this.processSteps.length;
        this.$message({
          message: `🎉 恭喜！订单已全部完工！操作人：${this.currentOperator}`,
          type: 'success'
        });
      } else {
        this.selectedOrder.status = 'producing';
        this.$message({
          message: `「${this.processSteps[index]}」工序完成，操作人：${this.currentOperator}，进入「${this.processSteps[index + 1]}」`,
          type: 'success'
        });
      }
      
      const orderIndex = this.orders.findIndex(o => o.id === this.selectedOrder.id);
      if (orderIndex !== -1) {
        this.$set(this.orders, orderIndex, this.selectedOrder);
      }
      
      this.saveOrders();
      this.$forceUpdate();
    },
    
    deleteOrder(orderId) {
      this.$confirm('确定要删除此订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.orders = this.orders.filter(o => o.id !== orderId);
        this.saveOrders();
        this.$message({
          message: '订单已删除',
          type: 'success'
        });
      }).catch(() => {});
    },
    
    refreshOrders() {
      this.loadOrders();
      this.$message({
        message: '订单列表已刷新',
        type: 'success'
      });
    },
    
    formatDateTime(date) {
      const pad = n => n.toString().padStart(2, '0');
      return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
    }
  }
});
