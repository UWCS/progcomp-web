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

var targetDate = null;
var quick = null;

// Update the count down every minute
const countdown = function () {
    if (!targetDate) return
    // Find the distance between now and the count down date
    const now = new Date().getTime();
    const distance = targetDate - now;

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

    let cd = document.getElementById("countdown");
    if (!cd) return clearInterval(x);
    console.log(time_rem_str);
    cd.innerHTML = `${time_rem_str}`;
    if (days > 0 && quick == null) {
        // Less frequent updates if far away
        clearInterval(x);
        x = setInterval(countdown, 60000);
        countdown.quick = false;
    }
    if (minutes < 10) {
        // Less frequent updates if far away
        clearInterval(x);
        x = setInterval(countdown, 1000);
        clearInterval(y);
        y = setInterval(countdown, 5000);
        countdown.quick = true;
    }
    // If the count down is finished, clear
    if (distance < 0) {
        clearInterval(x);
        cd.innerHTML = "Competition now ended!";
    }
};

const updateTarget = function () {
    fetch("http://localhost:5000/end_time")
        .then((r) => r.json())
        .then((json) => {
            console.log(json["end_time"]);
            targetDate = new Date(Number(json["end_time"]) * 1000);
            console.log("New target", targetDate);
            countdown();
        });
}

updateTarget()
let y = setInterval(updateTarget, 15000);

let x = setInterval(countdown, 5000);
