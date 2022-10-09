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
                    $(that).text("Unfollow")
                } else {
                    $(that).text("Follow")
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
                }
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