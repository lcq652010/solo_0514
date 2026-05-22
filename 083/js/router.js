Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        redirect: '/order'
    },
    {
        path: '/order',
        component: {
            template: '<order-form></order-form>'
        }
    },
    {
        path: '/admin',
        component: {
            template: '<admin-panel></admin-panel>'
        }
    }
];

const router = new VueRouter({
    routes
});