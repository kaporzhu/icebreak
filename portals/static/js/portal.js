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
        $('#food-detail-wrapper').animate({right: '-380px'});
        ShoppingCart.addFood($(this).data('id'), $(this).data('name'), $(this).data('price'));
        updateShoppingCart();
        updateFoodCount();
        toggleFoodsList(true);
    });

    function updateFoodCount() {
        $('#foods-list .foods .food').each(function(){
            $(this).find('.count').css('visibility', 'hidden').text('');
        });
        for (var i=0; i<ShoppingCart.data.length; i++) {
            var food = ShoppingCart.data[i];
            var $count = $('#food-' + food.id).find('.foot .count');
            if (food.count > 0) {
                $count.css('visibility', 'visible').text(food.count);
            } else {
                $count.css('visibility', 'hidden').text('');
            }
        }
    }
    updateFoodCount();

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
        updateFoodCount();
        toggleFoodsList(false);
    });

    $(document).on('click', '#shopping-cart .foods-list .hidden-btn', function(){
        var action = $(this).data('action');
        var food_id = $(this).data('id');
        ShoppingCart[action](food_id);
        updateShoppingCart();
        updateFoodCount();
        toggleFoodsList(true);
    });

    // show food detail
    $('#foods-list .food .body').click(function(){
        var $food = $(this).parents('.food');
        if ($('#food-detail-wrapper').css('right') == '0px') {
            if ($('#food-detail-wrapper h3').data('id') == $food.find('button').data('id')) {
                $('#food-detail-wrapper').animate({right: '-380px'});
                return;
            }
        }
        $('#food-detail-wrapper .food-detail').html(
            new Ractive({
                template:'#food-detail-template',
                data: {
                    name: $food.find('button').data('name'),
                    image: $food.find('img').attr('src'),
                    description: $food.find('button').data('description'),
                    ingredients: $food.find('button').data('ingredients'),
                    id: $food.find('button').data('id'),
                }
            }).toHTML()
        );
        $('#food-detail-wrapper').animate({right: '0px'});
    });
    $('#food-detail-wrapper .hide-btn').click(function(){
        $('#food-detail-wrapper').animate({right: '-380px'});
    });

    // load food steps
    $(document).on('shown.bs.tab', '#tabs a[href="#steps"]', function(){
        var $this = $(this);
        var $panel = $($this.attr('href'));
        if (!$this.data('loaded')) {
            $.ajax({
                url: $('#food-detail-wrapper .food-detail').data('load-steps-url'),
                data: {id: $this.data('id')},
                success: function(steps) {
                    $this.data('loaded', true);
                    $panel.html(
                        new Ractive({
                            template:'#food-steps-template',
                            data: {steps: steps}
                        }).toHTML()
                    );
                }
            });
        }
    });
});
