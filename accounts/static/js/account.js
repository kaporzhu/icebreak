$(function(){
    // send validation code
    $('#send-validation-code-btn').click(function(){
        var $send_btn = $('#send-validation-code-btn');
        $send_btn.attr('disabled', 'disabled').text('正在发送...').data('seconds', 60);
        $.ajax({
            url: $send_btn.data('url'),
            data: {phone: $('#login-form input[name="phone"]').val()},
            success: function(data) {
                if (!data.success) {
                    alert(data.reason);
                    $send_btn.removeAttr('disabled').text('发送验证码');
                } else {
                    send_validation_code_timer();
                }
            },
            error: function() {
                $send_btn.removeAttr('disabled').text('发送验证码');
            }
        });
    });

    // post message in staff home
    $('#create-message-btn').click(function(){
        if ($('#create-message-form textarea').val().length == 0) {
            alert('请填写留言内容');
            return;
        }
        $(this).parents('form').submit();
    });

    // reply to message
    $('.reply-btn').click(function(){
        $('.reply_to').removeClass('hidden');
        var name = $(this).parents('li').find('.name').text();
        var content = $(this).parents('li').find('.content').text();
        $('.reply_to .name').text('回复' + name);
        $('.reply_to .content').text(content);
        $('#create-message-form textarea').focus();
        $('#create-message-form input[name="reply_to"]').val($(this).parents('li').data('id'));
    });

    // highlight message by the user
    $(window).on('hashchange', function() {
        $('.highlight').removeClass('highlight');
        $('.' + location.hash.slice(1)).addClass('highlight');
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
