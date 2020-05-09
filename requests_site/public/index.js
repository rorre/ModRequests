$(".cancelbtn").click(function (e) {
    const set_id = $(this).data("set-id")
    $('body').toast({
        message: 'Are you sure you want to cancel?',
        displayTime: 0,
        actions: [
            {
                text: "Yes",
                icon: "check",
                class: "green",
                click: () => {
                    $('body').toast({ message: "Deleting..." })
                    axios.get("/request/" + set_id + "/delete").then((e) => {
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
