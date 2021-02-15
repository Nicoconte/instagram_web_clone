const pagePreload = () => {
    $("#main-container").css("display", "none")

    $(window).load(function(){
        $("#image-preload").fadeOut("slow");
    });
    
    setTimeout(() => {
        $("#main-container").fadeIn("fast")    
    }, 1000)
}

const restartModalStyles = () => {
    $(".modal-dialog").css({
        "margin" : "30px 40px 10px 250px",
    })

    $(".modal-body").css({
        "margin" : "0px",
        "padding" : "0px",
    })
}


const showPostOnModal = () => {
    
    $(document).on("click", ".post-preview", function() {

        let id  = $(this).attr("post-id")

        $.ajax({
            type : "GET",
            dataType : "JSON",
            url : "/post/modal/",
            data : {
                post_id : id
            },
            success : function(response) {
                console.log(response.image)
                $(".post-modal-image").css('background-image', 'url("' + response.image + '")');
                $(".post-modal-user p").text(response.username)
            }
        })
    })
}

$(document).ready(() => {   
    
    showPostOnModal();
    restartModalStyles();

    pagePreload();
})