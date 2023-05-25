// This is used in user profile page.

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

// Get post likes / comments
$(document).on('click', '.get-post-data', function(e) {
    var post_id = $(this).data('post-id');
    var data_choice = $(this).data('choice-type');
    var url = "/ajax-get-post-likes-comments/";
    $.ajax({
        url: url,
        type: 'post',
        data: { 
            'post_id': post_id,
            'data_choice': data_choice,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function(data) {
            $("#likeCommentModel .modal-body").html(data.html);
            $("#likeCommentModel .modal-title").html(data.title);
        }
    });
});


// Get reel likes / comments
$(document).on('click', '.get-reel-data', function(e) {
    var reel_id = $(this).data('reel-id');
    var data_choice = $(this).data('choice-type');
    var url = "/ajax-get-reel-likes-comments/";
    $.ajax({
        url: url,
        type: 'post',
        data: { 
            'reel_id': reel_id,
            'data_choice': data_choice,
            'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
        },
        dataType: 'json',
        success: function(data) {
            $("#likeCommentModel .modal-body").html(data.html);
            $("#likeCommentModel .modal-title").html(data.title);
        }
    });
});
