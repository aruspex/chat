$(document).ready(function() {
    // Should bot post ycombinator messagess to this channel?
    var tggl = false;

    var namespace = '/chat';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    var scrollDiv = document.getElementById("chat-messages");
    var container = $('#chat-messages');

    var post_message = function(container, msg) {
        container.append(msg);
        scrollDiv.scrollTop = scrollDiv.scrollHeight;
    }

    var user_message = function(usr, msg) {
        msg = '<div class="message"><address>' + usr +
              '</address><span>' + msg + '</span></div>'
        return msg
    };

    var system_message = function(msg) {
        msg = '<p class=bg-info>' + msg + '</p>'
        return msg
    }

    var clear = function() {
        $('#new-message').val('');
    };


    // so-called ycombinator-bot
    var parseRSS = function(url, container) {
        $.ajax({
            url: document.location.protocol +
                 '//ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=10&callback=?&q=' +
                 encodeURIComponent(url),
            dataType: 'json',
            success: function(data) {
                new_message('YCOMBINATOR-BOT', '');
                console.log(data);
                $.each(data.responseData.feed.entries, function(key, value) {
                    var content = '<p><a href="'+value.link+'" target="_blank">'+value.title+'</a></p>';
                    $(container).append(content);
                });
            }
        });
    };

    window.setInterval(function() {
        if (tggl) {
            parseRSS('https://news.ycombinator.com/rss', '#chat-messages');
        }        
    }, 180000);

    $('#bot-btn').on('click', function() {
        var $this = $(this);
        tggl = !tggl;
        if (tggl) {
            post_message(container, system_message('Bot will be posting Ycombinator news every 3 minutes'));
            $this.addClass('btn-success').removeClass('btn-warning');
        } else {
            $this.addClass('btn-warning').removeClass('btn-success');
        }
    });


    // socket.io-related stuff
    socket.on('connect', function() {
        var channelId = $('#chat').data('channelid');
        socket.emit('join', channelId);
    });

    socket.on('error', function(error) {
        console.log('Error ', error);
    });

    socket.on('msg_channel', function(user, msg) {
        post_message(container, user_message(user, msg));
    });


    $('#chat-form').submit(function(e) {
        e.preventDefault();
        var message = $('#new-message').val();

        post_message(container, user_message('me', message));
        clear();

        socket.emit('new message', message);
    });

    // search in chat history & highlight matches
    $(function() {
        $('#text-search').bind('keyup change', function(ev) {
            var searchTerm = $(this).val();
            $('body').removeHighlight();
            if ( searchTerm ) {
                $('body').highlight( searchTerm );
            };
        });
    });



});