var test_select_elem;

const selected = function () {
    const [last_prob, last_test] = [Cookies.get("last_prob"), Cookies.get("last_test")];
    console.log(last_prob, last_test);
    if (window.location.pathname == "/problems/" + last_prob) {
        test_select_elem.selectedIndex = last_test;
    }
}

// Set toggle button on load
window.addEventListener('load', function () {
    console.log("yoooo");
    test_select_elem = document.getElementById("test_select");
    selected();

    test_select_elem.addEventListener('change', () => {
        console.log("Loeaded")
        const prob = window.location.pathname.split("/")[2];
        Cookies.set("last_prob", prob, { SameSite: "Strict" });
        const test = test_select_elem.selectedIndex;
        Cookies.set("last_test", test, { SameSite: "Strict" });
        console.log(prob, test);
    });
});
