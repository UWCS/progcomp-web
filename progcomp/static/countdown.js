// Borrowed from github.com/uwcs/warwickspeedrun

const formatPlural = function (n, term) {
    if (n == 0) return "";
    if (n == 1) return `${n} ${term}`;
    else return `${n} ${term}s`;
}

const listStr = function (parts) {
    if (parts.length == 0) return "";
    if (parts.length == 1) return parts[0];
    var result = parts[0];
    for (var i = 1; i < parts.length - 1; i++) {
        result += `, ${parts[i]}`;
    }
    result += ` and ${parts[parts.length - 1]}`;
    return result;
}

const listStrNonEmpty = function (parts, max_numb) {
    filtered = parts.filter(Boolean);
    if (filtered.length > max_numb) {
        filtered = filtered.slice(0, max_numb);
    }
    return listStr(filtered);
}

const setIntervals = function (cd_t, ut_t, q) {
    if (quick == q) return;
    clearInterval(x);
    clearInterval(y);
    x = setInterval(countdown, cd_t * 1000);
    y = setInterval(updateTarget, ut_t * 1000);
    quick = q;
}

var targetDate = new Date(Cookies.get("end_time"));
var quick = null;
var x, y, cd;

// Update the count down every minute
const countdown = function () {
    if (!targetDate || !cd) return

    // Find the distance between now and the count down date
    const now = new Date().getTime();
    const distance = targetDate - now;
    if (distance < 0) {
        cd.innerHTML = "Competition now ended!";
        if (quick != "ended" && quick != null) location.reload()
        setIntervals(60, 300, "ended");
    } else {
        // Time calculations for days, hours, minutes and seconds
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / (1000));
        // Display the result in the countdown
        let daysText = formatPlural(days, "day");
        let hoursText = formatPlural(hours, "hour");
        let minutesText = formatPlural(minutes, "minute");
        let secondsText = formatPlural(seconds, "second");

        time_rem_str = listStrNonEmpty([daysText, hoursText, minutesText, secondsText], 2);
        if (days >= 7) time_rem_str = daysText;

        cd.innerHTML = `${time_rem_str} remaining`;

        // Set update time
        if (days > 0) {
            setIntervals(60, 300, "days");
        } else if (days == 0 && hours > 1) {
            setIntervals(1, 60, "hours");
        } else if (hours <= 1) {
            setIntervals(1, 15, "mins");
        }
    }

};

const updateTarget = function () {
    fetch("/poll")
        .then((r) => r.json())
        .then((json) => {
            const newDate = new Date(Number(json["end_time"]) * 1000);
            if (newDate != targetDate) {
                targetDate = newDate;
                Cookies.set("end_time", newDate.getTime(), { SameSite: "Strict" });
                countdown();
            }
        });
}

updateTarget();

window.addEventListener('load', () => {
    cd = document.getElementById("countdown");
    countdown()
});
