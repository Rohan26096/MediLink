document.addEventListener("DOMContentLoaded", () => {

    const themeBtn = document.querySelector(".theme-btn");

    const body = document.body;

    const icon = themeBtn ? themeBtn.querySelector("i") : null;

    function updateIcon() {
        if (!icon) return;

        if (body.classList.contains("dark-mode")) {
            icon.className = "fa-solid fa-sun";
        } else {
            icon.className = "fa-solid fa-moon";
        }
    }

    updateIcon();

    if (themeBtn) {

        themeBtn.addEventListener("click", () => {

            body.classList.toggle("dark-mode");

            localStorage.setItem(
                "theme",
                body.classList.contains("dark-mode") ? "dark" : "light"
            );

            updateIcon();

        });

    }

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        body.classList.add("dark-mode");
    } else {
        body.classList.remove("dark-mode");
    }

    updateIcon();

});