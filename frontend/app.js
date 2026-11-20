const form = document.querySelector('#greeting-form');
const nameInput = document.querySelector('#name');
const button = form.querySelector('button');
const result = document.querySelector('#greeting-result');

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const name = nameInput.value.trim();
  if (!name) {
    result.textContent = 'Enter your name to continue.';
    nameInput.focus();
    return;
  }

  button.disabled = true;
  result.textContent = 'Requesting a greeting…';

  try {
    const query = new URLSearchParams({ name });
    const response = await fetch(`/api/greet?${query}`);
    const body = await response.json();
    result.textContent = response.ok ? body.message : body.error;
  } catch {
    result.textContent = 'Could not reach the server. Try again.';
  } finally {
    button.disabled = false;
  }
});
