$(document).ready(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()

    $(".like").click(function() {
        let that = this
        $.ajax({
            url: "",
            method: "post",
            data: {
                post_pk: $(this).attr("name"),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                if (response.order === "like") {
                    $(that).text("Like Likes: " + response.likes_amount)
                } else {
                    $(that).text("Unlike Likes: " + response.likes_amount)
                }
            }
        })
    })

})