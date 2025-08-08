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

function getUpdateData(){ //Note: Update Names with apostrophes in their name will break this function!
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
                console.log(response);
                updateData = response.replaceAll("'", '"');
                updateData = JSON.parse(updateData);
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
    for (var i = updateData.length - 1; i >= 0; i--){
        var row = document.createElement("tr");
        var row_keys = Object.keys(updateData[i]);
        for (var t = 0; t < row_keys.length; t++){
            var column = document.createElement("td");
            if (updateData[i][row_keys[t]] === "None"){
                updateData[i][row_keys[t]] = "N/A";
            }
            column.innerHTML = updateData[i][row_keys[t]];
            row.appendChild(column);
        }
        if (i == 0){
            var column = document.createElement("td");
            column.innerHTML = "Game Added";
            column.id = "update_oldest";
            row.appendChild(column);
        }
        if (i == updateData.length - 1){
            var column = document.createElement("td");
            column.innerHTML = "Current Version";
            column.id = "update_current"
            row.appendChild(column);
        }
        updateTable.appendChild(row);
    }
}

function UpdateGoBack(){
    updateBackButton.style.display = "none";
    updateTable.style.display = "none";
    showButton.style.display = "inline";
    updateBackButton = null;
    updateTable = null;
    updateBackButton = null;
    updateData = null;
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
    updateBackButton.addEventListener("click", UpdateGoBack);
    updateBackButton.innerHTML = "Back";
    updateBackButton.className = "button";
    updateBackButton.id = "update_back_button";
    updateBox.appendChild(updateBackButton);
}

showButton.addEventListener("click", addUpdateBox);