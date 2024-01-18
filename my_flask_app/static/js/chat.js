var title = window.location.pathname.split('/')[2];

        // Attach an event handler to the form's submit event
        $('#chat_form').on('submit', function(event) {
            // Prevent the form from being submitted normally
            event.preventDefault();

            // Get the user's input from the text field
            var user_input = $('#user_input').val();

            // Send an AJAX POST request to the server
            $.ajax({
                url: '/ajax/' + title,
                method: 'POST',
                data: {
                    user_input: user_input
                },
                success: function(response) {
                    // Add the assistant's response to the chat
                    $('.responses').append(
                        '<div class="response">' +
                            '<img src="{{ url_for('static', filename='images/AIchat.png') }}" alt="Model response icon" class="response-icon">' +
                            '<p>' + response.assistant_message + '</p>' +
                        '</div>'
                    );

                    // Clear the text field
                    $('#user_input').val('');
                }
            });
        });