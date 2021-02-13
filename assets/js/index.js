const pagePreload = () => {
    $("#main-container").css("display", "none")

    $(window).load(function(){
        $("#image-preload").fadeOut("slow");
    });
    
    setTimeout(() => {
        $("#main-container").fadeIn("fast")    
    }, 1000)
}

$(document).ready(() => {   
    pagePreload();
})