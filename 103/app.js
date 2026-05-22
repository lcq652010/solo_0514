Vue.use(ElementUI);

const mockBooks = [
    { id: 1, isbn: '9787111544937', name: 'JavaScript高级程序设计', author: 'Nicholas C. Zakas', publisher: '机械工业出版社', category: '编程', stock: 5, available: 3, price: 129 },
    { id: 2, isbn: '9787115275790', name: '深入理解计算机系统', author: 'Randal E. Bryant', publisher: '机械工业出版社', category: '计算机', stock: 3, available: 2, price: 139 },
    { id: 3, isbn: '9787111544968', name: '算法导论', author: 'Thomas H. Cormen', publisher: '机械工业出版社', category: '算法', stock: 4, available: 4, price: 128 },
    { id: 4, isbn: '9787111504949', name: '设计模式', author: 'Erich Gamma', publisher: '机械工业出版社', category: '编程', stock: 3, available: 1, price: 89 },
    { id: 5, isbn: '9787115378545', name: '数据结构与算法分析', author: 'Mark Allen Weiss', publisher: '人民邮电出版社', category: '算法', stock: 6, available: 5, price: 79 },
    { id: 6, isbn: '9787302423287', name: '计算机网络', author: 'Andrew S. Tanenbaum', publisher: '清华大学出版社', category: '网络', stock: 4, available: 3, price: 99 },
    { id: 7, isbn: '9787111579546', name: '现代操作系统', author: 'Andrew S. Tanenbaum', publisher: '机械工业出版社', category: '操作系统', stock: 3, available: 2, price: 109 },
    { id: 8, isbn: '9787115428124', name: 'Python编程从入门到实践', author: 'Eric Matthes', publisher: '人民邮电出版社', category: '编程', stock: 8, available: 6, price: 89 }
];

const BORROW_LIMIT = 5;
const OVERDUE_RATE = 0.5;

const mockReaders = [
    { id: 1, name: '张三', phone: '13800138001', cardNo: 'C2024001' },
    { id: 2, name: '李四', phone: '13800138002', cardNo: 'C2024002' },
    { id: 3, name: '王五', phone: '13800138003', cardNo: 'C2024003' },
    { id: 4, name: '赵六', phone: '13800138004', cardNo: 'C2024004' },
    { id: 5, name: '钱七', phone: '13800138005', cardNo: 'C2024005' }
];

const mockFees = [
    { id: 1, recordId: 2, readerName: '李四', bookName: '深入理解计算机系统', borrowDate: '2024-04-20', dueDate: '2024-05-05', returnDate: null, overdueDays: 11, dailyRate: 0.5, amount: 5.50, status: 'unpaid' },
    { id: 2, recordId: 5, readerName: '钱七', bookName: '数据结构与算法分析', borrowDate: '2024-04-10', dueDate: '2024-04-25', returnDate: '2024-05-01', overdueDays: 6, dailyRate: 0.5, amount: 3.00, status: 'paid' }
];

const mockRecords = [
    { id: 1, bookId: 1, bookName: 'JavaScript高级程序设计', category: '编程', readerId: 1, readerName: '张三', borrowDate: '2024-05-01', dueDate: '2024-05-15', returnDate: null, status: 'borrowed', overdueDays: 0 },
    { id: 2, bookId: 2, bookName: '深入理解计算机系统', category: '计算机', readerId: 2, readerName: '李四', borrowDate: '2024-04-20', dueDate: '2024-05-05', returnDate: null, status: 'overdue', overdueDays: 11 },
    { id: 3, bookId: 3, bookName: '算法导论', category: '算法', readerId: 3, readerName: '王五', borrowDate: '2024-04-15', dueDate: '2024-04-30', returnDate: '2024-04-28', status: 'returned', overdueDays: 0 },
    { id: 4, bookId: 4, bookName: '设计模式', category: '编程', readerId: 4, readerName: '赵六', borrowDate: '2024-05-05', dueDate: '2024-05-20', returnDate: null, status: 'borrowed', overdueDays: 0 },
    { id: 5, bookId: 5, bookName: '数据结构与算法分析', category: '算法', readerId: 5, readerName: '钱七', borrowDate: '2024-04-10', dueDate: '2024-04-25', returnDate: '2024-05-01', status: 'returned', overdueDays: 6 },
    { id: 6, bookId: 6, bookName: '计算机网络', category: '网络', readerId: 1, readerName: '张三', borrowDate: '2024-04-25', dueDate: '2024-05-10', returnDate: null, status: 'overdue', overdueDays: 6 },
    { id: 7, bookId: 7, bookName: '现代操作系统', category: '操作系统', readerId: 2, readerName: '李四', borrowDate: '2024-05-10', dueDate: '2024-05-25', returnDate: null, status: 'borrowed', overdueDays: 0 },
    { id: 8, bookId: 8, bookName: 'Python编程从入门到实践', category: '编程', readerId: 3, readerName: '王五', borrowDate: '2024-05-08', dueDate: '2024-05-23', returnDate: null, status: 'borrowed', overdueDays: 0 }
];

