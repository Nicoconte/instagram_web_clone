const pagePreload = () => {
    $("#main-container").css("display", "none")

    $(window).load(function(){
        $("#image-preload").fadeOut("slow");
    });
    
    setTimeout(() => {
        $("#main-container").fadeIn("fast")    
    }, 1000)
}


const test = () => {
    
    console.log("Se llamaa")

    $(document).on("click", ".post-preview", function() {
        let id  = $(this).attr("post-id")
        let url = `post/${id}` 

        $.ajax({
            type : "GET",
            dataType : "JSON",
            url : url,
            success : function(response) {
                console.log(response)
            }
        })
    })
}

$(document).ready(() => {   
    
    test();

    pagePreload();
})