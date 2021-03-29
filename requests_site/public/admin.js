$(".acceptreq").click(function (e) {
    e.preventDefault();
    $this = $(this)

    const set_id = $this.data("set-id")
    axios.post("/request/" + set_id, { "status_": 2 }).then((e) => {
        // Hide Reject/Accept buttons
        var $optionButtons = $($this.parents()[2])
        $optionButtons.hide()

        // Update request status on UI
        var $card = $($this.parents()[3])
        $card.find(".reqStatus").html("Accepted")
    }).catch(handle_error)
})

$(".declinereq").click(function (e) {
    e.preventDefault();
    $this = $(this)
    const set_id = $this.data("set-id")

    // Append reasoning textbox
    const appended = `<div class="ui form"><div class="field"><label>Reason</label><textarea id="reason-${set_id}"></textarea></div><button class="ui button" type="submit" id="rejbtn-${set_id}">Submit</button></div>`;
    $($this.parents()[1]).append(appended)
    $("#rejbtn-" + set_id).click((e) => {
        e.preventDefault()
        axios.post("/request/" + set_id, { "status_": 1, "archive": true, "reason": $(`#reason-${set_id}`).val() }).then((e) => {
            // Hide Reject/Accept buttons
            var $optionButtons = $($this.parents()[2])
            $optionButtons.hide()

            // Update request status on UI
            var $card = $($this.parents()[3])
            $card.find(".reqStatus").html("Declined")
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

    createToast(
        'Are you sure you want to archive?',
        () => {
            $('body').toast({ message: "Archiving..." })
            axios.post("/request/" + set_id, { "status_": status, "archive": archive }).then((e) => {
                $($(this).parents()[1]).remove()
                $('body').toast({ message: "Done!" })
            }).catch(handle_error)
        }
    )
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

    createToast(
        'Are you sure you want to unarchive this map? The request will be back to accepted requests.',
        () => {
            $('body').toast({ message: "Unarchiving..." })
            axios.post("/request/" + set_id, { "status_": 2, "archive": false }).then((e) => {
                $('body').toast({ message: "Done!" })
                location.reload()
            }).catch(handle_error)
        }
    )
})

$(".pendingbtn").click(function (e) {
    const set_id = $(this).data("set-id")

    createToast(
        'Are you sure you want to bring this request back to Pending?',
        () => {
            $('body').toast({ message: "Unarchiving..." })
            axios.post("/request/" + set_id, { "status_": 0, "archive": false, "reason": "" }).then((e) => {
                $('body').toast({ message: "Done!" })
                location.reload()
            }).catch(handle_error)
        }
    )
})