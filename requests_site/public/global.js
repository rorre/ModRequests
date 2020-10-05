$(document).ready(function () {
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

function createToast(message, onClick) {
    $('body').toast({
        message: message,
        displayTime: 0,
        actions: [
            {
                text: "Yes",
                icon: "check",
                class: "green",
                click: onClick
            },
            {
                icon: 'ban',
                class: 'red',
                text: "No"
            }
        ]
    })
}

$('.ui.dropdown').dropdown()
$('#selector').change(function () {
    $("#nominator_select").submit()
})