const BookList = {
    template: `
        <div>
            <div class="page-header">
                <div class="page-title">📖 图书列表</div>
                <p>查看和管理所有图书信息</p>
            </div>
            <div class="page-content">
                <div class="search-bar">
                    <el-form :inline="true" :model="searchForm">
                        <el-form-item label="图书名称">
                            <el-input v-model="searchForm.name" placeholder="请输入图书名称" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="ISBN">
                            <el-input v-model="searchForm.isbn" placeholder="请输入ISBN" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="分类">
                            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
                                <el-option label="编程" value="编程"></el-option>
                                <el-option label="计算机" value="计算机"></el-option>
                                <el-option label="算法" value="算法"></el-option>
                                <el-option label="网络" value="网络"></el-option>
                                <el-option label="操作系统" value="操作系统"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleSearch">搜索</el-button>
                            <el-button @click="handleReset">重置</el-button>
                        </el-form-item>
                    </el-form>
                </div>

                <el-table :data="filteredBooks" border stripe style="width: 100%">
                    <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
                    <el-table-column prop="isbn" label="ISBN" width="150"></el-table-column>
                    <el-table-column prop="name" label="图书名称" min-width="200"></el-table-column>
                    <el-table-column prop="author" label="作者" width="150"></el-table-column>
                    <el-table-column prop="publisher" label="出版社" width="150"></el-table-column>
                    <el-table-column prop="category" label="分类" width="100" align="center"></el-table-column>
                    <el-table-column prop="price" label="定价(元)" width="100" align="center"></el-table-column>
                    <el-table-column prop="stock" label="总库存" width="100" align="center"></el-table-column>
                    <el-table-column prop="available" label="可借数量" width="100" align="center">
                        <template slot-scope="scope">
                            <span :class="['status-badge', scope.row.available > 0 ? 'status-available' : 'status-borrowed']">
                                {{ scope.row.available }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="120" align="center">
                        <template slot-scope="scope">
                            <el-button type="text" size="small" @click="handleBorrow(scope.row)" :disabled="scope.row.available <= 0">
                                借阅
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>

                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[10, 20, 50, 100]"
                    :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="filteredBooks.length"
                    style="margin-top: 20px; text-align: right;">
                </el-pagination>
            </div>
        </div>
    `,
    data() {
        return {
            searchForm: {
                name: '',
                isbn: '',
                category: ''
            },
            books: [],
            currentPage: 1,
            pageSize: 10
        };
    },
    computed: {
        filteredBooks() {
            let result = [...this.books];
            if (this.searchForm.name) {
                result = result.filter(book => book.name.includes(this.searchForm.name));
            }
            if (this.searchForm.isbn) {
                result = result.filter(book => book.isbn.includes(this.searchForm.isbn));
            }
            if (this.searchForm.category) {
                result = result.filter(book => book.category === this.searchForm.category);
            }
            return result;
        }
    },
    created() {
        this.books = [...mockBooks];
    },
    methods: {
        handleSearch() {
            this.currentPage = 1;
            this.$message.success('搜索完成');
        },
        handleReset() {
            this.searchForm = { name: '', isbn: '', category: '' };
            this.currentPage = 1;
        },
        handleBorrow(book) {
            this.$emit('navigate', '2', book);
        },
        handleSizeChange(val) {
            this.pageSize = val;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        }
    }
};

