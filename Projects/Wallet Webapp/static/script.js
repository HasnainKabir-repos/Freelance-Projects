// Get references to the loading overlay and form
const loadingOverlay = document.getElementById('loadingOverlay');
const form = document.querySelector('.form-container');

// Add an event listener to the form's submit button
form.addEventListener('submit', function () {
    // Show the loading overlay when the form is submitted
    loadingOverlay.style.display = 'flex';
});



