$(".acceptreq").click(function (e) {
    e.preventDefault();
    $this = $(this)

    const set_id = $this.data("set-id")
    axios.post("/request/" + set_id, {"status_": 2}).then((e) => {
        var $parent = $($this.parents()[1])
        $parent.hide()
        $parent.siblings("a").contents().last().replaceWith("Accepted")
    }).catch(handle_error)
})

$(".declinereq").click(function (e) {
    e.preventDefault();
    $this = $(this)
    const set_id = $this.data("set-id")

    const appended = `<div class="ui form"><div class="field"><label>Reason</label><textarea id="reason-${set_id}"></textarea></div><button class="ui button" type="submit" id="rejbtn-${set_id}">Submit</button></div>`
    $($this.parents()[1]).append(appended)
    $("#rejbtn-" + set_id).click((e) => {
        e.preventDefault()
        axios.post("/request/" + set_id, {"status_": 1, "archive": true, "reason": $(`#reason-${set_id}`).val()}).then((e) => {
            var $parent = $($this.parents()[1])
            $parent.hide()
            $parent.siblings("a").contents().last().replaceWith("Declined")
        }).catch(handle_error)
    })
})

$(".archivebtn").click(function (e) {
    const set_id = $(this).data("set-id")
    $('body').toast({
        message: 'Are you sure you want to archive?',
        displayTime: 0,
        actions: [
            {
                text: "Yes",
                icon: "check",
                class: "green",
                click: () => {
                    $('body').toast({ message: "Archiving..." })
                    axios.post("/request/" + set_id, {"status_": 3, "archive": true}).then((e) => {
                        $($(this).parents()[1]).remove()
                        $('body').toast({ message: "Done!" })
                    }).catch(handle_error)
                }
            },
            {
                icon: 'ban',
                class: 'red',
                text: "No"
            }
        ]
    })
})
