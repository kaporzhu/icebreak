$(document).ready(function(){
    // select row handler
    $('#all-orders .select-row-btn').change(function(){
        $(this).parents('tr').toggleClass('selected');
    });

    // select rows handler
    $('.select-rows-btn').click(function(){
        var type = $(this).data('type');
        select_rows(type);
    });

    // 
    function select_rows(type) {
        if (type == 'all') {
            $('#all-orders input:checkbox:not(:checked)').trigger('click');
        } else if (type == 'none') {
            $('#all-orders input:checkbox:checked').trigger('click');
        } else if (type == 'invert') {
            $('#all-orders input:checkbox').trigger('click');
        }
    }

    // update status button handler
    $('.update-status-btn').click(function(){
        // get selected order ids
        var selected_ids = [];
        $('#all-orders .select-row-btn:checkbox:checked').each(function(){
            selected_ids.push($(this).data('id'));
        });
        if (selected_ids.length == 0) {
            alert('没有选择任何订单');
            return;
        }

        $.ajax({
            url: $(this).data('update-status-url'),
            dataType: 'json',
            data: {
                ids: selected_ids.join(','),
                status: $(this).data('status')
            },
            success: function(result){
                $('#all-orders input:checkbox:checked').each(function(){
                    var $status_td = $(this).parents('tr').find('.status');
                    $status_td.text(result.status_label);
                    $status_td.removeAttr('class').addClass('status ' + result.status_color);
                });
                select_rows('none');
            }
        });
    });

    // datepicker
    $('.datepicker').datepicker({dateFormat: 'yy-mm-dd'}, $.datepicker.regional['zh-TW']);

    // print orders
    $('#print-orders-btn').click(function(){
        var ids = [];
        $('#all-orders .select-row-btn:checked').each(function(){
            ids.push($(this).data('id'));
        });
        window.open( $(this).data('url') + '?ids=' + ids.join(','));
    });
});
