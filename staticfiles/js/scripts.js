// Toggle dark mode
// function toggleDarkMode() {
//   document.body.classList.toggle("dark-mode");
//   localStorage.setItem("dark", document.body.classList.contains("dark-mode"));
// }

// // Keep dark mode on reload
// window.addEventListener("DOMContentLoaded", () => {
//   if(localStorage.getItem("dark") === "true") {
//     document.body.classList.add("dark-mode");
//   }
// });

document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("darkModeToggle");

    if (localStorage.getItem("darkMode") === "enabled") {
        document.body.classList.add("dark-mode");
    }

    toggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {
            localStorage.setItem("darkMode", "enabled");
        } else {
            localStorage.setItem("darkMode", "disabled");
        }
    });
});

