$(function() {
    $('.basic').jRating({
        step : true,
        bigStarsPath: $('.basic').data('star-url'),
        canRateAgain : true,
        showRateInfo: false,
        nbRates: 100,
        rateMax: 5,
        sendRequest: false,
        onClick : function(ele, rate) {
            $('#rating').val(rate);
            $('.rating').text(rate + '分');
        }
    });
});
