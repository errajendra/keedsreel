// his is used in user listing page .


// Activate or deactivate user
$(document).on('click', '.user-status', function(e) {
    var user_id = $(this).data('user-id');
    var task = $(this).data('task');
    if (confirm("Are You Sure to " + task + " user with id "+user_id)) {
        // Save it!
        console.log(task+'ing user.');
    
        var url = "/ajax-activate-deactivate-user/";
        $.ajax({
            url: url,
            type: 'post',
            data: { 
                'user_id': user_id,
                'task': task,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            dataType: 'json',
            success: function(data) {
                if (data.status == 200){
                    alert(data.message);
                    location.reload();
                }else{
                    alert(data.error);
                }
            }
        });
    } else {
        // Do nothing!
        console.log('Canceled to change user data.');
    }
});
