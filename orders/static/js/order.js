$(function(){
    // update shopping cart
    function updateShoppingCart() {
        if (ShoppingCart.data.length == 0) {
            $('#shopping-cart').html('您的购物车是空的 <a href="/">去挑选</a>');
            $('#order-detail').addClass('hidden');
            return;
        }
        $('#shopping-cart .foods').html(
            new Ractive({
                template: '#food-item-template',
                data: {foods: ShoppingCart.data}
            }).toHTML()
        );
        $('#shopping-cart .foot').html(
            new Ractive({
                template: '#shopping-cart-overview-template',
                data: {total_count: ShoppingCart.total_count, total_price: ShoppingCart.total_price}
            }).toHTML()
        );
    }
    updateShoppingCart();
    $(document).on('click', '#shopping-cart .foods .hidden-btn', function(){
        var action = $(this).data('action');
        var food_id = $(this).data('id');
        ShoppingCart[action](food_id);
        updateShoppingCart();
    });

    // auto load zones, floors or rooms
    var buildings = {};
    $('#order-detail .buildings').change(function(){
        var $selector = $(this);
        $selector.nextAll('select').remove();
        var building_pk = $('option:selected', $(this)).val();
        if (building_pk in buildings) {
            render_next_select($selector, {building: building_pk});
        } else {
            // building data doesn't exist, load from server
            $.ajax({
                url: $selector.parents('form').data('load-building-url'),
                dataType: 'json',
                data: {building_pk: building_pk},
                success: function(data) {
                    buildings[building_pk] = data;
                    render_next_select($selector, {building: building_pk});
                }
            });
        }
    });
    function generate_floors(floors) {
        var result = [];
        for (var i=0; i<floors; i++) {
            result.push({floor: i+1});
        }
        return result;
    }
    function render_next_select($selector, selected_ids) {
        $selector.nextAll('select').remove();
        var building = buildings[selected_ids.building];
        var data = {};
        var template = '';
        if ($selector.is('.buildings')) {
            if (building.is_multiple) {
                var zones = [];
                for (var id in building.zones) {
                    zones.push(building.zones[id]);
                }
                data = {zones: zones};
                template = '#zones-select-template';
            } else {
                data = {floors: generate_floors(building.floors)};
                template = '#floors-select-template';
            }
        } else if($selector.is('.zones')) {
            data = {floors: generate_floors(building.zones[selected_ids.zone].floors)};
            template = '#floors-select-template';
        } else if ($selector.is('.floors')) {
            var rooms = [];
            var rooms_dict = {};
            if (building.is_multiple) {
                rooms_dict = building.zones[selected_ids.zone].rooms;
            } else {
                rooms_dict = building.rooms;
            }
            for (var id in rooms_dict) {
                if (rooms_dict[id].floor == selected_ids.floor) {
                    rooms.push(rooms_dict[id]);
                }
            }
            data = {rooms: rooms};
            template = '#rooms-select-template';
        }

        $selector.after(
            new Ractive({
                template: template,
                data: data
            }).toHTML()
        );
    }
    $(document).on('change', '#order-detail .floors', function(){
        var building_pk = $('#order-detail .buildings option:selected').val();
        var zone_pk = $('#order-detail .zones option:selected').val();
        var floor_pk = $('#order-detail .floors option:selected').val();
        render_next_select($(this), {building: building_pk, zone: zone_pk, floor: floor_pk});
    });
    $(document).on('change', '#order-detail .zones', function(){
        var building_pk = $('#order-detail .buildings option:selected').val();
        var zone_pk = $('#order-detail .zones option:selected').val();
        var floor_pk = $('#order-detail .floors option:selected').val();
        render_next_select($(this), {building: building_pk, zone: zone_pk, floor: floor_pk});
    });
    $('#order-detail .overview .edit-btn').click(function(){
        $(this).parents('form').find('.wrapper').removeClass('hidden');
        $(this).parents('form').find('.overview').addClass('hidden');

        if ($(this).parents('.address').size() > 0) {
            // parse building, zone, floor and room
            var $overview = $(this).parents('form').find('.overview');
            var building_pk = $overview.data('building');
            if (building_pk in buildings) {
                parse_selected_address(building_pk, $overview.data('zone'), $overview.data('floor'), $overview.data('room'));
            } else {
                $.ajax({
                    url: $(this).parents('form').data('load-building-url'),
                    dataType: 'json',
                    data: {building_pk: building_pk},
                    success: function(data) {
                        buildings[building_pk] = data;
                        parse_selected_address(building_pk, $overview.data('zone'), $overview.data('floor'), $overview.data('room'));
                    }
                });
            }
        }
    });
    function parse_selected_address(building_pk, zone_pk, floor, room_pk) {
        var selected_ids = {building: building_pk, zone: zone_pk, floor: floor};
        render_next_select($('#order-detail .buildings'), selected_ids);
        render_next_select($('#order-detail .zones'), selected_ids);
        render_next_select($('#order-detail .floors'), selected_ids);
        $('#order-detail .buildings option[value="' + building_pk + '"]').prop('selected', 'selected');
        $('#order-detail .zones option[value="' + zone_pk + '"]').prop('selected', 'selected');
        $('#order-detail .floors option[value="' + floor + '"]').prop('selected', 'selected');
        $('#order-detail .rooms option[value="' + room_pk + '"]').prop('selected', 'selected');
    }

    $('#order-detail .wrapper .cancel-btn').click(function(){
        $(this).parents('form').find('.overview').removeClass('hidden');
        $(this).parents('form').find('.wrapper').addClass('hidden');
    });
    $('#order-detail .address .save-btn').click(function () {
        var $buildings = $('#order-detail .buildings');
        var $zones = $('#order-detail .zones');
        var $floors = $('#order-detail .floors');
        var $rooms = $('#order-detail .rooms');
        if ($buildings.val() === null) {
            alert('请选择写字楼');
            return;
        }
        if ($zones.val() === null) {
            alert('请选择区域');
            return;
        }
        if ($floors.val() === null) {
            alert('请选择楼层');
            return;
        }
        if ($rooms.val() === null) {
            alert('请选择办公室');
            return;
        }
        $(this).parents('form').find('.overview').removeClass('hidden');
        $(this).parents('form').find('.wrapper').addClass('hidden');
        $('#order-detail .address .overview').data('building', $buildings.val()).data('zone', $zones.val()).data('room', $rooms.val());
        var address = $buildings.children('option:selected').text() + $zones.children('option:selected').text() + $rooms.children('option:selected').text();
        $('#order-detail .address .overview span').text(address);
    });
    $('#order-detail .contact .save-btn').click(function () {
        var $phone = $('#order-detail .contact .phone');
        var $name = $('#order-detail .contact .name');
        if (!/^1[3-9]\d{9}$/.test($phone.val())) {
            alert('请提供正确的手机号');
            return;
        }
        if (!$name.val()) {
            alert('请提供名字');
            return;
        }
        $(this).parents('form').find('.overview').removeClass('hidden');
        $(this).parents('form').find('.wrapper').addClass('hidden');
        $('#order-detail .contact .overview').data('phone', $phone.val()).data('name', $name.val());
        $('#order-detail .contact .overview span').text($phone.val() + ', ' + $name.val());
    });

    // create order
    function get_data() {
        var foods = [];
        $('#shopping-cart .food-item').each(function(){
            foods.push({id: $(this).data('id'), count: $(this).data('count')});
        });

        var $address = $('#order-detail .address .overview');
        var $contact = $('#order-detail .contact .overview');
        var $coupon = $('#order-detail .coupon .overview');
        var $delivery_time = $('#order-detail .delivery_time select');

        var data = {
            building: $address.data('building'),
            zone: $address.data('zone'),
            room: $address.data('room'),
            foods: JSON.stringify(foods),
            phone: $contact.data('phone'),
            name: $contact.data('name'),
            coupon: $coupon.data('code'),
            delivery_time: $delivery_time.val(),
            csrfmiddlewaretoken: get_cookie('csrftoken')
        };
        return data;
    }
    $('#create-order-btn').click(function(){
        if ($('#order-detail .address .wrapper').is(':visible')) {
            alert('请先保存配送地址');
            return;
        }
        if ($('#order-detail .contact .wrapper').is(':visible')) {
            alert('请先保存联系信息');
            return;
        }

        var $button = $(this);
        var data = get_data();

        // check phone number and address first
        if ($button.data('is-authenticated') == false) {
            $.ajax({
                url: $(this).data('validate-url'),
                data: {phone: data.phone, room: data.room},
                success: function(response) {
                    if (response.validate_required) {
                        $('#validate-phone-modal .phone').val(data.phone);
                        $('#validate-phone-modal').modal();
                    } else {
                        create_order();
                    }
                }
            });
            return;
        } else {
            create_order();
        }
    });
    function create_order() {
        var $button = $('#create-order-btn');
        $button.attr('disabled', 'disabled').text('正在创建...');
        $.ajax({
            url: $button.data('url'),
            type: 'post',
            dataType: 'json',
            data: get_data(),
            success: function(data) {
                $button.text('创建成功');
                $('#validate-phone-btn').text('创建成功');
                location.href = data.next_url;
            },
            error: function() {
                $button.removeAttr('disabled', 'disabled').text('确认下单');
            }
        });
    }

    // send validation code
    $('#send-validation-code-btn').click(function(){
        $(this).attr('disabled', 'disabled').text('正在发送...').data('seconds', 60);
        $.ajax({
            url: $(this).data('url'),
            data: {phone: $('#validate-phone-modal .phone').val()},
            success: function(data) {
                if (!data.success) {
                    alert(data.reason);
                    $('#send-validation-code-btn').removeAttr('disabled').text('发送验证码');
                } else {
                    send_validation_code_timer();
                }
            },
            error: function() {
                $('#send-validation-code-btn').removeAttr('disabled').text('发送验证码');
            }
        });
    });

    // validate phone
    $('#validate-phone-btn').click(function(){
        var $button = $(this);
        $button.attr('disabled', 'disabled').text('正在验证...');
        $.ajax({
            url: $button.data('url'),
            data: {phone: $('#validate-phone-modal .phone').val(), code: $('#validate-phone-modal .code').val()},
            success: function(data, status, xhr) {
                if (!data.success) {
                    alert('验证码错误');
                    $button.removeAttr('disabled').text('提交');
                } else {
                    $button.text('正在创建订单...');
                    create_order();
                }
            },
            error: function() {
                $button.removeAttr('disabled').text('提交');
            }
        });
    });

    // coupon code
    $('#order-detail .coupon .overview .edit-btn').click(function(){
        $('#order-detail .coupon .wrapper').removeClass('hidden');
        $('#order-detail .coupon .overview').addClass('hidden');
    });
    $('#order-detail .coupon .wrapper .input-sm').keyup(function(){
        var codes = [];
        $('#order-detail .coupon .wrapper .input-sm').each(function(){
            codes.push($(this).val());
        });

        // check if current input has three numbers. Auto switch to next one if so.
        var text = $(this).val();
        if (text.length > 3) {
            $(this).val(text.substring(0, 3));
            $(this).next('.input-sm').val(text.substring(3)).focus();
            move_cursor_to_end($(this).next('.input-sm').get(0));
        }
    });
    $('#check-coupon-btn').click(function(){
        var codes = [];
        $('#order-detail .coupon .wrapper .input-sm').each(function(){
            codes.push($(this).val());
        });
        $.ajax({
            url: $(this).data('url'),
            data: {code: codes.join('')},
            success: function(data) {
                if (data.active) {
                    $('#order-detail .coupon .wrapper').addClass('hidden');
                    $('#order-detail .coupon .overview').removeClass('hidden').data('code', codes.join(''));
                    $('#order-detail .coupon .overview span').text(codes.join('-') + ', 优惠' + data.discount + '元');
                    $('#order-detail .coupon .overview a').remove();
                } else {
                    alert(data.reason);
                }
            }
        });
    });
});

function send_validation_code_timer() {
    var $button = $('#send-validation-code-btn');
    var seconds = $button.data('seconds');
    if (seconds > 0) {
        seconds -= 1;
        $button.data('seconds', seconds).text(seconds + '秒');
        setTimeout('send_validation_code_timer()', 1000);
    } else {
        $button.removeAttr('disabled').text('重新发送验证码');
    }
}