const BorrowForm = {
    template: `
        <div>
            <div class="page-header">
                <div class="page-title">📝 读者借阅</div>
                <p>为读者办理图书借阅手续</p>
            </div>
            <div class="page-content">
                <div class="form-container">
                    <el-form :model="borrowForm" :rules="rules" ref="borrowForm" label-width="120px">
                        <el-form-item label="读者信息" prop="readerId">
                            <el-select v-model="borrowForm.readerId" placeholder="请选择读者" style="width: 100%" filterable>
                                <el-option 
                                    v-for="reader in readers" 
                                    :key="reader.id" 
                                    :label="reader.name + ' - ' + reader.cardNo" 
                                    :value="reader.id">
                                </el-option>
                            </el-select>
                            <div v-if="borrowForm.readerId" :style="{marginTop: '8px', fontSize: '12px', color: remainingBorrows > 0 ? '#67c23a' : '#f56c6c'}">
                                当前已借阅 {{ readerBorrowCount }} 本，还可借阅 {{ remainingBorrows }} 本（上限 {{ BORROW_LIMIT }} 本）
                            </div>
                        </el-form-item>

                        <el-form-item label="选择图书" prop="bookId">
                            <el-select v-model="borrowForm.bookId" placeholder="请选择图书" style="width: 100%" filterable>
                                <el-option 
                                    v-for="book in availableBooks" 
                                    :key="book.id" 
                                    :label="book.name + ' (可借: ' + book.available + ')'" 
                                    :value="book.id">
                                </el-option>
                            </el-select>
                        </el-form-item>

                        <el-form-item label="借阅日期" prop="borrowDate">
                            <el-date-picker
                                v-model="borrowForm.borrowDate"
                                type="date"
                                placeholder="选择借阅日期"
                                style="width: 100%"
                                value-format="yyyy-MM-dd">
                            </el-date-picker>
                        </el-form-item>

                        <el-form-item label="借阅天数" prop="borrowDays">
                            <el-input-number v-model="borrowForm.borrowDays" :min="1" :max="60" style="width: 100%"></el-input-number>
                            <div style="color: #909399; font-size: 12px; margin-top: 5px;">
                                预计归还日期: {{ dueDate }}
                            </div>
                        </el-form-item>

                        <el-form-item label="备注">
                            <el-input type="textarea" v-model="borrowForm.remark" :rows="3" placeholder="请输入备注信息"></el-input>
                        </el-form-item>

                        <el-form-item>
                            <el-button type="primary" @click="submitForm" size="large">确认借阅</el-button>
                            <el-button @click="resetForm" size="large">重置</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </div>
    `,
    props: ['selectedBook'],
    data() {
        return {
            readers: [],
            books: [],
            BORROW_LIMIT: BORROW_LIMIT,
            borrowForm: {
                readerId: '',
                bookId: '',
                borrowDate: '',
                borrowDays: 15,
                remark: ''
            },
            rules: {
                readerId: [
                    { required: true, message: '请选择读者', trigger: 'change' }
                ],
                bookId: [
                    { required: true, message: '请选择图书', trigger: 'change' }
                ],
                borrowDate: [
                    { required: true, message: '请选择借阅日期', trigger: 'change' }
                ],
                borrowDays: [
                    { required: true, message: '请输入借阅天数', trigger: 'blur' },
                    { type: 'number', min: 1, max: 60, message: '借阅天数应在1-60天之间', trigger: 'blur' }
                ]
            }
        };
    },
    computed: {
        availableBooks() {
            return this.books.filter(book => book.available > 0);
        },
        dueDate() {
            if (!this.borrowForm.borrowDate) return '-';
            const date = new Date(this.borrowForm.borrowDate);
            date.setDate(date.getDate() + this.borrowForm.borrowDays);
            return date.toISOString().split('T')[0];
        },
        readerBorrowCount() {
            if (!this.borrowForm.readerId) return 0;
            return mockRecords.filter(r => 
                r.readerId === this.borrowForm.readerId && r.status !== 'returned'
            ).length;
        },
        remainingBorrows() {
            return BORROW_LIMIT - this.readerBorrowCount;
        }
    },
    created() {
        this.readers = [...mockReaders];
        this.books = [...mockBooks];
        const today = new Date();
        this.borrowForm.borrowDate = today.toISOString().split('T')[0];
    },
    watch: {
        selectedBook: {
            handler(val) {
                if (val) {
                    this.borrowForm.bookId = val.id;
                }
            },
            immediate: true
        }
    },
    methods: {
        submitForm() {
            this.$refs.borrowForm.validate((valid) => {
                if (valid) {
                    if (this.remainingBorrows <= 0) {
                        this.$message.error(`借阅失败！该读者已达到借阅上限（${BORROW_LIMIT}本），请先归还部分图书。`);
                        return false;
                    }
                    const book = this.books.find(b => b.id === this.borrowForm.bookId);
                    const reader = this.readers.find(r => r.id === this.borrowForm.readerId);
                    const newRecord = {
                        id: mockRecords.length + 1,
                        bookId: this.borrowForm.bookId,
                        bookName: book.name,
                        category: book.category,
                        readerId: this.borrowForm.readerId,
                        readerName: reader.name,
                        borrowDate: this.borrowForm.borrowDate,
                        dueDate: this.dueDate,
                        returnDate: null,
                        status: 'borrowed',
                        overdueDays: 0
                    };
                    mockRecords.unshift(newRecord);
                    book.available--;
                    this.$message.success(`借阅成功！该读者当前已借阅 ${this.readerBorrowCount + 1} 本，还可借阅 ${this.remainingBorrows - 1} 本。`);
                    this.resetForm();
                } else {
                    this.$message.error('请填写完整信息');
                    return false;
                }
            });
        },
        resetForm() {
            this.$refs.borrowForm.resetFields();
            const today = new Date();
            this.borrowForm.borrowDate = today.toISOString().split('T')[0];
            this.borrowForm.borrowDays = 15;
        }
    }
};

