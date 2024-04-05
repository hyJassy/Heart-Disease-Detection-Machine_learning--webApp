document.getElementById('login-toggle').addEventListener('click', () => toggleForm('login'));
document.getElementById('register-toggle').addEventListener('click', () => toggleForm('register'));

function toggleForm(formType) {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');
  if (formType === 'login') {
    loginForm.style.display = 'block';
    registerForm.style.display = 'none';
  } else if (formType === 'register') {
    loginForm.style.display = 'none';
    registerForm.style.display = 'block';
  }
}