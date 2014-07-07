var ShoppingCart = window.ShoppingCart = {
    data: [],
    total_count: 0,
    total_price: 0,
    final_price: 0,
    discount: 0,
    tip: '',

    STORAGE_KEY: 'shopping-cart',
    STORAGE_KEY_TIME: 'shopping-cart-time',

    calculate: function() {
        var total_count = 0;
        var total_price = 0;
        var primary_food_count = 0;
        var discounts = [0, 0, 0.01, 0.02, 0.03, 0.04, 0.05];
        var discount_labels = ['', '', '99折', '98折', '97折', '96折', '95折'];
        $.each(ShoppingCart.data, function(i, item){
            total_count += item['count'];
            total_price += item['count'] * item['price'];
            if (item['is_primary'] == 'True') {
                primary_food_count += item['count'];
            }
        });
        if (primary_food_count > 6) {
            ShoppingCart.discount = total_price * 0.05;
            ShoppingCart.tip = primary_food_count + '份，95折封顶';
        } else {
            ShoppingCart.discount = total_price * discounts[primary_food_count];
            if (primary_food_count > 1) {
                ShoppingCart.tip = primary_food_count + '份，' + discount_labels[primary_food_count];
            } else {
                ShoppingCart.tip = '';
            }
        }
        ShoppingCart.total_count = total_count;
        ShoppingCart.total_price = total_price;
        ShoppingCart.final_price = ShoppingCart.total_price - ShoppingCart.discount;
    },

    load: function() {
        // load from localStorage
        try {
            var time = localStorage[ShoppingCart.STORAGE_KEY_TIME];
            if (!time || new Date().getTime()-time > 3600000) {
                ShoppingCart.empty();
            } else {
                ShoppingCart.data = JSON.parse(localStorage[ShoppingCart.STORAGE_KEY]);
            }
        } catch(err){
            ShoppingCart.data = [];
        }
        ShoppingCart.calculate();
    },

    save: function() {
        // save data to localStorage
        localStorage[ShoppingCart.STORAGE_KEY] = JSON.stringify(ShoppingCart.data);
        localStorage[ShoppingCart.STORAGE_KEY_TIME] = new Date().getTime();
    },

    addFood: function(food_id, food_name, food_price, is_primary) {
        var new_one = true;
        $.each(ShoppingCart.data, function(i, item){
            if (item['id'] == food_id) {
                item['count'] += 1;
                item['subtotal_price'] = item['count'] * item['price'];
                new_one = false;
            }
        });
        if (new_one) {
            ShoppingCart.data.push({id: food_id, name: food_name, price: food_price, is_primary: is_primary, count: 1, subtotal_price: food_price});
        }
        ShoppingCart.calculate();
        ShoppingCart.save();
    },

    removeFood: function(food_id) {
        var removed = false;
        for(var i=0; i<ShoppingCart.data.length; i++) {
            if (ShoppingCart.data[i]['id'] == food_id) {
                ShoppingCart.data.splice(i, 1);
                removed = true;
                break;
            }
        }
        ShoppingCart.calculate();
        ShoppingCart.save();
        return removed;
    },

    minusFood: function(food_id){
        for (var i=0; i<ShoppingCart.data.length; i++) {
            var item = ShoppingCart.data[i];
            if (item['id'] == food_id) {
                item['count'] -= 1;
                item['subtotal_price'] = item['count'] * item['price'];
                if (item['count'] <= 0) {
                    ShoppingCart.data.splice(i, 1);
                    break;
                }
            }
        }
        ShoppingCart.calculate();
        ShoppingCart.save();
    },

    empty: function() {
        ShoppingCart.data = [];
        ShoppingCart.calculate();
        ShoppingCart.save();
    }
};

ShoppingCart.load();
