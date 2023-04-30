const { createApp } = Vue;

createApp({
    delimiters: ['[[', ']]'],
    data() {
      return {
        orders: {},
        order: {},
        message: 'orders',
        orderLoading: false
      }
    },

    mounted(){
        this.getOrders()
    },

    methods:{
        async getOrders(){
            const response = await fetch(ordersURL, {
                method: 'GET',
                headers: { "X-CSRFToken": csrftoken },
            });

            const data = await response.json()
            this.orders = data?.results
        },

        async verifyOrder(orderId){
            try {
                const response = await fetch(`${ordersURL}/${orderId}/verify`, {
                    method: 'POST',
                    headers: { "X-CSRFToken": csrftoken },
                });
    
                if(response.ok){
                    this.orders.find(order => order.id === orderId).billing_status = true
                }
            } catch (error) {
                console.log(error)
            }
        },

        async getOrderDetails(orderId){
            try {
                this.orderLoading = true
                const response = await fetch(`${ordersURL}/${orderId}`, {
                    method: 'GET',
                    headers: { "X-CSRFToken": csrftoken },
                });
    
                if(response.ok){
                    this.order = await response.json()
                    this.orderLoading = false
                }
            } catch (error) {
                console.log(error)
            }
        }
    },

    filters: {
        date: function (value) {
            if (!value) return ''
            date = new Date(value.toString())
            console.log(date)
            return date.toLocaleDateString()
        }
    }
}).mount('#orders-app')

