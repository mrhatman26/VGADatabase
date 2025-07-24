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
    if (/\s/g.test(devpubForm[3].value) || devpubForm[3].value === "" || !devpubForm[3].value){
        console.log("OMG THE DEVPUB FORM IS EMPTY!");
        devpubForm[3].value = "NDATE";
    }
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
            console.log(response);
            if (response === "success"){
                if (devpubData["developer_isPub"] === "false"){
                    window.location.replace("/developers/");
                }
                else{
                    window.location.replace("/publishers/");
                }
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
            else if (response === "invalidfounding"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Founding date is invalid";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Founding date is invalid";
                }
            }
            else if (response === "invaliddefunct"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Defunct date is invalid";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Defunct date is invalid";
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