$(function(){
    $('#is_closed_checkbox').change(function(){
        if ($(this).is(':checked')) {
            $('.close_tip').addClass('hidden');
        } else {
            $('.close_tip').removeClass('hidden');
        }
    });
});
