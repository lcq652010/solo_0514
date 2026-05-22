## 1. 架构设计
```mermaid
layeredGraph LR
    subgraph 前端层
        A[Vue2 + ElementUI]
    end
    subgraph 路由层
        B[Vue Router]
    end
    subgraph 状态管理
        C[Vuex]
    end
    subgraph 数据层
        D[Mock 数据]
    end
    A --> B
    A --> C
    C --> D
```

## 2. 技术选型
- 前端框架：Vue@2.7.14
- UI 组件库：ElementUI@2.15.14
- 路由管理：Vue Router@3.6.5
- 状态管理：Vuex@3.6.2
- 构建工具：Vite@5.2.0
- 语言：JavaScript ES6+

## 3. 路由定义
| 路由路径 | 页面组件 | 功能描述 |
|----------|----------|----------|
| / | OrderForm.vue | 客户下单页面 |
| /admin | OrderList.vue | 管理员订单列表页面 |

## 4. 数据模型

### 4.1 订单数据结构
```javascript
{
  id: String,           // 订单编号
  stoneType: String,    // 砚石材类型
  length: Number,       // 长度（cm）
  width: Number,        // 宽度（cm）
  carvingStyle: String, // 雕刻样式
  inkPoolShape: String, // 砚池形制
  status: String,       // 当前工序状态
  createdAt: String,    // 创建时间
  processSteps: Array   // 工序步骤记录
}
```

### 4.2 生产工序定义
| 工序名称 | 标识 | 顺序 |
|----------|------|------|
| 采石 | quarrying | 1 |
| 切坯 | cutting | 2 |
| 整形 | shaping | 3 |
| 雕刻 | carving | 4 |
| 打磨 | polishing | 5 |
| 上蜡 | waxing | 6 |
| 质检 | inspecting | 7 |
| 完工 | completed | 8 |

## 5. 项目结构
```
src/
├── components/
│   ├── Navbar.vue          # 导航组件
│   └── ProcessSteps.vue    # 工序进度组件
├── views/
│   ├── OrderForm.vue       # 客户下单页
│   └── OrderList.vue       # 管理员订单页
├── store/
│   └── orders.js           # 订单状态管理
├── data/
│   └── mockData.js         # Mock 数据
├── router/
│   └── index.js            # 路由配置
├── App.vue
├── main.js
└── style.css
```

## 6. 核心 API

### 6.1 订单相关
| 方法 | 功能 | 参数 | 返回值 |
|------|------|------|--------|
| addOrder | 添加新订单 | order 对象 | 订单列表 |
| getOrders | 获取所有订单 | 无 | 订单列表 |
| updateStatus | 更新订单状态 | orderId, status | 更新后的订单 |

### 6.2 数据字段选项
- **砚石材类型**：端砚石、歙砚石、洮砚石、澄泥砚石、红丝砚石、松花砚石
- **雕刻样式**：素面、云龙纹、山水纹、梅兰竹菊、花鸟鱼虫、人物故事、吉祥图案
- **砚池形制**：圆形、方形、椭圆形、长方形、异形、天然形
