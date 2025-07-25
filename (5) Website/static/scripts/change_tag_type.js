console.log("change_tag_type.js loaded");
let changeButton = document.getElementById("change_button");
let tagTypeText = document.getElementById("tag_type");
let typeSelect = null;
let submitButton = null;
let backButton = null;
let tagID = document.getElementById("tag_id");
let selectOptions = ["Normal", "Genre", "Feature"];
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
    typeSelect.style.display = "none";
    submitButton.style.display = "none";
    backButton.style.display = "none";
    changeButton.style.display = "inline";
    typeSelect = null;
    submitButton = null;
    backButton = null;
}

function addOptions(){
    for (var i = 0; i < selectOptions.length; i++){
        var type = document.createElement("option");
        type.value = selectOptions[i].toLowerCase();
        type.text = selectOptions[i];
        if (i === 0){
            type.selected = true;
        }
        typeSelect.appendChild(type);
    }
}

function addSelect(){
    changeButton.style.display = "none";
    typeSelect = document.createElement("select")
    submitButton = document.createElement("a");
    backButton = document.createElement("a")
    extraSpace = document.createElement("p");
    //Select
    typeSelect.className = "dropDown";
    typeSelect.id = "change_type_select";
    addOptions();
    tagTypeText.appendChild(extraSpace);
    tagTypeText.appendChild(typeSelect);
    //Change submit button
    submitButton.style.marginRight = "1%";
    submitButton.innerHTML = "Change";
    submitButton.className = "button";
    tagTypeText.appendChild(document.createElement("p"));
    tagTypeText.appendChild(submitButton);
    //Back button
    backButton.innerHTML = "Back";
    backButton.className = "button";
    tagTypeText.appendChild(backButton);
    backButton.addEventListener("click", goBack);
    submitButton.addEventListener("click", submitNewType)
}

changeButton.addEventListener("click", addSelect);