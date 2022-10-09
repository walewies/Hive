$(document).ready(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()

    $(".follow").click(function() {
        let that = this;
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "follow",
                follow_user: $(this).attr("follow_user"),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                if (response.order === "unfollow") {
                    $(that).text("Unfollow")
                } else {
                    $(that).text("Follow")
                }
            }
        })
   })
})