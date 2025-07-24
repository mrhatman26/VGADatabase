console.log("devpub_denial.js loaded");
let approveButton = document.getElementById("approve_button");
let denyButton = document.getElementById("deny_button");
let denyText = null;
let submitButton = null;
let approvalText = document.getElementById("needs_approval");
let backButton = null;
let gameID = document.getElementById("developer_id");

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function submitReason(){
    denialData = {
        "denial_text": denyText.value,
        "denial_developer_id": gameID.innerHTML.split(": ")[1]
    }
    $.ajax({
        type: "POST",
        url: "/mod/approvals/devpubs/deny/",
        data: JSON.stringify(denialData),
        success: function(response){
            if (response === "success"){
                window.location.replace("/");
            }
            else if (response === "alreadydenied"){
                var mainBody = document.getElementById("page_mainbody_home");
                if (oldErrorCheck() === false){
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "This devpub has already been denied";
                    mainBody.appendChild(errorMessage);
                }
            }
            else{
                var mainBody = document.getElementById("page_mainbody_home");
                if (oldErrorCheck() === false){
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "A server error occured";
                    mainBody.appendChild(errorMessage);
                }
            }
        }
    });
}

function goBack(){
    denyText.style.display = "none";
    submitButton.style.display = "none";
    backButton.style.display = "none";
    approveButton.style.display = "inline";
    denyButton.style.display = "inline";
    denyText = null;
    submitButton = null;
    backButton = null;
}

function addTextBox(){
    approveButton.style.display = "none";
    denyButton.style.display = "none";
    denyText = document.createElement("textarea");
    submitButton = document.createElement("a");
    backButton = document.createElement("a")
    //Deny text box
    denyText.style.resize = "none";
    denyText.className = "textbox";
    denyText.type = "text";
    denyText.name = "txt_deny_reason";
    denyText.placeholder = "Reason for game denial";
    denyText.required = true;
    approvalText.appendChild(document.createElement("p"));
    approvalText.appendChild(denyText);
    //Deny submit button
    submitButton.style.marginRight = "1%";
    submitButton.innerHTML = "Deny";
    submitButton.className = "button";
    approvalText.appendChild(document.createElement("p"));
    approvalText.appendChild(submitButton);
    //Back button
    backButton.innerHTML = "Back";
    backButton.className = "button";
    approvalText.appendChild(backButton);
    backButton.addEventListener("click", goBack);
    submitButton.addEventListener("click", submitReason)
}

denyButton.addEventListener("click", addTextBox);