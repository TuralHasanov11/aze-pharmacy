jQuery(document).ready(function ($) {
    $('#add-to-cart-btn').on('click', (e) => {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: cartAddURL,
            data: {
                product_id: $('#add-to-cart-btn').val(),
                product_quantity: $('#quantity').val(),
                csrfmiddlewaretoken: csrftoken,
            },
            success: function (json) {
                document.getElementById("cart-quantity").innerHTML = json.quantity
                // document.getElementById("cart-total-price").innerHTML = json.total_price
            },
            error: function (xhr, errmsg, err) { }
        });
    })
});