document.addEventListener("DOMContentLoaded", () => {

    console.log("theme.js loaded");

    const themeBtn = document.getElementById("theme-toggle");

    if (!themeBtn) {
        console.error("Theme button not found!");
        return;
    }

    console.log("Theme button found");

    const root = document.documentElement;
    const icon = themeBtn.querySelector("i");

    // Load saved theme
    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        root.classList.add("dark-mode");
        console.log(root.classList.contains("dark-mode"));
        setTimeout(() => {
            console.log("After 1 second:", root.className);
        }, 1000);
    }

    updateIcon();

    themeBtn.addEventListener("click", () => {
        console.log("Before:", root.className);

        root.classList.toggle("dark-mode");

        console.log("After toggle:", root.className);

        setTimeout(() => {
            console.log("After 100ms:", root.className);
        }, 100);

        setTimeout(() => {
            console.log("After 1s:", root.className);
        }, 1000);
    });

    function updateIcon() {

        if (!icon) return;

        if (root.classList.contains("dark-mode")) {
            icon.className = "fa-solid fa-sun";
        } else {
            icon.className = "fa-solid fa-moon";
        }

    }

});