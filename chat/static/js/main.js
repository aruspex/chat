$(function() {

    $('#signTab a').click(function(e) {
        e.preventDefault();
        $(this).tab('show');
    });

    $('#addChannelSubmit').on('click', function(e) {
        console.log('click');
        e.preventDefault();
        $('#addChannelForm').submit();
    });
});