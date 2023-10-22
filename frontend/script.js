document.addEventListener('DOMContentLoaded', function () {
    var chatButton = document.getElementById('chat-button');
    var chatContent = document.getElementById('chat-content');
    var userInput = document.getElementById('user-input');
    var messages = document.getElementById('messages');

    function createMessageElement(text, className) {
        var messageElement = document.createElement('div');
        messageElement.appendChild(document.createTextNode(text));
        messageElement.className = className;
        messages.appendChild(messageElement);
    }

    chatButton.addEventListener('click', function() {
        chatContent.classList.toggle('hidden');
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && userInput.value.trim() !== '') {
            var message = userInput.value;
            userInput.value = '';

            // Create a message element in the chat for the user's message
            createMessageElement(message, 'user-message');

            // Send the message to the Flask server
            fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message}),
            })
            .then(response => response.json())
            .then(data => {
                // Create a message element in the chat for the bot's message
                createMessageElement(data.response, 'bot-message');
            })
            .catch((error) => {
                console.error('Error:', error);
                createMessageElement('Error occurred', 'bot-message');  // You can handle errors more gracefully
            });
        }
    });
});
