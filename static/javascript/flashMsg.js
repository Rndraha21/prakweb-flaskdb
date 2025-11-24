document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll("#flash-msg-container .alert");
  const msgContainer = document.getElementById("flash-msg-container");

  if (alerts && msgContainer) {
    alerts.forEach((alert) => {
      setTimeout(() => {
        alert.classList.remove("show");
        setTimeout(() => {
          alert.remove();
          msgContainer.style.display = "none";
        }, 500);
      }, 3000);
    });
  }
});
