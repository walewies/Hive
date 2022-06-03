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
                    console.log("Also Here")
                    $(that).text("Like")
                    
                } else {
                    $(that).text("Unlike")
                }
                $(".likes_amount_post" + $(that).attr("post_pk")).text("Likes: " + response.likes_amount)
            }
        })
    })

})