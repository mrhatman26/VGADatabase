console.log("tag_add.js loaded");
let tagForm = document.getElementById("tag_add_form");
let mainBody = document.getElementById("tag_add_form");
let errorMessage = null;

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function submitDevpub(event){
    event.preventDefault();
    var devpubData = {
        "tag_name": tagForm[0].value,
        "tag_desc": tagForm[1].value,
        "tag_type": tagForm[2].value,
        "tag_isNSFW": tagForm[3].value
    };
    $.ajax({
        type: "POST",
        url: "/tags/add/validate/",
        data: JSON.stringify(devpubData),
        success: function(response){
            console.log(response);
            if (response === "success"){
                window.location.replace("/tags/");
            }
            else if (response === "tagexists"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Tag already exists";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Tag already exists";
                }
            }
            else{
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "A server error occured";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "A server error occured";
                }
            }
        }
    });
}

tagForm.addEventListener("submit", submitDevpub);