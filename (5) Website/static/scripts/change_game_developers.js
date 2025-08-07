console.log("change_game_tags.js loaded");
let changeDeveloperButton = document.getElementById("change_dev_button");
let currentDevelopers = document.getElementById("developer_box");
let changeDeveloperDiv = document.getElementById("change_developer_box");
let developerTextBox = null;
let developerSubmitButton = null;
let devpubBackButton = null;
let devpubGameID = document.getElementById("game_id");
let developerList = null;
let currentDevelopersText = null;
let devpubExtraSpace = null;

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function submitNewDevelopers(){
    devData = {
        "change_game_id": devpubGameID.innerHTML.split(": ")[1],
        "change_new_developers": developerList,
        "change_isPub": "false" //Change this
    }
    console.log(devData["change_new_developers"]);
    $.ajax({
        type: "POST",
        url: "/games/devpubs/change/",
        data: JSON.stringify(devData),
        success: function(response){
            console.log(response);
            if (response === "success"){
                window.location.replace("/games/game_id=" + devData["change_game_id"]);
            }
            else if (response.includes("tagnotexist")){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "The following developers do not exist:\n" + response.split("|")[1].replaceAll("+", ", ");
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "The following developers do not exist:\n" + response.split("|")[1].replaceAll("+", ", ");
                }
            }
            else if (response.includes("nouser")){
                window.location.replace("/users/login/");
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

function getNewDevelopers(){
    var developerTextBoxValue = developerTextBox.value;
    developerTextBoxValue = developerTextBoxValue.toLowerCase().replaceAll("_,_", ",").replaceAll("_,", ",").replaceAll(",_", ",").replaceAll(", ", ",");
    developerList = developerTextBoxValue.split(",");
    for (var i = 0; i < developerList.length; i++){
        if (developerList[i].includes(" ")){
            if (oldErrorCheck() === false){
                var mainBody = document.getElementById("page_mainbody_home");
                errorMessage = document.createElement("p");
                errorMessage.id = "errorMessage";
                errorMessage.style.color = "red";
                errorMessage.innerHTML = "Tags cannot contain spaces";
                mainBody.appendChild(errorMessage);
            }
            else{
                errorMessage.innerHTML = "Tags cannot contain spaces";
            }
            developerList = null;
            return;
        }
    }
    submitNewDevelopers();
}

function developerGoBack(){ //Finish this
    developerTextBox.style.display = "none";
    developerSubmitButton.style.display = "none";
    devpubBackButton.style.display = "none";
    changeDeveloperButton.style.display = "inline";
    tagDict = null;
    currentDevelopersText = null;
    developerSubmitButton = null;
    devpubBackButton = null;
}

function getcurrentDevelopers(){
    developerList = []
    if (!(currentDevelopers === null)){
        var currentDevelopersChildren = currentDevelopers.children;
        for (var i = 0; i < currentDevelopersChildren.length; i++){
            developerList.push(currentDevelopersChildren[i].children[0].innerHTML.replaceAll(" ", "_").toLowerCase());
        }
    }
    for (var i = 0; i < developerList.length; i++){
        if (currentDevelopersText === null){
            currentDevelopersText = String(developerList[i]);
        }
        else{
            currentDevelopersText = currentDevelopersText + ", " + String(developerList[i]);
        }
    }
}

function addDeveloperBox(){
    changeDeveloperButton.style.display = "none";
    developerTextBox = document.createElement("textarea")
    developerSubmitButton = document.createElement("a");
    devpubBackButton = document.createElement("a")
    devpubExtraSpace = document.createElement("p");
    devpubBackButton.addEventListener("click", developerGoBack);
    developerSubmitButton.addEventListener("click", getNewDevelopers)
    //TextBox
    getcurrentDevelopers();
    developerTextBox.value = currentDevelopersText;
    developerTextBox.style.resize = "none";
    developerTextBox.style.height = "10em";
    developerTextBox.style.width = "50%";
    developerTextBox.className = "textbox";
    developerTextBox.type = "text";
    developerTextBox.name = "txt_tag_box";
    developerTextBox.required = true;
    developerTextBox.placeholder = "Developers";
    changeDeveloperDiv.appendChild(devpubExtraSpace);
    changeDeveloperDiv.appendChild(developerTextBox)
    //Change submit button
    developerSubmitButton.style.marginRight = "1%";
    developerSubmitButton.innerHTML = "Change";
    developerSubmitButton.id = "change_developer_submit";
    changeDeveloperDiv.appendChild(devpubExtraSpace);
    changeDeveloperDiv.appendChild(developerSubmitButton);
    developerSubmitButton.className = "button";
    //Back button    
    devpubBackButton.innerHTML = "Back";
    devpubBackButton.id = "change_developer_back_button";
    changeDeveloperDiv.appendChild(devpubBackButton);
    devpubBackButton.className = "button";    
}

changeDeveloperButton.addEventListener("click", addDeveloperBox);