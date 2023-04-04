jQuery(function ($) {
    if (!String.prototype.getDecimals) {
        String.prototype.getDecimals = function () {
            var num = this,
                match = ('' + num).match(/(?:\.(\d+))?(?:[eE]([+-]?\d+))?$/);
            if (!match) {
                return 0;
            }
            return Math.max(0, (match[1] ? match[1].length : 0) - (match[2] ? +match[2] : 0));
        }
    }
    // Quantity "plus" and "minus" buttons
    $(document.body).on('click', '.plus, .minus', function () {
        var $qty = $(this).closest('.quantity').find('.qty'),
            currentVal = parseFloat($qty.val()),
            max = parseFloat($qty.attr('max')),
            min = parseFloat($qty.attr('min')),
            step = $qty.attr('step');

        // Format values
        if (!currentVal || currentVal === '' || currentVal === 'NaN') currentVal = 0;
        if (max === '' || max === 'NaN') max = '';
        if (min === '' || min === 'NaN') min = 0;
        if (step === 'any' || step === '' || step === undefined || parseFloat(step) === 'NaN') step = 1;

        // Change the value
        if ($(this).is('.plus')) {
            if (max && (currentVal >= max)) {
                $qty.val(max);
            } else {
                $qty.val((currentVal + parseFloat(step)).toFixed(step.getDecimals()));
            }
        } else {
            if (min && (currentVal <= min)) {
                $qty.val(min);
            } else if (currentVal > 0) {
                $qty.val((currentVal - parseFloat(step)).toFixed(step.getDecimals()));
            }
        }

        // Trigger change event
        $qty.trigger('change');
    });
});

(function () {
    var c = document.body.className;
    c = c.replace(/woocommerce-no-js/, 'woocommerce-js');
    document.body.className = c;
})();


var tinvwl_add_to_wishlist = { "text_create": "Create New", "text_already_in": "{product_name} already in Wishlist", "simple_flow": "", "hide_zero_counter": "", "i18n_make_a_selection_text": "Please select some product options before adding this product to your wishlist.", "tinvwl_break_submit": "No items or actions are selected.", "tinvwl_clipboard": "Copied!", "allow_parent_variable": "", "block_ajax_wishlists_data": "", "update_wishlists_data": "", "hash_key": "ti_wishlist_data_12c29c7152456052273931eb685ebc04", "nonce": "37820e1a9c", "rest_root": "https:\/\/themegenix.net\/wp\/suxnix\/wp-json\/", "plugin_url": "https:\/\/themegenix.net\/wp\/suxnix\/wp-content\/plugins\/ti-woocommerce-wishlist\/", "wc_ajax_url": "\/wp\/suxnix\/?wc-ajax=tinvwl", "stats": "", "popup_timer": "6000" };
