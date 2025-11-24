document.addEventListener("DOMContentLoaded", () => {
  const dropdownBtn = document.getElementById("dropdown-btn");

  dropdownBtn.addEventListener("click", () => {
    document.getElementById("dropdown-container").classList.toggle("hidden");
  });
});
