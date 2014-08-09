$(document).ready(function() {
    var namespace = '/chat';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    var scrollDiv = document.getElementById("chat-messages");

    var new_message = function(usr, msg) {
        msg = '<div class="message"><address>' + usr + '</address><span>' + msg + '</span></div>'
        $('#chat-messages').append(msg);
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
    };

    var clear = function() {
        $('#new-message').val('');
    };

    socket.on('connect', function() {
        var channelId = $('#chat').data('channelid');
        socket.emit('join', channelId);
    });

    socket.on('error', function(error) {
        console.log('Error ', error);
    });

    socket.on('msg_channel', function(user, msg) {
        new_message(user, msg);
    });


    $('#chat-form').submit(function(e) {
        e.preventDefault();
        var message = $('#new-message').val();

        new_message('me', message);
        clear();

        socket.emit('new message', message);
    });

});