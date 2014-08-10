$(function() {

    $('#signTab a').click(function(e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#addChannelSubmit').on('click', function(e) {
        e.preventDefault();
        $('#addChannelForm').submit();
    });
});