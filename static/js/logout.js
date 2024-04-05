document.addEventListener("DOMContentLoaded", function() {
    // Get the logout button element
    var logoutButton = document.querySelector('.btn-outline-danger');

    // Add click event listener
    logoutButton.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default action (e.g., form submission or link redirection)
        
        // Perform logout action here (e.g., make an AJAX request to the logout route)
        // Replace 'logoutRoute' with the actual URL for your logout route
        fetch('/logout', {
            method: 'POST' // Assuming logout is handled via POST request, adjust accordingly
        })
        .then(function(response) {
            // Handle response (e.g., redirect user to login page)
            window.location.href = '/login'; // Redirect to login page after successful logout
        })
        .catch(function(error) {
            console.error('Logout failed:', error); // Log any errors
            // Optionally, display an error message to the user
        });
    });
});
