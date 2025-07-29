console.log("update_show.js loaded");
let showButton = document.getElementById("show_update_button");
let updateBox = document.getElementById("update_box");
let updateName = document.getElementById("update_name");
let updateTableHeaders = ["Version", updateName.innerHTML, "Added", "Removed", "Username", "Time"];
let headerRow = null;
let updateTable = null;
let updateBackButton = null;
let updateData = null;
let updateID = document.getElementById("update_id");

function oldErrorCheck(){
    var oldErrorMessage = document.getElementById("errorMessage");
    if (oldErrorMessage === null){
        return false;
    }
    else{
        return true;
    }
}

function getUpdateData(){
    updateData = {
        "update_id": updateID.innerHTML.split(": ")[1],
        "update_type": updateName.innerHTML.toLowerCase()
    }
    $.ajax({
        type: "POST",
        url: "/updates/get/",
        data: JSON.stringify(updateData),
        success: function(response){
            if (!(response === "servererror")){
                updateData = response;
                console.log(updateData);
                updateData = Array.from(updateData); //Doesn't work
                console.log(updateData);
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

function tableAddColumns(){
    var headerRow = document.createElement("tr");
    updateTable.appendChild(headerRow);
    for (var i = 0; i < updateTableHeaders.length; i++){
        var updateColumn = document.createElement("th");
        updateColumn.innerHTML = updateTableHeaders[i];
        headerRow.appendChild(updateColumn);
    }
}

function tableAddRows(){
    getUpdateData();
}

function goBack(){ //Finish this
    tagTextBox.style.display = "none";
    submitButton.style.display = "none";
    updateBackButton.style.display = "none";
    showButton.style.display = "inline";
    tagDict = null;
    currentTagsText = null;
    submitButton = null;
    updateBackButton = null;
}

function addUpdateBox(){
    showButton.style.display = "none";
    updateBackButton = document.createElement("a");
    updateTable = document.createElement("table");
    //Table
    tableAddColumns();
    tableAddRows();
    updateBox.appendChild(updateTable);
    //Back button
    updateBackButton.innerHTML = "Back";
    updateBackButton.className = "button";
    updateBox.appendChild(updateBackButton);
    updateBackButton.addEventListener("click", goBack);
}

showButton.addEventListener("click", addUpdateBox);