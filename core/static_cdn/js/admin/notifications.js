const notificationContainer = document.getElementById('admin-notifications')
const navbarDropdownAlertsToggle = document.getElementById('navbarDropdownAlerts')
const isPaidPage = new URLSearchParams(window.location.search).get('status') === 'paid' || ''
const pusherAppKey = document.getElementById("PUSHER_APP_KEY")?.value
const pusherAppCluster = document.getElementById("PUSHER_APP_CLUSTER")?.value


var pusher = new Pusher(pusherAppKey, {
    cluster: pusherAppCluster
});

var ordersChannel = pusher.subscribe('orders');

ordersChannel.bind('created', function(response) {
    getOrders()
    toastContainer.innerHTML += toastComponent(response.message)
    notificationContainer.innerHTML += orderNotificationComponent(response)
    navbarDropdownAlertsToggle.classList.replace('btn-transparent-dark', 'btn-danger')
});