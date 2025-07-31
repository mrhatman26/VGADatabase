console.log("change_game_tags.js loaded");
let changeButton = document.getElementById("change_button");
let currentTags = document.getElementById("tag_box");
let changeTagDiv = document.getElementById("change_tag_box");
let tagTextBox = null;
let submitButton = null;
let backButton = null;
let gameID = document.getElementById("game_id");
let tagList = null;
let currentTagsText = null;
let extraSpace = null;

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function submitNewTags(){
    tagData = {
        "change_game_id": gameID.innerHTML.split(": ")[1],
        "change_new_tags": tagList
    }
    console.log(tagData);
    $.ajax({
        type: "POST",
        url: "/games/tags/change/",
        data: JSON.stringify(tagData),
        success: function(response){
            console.log(response);
            if (response === "success"){
                window.location.replace("/games/game_id=" + tagData["change_game_id"]);
            }
            else if (response.includes("tagnotexist")){
                if (oldErrorCheck() === false){
                    var mainBody = document.getElementById("page_mainbody_home");
                    errorMessage = document.createElement("p");
                    errorMessage.id = "errorMessage";
                    errorMessage.style.color = "red";
                    errorMessage.innerHTML = "The following tags do not exist:\n" + response.split("|")[1].replaceAll("+", ", ");
                    mainBody.appendChild(errorMessage);
                }
                else{
                    errorMessage.innerHTML = "The following tags do not exist:\n" + response.split("|")[1].replaceAll("+", ", ");
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

function getNewTags(){
    var tagTextBoxValue = tagTextBox.value;
    tagTextBoxValue = tagTextBoxValue.toLowerCase().replaceAll("_,_", ",").replaceAll("_,", ",").replaceAll(",_", ",").replaceAll(", ", ",");
    tagList = tagTextBoxValue.split(",");
    for (var i = 0; i < tagList.length; i++){
        console.log("'" + tagList[i] + "'");
        if (tagList[i].includes(" ")){
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
            tagList = null;
            return;
        }
    }
    submitNewTags();
}

function goBack(){ //Finish this
    tagTextBox.style.display = "none";
    submitButton.style.display = "none";
    backButton.style.display = "none";
    changeButton.style.display = "inline";
    tagDict = null;
    currentTagsText = null;
    submitButton = null;
    backButton = null;
}

function getCurrentTags(){
    tagList = []
    if (!(currentTags === null)){
        var currentTagsChildren = currentTags.children;
        for (var i = 0; i < currentTagsChildren.length; i++){
            tagList.push(currentTagsChildren[i].children[0].innerHTML.replaceAll(" ", "_").toLowerCase());
        }
    }
    for (var i = 0; i < tagList.length; i++){
        if (currentTagsText === null){
            currentTagsText = String(tagList[i]);
        }
        else{
            currentTagsText = currentTagsText + ", " + String(tagList[i]);
        }
    }
}

function addTagBox(){
    changeButton.style.display = "none";
    tagTextBox = document.createElement("textarea")
    submitButton = document.createElement("a");
    backButton = document.createElement("a")
    extraSpace = document.createElement("p");
    //TextBox
    getCurrentTags();
    tagTextBox.value = currentTagsText;
    tagTextBox.style.resize = "none";
    tagTextBox.style.height = "10em";
    tagTextBox.style.width = "50%";
    tagTextBox.className = "textbox";
    tagTextBox.type = "text";
    tagTextBox.name = "txt_tag_box";
    tagTextBox.required = true;
    tagTextBox.placeholder = "Tags";
    changeTagDiv.appendChild(extraSpace);
    changeTagDiv.appendChild(tagTextBox)
    //Change submit button
    submitButton.style.marginRight = "1%";
    submitButton.innerHTML = "Change";
    submitButton.className = "button";
    changeTagDiv.appendChild(extraSpace);
    changeTagDiv.appendChild(submitButton);
    //Back button
    backButton.addEventListener("click", goBack);
    backButton.innerHTML = "Back";
    backButton.className = "button";
    backButton.id = "add_tag_back_button";
    changeTagDiv.appendChild(backButton);
    submitButton.addEventListener("click", getNewTags)
}

changeButton.addEventListener("click", addTagBox);