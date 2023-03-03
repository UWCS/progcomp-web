const dark = function () {
    const curr_dark = Cookies.get("dark_mode") == "dark";
    document.documentElement.setAttribute('data-bs-theme', curr_dark ? "dark" : 'light');
}

document.getElementById('dark-mode').addEventListener('click', () => {
    const curr_dark = Cookies.get("dark_mode") == "dark";
    Cookies.set("dark_mode", curr_dark ? "light" : "dark", { SameSite: "None" });
    dark();
});

dark();