const BorrowRecord = {
    template: `
        <div>
            <div class="page-header">
                <div class="page-title">📋 借阅记录</div>
                <p>查看所有借阅记录和状态</p>
            </div>
            <div class="page-content">
                <div class="search-bar">
                    <el-form :inline="true" :model="searchForm">
                        <el-form-item label="读者姓名">
                            <el-input v-model="searchForm.readerName" placeholder="请输入读者姓名" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="图书名称">
                            <el-input v-model="searchForm.bookName" placeholder="请输入图书名称" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="图书分类">
                            <el-select v-model="searchForm.category" placeholder="请选择分类" clearable>
                                <el-option label="编程" value="编程"></el-option>
                                <el-option label="计算机" value="计算机"></el-option>
                                <el-option label="算法" value="算法"></el-option>
                                <el-option label="网络" value="网络"></el-option>
                                <el-option label="操作系统" value="操作系统"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item label="借阅日期">
                            <el-date-picker
                                v-model="searchForm.borrowDateRange"
                                type="daterange"
                                range-separator="至"
                                start-placeholder="开始日期"
                                end-placeholder="结束日期"
                                value-format="yyyy-MM-dd">
                            </el-date-picker>
                        </el-form-item>
                        <el-form-item label="借阅状态">
                            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
                                <el-option label="借阅中" value="borrowed"></el-option>
                                <el-option label="已逾期" value="overdue"></el-option>
                                <el-option label="已归还" value="returned"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleSearch">搜索</el-button>
                            <el-button @click="handleReset">重置</el-button>
                        </el-form-item>
                    </el-form>
                </div>

                <el-table :data="paginatedRecords" border stripe style="width: 100%">
                    <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
                    <el-table-column prop="readerName" label="读者姓名" width="120"></el-table-column>
                    <el-table-column prop="bookName" label="图书名称" min-width="200"></el-table-column>
                    <el-table-column prop="category" label="分类" width="100" align="center"></el-table-column>
                    <el-table-column prop="borrowDate" label="借阅日期" width="120" align="center"></el-table-column>
                    <el-table-column prop="dueDate" label="应还日期" width="120" align="center"></el-table-column>
                    <el-table-column prop="returnDate" label="归还日期" width="120" align="center">
                        <template slot-scope="scope">
                            {{ scope.row.returnDate || '-' }}
                        </template>
                    </el-table-column>
                    <el-table-column prop="overdueDays" label="逾期天数" width="100" align="center">
                        <template slot-scope="scope">
                            <span v-if="scope.row.overdueDays > 0" style="color: #f56c6c; font-weight: bold;">
                                {{ scope.row.overdueDays }}天
                            </span>
                            <span v-else>-</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="状态" width="100" align="center">
                        <template slot-scope="scope">
                            <span :class="getStatusClass(scope.row.status)">
                                {{ getStatusText(scope.row.status) }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="120" align="center">
                        <template slot-scope="scope">
                            <el-button 
                                type="text" 
                                size="small" 
                                @click="handleReturn(scope.row)" 
                                :disabled="scope.row.status === 'returned'">
                                归还
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>

                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[5, 10, 20, 50]"
                    :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="filteredRecords.length"
                    style="margin-top: 20px; text-align: right;">
                </el-pagination>
            </div>
        </div>
    `,
    data() {
        return {
            searchForm: {
                readerName: '',
                bookName: '',
                category: '',
                borrowDateRange: [],
                status: ''
            },
            records: [],
            currentPage: 1,
            pageSize: 5
        };
    },
    computed: {
        filteredRecords() {
            let result = [...this.records];
            if (this.searchForm.readerName) {
                result = result.filter(r => r.readerName.includes(this.searchForm.readerName));
            }
            if (this.searchForm.bookName) {
                result = result.filter(r => r.bookName.includes(this.searchForm.bookName));
            }
            if (this.searchForm.category) {
                result = result.filter(r => r.category === this.searchForm.category);
            }
            if (this.searchForm.borrowDateRange && this.searchForm.borrowDateRange.length === 2) {
                const startDate = this.searchForm.borrowDateRange[0];
                const endDate = this.searchForm.borrowDateRange[1];
                result = result.filter(r => r.borrowDate >= startDate && r.borrowDate <= endDate);
            }
            if (this.searchForm.status) {
                result = result.filter(r => r.status === this.searchForm.status);
            }
            return result;
        },
        paginatedRecords() {
            const start = (this.currentPage - 1) * this.pageSize;
            const end = start + this.pageSize;
            return this.filteredRecords.slice(start, end);
        }
    },
    created() {
        this.records = mockRecords;
    },
    methods: {
        getStatusClass(status) {
            const map = {
                borrowed: 'status-badge status-borrowed',
                overdue: 'status-badge status-overdue',
                returned: 'status-badge status-returned'
            };
            return map[status] || '';
        },
        getStatusText(status) {
            const map = {
                borrowed: '借阅中',
                overdue: '已逾期',
                returned: '已归还'
            };
            return map[status] || status;
        },
        handleSearch() {
            this.currentPage = 1;
            this.$message.success('搜索完成，共 ' + this.filteredRecords.length + ' 条记录');
        },
        handleReset() {
            this.searchForm = { readerName: '', bookName: '', category: '', borrowDateRange: [], status: '' };
            this.currentPage = 1;
        },
        handleReturn(record) {
            this.$emit('navigate', '4', record);
        },
        handleSizeChange(val) {
            this.pageSize = val;
            this.currentPage = 1;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        }
    }
};

