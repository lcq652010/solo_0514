export const bookList = [
  { id: 1, isbn: '9787111544937', name: 'JavaScript高级程序设计', author: '马特·弗里斯比', publisher: '机械工业出版社', category: '编程语言', stock: 15, price: 129.00, publishDate: '2020-10-01' },
  { id: 2, isbn: '9787115428028', name: 'Python编程：从入门到实践', author: '埃里克·马瑟斯', publisher: '人民邮电出版社', category: '编程语言', stock: 8, price: 89.00, publishDate: '2016-07-01' },
  { id: 3, isbn: '9787111213826', name: '深入理解计算机系统', author: '兰德尔·布莱恩特', publisher: '机械工业出版社', category: '计算机基础', stock: 6, price: 139.00, publishDate: '2016-11-01' },
  { id: 4, isbn: '9787121302978', name: '算法导论', author: '托马斯·科尔曼', publisher: '电子工业出版社', category: '算法', stock: 10, price: 128.00, publishDate: '2013-01-01' },
  { id: 5, isbn: '9787111398124', name: '设计模式：可复用面向对象软件的基础', author: '埃里克·伽玛', publisher: '机械工业出版社', category: '软件工程', stock: 5, price: 59.00, publishDate: '2017-09-01' },
  { id: 6, isbn: '9787564126094', name: '数据结构与算法分析', author: '马克·艾伦·维斯', publisher: '机械工业出版社', category: '算法', stock: 12, price: 79.00, publishDate: '2019-03-01' },
  { id: 7, isbn: '9787111606567', name: '代码整洁之道', author: '罗伯特·马丁', publisher: '机械工业出版社', category: '软件工程', stock: 9, price: 69.00, publishDate: '2018-01-01' },
  { id: 8, isbn: '9787115505194', name: 'Vue.js设计与实现', author: '霍春阳', publisher: '人民邮电出版社', category: '前端开发', stock: 20, price: 99.00, publishDate: '2022-04-01' },
  { id: 9, isbn: '9787115411099', name: 'React设计模式与最佳实践', author: '米凯莱·贝尔托利', publisher: '人民邮电出版社', category: '前端开发', stock: 0, price: 79.00, publishDate: '2018-05-01' }
];

export const borrowRecords = [
  { id: 1, bookId: 1, bookName: 'JavaScript高级程序设计', borrower: '张三', borrowerNo: 'ST001', borrowDate: '2024-05-01', dueDate: '2024-06-01', returnDate: null, status: 'borrowed' },
  { id: 2, bookId: 2, bookName: 'Python编程：从入门到实践', borrower: '李四', borrowerNo: 'ST002', borrowDate: '2024-04-15', dueDate: '2024-05-15', returnDate: '2024-05-10', status: 'returned' },
  { id: 3, bookId: 3, bookName: '深入理解计算机系统', borrower: '王五', borrowerNo: 'ST003', borrowDate: '2024-04-20', dueDate: '2024-05-20', returnDate: null, status: 'overdue' },
  { id: 4, bookId: 4, bookName: '算法导论', borrower: '赵六', borrowerNo: 'ST004', borrowDate: '2024-05-10', dueDate: '2024-06-10', returnDate: null, status: 'borrowed' },
  { id: 5, bookId: 5, bookName: '设计模式：可复用面向对象软件的基础', borrower: '钱七', borrowerNo: 'ST005', borrowDate: '2024-03-01', dueDate: '2024-04-01', returnDate: null, status: 'overdue' },
  { id: 6, bookId: 6, bookName: '数据结构与算法分析', borrower: '孙八', borrowerNo: 'ST006', borrowDate: '2024-05-05', dueDate: '2024-06-05', returnDate: '2024-05-20', status: 'returned' },
  { id: 7, bookId: 7, bookName: '代码整洁之道', borrower: '周九', borrowerNo: 'ST007', borrowDate: '2024-04-01', dueDate: '2024-05-01', returnDate: null, status: 'overdue' },
  { id: 8, bookId: 8, bookName: 'Vue.js设计与实现', borrower: '吴十', borrowerNo: 'ST008', borrowDate: '2024-05-15', dueDate: '2024-06-15', returnDate: null, status: 'borrowed' },
  { id: 9, bookId: 1, bookName: 'JavaScript高级程序设计', borrower: '郑十一', borrowerNo: 'ST009', borrowDate: '2024-03-10', dueDate: '2024-04-10', returnDate: '2024-04-05', status: 'returned' },
  { id: 10, bookId: 2, bookName: 'Python编程：从入门到实践', borrower: '王十二', borrowerNo: 'ST010', borrowDate: '2024-05-02', dueDate: '2024-06-02', returnDate: null, status: 'borrowed' },
  { id: 11, bookId: 3, bookName: '深入理解计算机系统', borrower: '刘十三', borrowerNo: 'ST011', borrowDate: '2024-02-15', dueDate: '2024-03-15', returnDate: null, status: 'overdue' },
  { id: 12, bookId: 4, bookName: '算法导论', borrower: '陈十四', borrowerNo: 'ST012', borrowDate: '2024-04-25', dueDate: '2024-05-25', returnDate: '2024-05-18', status: 'returned' },
  { id: 13, bookId: 5, bookName: '设计模式：可复用面向对象软件的基础', borrower: '杨十五', borrowerNo: 'ST013', borrowDate: '2024-05-08', dueDate: '2024-06-08', returnDate: null, status: 'borrowed' },
  { id: 14, bookId: 6, bookName: '数据结构与算法分析', borrower: '黄十六', borrowerNo: 'ST014', borrowDate: '2024-01-20', dueDate: '2024-02-20', returnDate: null, status: 'overdue' },
  { id: 15, bookId: 7, bookName: '代码整洁之道', borrower: '赵十七', borrowerNo: 'ST015', borrowDate: '2024-05-12', dueDate: '2024-06-12', returnDate: null, status: 'borrowed' },
  { id: 16, bookId: 8, bookName: 'Vue.js设计与实现', borrower: '周十八', borrowerNo: 'ST016', borrowDate: '2024-04-18', dueDate: '2024-05-18', returnDate: '2024-05-15', status: 'returned' },
  { id: 17, bookId: 1, bookName: 'JavaScript高级程序设计', borrower: '吴十九', borrowerNo: 'ST017', borrowDate: '2024-02-28', dueDate: '2024-03-28', returnDate: '2024-03-20', status: 'returned' },
  { id: 18, bookId: 2, bookName: 'Python编程：从入门到实践', borrower: '郑二十', borrowerNo: 'ST018', borrowDate: '2024-05-20', dueDate: '2024-06-20', returnDate: null, status: 'borrowed' }
];

export const categoryList = ['编程语言', '计算机基础', '算法', '软件工程', '前端开发', '数据库', '网络技术'];