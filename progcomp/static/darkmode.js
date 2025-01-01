const dark = function (not_loaded = false) {
    const curr_light = Cookies.get("dark_mode") == "light";
    document.documentElement.setAttribute('data-bs-theme', curr_light ? "light" : 'dark');
    
    if (not_loaded) return

    document.getElementById("dark-mode-icon").classList.add(curr_light ? "bi-moon-fill" : "bi-sun-fill")
    document.getElementById("dark-mode-icon").classList.remove(curr_light ? "bi-sun-fill" : "bi-moon-fill")
}

dark(true);

// Set toggle button on load
window.addEventListener('load', function () {
    dark()
    document.getElementById('dark-mode').addEventListener('click', () => {
        const curr_dark = Cookies.get("dark_mode") == "dark";
        Cookies.set("dark_mode", curr_dark ? "light" : "dark", { SameSite: "Strict" });
        dark();
    });
});
