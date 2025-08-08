console.log("change_game_devpubs.js loaded");
let changeDeveloperButton = document.getElementById("change_dev_button");
let changePublisherButton = document.getElementById("change_pub_button");
let currentDevelopers = document.getElementById("developer_box");
let currentPublishers = document.getElementById("publisher_box");
let changeDeveloperDiv = document.getElementById("change_developer_box");
let changePublisherDiv = document.getElementById("change_publisher_box");
let developerTextBox = null;
let developerSubmitButton = null;
let devpubBackButton = null;
let devpubGameID = document.getElementById("game_id");
let developerList = null;
let currentDevelopersText = null;
let devpubExtraSpace = null;
let developerClicked = false;
let publisherClicked = false;

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function submitNewDevpubs(isPub){
    devData = {
        "change_game_id": devpubGameID.innerHTML.split(": ")[1],
        "change_new_developers": developerList,
        "change_isPub": isPub.toString() //Change this
    }
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
                errorMessage.innerHTML = "Developers cannot contain spaces";
                mainBody.appendChild(errorMessage);
            }
            else{
                errorMessage.innerHTML = "Developers cannot contain spaces";
            }
            developerList = null;
            return;
        }
    }
    submitNewDevpubs(false);
}

function developerGoBack(){
    developerTextBox.style.display = "none";
    developerSubmitButton.style.display = "none";
    devpubBackButton.style.display = "none";
    changeDeveloperButton.style.display = "inline";
    changeDeveloperDiv.removeChild(developerSubmitButton);
    changeDeveloperDiv.removeChild(developerTextBox);
    changeDeveloperDiv.removeChild(devpubBackButton);
    currentDevelopersText = null;
    developerSubmitButton = null;
    devpubBackButton = null;
    developerTextBox = null;
    developerClicked = false;
}

function publisherGoBack(){
    developerTextBox.style.display = "none";
    developerSubmitButton.style.display = "none";
    devpubBackButton.style.display = "none";
    changePublisherButton.style.display = "inline";
    changePublisherDiv.removeChild(developerSubmitButton);
    changePublisherDiv.removeChild(developerTextBox);
    changePublisherDiv.removeChild(devpubBackButton);
    currentDevelopersText = null;
    developerSubmitButton = null;
    devpubBackButton = null;
    developerTextBox = null;
    publisherClicked = false;
}

//Developers
function getcurrentDevelopers(){
    developerList = [];
    if (!(currentDevelopers === null)){
        var currentDevelopersChildren = currentDevelopers.children;
        console.log(currentDevelopersChildren);
        for (var i = 0; i < currentDevelopersChildren.length; i++){
            if (currentDevelopersChildren[i].innerHTML === "This game has no known developers"){
                break;
            }
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
    if (publisherClicked === true){
        publisherGoBack();
        publisherClicked = false;
    }
    developerClicked = true;
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

//Publishers
function getNewPublishers(){
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
                errorMessage.innerHTML = "Publishers cannot contain spaces";
                mainBody.appendChild(errorMessage);
            }
            else{
                errorMessage.innerHTML = "Publishers cannot contain spaces";
            }
            developerList = null;
            return;
        }
    }
    submitNewDevpubs(true);
}

function getCurrentPublishers(){
    developerList = [];
    if (!(currentPublishers === null)){
        var currentPublishersChildren = currentPublishers.children;
        for (var i = 0; i < currentPublishersChildren.length; i++){
            if (currentPublishersChildren[i].innerHTML === "This game has no known publishers"){
                break;
            }
            developerList.push(currentPublishersChildren[i].children[0].innerHTML.replaceAll(" ", "_").toLowerCase());
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

function addPublishersBox(){
    if (developerClicked === true){
        developerGoBack();
        developerClicked = false;
    }
    publisherClicked = true;
    changePublisherButton.style.display = "none";
    developerTextBox = document.createElement("textarea")
    developerSubmitButton = document.createElement("a");
    devpubBackButton = document.createElement("a")
    devpubExtraSpace = document.createElement("p");
    devpubBackButton.addEventListener("click", publisherGoBack);
    developerSubmitButton.addEventListener("click", getNewPublishers)
    //TextBox
    getCurrentPublishers();
    developerTextBox.value = currentDevelopersText;
    developerTextBox.style.resize = "none";
    developerTextBox.style.height = "10em";
    developerTextBox.style.width = "50%";
    developerTextBox.className = "textbox";
    developerTextBox.type = "text";
    developerTextBox.name = "txt_tag_box";
    developerTextBox.required = true;
    developerTextBox.placeholder = "Publishers";
    changePublisherDiv.appendChild(devpubExtraSpace);
    changePublisherDiv.appendChild(developerTextBox)
    //Change submit button
    developerSubmitButton.style.marginRight = "1%";
    developerSubmitButton.innerHTML = "Change";
    developerSubmitButton.id = "change_publisher_submit";
    changePublisherDiv.appendChild(devpubExtraSpace);
    changePublisherDiv.appendChild(developerSubmitButton);
    developerSubmitButton.className = "button";
    //Back button    
    devpubBackButton.innerHTML = "Back";
    devpubBackButton.id = "change_developer_back_button";
    changePublisherDiv.appendChild(devpubBackButton);
    devpubBackButton.className = "button";    
}

changeDeveloperButton.addEventListener("click", addDeveloperBox);
changePublisherButton.addEventListener("click", addPublishersBox);