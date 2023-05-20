const { createApp } = Vue;
const { required, minLength } = VuelidateValidators


createApp({
  data() {
    return {
      first_name: "",
      last_name: "",
      city: "",
      phone: "",
      address: "",
      email: "",
      v$: Vuelidate.useVuelidate()
    };
  },

  validations: {
    first_name: {
        required,
    },
    last_name: {
        required,
    },
    city: {
        required,
    },
    phone: {
        required,
    },
    address: {
        required,
    },
    email: {
        email,
    },
  }
}).mount("#checkout-app");


jQuery(document).ready(function ($) {

    let firstNameValid = false
    let lastNameValid = false
    let emailValid = false
    let addressValid = false 
    let cityValid = false
    let phoneValid = false
    let notesValid = false

    function setValidity(event, valid=true){
        if(valid){
            $(event.currentTarget).removeClass('is-invalid')
            $(event.currentTarget).siblings('.invalid-feedback').hide()
        }else{
            $(event.currentTarget).addClass('is-invalid')
            $(event.currentTarget).siblings('.invalid-feedback').show()
        }
        $('.checkout-btn').prop('disabled', formValid())
    }

    $('input[name="first_name"]').on('blur', (event) => {
        const valid = event.currentTarget.checkValidity()
        setValidity(event, valid)
        firstNameValid = valid
    })


    $('input[name="last_name"]').on('blur', (event) => {
        const valid = event.currentTarget.checkValidity()
        setValidity(event, valid)
        lastNameValid = valid
    })

    $('input[name="address"]').on('blur', (event) => {
        const valid = event.currentTarget.checkValidity()
        setValidity(event, valid)
        addressValid = valid
    })

    $('select[name="city"]').on('change', (event) => {
        const valid = event.currentTarget.checkValidity()
        console.log(event.currentTarget.checkValidity())
        setValidity(event, valid)
        cityValid = valid
    })

    $('input[name="phone"]').on('blur', (event) => {
        const valid = event.currentTarget.checkValidity() || !validatePhoneNumber($(event.currentTarget).val())
        setValidity(event, valid)
        phoneValid = valid
    })

    function validatePhoneNumber(input_str) {
        return /^\+?1?\d{9,15}$/.test(input_str);
    }

    $('input[name="email"]').on('blur', (event) => {
        const valid = event.currentTarget.checkValidity()
        setValidity(event, valid)
        emailValid = valid
    })

    $('textarea[name="notes"]').on('blur', (event) => {
        const valid = event.currentTarget.checkValidity()
        setValidity(event, valid)
        notesValid = valid
    })

    let url = `ws://${window.location.host}/ws/order-socket-server/`

    const orderSocket = new WebSocket(url)

    orderSocket.onclose = function (e) {
        console.log("Socket closed")
    }

    function formValid(){
        return firstNameValid && lastNameValid && emailValid && addressValid && cityValid && phoneValid && notesValid
    }

    const checkoutForm = $('form.checkout')
    checkoutForm.on('submit', async (event) => {
        event.preventDefault()
        if(formValid()){
            let formData = new FormData(event.currentTarget);
            await createOrder(formData)
        }
    })

    async function createOrder(formData) {
        try {
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

});

