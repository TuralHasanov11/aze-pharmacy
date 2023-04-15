jQuery(document).ready(function ($) {
    
    $('.remove_from_cart_button').on('click', async (e) => {
        e.preventDefault();

        const response = await fetch(cartRemoveURL, {
            method: 'POST',
            body: JSON.stringify({
                product_id: $(e.currentTarget).data('product_id'), 
            }),
            headers: { "X-CSRFToken": csrftoken },
        });

        if(response.ok){
            location.reload();
        }
    })

    $('form.woocommerce-cart-form').on('submit', async (e) => {
        e.preventDefault();
        
        const data = {}
        $('input.product-quantity').each(function(){
            data[$(this).data('product_id')] = $(this).val()
        })

        const response = await fetch(cartUpdateURL, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { "X-CSRFToken": csrftoken },
        });

        if(response.ok){
            location.reload();
        }
    })

});