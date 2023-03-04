var visible;

// Copy of keep_selected for progcomp
const selected = function () {
    const last_pg = Cookies.get("last_pg");
    if (last_pg)
        document.getElementById("progcomp").value = last_pg;
}

const set_info = function (val) {
    if (visible) visible.hidden = true;
    visible = document.getElementById("progcomp-help-" + val);
    visible.hidden = false;
}

window.addEventListener('load', function () {
    set_info(document.getElementById("progcomp").value);
    selected();
    document.getElementById("progcomp").addEventListener('change', (e) => {
        set_info(e.target.value);
        Cookies.set("last_pg", e.target.value, { SameSite: "Strict" });
    });
})
