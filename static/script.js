window.onload = function() {
    var loginButton = document.getElementById('login-button');
    if (loginButton) {
        window.location.href = loginButton.getAttribute('href');
    }
};


