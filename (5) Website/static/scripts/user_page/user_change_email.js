console.log("user_change_email.js loaded");
let changeEmailButton = document.getElementById("change_email_button");
let changeEmailDiv = document.getElementById("change_email_div");
let emailBox = null;
let changeEmailBackButton = null;
let submitNewEmailButton = null;

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function changeEmailSubmit(){
    event.preventDefault();
    var regex = new RegExp("([A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]+)|([A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)");
    if (/\S/.test(emailBox.value)){
        if (regex.test(emailBox.value)){
            email_data = {
                "user_email": emailBox.value
            };
            $.ajax({
                type: "POST",
                url: "/users/modify/email/",
                data: JSON.stringify(email_data),
                success: function(response){
                    console.log(response);
                    if (response === "success"){
                        window.location.reload();
                    }
                    else if (response === "sameemail"){
                        if (oldErrorCheck() === false){
                            var mainBody = document.getElementById("page_mainbody_home");
                            errorMessage = document.createElement("p");
                            errorMessage.id = "errorMessage";
                            errorMessage.style.color = "red";
                            errorMessage.innerHTML = "You're already using that email!";
                            mainBody.appendChild(errorMessage);
                        }
                        else{
                            errorMessage.innerHTML = "You're already using that email!";
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
                errorMessage.innerHTML = "Please enter a valid email";
                mainBody.appendChild(errorMessage);
            }
            else{
                errorMessage.innerHTML = "Please enter a valid email";
            }
        }
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

function changeEmailBack(){
    if (oldErrorCheck()){
        document.getElementById("page_mainbody_home").removeChild(errorMessage);
        errorMessage = null;
    }
    emailBox.style.display = "none";
    submitNewEmailButton.style.display = "none";
    changeEmailBackButton.style.display = "none";
    changeEmailButton.style.display = "inline";
    changeEmailDiv.removeChild(emailBox);
    changeEmailDiv.removeChild(submitNewEmailButton);
    changeEmailDiv.removeChild(changeEmailBackButton);
    emailBox = null;
    submitNewEmailButton = null;
    changeEmailBackButton = null;
}

function showChange(){
    changeEmailButton.style.display = "none";
    //New email box
    emailBox = document.createElement("input")
    emailBox.className = "textbox";
    emailBox.type = "text";
    emailBox.placeholder = "New Email";
    changeEmailDiv.appendChild(emailBox);
    changeEmailDiv.appendChild(document.createElement("p"));
    //Submit button
    submitNewEmailButton = document.createElement("a");
    submitNewEmailButton.className = "button";
    submitNewEmailButton.innerHTML = "Submit";
    submitNewEmailButton.addEventListener("click", changeEmailSubmit);
    emailBox.addEventListener("keypress", function(event){
        if (event.key === "Enter"){
            submitNewEmailButton.click();
        }
    });
    changeEmailDiv.appendChild(submitNewEmailButton);
    //Back Button
    changeEmailBackButton = document.createElement("a");
    changeEmailBackButton.className = "button";
    changeEmailBackButton.innerHTML = "Back";
    changeEmailBackButton.style.marginLeft = "1%";
    changeEmailBackButton.addEventListener("click", changeEmailBack);
    changeEmailDiv.appendChild(changeEmailBackButton);
}

changeEmailButton.addEventListener("click", showChange);