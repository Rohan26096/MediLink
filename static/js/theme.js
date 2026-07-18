document.addEventListener("DOMContentLoaded", () => {

    const themeBtn = document.getElementById("theme-toggle");

    if (!themeBtn) return;

    const root = document.documentElement;
    const icon = themeBtn.querySelector("i");

    function applyTheme(theme) {

        if (theme === "dark") {
            root.classList.add("dark-mode");
            icon.className = "fa-solid fa-sun";
        } else {
            root.classList.remove("dark-mode");
            icon.className = "fa-solid fa-moon";
        }

        localStorage.setItem("theme", theme);
    }

    applyTheme(localStorage.getItem("theme") || "light");

    themeBtn.addEventListener("click", () => {

        const newTheme = root.classList.contains("dark-mode")
            ? "light"
            : "dark";

        applyTheme(newTheme);

    });

});