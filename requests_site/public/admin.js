$(".acceptreq").click(function (e) {
    e.preventDefault();
    $this = $(this)

    const set_id = $this.data("set-id")
    axios.post("/request/" + set_id, { "status_": 2 }).then((e) => {
        var $parent = $($this.parents()[2])
        $parent.hide()
        var $a_status = $parent.siblings(".extra.content").contents("a")
        $a_status.contents().first().replaceWith("Accepted")
    }).catch(handle_error)
})

$(".declinereq").click(function (e) {
    e.preventDefault();
    $this = $(this)
    const set_id = $this.data("set-id")

    const appended = `<div class="ui form"><div class="field"><label>Reason</label><textarea id="reason-${set_id}"></textarea></div><button class="ui button" type="submit" id="rejbtn-${set_id}">Submit</button></div>`;
    $($this.parents()[1]).append(appended)
    $("#rejbtn-" + set_id).click((e) => {
        e.preventDefault()
        axios.post("/request/" + set_id, { "status_": 1, "archive": true, "reason": $(`#reason-${set_id}`).val() }).then((e) => {
            var $parent = $($this.parents()[2])
            $parent.hide()
            var $a_status = $parent.siblings(".extra.content").contents("a")
            $a_status.contents().first().replaceWith("Declined")
        }).catch(handle_error)
    })
})

$(".archivebtn").click(function (e) {
    const set_id = $(this).data("set-id")
    const checkbox_val = $("#nominate-" + set_id).prop('checked')
    var status, archive;
    if (checkbox_val) {
        status = 4
        archive = false
    } else {
        status = 3
        archive = true
    }

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
                    axios.post("/request/" + set_id, { "status_": status, "archive": archive }).then((e) => {
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

$(".nominatedbtn").click(function (e) {
    const set_id = $(this).data("set-id")
    $('body').toast({ message: "Marking..." })
    axios.post("/request/" + set_id, { "status_": 5, "archive": true }).then((e) => {
        $('body').toast({ message: "Done!" })
        location.reload()
    }).catch(handle_error)
})


$(".unarchivebtn").click(function (e) {
    const set_id = $(this).data("set-id")

    $('body').toast({
        message: 'Are you sure you want to unarchive this map? The request will be back to accepted requests.',
        displayTime: 0,
        actions: [
            {
                text: "Yes",
                icon: "check",
                class: "green",
                click: () => {
                    $('body').toast({ message: "Unarchiving..." })
                    axios.post("/request/" + set_id, { "status_": 2, "archive": false }).then((e) => {
                        $('body').toast({ message: "Done!" })
                        location.reload()
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

$(".pendingbtn").click(function (e) {
    const set_id = $(this).data("set-id")

    $('body').toast({
        message: 'Are you sure you want to bring this request back to Pending?',
        displayTime: 0,
        actions: [
            {
                text: "Yes",
                icon: "check",
                class: "green",
                click: () => {
                    $('body').toast({ message: "Unarchiving..." })
                    axios.post("/request/" + set_id, { "status_": 0, "archive": false, "reason": "" }).then((e) => {
                        $('body').toast({ message: "Done!" })
                        location.reload()
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