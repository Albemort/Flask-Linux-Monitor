const Token = sessionStorage.getItem('token');

if (Token) {
// Token exists, allow access to the protected resource
// For example, show the dashboard
window.location.href = '/dashboard';
}

  const form = document.querySelector('#login-form');
  form.addEventListener('submit', (event) => {
  event.preventDefault();
  
  const formData = new FormData(form);
  const jsonData = JSON.stringify(Object.fromEntries(formData.entries()));
  
  fetch('/login', {
      method: 'POST',
      headers: {
      'Content-Type': 'application/json'
      },
      body: jsonData
  })
  .then(response => {
    if (!response.ok) {
      alert("Invalid username/password!")
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    if (data.token) {
      // Store the token in sessionStorage
      sessionStorage.setItem('token', data.token);

      // Redirect to the dashboard
      window.location.href = '/dashboard';
    } else {
      throw new Error('Invalid token received from server');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
});