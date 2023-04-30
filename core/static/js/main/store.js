jQuery(document).ready(function ($) {
    
    $('.add_to_wishlist_button').on('click', async (e)=>{
      e.preventDefault();
      const productId = $(e.currentTarget).data('product_id');
      const result = await addToWishlist(productId)
      $(e.currentTarget).hide()
      $(e.currentTarget).siblings('.remove_from_wishlist_button').show()
      $('#wishlist-quantity').html(result.quantity)
    })

    $('.remove_from_wishlist_button').on('click', async (e)=>{
      e.preventDefault();
      const productId = $(e.currentTarget).data('product_id');
      const result = await removeFromWishlist(productId)
      $(e.currentTarget).hide()
      $(e.currentTarget).closest('.wishlist_product').hide()
      $(e.currentTarget).siblings('.add_to_wishlist_button').show()
      $('#wishlist-quantity').html(result.quantity)
    })

    async function addToWishlist(productId){
      try {
        const response = await fetch(wishlistAddURL, {
          method: 'POST',
          body: JSON.stringify({
            product_id: productId,
          }),
          headers: { "X-CSRFToken": csrftoken },
        });

        return await response.json()
      } catch (error) {
        console.log(error)
      }
    }

    async function removeFromWishlist(productId){
      try {
        const response = await fetch(wishlistRemoveURL, {
          method: 'POST',
          body: JSON.stringify({
            product_id: productId,
          }),
          headers: { "X-CSRFToken": csrftoken },
        });

        return await response.json()
      } catch (error) {
        console.log(error)
      }
    }

    $('.add_to_cart_button').on('click', async (e) => {
        e.preventDefault();
        const productId = $(e.currentTarget).data('product_id');
        const productQuantity = $(e.currentTarget).data('quantity');

        try {
          const response = await fetch(cartAddURL, {
              method: 'POST',
              body: JSON.stringify({
                product_id: productId,
                product_quantity: productQuantity
              }),
              headers: { "X-CSRFToken": csrftoken },
          });
  
          const data = await response.json();

          const product = productComponent(data)

          if($(`.mini_cart_item[data-product_id='${productId}']`).length === 0){
            $(".cart_list" ).append(product);
          }else{
            $(`.mini_cart_item[data-product_id='${productId}']`).html(product)
          }

          $("#cart-total-price").html(data.total_price);
          $("#cart-quantity").html(data.quantity)
        }catch(error){
          console.log(error)
        }
      })

    $('.remove_from_cart_button').on('click', async (e) => {
        e.preventDefault();
        try {
            await fetch(cartRemoveURL, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: $(e.currentTarget).data('product_id'), 
                }),
                headers: { "X-CSRFToken": csrftoken },
            });
            location.reload();
        } catch (error) {
          console.log(error)
        }
    })

    $('.update_qty.qty_button.plus, .update_qty.qty_button.minus').on('click', (e)=>{
        quantityHandler(e.currentTarget)
        $(e.currentTarget).closest('.quantity').find('.qty').trigger('change')
    })

    $('.add_qty.qty_button.plus, .add_qty.qty_button.minus').on('click', (e)=>{
      quantityHandler(e.currentTarget)
      $('.add_to_cart_button').data('quantity', $(e.currentTarget).closest('.quantity').find('.qty').val())
    })

    function quantityHandler(element){
      let quantity = $(element).closest('.quantity').find('.qty')
      let currentVal = parseFloat(quantity.val())
      let max = parseFloat(quantity.attr('max'))
      let min = parseFloat(quantity.attr('min'))
      let step = quantity.attr('step');

      if (!currentVal || currentVal === '' || currentVal === 'NaN') currentVal = 0;
      if (max === '' || max === 'NaN') max = '';
      if (min === '' || min === 'NaN') min = 0;
      if (step === 'any' || step === '' || step === undefined || parseFloat(step) === 'NaN') step = 1;
    
      if ($(element).is('.plus')) {
          if (max && (currentVal >= max)) {
              quantity.val(max);
          } else {
              quantity.val((currentVal + parseFloat(step)).toFixed(step.getDecimals()));
          }
      } else {
        if (min && (currentVal <= min)) {
            quantity.val(min);
        } else if (currentVal > 0) {
            quantity.val((currentVal - parseFloat(step)).toFixed(step.getDecimals()));
        }
      }
    }

      $('.quantity input.qty').on('change', async(e)=>{
        try {
            const productId = $(e.currentTarget).data('product_id')
            const productQuantity = $(e.currentTarget).val()
            const response = await fetch(cartUpdateURL, {
                method: 'POST',
                body: JSON.stringify({
                    product_id: productId, 
                    product_quantity: productQuantity
                }),
                headers: { "X-CSRFToken": csrftoken },
            });

            const data = await response.json()
            $("#cart-total-price").html(data.total_price);
            $(`.mini_cart_item[data-product_id='${productId}'] .product-quantity`).html(productQuantity)
            $("#cart-quantity").html(data.quantity)
        } catch (error) {
          console.log(error)
        }
      })
                        
      function productComponent(data){
        const url = productUrl.replace('category_slug_value', data.item.product.category_slug)
                              .replace('product_slug_value', data.item.product.slug)
        return `<div class="woocommerce-mini-cart-item mini_cart_item" data-product_id="${data.item.product.id}">
          <div class="mini-cart-thumb">
            <a href="${url}"">
              <img width="350" height="350" src="${data.item.product.image_feature}" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail" alt="" loading="lazy" />							
            </a>
          </div>
          <div class="min-cart-content">
            <h3 class="mini-cart-title"><a href="${url}">${data.item.product.name}</a></h3>
            <div class="min-cart-price">
            <span class="quantity"><span class="product-quantity">${data.item.quantity}</span> &times; <span class="woocommerce-Price-amount amount"><bdi><span class="woocommerce-Price-currencySymbol">&#36;</span>${data.item.price}</bdi></span></span>
          </div>
          </div>
        </div>`
      }
});