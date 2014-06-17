$(function(){
    function toggleFoodsList(showOrHide) {
        var $foods_list = $('#shopping-cart .foods-list-wrapper');
        if (showOrHide === undefined) {
            showOrHide = !$foods_list.is('.visible');
        }
        if (showOrHide) {
            $foods_list.addClass('visible');
            var height = $foods_list.height();
            var max_height = $(window).height() * 0.5;
            $foods_list.animate({
                top: -height + 'px',
                'max-height': max_height + 'px'
            });
        } else {
            $foods_list.removeClass('visible');
            $foods_list.animate({top: 0});
        }
    }

    $('#shopping-cart .foods-overview').click(function(){
        toggleFoodsList();
    });

    $('.add-food-btn').click(function(){
        ShoppingCart.addFood($(this).data('id'), $(this).data('name'), $(this).data('price'));
        updateShoppingCart();
        toggleFoodsList(true);
    });

    function updateShoppingCart() {
        $('#shopping-cart .foods-list').html(
            new Ractive({
                template:'#foods-list-item-template',
                data: {foods: ShoppingCart.data}
            }).toHTML()
        );
        if (ShoppingCart.total_count == 0) {
            toggleFoodsList(false);
            $('#shopping-cart .foods-overview').text('现在购物车是空的');
            $('#checkout-btn').hide();
        } else {
            $('#shopping-cart .foods-overview').html(
                new Ractive({
                    template: '#foods-overview-template',
                    data: {total_count: ShoppingCart.total_count, total_price: ShoppingCart.total_price}
                }).toHTML()
            );
            $('#checkout-btn').show();
        }
    }
    updateShoppingCart();

    $('#empty-shoppingcart-btn').click(function(){
        ShoppingCart.empty();
        updateShoppingCart();
        toggleFoodsList(false);
    });

    $(document).on('click', '#shopping-cart .foods-list .hidden-btn', function(){
        var action = $(this).data('action');
        var food_id = $(this).data('id');
        ShoppingCart[action](food_id);
        updateShoppingCart();
    });
});