const ReturnForm = {
    template: `
        <div>
            <div class="page-header">
                <div class="page-title">↩️ 图书归还</div>
                <p>办理图书归还手续</p>
            </div>
            <div class="page-content">
                <div class="form-container">
                    <el-form :model="returnForm" :rules="rules" ref="returnForm" label-width="120px">
                        <el-form-item label="选择借阅记录" prop="recordId">
                            <el-select v-model="returnForm.recordId" placeholder="请选择借阅记录" style="width: 100%" filterable @change="onRecordChange">
                                <el-option 
                                    v-for="record in unreturnedRecords" 
                                    :key="record.id" 
                                    :label="record.readerName + ' - ' + record.bookName" 
                                    :value="record.id">
                                </el-option>
                            </el-select>
                        </el-form-item>

                        <div v-if="selectedRecord" style="background: #f9fafc; padding: 20px; border-radius: 4px; margin-bottom: 20px;">
                            <h4 style="margin-bottom: 15px; color: #303133;">借阅详情</h4>
                            <el-descriptions :column="2" border>
                                <el-descriptions-item label="读者">{{ selectedRecord.readerName }}</el-descriptions-item>
                                <el-descriptions-item label="图书">{{ selectedRecord.bookName }}</el-descriptions-item>
                                <el-descriptions-item label="借阅日期">{{ selectedRecord.borrowDate }}</el-descriptions-item>
                                <el-descriptions-item label="应还日期">{{ selectedRecord.dueDate }}</el-descriptions-item>
                                <el-descriptions-item label="逾期天数" :span="2">
                                    <span :style="{color: actualOverdueDays > 0 ? '#f56c6c' : '#67c23a'}">
                                        {{ actualOverdueDays > 0 ? actualOverdueDays + '天' : '未逾期' }}
                                    </span>
                                </el-descriptions-item>
                            </el-descriptions>
                        </div>

                        <el-form-item label="归还日期" prop="returnDate">
                            <el-date-picker
                                v-model="returnForm.returnDate"
                                type="date"
                                placeholder="选择归还日期"
                                style="width: 100%"
                                value-format="yyyy-MM-dd"
                                @change="onReturnDateChange">
                            </el-date-picker>
                        </el-form-item>

                        <el-form-item v-if="calculatedFee > 0" label="逾期费用">
                            <el-input v-model="returnForm.overdueFee" disabled style="width: 100%">
                                <template slot="append">元</template>
                            </el-input>
                            <div style="color: #f56c6c; font-size: 12px; margin-top: 5px;">
                                逾期 {{ actualOverdueDays }} 天 × {{ OVERDUE_RATE }}元/天 = {{ calculatedFee }}元
                            </div>
                        </el-form-item>

                        <el-form-item label="备注">
                            <el-input type="textarea" v-model="returnForm.remark" :rows="3" placeholder="请输入备注信息"></el-input>
                        </el-form-item>

                        <el-form-item>
                            <el-button type="primary" @click="submitForm" size="large">确认归还</el-button>
                            <el-button @click="resetForm" size="large">重置</el-button>
                        </el-form-item>
                    </el-form>
                </div>
            </div>
        </div>
    `,
    props: ['selectedRecordFromList'],
    data() {
        return {
            records: [],
            books: [],
            returnForm: {
                recordId: '',
                returnDate: '',
                overdueFee: '0.00',
                remark: ''
            },
            rules: {
                recordId: [
                    { required: true, message: '请选择借阅记录', trigger: 'change' }
                ],
                returnDate: [
                    { required: true, message: '请选择归还日期', trigger: 'change' }
                ]
            },
            selectedRecord: null,
            OVERDUE_RATE: OVERDUE_RATE
        };
    },
    computed: {
        unreturnedRecords() {
            return this.records.filter(r => r.status !== 'returned');
        },
        actualOverdueDays() {
            if (!this.selectedRecord || !this.returnForm.returnDate) return 0;
            const returnDate = new Date(this.returnForm.returnDate);
            const dueDate = new Date(this.selectedRecord.dueDate);
            const diff = Math.floor((returnDate - dueDate) / (1000 * 60 * 60 * 24));
            return Math.max(0, diff);
        },
        calculatedFee() {
            return (this.actualOverdueDays * OVERDUE_RATE).toFixed(2);
        }
    },
    created() {
        this.records = mockRecords;
        this.books = mockBooks;
        const today = new Date();
        this.returnForm.returnDate = today.toISOString().split('T')[0];
    },
    watch: {
        selectedRecordFromList: {
            handler(val) {
                if (val && val.status !== 'returned') {
                    this.returnForm.recordId = val.id;
                    this.selectedRecord = val;
                    this.calculateFee();
                }
            },
            immediate: true
        },
        calculatedFee: {
            handler(newVal) {
                this.returnForm.overdueFee = newVal;
            }
        }
    },
    methods: {
        onRecordChange(id) {
            this.selectedRecord = this.records.find(r => r.id === id);
            this.calculateFee();
        },
        onReturnDateChange() {
            this.calculateFee();
        },
        calculateFee() {
            if (this.selectedRecord && this.returnForm.returnDate) {
                this.returnForm.overdueFee = this.calculatedFee;
            }
        },
        submitForm() {
            this.$refs.returnForm.validate((valid) => {
                if (valid) {
                    const recordIndex = this.records.findIndex(r => r.id === this.returnForm.recordId);
                    const record = this.records[recordIndex];
                    
                    mockRecords[recordIndex].returnDate = this.returnForm.returnDate;
                    mockRecords[recordIndex].status = 'returned';
                    mockRecords[recordIndex].overdueDays = this.actualOverdueDays;
                    
                    const bookIndex = this.books.findIndex(b => b.name === record.bookName);
                    if (bookIndex !== -1) {
                        mockBooks[bookIndex].available++;
                    }
                    
                    if (this.actualOverdueDays > 0) {
                        const existingFee = mockFees.find(f => f.recordId === record.id);
                        if (!existingFee) {
                            const newFee = {
                                id: mockFees.length + 1,
                                recordId: record.id,
                                readerName: record.readerName,
                                bookName: record.bookName,
                                borrowDate: record.borrowDate,
                                dueDate: record.dueDate,
                                returnDate: record.returnDate,
                                overdueDays: this.actualOverdueDays,
                                dailyRate: OVERDUE_RATE,
                                amount: parseFloat(this.calculatedFee),
                                status: 'unpaid'
                            };
                            mockFees.unshift(newFee);
                        }
                        this.$message({
                            type: 'warning',
                            message: `归还成功！逾期 ${this.actualOverdueDays} 天，产生逾期费用 ${this.calculatedFee} 元，请在逾期费用页面支付。`,
                            duration: 5000
                        });
                    } else {
                        this.$message.success('归还成功！未产生逾期费用。');
                    }
                    this.resetForm();
                } else {
                    this.$message.error('请填写完整信息');
                    return false;
                }
            });
        },
        resetForm() {
            this.$refs.returnForm.resetFields();
            const today = new Date();
            this.returnForm.returnDate = today.toISOString().split('T')[0];
            this.returnForm.overdueFee = '0.00';
            this.selectedRecord = null;
        }
    }
};

