$(document).ready(function () {
    var usernamePage = $('#username-page');
    var chatPage = $('#chat-page');
    var usernameForm = $('#usernameForm');
    var messageForm = $('#messageForm');
    var messageInput = $('#message');
    var messageArea = $('#messageArea');

    var username = null;
    var ai = "AI Assistant";

    var colors = [
        '#2196F3', '#32c787', '#00BCD4', '#ff5652',
        '#ffc107', '#ff85af', '#FF9800', '#39bbb0'
    ];

    usernameForm.on('submit', connect);
    messageForm.on('submit', send);

    function connect(event) {
        username = $('#name').val().trim();

        if (username) {
            usernamePage.addClass('hidden');
            chatPage.removeClass('hidden');

            var message = {
                "messageType": "JOIN",
                "sender": username,
                "content": ""
            };
            onMessageReceived(message);

            message.sender = ai;
            onMessageReceived(message);

            message.sender = ai;
            message.messageType = "CHAT";
            message.content = "Welcome " + username + "!!! I am AI Assistant. How may I help you?";
            onMessageReceived(message);
        }
        event.preventDefault();
    }

    function send(event) {
        var question = messageInput.val().trim();
        var message = {
            "messageType": "CHAT",
            "sender": username,
            "content": question
        };
        onMessageReceived(message);

        message = {
            "messageType": "CHAT",
            "sender": ai,
            "content": "..."
        };
        var tobedeleted = onMessageReceived(message);
        messageInput.val("");

        // Make an asynchronous GET request using jQuery
        $.ajax({
            url: 'http://localhost:8000/doc/chat?query=' + question,
            method: 'GET',
            dataType: 'json',
            headers: {
                'Origin': 'http://localhost:7000',
            },
            success: function (data) {
                tobedeleted.remove();
                var message = {
                    "messageType": "CHAT",
                    "sender": ai,
                    "content": data.output
                };
                onMessageReceived(message);
            },
            error: function (xhr, status, error) {
                tobedeleted.remove();
                var message = {
                    "messageType": "CHAT",
                    "sender": ai,
                    "content": "Something went wrong. Please try again"
                };
                onMessageReceived(message);
            }
        });

        event.preventDefault();
    }

    function onMessageReceived(message) {
        var messageElement = $('<li></li>');
        var isAsync = false;

        if (message.messageType === 'JOIN' || message.messageType === 'LEAVE') {
            messageElement.addClass('event-message');
            message.content = message.sender + ' ' + (message.messageType === 'JOIN' ? 'joined!' : 'left!');
        } else {
            messageElement.addClass('chat-message');

            var avatarElement = $('<i></i>').text(message.sender[0]);
            avatarElement.css('background-color', getAvatarColor(message.sender));

            messageElement.append(avatarElement);

            var usernameElement = $('<span></span>').text(message.sender);
            messageElement.append(usernameElement);
        }

        messageArea.append(messageElement);
        var textElement = $('<p></p>');
        messageElement.append(textElement);
        messageContent = message.content;

        if (message.sender === ai && message.messageType !== "JOIN") {
            messageElement.css('background-color', "beige");
            typeMessage(messageContent, textElement);
        } else {
            displayMessage(messageContent, textElement);
        }
        messageArea.scrollTop(messageArea[0].scrollHeight);

        return messageElement;
    }

    function displayMessage(messageContent, textElement) {
        textElement.html(messageContent);
    }

    async function typeMessage(messageContent, textElement) {
        var messageLength = messageContent.length;
        for (var i = 0; i < messageLength; i++) {
            textElement.html(textElement.html() + messageContent[i]);
            await sleep(5);
            messageArea.scrollTop(messageArea[0].scrollHeight);
        }
    }
    
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    function getAvatarColor(messageSender) {
        var hash = 0;
        for (var i = 0; i < messageSender.length; i++) {
            hash = 31 * hash + messageSender.charCodeAt(i);
        }

        var index = Math.abs(hash % colors.length);
        return colors[index];
    }
});
