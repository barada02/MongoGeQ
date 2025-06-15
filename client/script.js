document.addEventListener('DOMContentLoaded', function() {
    // Use environment variable if defined, otherwise fallback to localhost
    // This will be replaced by a build step in Cloud Run
    const API_URL = window.API_URL || 'http://localhost:8000';
    const messageForm = document.getElementById('messageForm');
    const defaultMessage = document.getElementById('defaultMessage');
    const responseMessage = document.getElementById('responseMessage');
    const getMessageBtn = document.getElementById('getMessageBtn');
    
    // Get default message when page loads
    getDefaultMessage();
    
    // Event listeners
    messageForm.addEventListener('submit', sendMessage);
    getMessageBtn.addEventListener('click', getDefaultMessage);
    
    // Get default message from the API
    function getDefaultMessage() {
        defaultMessage.textContent = 'Loading message...';
        
        fetch(`${API_URL}/message`)
            .then(response => response.json())
            .then(data => {
                defaultMessage.textContent = data.message;
            })
            .catch(error => {
                console.error('Error fetching message:', error);
                defaultMessage.textContent = 'Error loading message. Please try again.';
            });
    }
    
    // Send custom message to the API
    function sendMessage(e) {
        e.preventDefault();
        
        const messageContent = document.getElementById('message').value;
        
        if (!messageContent.trim()) {
            responseMessage.textContent = 'Please enter a message';
            return;
        }
        
        const messageData = {
            content: messageContent
        };
        
        responseMessage.textContent = 'Sending message...';
        
        fetch(`${API_URL}/message`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(messageData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            responseMessage.textContent = `Server received: "${data.received}"
Status: ${data.status}`;
            messageForm.reset();
        })
        .catch(error => {
            console.error('Error sending message:', error);
            responseMessage.textContent = 'Error sending message. Please try again.';
        });
    }
});