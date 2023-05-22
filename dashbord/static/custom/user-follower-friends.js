
// Get user followers / Friends / Following from profile page
$(document).on('click', '.show-user-data', function(e) {
    var user_id = $(this).data('user-id');
    var list_type = $(this).data('type');
    var url = "/ajax-get-user-follow/";
    $.ajax({
        url: url,
        type: 'post',
        data: { 
            'user_id': user_id,
            'list_type': list_type,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function(data) {
            $("#userModal .modal-body").html(data.html);
            $("#userModal .modal-title").html(data.title);
        }
    });
});
