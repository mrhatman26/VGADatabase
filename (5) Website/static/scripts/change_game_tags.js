console.log("change_game_tags.js loaded");
let changeButton = document.getElementById("change_button");
let currentTags = document.getElementById("tag_box");
let changeTagDiv = document.getElementById("change_tag_box");
let tagTextBox = null;
let submitButton = null;
let backButton = null;
let gameID = document.getElementById("game_id");
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

function submitNewType(){
    typeData = {
        "type_newtype": typeSelect.value,
        "type_tag_id": tagID.innerHTML.split(": ")[1]
    }
    console.log(typeData);
    $.ajax({
        type: "POST",
        url: "/tags/type/change/",
        data: JSON.stringify(typeData),
        success: function(response){
            if (response === "success"){
                window.location.replace("/tags/tag_id=" + typeData["type_tag_id"]);
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

function goBack(){ //Finish this
    tagTextBox.style.display = "none";
    submitButton.style.display = "none";
    backButton.style.display = "none";
    changeButton.style.display = "inline";
    currentTagsText = null;
    submitButton = null;
    backButton = null;
}

function getCurrentTags(){
    var tagDict = {}
    var currentTagsChildren = currentTags.children;
    for (var i = 0; i < currentTagsChildren.length; i++){
        var tagName = currentTagsChildren[i].children[0].innerHTML;
        var tagType = currentTagsChildren[i].children[0].className;
        tagDict[tagName] = tagType;
    }
    var tagDictKeys = Object.keys(tagDict)
    for (var i = 0; i < tagDictKeys.length; i++){
        if (currentTagsText === null){
            currentTagsText = String(tagDictKeys[i]);
        }
        else{
            currentTagsText = currentTagsText + ", " +String(tagDictKeys[i]);
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
    changeTagDiv.appendChild(extraSpace);
    changeTagDiv.appendChild(tagTextBox)
    //Change submit button
    submitButton.style.marginRight = "1%";
    submitButton.innerHTML = "Change";
    submitButton.className = "button";
    changeTagDiv.appendChild(extraSpace);
    changeTagDiv.appendChild(submitButton);
    //Back button
    backButton.innerHTML = "Back";
    backButton.className = "button";
    changeTagDiv.appendChild(backButton);
    backButton.addEventListener("click", goBack);
    submitButton.addEventListener("click", submitNewType)
}

changeButton.addEventListener("click", addTagBox);