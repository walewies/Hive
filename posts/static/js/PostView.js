$(document).ready(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()

    $(".comment-like").click(function() {
        console.log("Hello World")
        let that = this
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "comment_like",
                comment_pk: $(this).attr("comment_pk"),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                if (response.order === "like") {
                    $(that).text("Like")
                    
                } else {
                    $(that).text("Unlike")
                }
                $(".likes_amount_comment" + $(that).attr("comment_pk")).text("Likes: " + response.likes_amount)
            }
        })
    })
})