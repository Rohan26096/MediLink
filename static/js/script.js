const themeBtn = document.querySelector(".theme-btn");

function updateTheme(theme) {
    if (theme === "dark") {
        document.body.classList.add("dark-mode");
        themeBtn.innerHTML = '<i class="fa-solid fa-sun"></i>';
    } else {
        document.body.classList.remove("dark-mode");
        themeBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
    }
}

updateTheme(localStorage.getItem("theme") || "light");

themeBtn.addEventListener("click", () => {
    const isDark = document.body.classList.toggle("dark-mode");

    const theme = isDark ? "dark" : "light";
    localStorage.setItem("theme", theme);

    updateTheme(theme);
});