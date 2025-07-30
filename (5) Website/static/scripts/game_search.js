console.log("game_search.js loaded");
let mainBody = document.getElementById("page_mainbody_home");
let previousSearch = document.getElementById("previos_search");
let searchBox = document.getElementById("game_search");
let searchButton = document.getElementById("game_search_button");
let errorMessage = null;

function submitSearch(event){
    event.preventDefault();
    console.log("!");
    if (/\S/.test(searchBox.value)){
        var search = searchBox.value.replaceAll(" ", "+");
        window.location.replace("/games/pid=0?search=" + search);
    }
    else{
        window.location.replace("/games/pid=0");
    }
}

searchBox.value = previousSearch.innerHTML;
searchButton.addEventListener("click", submitSearch);
searchBox.addEventListener("keypress", function(event){
    if (event.key === "Enter"){
        searchButton.click()
    }
});