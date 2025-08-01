console.log("devpub_search.js loaded");
let searchBox = document.getElementById("tag_search");
let searchButton = document.getElementById("game_search_button");

function submitSearch(){
    event.preventDefault();
    if (/\S/.test(searchBox.value)){
        var current_loc = window.location.href;
        if (current_loc.includes("developers")){
            window.location.replace("/developers/pid=0?search=" + searchBox.value);
        }
        else if (current_loc.includes("publishers")){
            window.location.replace("/publishers/pid=0?search=" + searchBox.value);
        }
        else{
            return;
        }
    }
}

searchButton.addEventListener("click", submitSearch);
searchBox.addEventListener("keypress", function(event){
    if (event.key === "Enter"){
        searchButton.click()
    }
});