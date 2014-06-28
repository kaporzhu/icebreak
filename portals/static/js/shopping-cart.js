var ShoppingCart = window.ShoppingCart = {
    data: [],
    total_count: 0,
    total_price: 0,

    STORAGE_KEY: 'shopping-cart',
    STORAGE_KEY_DATE: 'shopping-cart-date',

    calculate: function() {
        var total_count = 0;
        var total_price = 0;
        $.each(ShoppingCart.data, function(i, item){
            total_count += item['count'];
            total_price += item['count'] * item['price'];
        });
        ShoppingCart.total_count = total_count;
        ShoppingCart.total_price = total_price;
    },

    load: function() {
        // load from localStorage
        try{
            if (localStorage[ShoppingCart.STORAGE_KEY_DATE] != new Date().toDateString()) {
                ShoppingCart.empty();
            } else {
                ShoppingCart.data = JSON.parse(localStorage[ShoppingCart.STORAGE_KEY]);
                ShoppingCart.calculate();
            }
        } catch(err){
            ShoppingCart.data = [];
        }
    },

    save: function() {
        // save data to localStorage
        localStorage[ShoppingCart.STORAGE_KEY] = JSON.stringify(ShoppingCart.data);
        localStorage[ShoppingCart.STORAGE_KEY_DATE] = new Date().toDateString();
    },

    addFood: function(food_id, food_name, food_price) {
        var new_one = true;
        $.each(ShoppingCart.data, function(i, item){
            if (item['id'] == food_id) {
                item['count'] += 1;
                item['subtotal_price'] = item['count'] * item['price'];
                new_one = false;
            }
        });
        if (new_one) {
            ShoppingCart.data.push({id: food_id, name: food_name, price: food_price, count: 1, subtotal_price: food_price});
        }
        ShoppingCart.calculate();
        ShoppingCart.save();
    },

    removeFood: function(food_id) {
        for(var i=0; i<ShoppingCart.data.length; i++) {
            if (ShoppingCart.data[i]['id'] == food_id) {
                ShoppingCart.data.splice(i, 1);
                break;
            }
        }
        ShoppingCart.calculate();
        ShoppingCart.save();
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
