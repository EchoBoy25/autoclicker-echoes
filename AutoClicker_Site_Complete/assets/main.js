
// Countdown loading screen
let seconds = 6;
const countdownEl = document.getElementById('countdown');
const skipBtn = document.getElementById('skip-button');

const interval = setInterval(() => {
  seconds--;
  countdownEl.textContent = seconds;
  if (seconds <= 0) {
    clearInterval(interval);
    skipBtn.disabled = false;
    skipBtn.classList.add('enabled');
    skipBtn.textContent = 'Continue';
  }
}, 1000);

skipBtn.addEventListener('click', () => {
  document.getElementById('loading-screen').style.display = 'none';
  document.getElementById('main-content').style.display = 'block';
});

// Echo Chatbot (minimal logic)
const input = document.getElementById('user-input');
const log = document.getElementById('chat-log');
const header = document.getElementById('chat-header');
const body = document.getElementById('chat-body');

header.addEventListener('click', () => {
  body.style.display = body.style.display === 'none' ? 'block' : 'none';
});

input.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    const userMsg = input.value.trim();
    if (!userMsg) return;
    log.innerHTML += `<div><b>You:</b> ${userMsg}</div>`;
    input.value = '';
    setTimeout(() => {
      log.innerHTML += `<div><b>Echo:</b> <i>Typing...</i></div>`;
      setTimeout(() => {
        log.lastChild.innerHTML = "<b>Echo:</b> Of course! This auto-clicker works great on io games, lets you customize keys, and it’s super easy to use!";
      }, 1000);
    }, 500);
  }
});
