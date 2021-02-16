let months = {
    "01" : "Enero",
    "02" : "Febrero",
    "03" : "Marzo",
    "04" : "Abril",
    "05" : "Mayo",
    "06" : "Junio",
    "07" : "Julio",
    "08" : "Agosto",
    "09" : "Septiembre",
    "10": "Octubre",
    "11": "Noviembre",
    "12": "Diciembre"
}

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
        "margin" : "30px 40px 10px 240px",
    })

    $(".modal-body").css({
        "margin" : "0px",
        "padding" : "0px",
    })
}

const convertDate = (date) => {

    let word = "";
    let dateAsArray = date.split("-")
    let day = dateAsArray[0]
    let monthAsNumber = dateAsArray[1]
    let year = dateAsArray[2]
    

    if (monthAsNumber in months) {
        word = `${day} de ${months[monthAsNumber]} de 20${year}`
    }

    return word.toUpperCase();
}

const userDescriptionTemplate = (object) => {
    return `
        <p class="mt-2" style="margin-left:13px;"> <b class="text-muted">
            ${object.username}</b> ${object.description} 
        </p>
    `
}

const commentTemplate = (object) => {
    return `
    <div class="post-modal-people-comment-content">
        <div class="post-modal-comment-image mt-2">
            <div class="post-modal-user-image" style="background-image: url('${object.profile}');"></div>                                    
        </div>
        <div class="post-modal-comment-text"> 
            <p class="mt-2" style="margin-left:13px"> <b class="text-muted">${object.username}</b> ${object.comment}</p>
        </div>                             
    </div>
    `
}

const likesTemplate = (object) => {
    return `
        <p>Les gusta a 
            ${object.likes > 1000 ? 
                '<b>miles de personas</b>' : '<b>' + object.likes + ' personas</b>.'
            }
        </p> 
        <p class="text-muted font-weight-light">${convertDate(object.publish_date)}</p>
    `
}

//Obtenemos la informacion de la publicacion para ser mostrada en un modal
const getPostDataForModal = (id) => {
    let template = ""

    $.ajax({
        type : "GET",
        dataType : "JSON",
        url : "/post/modal/",
        data : {
            post_id : id
        },
        success : function(response) {
            
            //Foto del modal
            $(".post-modal-image").css('background-image', 'url("' + response.image + '")');

            //Nombre de usuario en la parte superior del modal
            $(".post-modal-user p").text(response.username)
            
            //Descripcion del usuario
            $("#post-modal-user-text").html( userDescriptionTemplate(response) )
            
            //Fetch de los comentarios y foto de cada usuario 
            response.comments.forEach(comment => {
                template += commentTemplate(comment)  
            })
            
            //Colocamos los comentarios de la gente
            $(".post-modal-people-comment").html(template)

            //Colocamos la cantidad de likes en la publicacion
            $(".post-modal-actions-likes").html(likesTemplate(response))

            $(".post-modal-actions").attr("post-id", response.id)

            changeHeartIcon(response);

        }
    })
}

const showPostOnModal = () => {
    
    restartModalStyles(); // Antes de mostrar el modal, reiniciamos algunos estilos del mismo
    
    $(document).on("click", ".post-preview", function() {

        let id  = $(this).attr("post-id")

        getPostDataForModal(id)

    })
}

const likeAPost = () => {
    $(document).on("click", ".like-post-btn", function() {

        let htmlParent = $(this)[0].parentElement.parentElement.parentElement
        let id  = Number($(htmlParent).attr("post-id"))

        $.ajax({
            type : "POST",
            dataType : "JSON",
            url : "/post/like/",
            data : {
                post_id : id
            },
            success : function(response) {
                if (response.liked) {
                    getPostDataForModal(id); // "Refrescamos" el modal con nueva informacion
                }
            }
        })
    })    
}


const commentPost = () => {
    $(document).on("click", ".comment-post-btn", function() {
        
        if (validateInput(["#post-comment-input"])) {
            alert("Complete el campo")
            
            return;
        }
        
        let htmlParent = $(this)[0].parentElement.parentElement

        let id = $(htmlParent).attr("post-id")
        let comment = $("#post-comment-input").val()
        
        console.log(id)

        $.ajax({
            type : "POST",
            dataType : "JSON",
            url : "/post/comment/",
            data : {
                post_id : id,
                comment : comment
            },
            success : function(response) {
                if (response.commented) {
                    getPostDataForModal(id); // "Refrescamos" el modal con nueva informacion
                    clearInput(["#post-comment-input"])
                    $(".post-modal-comments").scrollTop($(".post-modal-comments")[0].scrollHeight);
                }
            }
        })
        
    })
}

const clearInput = (inputs) => {
    return inputs.forEach(input => $(input).val(""))
}

const validateInput = (inputs) => {
    return inputs.some(input => $(input).val().length <= 0 );
}

const changeHeartIcon = (response) => {
    if (response.was_liked) {
        $(".like-post-btn i").removeClass("fa fa-heart-o")
        $(".like-post-btn i").addClass("fa fa-heart text-danger")
    } else {
        $(".like-post-btn i").removeClass("fa fa-heart text-danger")
        $(".like-post-btn i").addClass("fa fa-heart-o")
    }
}

const focusOnCommentInput = () => {
    $("#focus-on-comment-btn").click(() => {
        $("#post-comment-input").focus()
    })
}

$(document).ready(() => {   
    
    showPostOnModal();
    commentPost();
    likeAPost();

    focusOnCommentInput();

    pagePreload();
})