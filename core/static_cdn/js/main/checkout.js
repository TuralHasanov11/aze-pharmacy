const { createApp } = Vue;
const { required, minLength, email, helpers  } = VuelidateValidators

// let url = `ws://${window.location.host}/ws/order-socket-server/`

// const orderSocket = new WebSocket(url)

// orderSocket.onclose = function (e) {
//     console.log("Socket closed")
// }

const phoneValidator = helpers.regex(/^\+?1?\d{12}$/)

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
      checkoutFormValidationMessages:{},
      checkoutFormLabels:{},
      submitLoading: false
    };
  },

  mounted(){
    this.getCities()
    this.getCheckoutFormDetails()
  },

  methods:{
    async getCities(){
        const response = await fetch('/api/cities');
        this.cities = await response.json() 
    },

    async getCheckoutFormDetails(){
        const response = await fetch("/api/checkout-form-details");
        const data = await response.json() 
        for (const field in data) {
            this.checkoutFormValidationMessages[field] = data[field].error_messages
            this.checkoutFormLabels[field] = data[field].label
        }
    },

    async checkout(){
        try {
            this.v$.$touch()
            if (this.v$.$invalid) return 
            
            this.submitLoading = true
            
            const formData = new FormData();
            formData.append('first_name', this.checkoutForm.firstName)
            formData.append('last_name', this.checkoutForm.lastName)
            formData.append('phone', this.checkoutForm.phone)
            formData.append('address', this.checkoutForm.address)
            formData.append('city', this.checkoutForm.city)
            formData.append('email', this.checkoutForm.email)
            formData.append('notes', this.checkoutForm.notes)

            const response = await fetch('/api/checkout', {
                method: 'POST',
                body: formData,
                headers: { "X-CSRFToken": csrftoken },
            });

            const data = await response.json()

            if(response.ok){
                window.location.replace(data?.paymentUrl);
            }else{
                throw new Error(JSON.stringify(data))
            }
        } catch (e) {
            this.submitLoading = false
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
