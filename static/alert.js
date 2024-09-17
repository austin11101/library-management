// Function to display alert messages
function showAlert(message) {
    alert(message);
}

// Function to handle flash messages and display alerts
function displayFlashMessages() {
    const messages = JSON.parse(document.getElementById('flash-messages').textContent);
    messages.forEach(message => {
        showAlert(message);
    });
}

// Call displayFlashMessages when the page loads
window.onload = function() {
    displayFlashMessages();
};
