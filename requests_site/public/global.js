$(document).ready(function() {
    $("time.timeago").timeago();
});

function handle_error(err) {
    var message;
    if (err.response) {
        if (err.response.data.hasOwnProperty("err")) message = err.response.data.err
        else message = err.response.statusText
    } else if (err.message) {
        message = err.message
    } else {
        message = "An unknown error occured."
    }
    $("#err").removeClass("hidden")
    $("#err").html(message)
}

$('.ui.search').search({
    apiSettings: {
        url: '/request/search/{query}'
    },
    minCharacters : 3
})
