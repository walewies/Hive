$(document).ready(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()

    $(".follow").click(function() {
        that = this
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "follow",
                post_pk: $(this).attr("post_pk"),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                if (response.order === "unfollow") {
                    $(".follow[post_user=" + response.post_user +"]").text("Unfollow")
                } else {
                    $(".follow[post_user=" + response.post_user +"]").text("Follow")
                }
            }
        })

    })

    $(".like").click(function() {
        let that = this
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "like",
                post_pk: $(this).attr("post_pk"),
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