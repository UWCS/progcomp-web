var visible;

const set_info = function (val) {
    if (visible) visible.hidden = true;
    visible = document.getElementById("progcomp-help-" + val);
    visible.hidden = false;
}

window.addEventListener('load', function () {
    set_info(document.getElementById("progcomp").value);
    document.getElementById("progcomp").addEventListener('change', (e) => {
        set_info(e.target.value);
    });
})
