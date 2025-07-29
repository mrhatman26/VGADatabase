console.log("update_show.js loaded");
let showButton = document.getElementById("show_update_button");
let updateBox = document.getElementById("update_box");
let updateName = document.getElementById("update_name");
let updateTableHeaders = ["Version", updateName.innerHTML, "Added", "Removed", "Username", "Time"];
let headerRow = null;
let updateTable = null;
let updateBackButton = null;
let updateID = document.getElementById("update_id");
let updateData = null;

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
    var data = {
        "update_id": updateID.innerHTML.split(": ")[1],
        "update_type": updateName.innerHTML.toLowerCase()
    }
    $.ajax({
        type: "POST",
        url: "/updates/get/",
        data: JSON.stringify(data),
        success: function(response){
            if (!(response === "servererror")){
                updateData = response.split(", ");
                for (var i = 0; i < updateData.length; i++){
                    updateData[i] = updateData[i].split("+");
                }
                console.log(updateData);
                tableAddRows();
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
    console.log(updateData);
    for (var i = 0; i < updateData.length; i++){
        var row = document.createElement("tr");
        for (var t = 0; t < updateData[i].length; t++){
            var column = document.createElement("td");
            column.innerHTML = updateData[i][t];
            row.appendChild(column);
        }
        updateTable.appendChild(row);
    }
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
    getUpdateData();
    updateBox.appendChild(updateTable);
    //Back button
    updateBackButton.innerHTML = "Back";
    updateBackButton.className = "button";
    updateBox.appendChild(updateBackButton);
    updateBackButton.addEventListener("click", goBack);
}

showButton.addEventListener("click", addUpdateBox);