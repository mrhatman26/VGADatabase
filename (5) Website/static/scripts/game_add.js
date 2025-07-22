console.log("game_add.js loaded");
let gameForm = document.getElementById("game_add_form");
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

function submitGame(event){
    event.preventDefault();
    //Make sure password does not contain text from the other boxes
    //https://stackoverflow.com/questions/2031085/how-can-i-check-if-string-contains-characters-whitespace-not-just-whitespace
    var signupData = {
        "game_title": gameForm[0].value,
        "game_aka": gameForm[1].value,
        "game_desc": gameForm[2].value,
        "game_rdate": gameForm[3].value
    };
    $.ajax({
        type: "POST",
        url: "/games/add/validate",
        data: JSON.stringify(signupData),
        success: function(response){
            if (response === "success"){
                window.location.replace("/games/");
            }
            else if (response === "gameexists"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Game already exists";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Game already exists";
                }
            }
            else if (response === "invaliddate"){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "Invalid releaase date";
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "Invalid releaase date";
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

gameForm.addEventListener("submit", submitGame);