Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        redirect: '/rooms'
    },
    {
        path: '/rooms',
        name: 'Rooms',
        component: RoomList
    },
    {
        path: '/booking',
        name: 'Booking',
        component: BookingForm
    },
    {
        path: '/checkin',
        name: 'Checkin',
        component: CheckinPage
    },
    {
        path: '/orders',
        name: 'Orders',
        component: OrderList
    },
    {
        path: '/checkout',
        name: 'Checkout',
        component: CheckoutPage
    }
];

const router = new VueRouter({
    mode: 'hash',
    routes
});