// fix placeholder for IE8-9
jQuery.support.placeholder = (function(){
    var i = document.createElement('input');
    return 'placeholder' in i;
})();

$.ajaxSetup({ cache: false });

$(function(){
    if (!$.support.placeholder) {
        $('input, textarea').placeholder();
    }
});

function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function move_cursor_to_end(el) {
    if (!el) {
        return;
    }
    if (typeof el.selectionStart == 'number') {
        el.selectionStart = el.selectionEnd = el.value.length;
    } else if (typeof el.createTextRange != 'undefined') {
        el.focus();
        var range = el.createTextRange();
        range.collapse(false);
        range.select();
    }
}
