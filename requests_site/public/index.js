$(".cancelbtn").click(function (e) {
    const set_id = $(this).data("set-id")
    createToast(
        'Are you sure you want to cancel?',
        () => {
            $('body').toast({ message: "Deleting..." })
            axios.get("/request/" + set_id + "/delete").then((e) => {
                $($(this).parents()[1]).remove()
                $('body').toast({ message: "Done!" })
            }).catch(handle_error)
        }
    )
})

$(".reason").popup({
    on: 'hover'
});

$(".showmodal").click(function () {
    $this = $(this)
    const dbid = $this.data("dbid")
    $("#db-" + dbid).modal("show")
})