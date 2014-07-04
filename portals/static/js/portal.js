$(function(){
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

    updateFoodCount();
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
    $('#foods-list .food .body, #foods-list .food .foot .name').click(function(){
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

    // load food comments
    function load_comments(type){
        var $comments_tab = $('#tabs a[href="#comments"]');
        var $panel = $($comments_tab.attr('href'));
        var page = $comments_tab.data('page');
        $('#load_more_comments').hide();
        if ((type == 'initial' && !$comments_tab.data('loaded')) || (type == 'more')) {
            $.ajax({
                url: $('#food-detail-wrapper .food-detail').data('load-comments-url'),
                data: {id: $comments_tab.data('id'), page: page},
                success: function(comments) {
                    $comments_tab.data('loaded', true);
                    $comments_tab.data('page', page+1);
                    var $comments_html = $(new Ractive({
                        template:'#food-comments-template',
                        data: {comments: comments}
                    }).toHTML());
                    if (type == 'initial') {
                        $panel.find('.body').html($comments_html);
                    } else {
                        $panel.find('.body').append($comments_html);
                    }
                    if (comments.length > 0) {
                        $('#load_more_comments').show();
                    }
                    $('.rating-stars').each(function(){
                        var rating = $(this).data('rating');
                        for (var i=0; i<rating; i++) {
                            $($(this).children('i').get(i)).addClass('on');
                        }
                    });
                }
            });
        }
    }
    $(document).on('shown.bs.tab', '#tabs a[href="#comments"]', function(){load_comments('initial');});
    $(document).on('click', '#load_more_comments', function(){load_comments('more');});

});

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

// update foods count
function update_foods_count() {
    $.ajax({
        url: '/shops/load_foods_count/',
        data: {id: 1},
        success: function(response){
            var changed = false;
            for (var id in response) {
                if (response[id] <= 0) {
                    $('#food-' + id).addClass('sell-out');
                    changed = ShoppingCart.removeFood(id);
                } else {
                    var $count_today = $('#food-' + id).find('.count-today span');
                    $('#food-' + id).removeClass('sell-out');
                    if (parseInt($count_today.text()) != response[id]) {
                        $count_today.data('count', response[id]).addClass('highlight').animate({opacity: 0}, 'slow', function(){
                            $(this).text($(this).data('count')).animate({opacity: 1}, 'slow', function(){$(this).removeClass('highlight');});
                        });
                    }
                }
            }
            updateShoppingCart();
            updateFoodCount();
            if (changed) {
                toggleFoodsList(true);
            }
        },
        complete: function() {
            setTimeout('update_foods_count()', 5000);
        }
    });
}

setTimeout('update_foods_count()', 5000);
