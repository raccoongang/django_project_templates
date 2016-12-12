$(document).ready(function () {
    $('.social-login_link__active').on('click', function () {
        var button = $(this);
        if (confirm("Are you really want to delete this association?")) {
            var csrf_input = button.parent().find('input[type=hidden]'),
                data = {}
            data[csrf_input.attr('name')]=csrf_input.val()
            data['provider']= button.data('provider')
            $.ajax({
                url: '/accounts/delete_association/',
                type: 'POST',
                data: data,
                success: function (result) {
                    button.removeClass("social-login_link__active");
                }
            });
        }
        return false;
    })

});