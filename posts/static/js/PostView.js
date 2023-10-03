$(document).ready(function() {
    let csrf = $("input[name=csrfmiddlewaretoken]").val()

    $(".submit-comment-btn").click(function() {
        console.log("submit comment")
        $.ajax({
            url: "",
            method: "post",
            data: {
                task: "add_comment",
                comment_body: $("#comment_body").val(),
                csrfmiddlewaretoken: csrf
            },
            success: function(response) {
                $(".comments_amount").text("Comments: " + response.comments_amount)

                let default_comment_structure = "<li><a href=\"/accounts/" + response.comment_user_slug + "/profile/\"><h5>@" + response.comment_user + "</h5></a><p>" + response.comment_body + "</p></li>"
                let default_like_structure = "<h3 class=\"comment-like\" comment_pk=\""+ response.comment_pk +"\">Like</h3><h3 class=\"likes_amount_comment" + response.comment_pk + "\">Likes: 0</h3><br>"

                $("#comments-list").prepend(default_comment_structure + default_like_structure)
                $("#comment_body").val("")
            }
        })
    })

    // Use .on instead of .click, because .click doesn't work for the newly
    // generated comment see https://stackoverflow.com/questions/6658752/click-event-doesnt-work-on-dynamically-generated-elements
    $("#comments-list").on("click", ".comment-like", function() {
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