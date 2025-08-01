console.log("tag_search.js loaded");
let searchBox = document.getElementById("tag_search");
let searchButton = document.getElementById("game_search_button");

function submitSearch(){
    event.preventDefault();
    if (/\S/.test(searchBox.value)){
        window.location.replace("/tags/pid=0?search=" + searchBox.value);
    }
    else{
        window.location.replace("/tags/pid=0");
    }
}

searchButton.addEventListener("click", submitSearch);
searchBox.addEventListener("keypress", function(event){
    if (event.key === "Enter"){
        searchButton.click()
    }
});