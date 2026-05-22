Vue.use(ElementUI);

const App = {
    template: `
        <div class="app-container">
            <el-menu 
                :default-active="activeRoute" 
                mode="horizontal" 
                router
                class="nav-menu"
                background-color="#8B4513"
                text-color="#fff"
                active-text-color="#ffd04b">
                <el-menu-item index="/order">
                    <i class="el-icon-s-order"></i>
                    <span>客户下单</span>
                </el-menu-item>
                <el-menu-item index="/admin">
                    <i class="el-icon-s-custom"></i>
                    <span>管理员</span>
                </el-menu-item>
            </el-menu>
            <router-view></router-view>
        </div>
    `,
    computed: {
        activeRoute() {
            return this.$route.path;
        }
    }
};

new Vue({
    el: '#app',
    router,
    render: h => h(App)
});

const style = document.createElement('style');
style.textContent = `
    .app-container {
        min-height: 100vh;
        background-color: #f5f5f5;
    }
    .nav-menu {
        margin-bottom: 0;
    }
    .el-menu-item {
        font-size: 16px;
    }
`;
document.head.appendChild(style);