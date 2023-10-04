$(document).ready(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()

    $(".follow").click(function() {
        let that = this;
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
                    $(".follow[post_user|=" + $(that).attr("post_user") + "]").text("Unfollow")
                } else {
                    $(".follow[post_user|=" + $(that).attr("post_user") + "]").text("Follow")
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
                    $(that).text("Like")
                } else {
                    $(that).text("Unlike")
                    $(".dislike[post_pk|=" + $(that).attr("post_pk") + "]").text("Dislike")
                }
                $(".likes_amount_post" + $(that).attr("post_pk")).text("Likes: " + response.likes_amount)
                $(".dislikes_amount_post" + $(that).attr("post_pk")).text("Dislikes: " + response.dislikes_amount)
            }
        })
    })

    $(".dislike").click(function() {
        let that = this
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "dislike",
                post_pk: $(this).attr("post_pk"),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                if (response.order === "dislike") {
                    $(that).text("Dislike")           
                } else {
                    $(that).text("Undislike")
                    $(".like[post_pk|=" + $(that).attr("post_pk") + "]").text("Like")
                }
                $(".dislikes_amount_post" + $(that).attr("post_pk")).text("Dislikes: " + response.dislikes_amount)
                $(".likes_amount_post" + $(that).attr("post_pk")).text("Likes: " + response.likes_amount)
            }
        })
    })

    $(".save").click(function() {
        let that = this
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "save",
                post_pk: $(this).attr("post_pk"),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                if (response.order === "save") {
                    $(that).text("Save")
                } else {
                    $(that).text("Unsave")
                }  
            }
        })
    })   
})