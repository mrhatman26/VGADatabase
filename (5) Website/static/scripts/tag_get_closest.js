console.log("tag_get_closes.js loaded");
let gameSearchBox = document.getElementById("game_search");
let previousIsLetter = false;
let tagList = document.getElementById("drop_down_content");
let tagId = "";

function addTag(tag){
    var gameSearchSplit = gameSearchBox.value.split(" ");
    gameSearchSplit.pop();
    gameSearchSplit.push(tag);
    gameSearchBox.value = "";
    for (var i = 0; i < gameSearchSplit.length; i++){
        if (gameSearchBox.value === ""){
            gameSearchBox.value = gameSearchSplit[i];
        }
        else{
            gameSearchBox.value = gameSearchBox.value + " " + gameSearchSplit[i];
        }
    }
    tagList.style.display = "none";
    tagList.innerHTML = "";
    gameSearchBox.value = gameSearchBox.value + " ";
}

function getClosestTag(tag){
    $.ajax({
        type: "POST",
        url: "/tags/search/closest/",
        data: tag,
        success: function(response){
            if (!(response === "servererror") && !(response === "-999notag")){
                if (tagList.hasChildNodes()){
                    tagList.innerHTML = "";
                }
                var tags = response.split("|");
                for (var i = 0; i < tags.length; i++){
                    var tagOption = document.createElement("a");
                    tagOption.innerHTML = tags[i];
                    tagOption.id = tags[i];
                    tagOption.className = "drop_down_content_item";
                    tagList.appendChild(tagOption);
                }
                tagList.style.display = "inline";
                for (var i = 0; i < tagList.childNodes.length; i++){
                    tagList.childNodes[i].addEventListener("click", function(e){
                        addTag(e.target.id);
                    });
                }
            }
        }
    });
}
gameSearchBox.addEventListener("keyup", function(event){
    if (event.key === "Home"){
        gameSearchBox.value = "";
    }
    if (event.key != "Enter" && event.key != "ArrowUp" && event.key != "ArrowDown" && event.key != "ArrowRight" && event.key != "ArrowLeft"){
        try{
            if (gameSearchBox.value[gameSearchBox.selectionStart - 1] != " "){
                previousIsLetter = true;
            }
            else{
                tagList.style.display = "none";
                tagList.innerHTML = "";
                previousIsLetter = false;
            }
        }
        catch{
            previousIsLetter = false;
            tagList.innerHTML = "";
        }
        if (previousIsLetter === true){
            if (gameSearchBox.selectionStart === gameSearchBox.value.length){
                var valSplit = gameSearchBox.value.split(" ");
                if (valSplit[valSplit.length - 1].length >= 3){
                    getClosestTag(valSplit[valSplit.length - 1]);
                }
            }
        }
    }
});