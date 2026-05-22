Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/order'
    },
    {
        path: '/order',
        name: 'Order',
        component: OrderPage
    },
    {
        path: '/admin',
        name: 'Admin',
        component: AdminPage
    }
]

const router = new VueRouter({
    routes
})