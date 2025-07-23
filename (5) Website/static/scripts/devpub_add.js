console.log("develope_add.js loaded");
let devpubForm = document.getElementById("devpub_add_form");
let mainBody = document.getElementById("page_mainbody_home");
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
        "developer_name": devpubForm[0].value,
        "developer_desc": devpubForm[1].value,
        "developer_foundDate": devpubForm[2].value,
        "developer_defunctDate": devpubForm[3].value,
        "developer_isPub": devpubForm[4].value,
    };
    $.ajax({
        type: "POST",
        url: "/devpubs/add/validate/",
        data: JSON.stringify(devpubData),
        success: function(response){
            if (response === "success"){
                window.location.replace("/games/");
            }
            else if (response === "developerexists"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Developer already exists";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Developer already exists";
                }
            }
            else if (response === "invaliddate"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Invalid Founding or Defunct date";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Invalid Founding or Defunct date";
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

devpubForm.addEventListener("submit", submitDevpub);