var timer;
var timeout = 1000;
const mapsetRegexp = /http[s]?:\/\/osu\.ppy\.sh\/([b]?(?:eatmapset)?[s]?)\/([0-9]+)(?:#[a-z]+\/([0-9]+))?/

$('#link').keyup(function () {
    clearTimeout(timer);
    if ($('#link').val()) {
        timer = setTimeout(doneTyping, timeout);
    }
});

$("#link").keydown(function () {
    clearTimeout(timer);
    $(".form").removeClass("loading")
    $("#song").val('')
    $("#mapset_id").val('')
    $("#mapper").val('')
    $("#err").addClass("hidden")
    $("#err").empty()
})

function doneTyping() {
    $(".form").addClass("loading")
    $("#err").addClass("hidden")
    $("#err").empty()

    const value = $('#link').val()
    var match = value.match(mapsetRegexp)

    if (!match) {
        $(".form").removeClass("loading")
        $("#err").removeClass("hidden")
        $("#err").html("Cant find matching osu! beatmap URL.")
    } else {
        var mode
        if (match[1] == "b") { mode = "b" }
        else { mode = "s" }
        axios.get(`/${mode}/${match[2]}`).then(function (response) {
            $("#song").val(response.data.song)
            $("#mapset_id").val(response.data.mapset_id)
            $("#mapper").val(response.data.mapper)
        }).catch(handle_error).finally(() => { $(".form").removeClass("loading") })
    }
}

$("#target_bn").change(function () {
    $this = $(this)
    axios.get(`/rules/${$this.val()}`).then(function (response) {
        $("#bn_rules").html(response.data)
    }).catch(handle_error)
})