console.log("game_denial.js loaded");
let approveButton = document.getElementById("approve_button");
let denyButton = document.getElementById("deny_button");
let denyText = null;
let submitButton = null;
let approvalText = document.getElementById("needs_approval");
let backButton = null;

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
    approvalText.appendChild(document.createElement("p"));
    approvalText.appendChild(denyText);
    //Deny submit button
    submitButton.innerHTML = "Deny";
    submitButton.className = "button";
    approvalText.appendChild(document.createElement("p"));
    approvalText.appendChild(submitButton);
    //Back button
    backButton.innerHTML = "Back";
    backButton.className = "button";
    approvalText.appendChild(backButton);
    backButton.addEventListener("click", goBack);
}

denyButton.addEventListener("click", addTextBox);