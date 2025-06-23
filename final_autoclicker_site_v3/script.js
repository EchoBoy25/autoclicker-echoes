
document.addEventListener('DOMContentLoaded', () => {
  let seconds = 6;
  const countdown = document.getElementById('countdown');
  const skipBtn = document.getElementById('skip-btn');
  const loadingScreen = document.getElementById('loading-screen');
  const mainContent = document.getElementById('main-content');

  const interval = setInterval(() => {
    seconds--;
    countdown.textContent = seconds;
    if (seconds <= 0) {
      clearInterval(interval);
      skipBtn.disabled = false;
    }
  }, 1000);

  skipBtn.addEventListener('click', () => {
    loadingScreen.style.display = 'none';
    mainContent.style.display = 'block';
  });

  // Echo chatbot
  const echoInput = document.getElementById('echo-input');
  const echoBody = document.getElementById('echo-body');

  echoInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      const question = echoInput.value.trim().toLowerCase();
      let reply = "I'm Echo! I can help with questions about this app. Ask away!";

      if (question.includes("what") && question.includes("app")) {
        reply = "This app automates mouse clicks for games like Zombs.io, Cookie Clicker, and more!";
      } else if (question.includes("mac")) {
        reply = "Yep! There's a Mac version included. Just click the Mac download button!";
      } else if (question.includes("windows")) {
        reply = "Totally! The Windows version is optimized and included for free.";
      }

      echoBody.innerHTML += `<div><strong>You:</strong> ${echoInput.value}</div>`;
      echoBody.innerHTML += `<div><strong>Echo:</strong> ${reply}</div>`;
      echoInput.value = "";
    }
  });
});
