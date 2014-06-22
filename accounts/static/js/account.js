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
