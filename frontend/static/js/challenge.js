function startQuestionTimer(game_id, end) {
    countdown(
        function(ts) {
            const proportion = (ts.seconds / 20) * 100

            document.getElementById('time_left_bar').style.width = proportion + '%'
            document.getElementById('time_left').innerHTML = ts.toHTML()

            let bg

            if (100 >= proportion && proportion > 75) {
                bg = 'primary'
            } else if (75 >= proportion && proportion > 50) {
                bg = 'success'
            } else if (50 >= proportion && proportion > 25) {
                bg = 'warning'
            } else if (25 >= proportion && proportion >= 0) {
                bg = 'danger'
            }

            document.getElementById('time_left_bar').className = "progress-bar progress-bar-striped progress-bar-animated bg-" + bg

            if (ts.seconds === 0) {
                window.location.replace('/game/outcome/' + game_id)
            }
        },
        end,
        countdown.SECONDS
    )
}

function startOutcomeTimer(game_id, is_last_question) {
    if (!is_last_question) {
        setTimeout(function () {
            window.location.replace('/game/play/' + game_id)
        }, 10 * 1000)
    } else {
        setTimeout(function () {
            window.location.replace('/game/end/' + game_id)
        }, 10 * 1000)
    }
}