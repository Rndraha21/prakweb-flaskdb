const hamburgerBtn = document.getElementById("hamburger");
const sidebar = document.getElementById("sidebar");

if (hamburgerBtn) {
  hamburgerBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });
}
