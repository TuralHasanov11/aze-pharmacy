
jQuery(document).ready(function ($) {
    document.querySelectorAll('.contact-form input').forEach(function (element){
        if(!element.checkValidity()){
            element.setCustomValidity(element.getAttribute('title'))
        }else{
            element.setCustomValidity("");
        }
        element.addEventListener('input', function(event){
            if(!event.currentTarget.checkValidity()){
                event.currentTarget.setCustomValidity(event.currentTarget.getAttribute('title'))
            }
            event.currentTarget.setCustomValidity("");
        })
    })

    document.querySelectorAll('.contact-form select').forEach(function (element){
        if(!element.checkValidity()){
            element.setCustomValidity(element.getAttribute('title'))
        }else{
            element.setCustomValidity("");
        }
        element.addEventListener('change', function(event){
            if(!event.currentTarget.checkValidity()){
                event.currentTarget.setCustomValidity(event.currentTarget.getAttribute('title'))
            }
            event.currentTarget.setCustomValidity("");
        })  
    })

    document.querySelectorAll('.contact-form textarea').forEach(function (element){
        if(!element.checkValidity()){
            element.setCustomValidity(element.getAttribute('title'))
        }else{
            element.setCustomValidity("");
        }
        element.addEventListener('change', function(event){
            if(!event.currentTarget.checkValidity()){
                event.currentTarget.setCustomValidity(event.currentTarget.getAttribute('title'))
            }
            event.currentTarget.setCustomValidity("");
        })
    })

    document.querySelector('#contact-form form').addEventListener('submit', (e)=>{
        e.preventDefault()
        document.getElementById('contact-form-btn').disabled = true
        e.currentTarget.submit()
    })
});
