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
    console.log(gameForm[0].value + "\n" + gameForm[1].value + "\n" + gameForm[2].value + "\n" + gameForm[3].value);
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