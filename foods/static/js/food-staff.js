$(function(){
    $('.update-count-today-btn').click(function(){
        var $btn = $(this);
        $btn.attr('disabled', 'disabled').text('正在修改...');
        $.ajax({
            url: $btn.parents('form').data('url'),
            data: {
                count: $btn.siblings('input').val(),
                id: $btn.parents('form').data('id')
            },
            success: function() {
                $btn.removeAttr('disabled').text('修改');
            }
        });
    });

    $('.update-food-status-btn').click(function(){
        var $btn = $(this);
        $.getJSON($(this).data('url'), {id: $(this).data('id')}, function(response){
            if (response.is_active) {
                $btn.text('在售');
            } else {
                $btn.text('停售');
            }
        });
    });
});
