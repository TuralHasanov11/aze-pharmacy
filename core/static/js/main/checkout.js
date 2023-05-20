const { createApp } = Vue;
const { required, minLength, email, helpers  } = VuelidateValidators

let url = `ws://${window.location.host}/ws/order-socket-server/`

const orderSocket = new WebSocket(url)

orderSocket.onclose = function (e) {
    console.log("Socket closed")
}

const phoneValidator = helpers.regex(/^\+?1?\d{9,15}$/)

createApp({
  data() {
    return {
      checkoutForm:{
        firstName: "",
        lastName: "",
        city: "",
        phone: "+994",
        address: "",
        email: "",
        notes:"",
      },
      v$: Vuelidate.useVuelidate(),
      cities: [],
      orderValidationMessages:{},
      submitLoading: false
    };
  },

  mounted(){
    this.getCities()
    this.getOrderValidationMessages()
  },

  methods:{
    async getCities(){
        const response = await fetch(citiesApiURL);
        this.cities = await response.json() 
    },

    async getOrderValidationMessages(){
        const response = await fetch(orderValidationMessagesApiURL);
        this.orderValidationMessages = await response.json() 
    },

    async checkout(){
        try {
            this.v$.$touch()
            if (this.v$.$invalid) return 
            
            this.submitLoading = true

            const formData = new FormData();
            formData.append('first_name', this.firstName)
            formData.append('last_name', this.lastName)
            formData.append('phone', this.phone)
            formData.append('address', this.address)
            formData.append('city', this.city)
            formData.append('email', this.email)
            formData.append('notes', this.notes)

            const response = await fetch(checkoutURL, {
                method: 'POST',
                body: formData,
                headers: { "X-CSRFToken": csrftoken },
            });

            const data = await response.json()

            if(response.ok && data.success_url){
                window.location.replace(data?.success_url);
            }else{
                throw new Error(JSON.stringify(data))
            }
        } catch (e) {
            console.log(e)
        }
    }
  },

  validations: {
    checkoutForm:{
        firstName: {
            required
        },
        lastName: {
            required
        },
        city: {
            required
        },
        phone: {
            required,
            phoneValidator
        },
        address: {
            required
        },
        email: {
            email
        },
    },
  }
}).mount("#checkout-app");
