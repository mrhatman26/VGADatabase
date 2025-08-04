console.log("tag_get_closes.js loaded");
let gameSearchBox = document.getElementById("game_search");
let previousIsLetter = false;
let tagList = document.getElementById("tag_list");

function getClosestTag(tag){
    $.ajax({
        type: "POST",
        url: "/tags/search/closest/",
        data: tag,
        success: function(response){
            if (!(response === "servererror") && !(response === "-999notag")){
                if (tagList.hasChildNodes()){
                    console.log("oh no");
                    tagList.innerHTML = "";
                }
                var tags = response.split("|");
                for (var i = 0; i < tags.length; i++){
                    var tagOption = document.createElement("option");
                    tagOption.value = tags[i]
                    tagList.appendChild(tagOption);
                }
                console.log(tags);
            }
        }
    });
}

gameSearchBox.addEventListener("keyup", function(event){
    console.log(tagList.childNodes.length);
    try{
        if (gameSearchBox.value[gameSearchBox.selectionStart - 1] != " "){
            previousIsLetter = true;
        }
        else{
            tagList.innerHTML = "";
            previousIsLetter = false;
        }
    }
    catch{
        previousIsLetter = false;
    }
    if (previousIsLetter === true){
        if (gameSearchBox.selectionStart === gameSearchBox.value.length){
            var valSplit = gameSearchBox.value.split(" ");
            if (valSplit[valSplit.length - 1].length >= 3){
                getClosestTag(valSplit[valSplit.length - 1]);
            }
        }
    }
});