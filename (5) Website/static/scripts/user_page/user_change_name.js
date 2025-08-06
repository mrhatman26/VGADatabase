console.log("user_change_name.js loaded");
let changeNameButton = document.getElementById("change_name_button");
let changeNameDiv = document.getElementById("change_name_div");
let nameBox = null;
let changeNameBackButton = null;
let submitNewNameButton = null;
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

function submitNewName(){
    event.preventDefault();
    if (/\S/.test(nameBox.value)){
        username_data = {
            "user_name": nameBox.value
        };
        $.ajax({
            type: "POST",
            url: "/users/modify/username/",
            data: JSON.stringify(username_data),
            success: function(response){
                if (response === "success"){
                    window.location.reload();
                }
                else if (response === "userexists"){
                    if (oldErrorCheck() === false){
                        var mainBody = document.getElementById("page_mainbody_home");
                        errorMessage = document.createElement("p");
                        errorMessage.id = "errorMessage";
                        errorMessage.style.color = "red";
                        errorMessage.innerHTML = "Username already exists";
                        mainBody.appendChild(errorMessage);
                    }
                    else{
                        errorMessage.innerHTML = "Username already exists";
                    }
                }
                else if (response === "samename"){
                    if (oldErrorCheck() === false){
                        var mainBody = document.getElementById("page_mainbody_home");
                        errorMessage = document.createElement("p");
                        errorMessage.id = "errorMessage";
                        errorMessage.style.color = "red";
                        errorMessage.innerHTML = "You're already using that username!";
                        mainBody.appendChild(errorMessage);
                    }
                    else{
                        errorMessage.innerHTML = "You're already using that username!";
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
    else{
        if (oldErrorCheck() === false){
            var mainBody = document.getElementById("page_mainbody_home");
            errorMessage = document.createElement("p");
            errorMessage.id = "errorMessage";
            errorMessage.style.color = "red";
            errorMessage.innerHTML = "Please enter a username";
            mainBody.appendChild(errorMessage);
        }
        else{
            errorMessage.innerHTML = "Please enter a username";
        }
    }
}

function changeNameBack(){
    if (oldErrorCheck()){
        document.getElementById("page_mainbody_home").removeChild(errorMessage);
        errorMessage = null;
    }
    nameBox.style.display = "none";
    submitNewNameButton.style.display = "none";
    changeNameBackButton.style.display = "none";
    changeNameButton.style.display = "inline";
    changeNameDiv.removeChild(nameBox);
    changeNameDiv.removeChild(submitNewNameButton);
    changeNameDiv.removeChild(changeNameBackButton);
    nameBox = null;
    submitNewNameButton = null;
    changeNameBackButton = null;
}

function showChange(){
    changeNameButton.style.display = "none";
    //New name box
    nameBox = document.createElement("input")
    nameBox.className = "textbox";
    nameBox.type = "text";
    nameBox.placeholder = "New Username";
    changeNameDiv.appendChild(nameBox);
    changeNameDiv.appendChild(document.createElement("p"));
    //Submit button
    submitNewNameButton = document.createElement("a");
    submitNewNameButton.className = "button";
    submitNewNameButton.innerHTML = "Submit";
    submitNewNameButton.addEventListener("click", submitNewName);
    nameBox.addEventListener("keypress", function(event){
        if (event.key === "Enter"){
            submitNewNameButton.click();
        }
    });
    changeNameDiv.appendChild(submitNewNameButton);
    //Back Button
    changeNameBackButton = document.createElement("a");
    changeNameBackButton.className = "button";
    changeNameBackButton.innerHTML = "Back";
    changeNameBackButton.style.marginLeft = "1%";
    changeNameBackButton.addEventListener("click", changeNameBack);
    changeNameDiv.appendChild(changeNameBackButton);
}

changeNameButton.addEventListener("click", showChange);