const OverdueFee = {
    template: `
        <div>
            <div class="page-header">
                <div class="page-title">💰 逾期费用计算</div>
                <p>查询和计算逾期费用</p>
            </div>
            <div class="page-content">
                <div class="search-bar">
                    <el-form :inline="true" :model="searchForm">
                        <el-form-item label="读者姓名">
                            <el-input v-model="searchForm.readerName" placeholder="请输入读者姓名" clearable></el-input>
                        </el-form-item>
                        <el-form-item label="借阅状态">
                            <el-select v-model="searchForm.status" placeholder="请选择状态" clearable>
                                <el-option label="未支付" value="unpaid"></el-option>
                                <el-option label="已支付" value="paid"></el-option>
                            </el-select>
                        </el-form-item>
                        <el-form-item>
                            <el-button type="primary" @click="handleSearch">搜索</el-button>
                            <el-button @click="handleReset">重置</el-button>
                        </el-form-item>
                    </el-form>
                </div>

                <el-row :gutter="20" style="margin-bottom: 20px;">
                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div slot="header" style="color: #909399;">逾期总金额</div>
                            <div style="font-size: 32px; font-weight: bold; color: #f56c6c;">{{ totalFee }} 元</div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div slot="header" style="color: #909399;">未支付金额</div>
                            <div style="font-size: 32px; font-weight: bold; color: #e6a23c;">{{ unpaidFee }} 元</div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div slot="header" style="color: #909399;">逾期记录数</div>
                            <div style="font-size: 32px; font-weight: bold; color: #409eff;">{{ overdueCount }} 条</div>
                        </el-card>
                    </el-col>
                    <el-col :span="6">
                        <el-card shadow="hover">
                            <div slot="header" style="color: #909399;">涉及读者</div>
                            <div style="font-size: 32px; font-weight: bold; color: #67c23a;">{{ readerCount }} 人</div>
                        </el-card>
                    </el-col>
                </el-row>

                <el-table :data="filteredFees" border stripe style="width: 100%">
                    <el-table-column prop="id" label="ID" width="80" align="center"></el-table-column>
                    <el-table-column prop="readerName" label="读者姓名" width="120"></el-table-column>
                    <el-table-column prop="bookName" label="图书名称" min-width="200"></el-table-column>
                    <el-table-column prop="borrowDate" label="借阅日期" width="120" align="center"></el-table-column>
                    <el-table-column prop="dueDate" label="应还日期" width="120" align="center"></el-table-column>
                    <el-table-column prop="returnDate" label="归还日期" width="120" align="center">
                        <template slot-scope="scope">
                            {{ scope.row.returnDate || '-' }}
                        </template>
                    </el-table-column>
                    <el-table-column prop="overdueDays" label="逾期天数" width="100" align="center">
                        <template slot-scope="scope">
                            <span style="color: #f56c6c; font-weight: bold;">{{ scope.row.overdueDays }}天</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="dailyRate" label="日费率" width="100" align="center">
                        <template slot-scope="scope">
                            {{ scope.row.dailyRate }}元/天
                        </template>
                    </el-table-column>
                    <el-table-column prop="amount" label="费用金额" width="120" align="center">
                        <template slot-scope="scope">
                            <span style="color: #f56c6c; font-weight: bold; font-size: 16px;">
                                {{ (scope.row.amount).toFixed(2) }}元
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="status" label="支付状态" width="100" align="center">
                        <template slot-scope="scope">
                            <span :class="scope.row.status === 'paid' ? 'status-badge status-returned' : 'status-badge status-overdue'">
                                {{ scope.row.status === 'paid' ? '已支付' : '未支付' }}
                            </span>
                        </template>
                    </el-table-column>
                    <el-table-column label="操作" width="120" align="center">
                        <template slot-scope="scope">
                            <el-button 
                                type="text" 
                                size="small" 
                                @click="handlePay(scope.row)" 
                                :disabled="scope.row.status === 'paid'"
                                style="color: #67c23a;">
                                标记支付
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>

                <el-pagination
                    @size-change="handleSizeChange"
                    @current-change="handleCurrentChange"
                    :current-page="currentPage"
                    :page-sizes="[10, 20, 50, 100]"
                    :page-size="pageSize"
                    layout="total, sizes, prev, pager, next, jumper"
                    :total="filteredFees.length"
                    style="margin-top: 20px; text-align: right;">
                </el-pagination>
            </div>
        </div>
    `,
    data() {
        return {
            searchForm: {
                readerName: '',
                status: ''
            },
            fees: [],
            currentPage: 1,
            pageSize: 10
        };
    },
    computed: {
        filteredFees() {
            let result = [...this.fees];
            if (this.searchForm.readerName) {
                result = result.filter(f => f.readerName.includes(this.searchForm.readerName));
            }
            if (this.searchForm.status) {
                result = result.filter(f => f.status === this.searchForm.status);
            }
            return result;
        },
        totalFee() {
            return this.fees.reduce((sum, f) => sum + parseFloat(f.amount), 0).toFixed(2);
        },
        unpaidFee() {
            return this.fees.filter(f => f.status === 'unpaid').reduce((sum, f) => sum + parseFloat(f.amount), 0).toFixed(2);
        },
        overdueCount() {
            return this.fees.length;
        },
        readerCount() {
            return new Set(this.fees.map(f => f.readerName)).size;
        }
    },
    created() {
        this.fees = mockFees;
    },
    methods: {
        refreshFees() {
            this.fees = [...mockFees];
        },
        handleSearch() {
            this.currentPage = 1;
            this.$message.success('搜索完成');
        },
        handleReset() {
            this.searchForm = { readerName: '', status: '' };
            this.currentPage = 1;
        },
        handlePay(fee) {
            this.$confirm('确认标记该费用为已支付吗?', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning'
            }).then(() => {
                fee.status = 'paid';
                this.$message.success('支付成功！');
            }).catch(() => {});
        },
        handleSizeChange(val) {
            this.pageSize = val;
        },
        handleCurrentChange(val) {
            this.currentPage = val;
        }
    }
};

const app = new Vue({
    el: '#app',
    data: {
        currentPage: 'BookList',
        activeIndex: '1',
        selectedBook: null,
        selectedRecord: null,
        refreshKey: 0
    },
    components: {
        BookList,
        BorrowForm,
        BorrowRecord,
        ReturnForm,
        OverdueFee
    },
    methods: {
        handleMenuSelect(index) {
            this.activeIndex = index;
            this.selectedBook = null;
            this.selectedRecord = null;
            this.refreshKey++;
            const pageMap = {
                '1': 'BookList',
                '2': 'BorrowForm',
                '3': 'BorrowRecord',
                '4': 'ReturnForm',
                '5': 'OverdueFee'
            };
            this.currentPage = pageMap[index];
        },
        handleNavigate(index, data) {
            if (index === '2') {
                this.selectedBook = data;
            } else if (index === '4') {
                this.selectedRecord = data;
            }
            this.handleMenuSelect(index);
        }
    }
});
